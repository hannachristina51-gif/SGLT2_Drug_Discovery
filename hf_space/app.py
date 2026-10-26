import streamlit as st

# --- Page Configuration (Wajib menjadi instruksi Streamlit paling pertama) ---
st.set_page_config(
    page_title="SGLT2 Virtual Screening",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os
import sys
import io

# 1. Pastikan seluruh lokasi site-packages potensial di cloud terdaftar pada sys.path
for site_path in [
    "/home/adminuser/venv/lib/python3.11/site-packages",
    "/home/adminuser/venv/lib/python3.12/site-packages",
    "/home/adminuser/venv/lib/python3.10/site-packages",
    "/home/adminuser/venv/lib/python3.14/site-packages",
    "/home/appuser/venv/lib/python3.11/site-packages",
    "/home/appuser/venv/lib/python3.12/site-packages",
    "/home/appuser/venv/lib/python3.10/site-packages",
    os.path.expanduser("~/.local/lib/python3.11/site-packages"),
    os.path.expanduser("~/.local/lib/python3.12/site-packages"),
    os.path.expanduser("~/.local/lib/python3.14/site-packages"),
]:
    if os.path.exists(site_path) and site_path not in sys.path:
        sys.path.insert(0, site_path)

# 2. Impor pustaka Machine Learning & Kimia dengan fallback bertingkat
try:
    import joblib
except ImportError:
    try:
        import sklearn.utils._joblib as joblib
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "joblib"])
        import joblib

try:
    import pandas as pd
    import numpy as np
    import sklearn
    from rdkit import Chem
    from rdkit.Chem import Descriptors, Lipinski, AllChem, Draw
except ImportError as err:
    import subprocess
    st.info(f"Sedang mengunduh dependensi ({err})... Mohon tunggu sebentar.")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "scikit-learn", "rdkit", "pandas", "numpy", "pillow"
    ])
    import pandas as pd
    import numpy as np
    import sklearn
    from rdkit import Chem
    from rdkit.Chem import Descriptors, Lipinski, AllChem, Draw
    st.rerun()





# --- Custom Styling ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 10px;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.title("🧬 SGLT2 Inhibitor - Virtual Screening App")
st.markdown(
    "Aplikasi *Machine Learning* in-silico untuk memprediksi potensi bioaktivitas inhibitor "
    "**Sodium-Glucose Cotransporter 2 (SGLT2)** pada pengobatan Diabetes Melitus Tipe 2."
)

# --- Sidebar: Model & Project Info ---
with st.sidebar:
    st.header("ℹ️ Informasi Proyek & Model")
    st.markdown("""
    - **Target Biologis**: SGLT2 (*SLC5A2*)
    - **Dataset**: ChEMBL (Target ID: `CHEMBL1808`)
    - **Data Terkurasi**: 1.760 senyawa
    - **Algoritma**: *Random Forest Regressor*
    - **Validasi**: *Bemis-Murcko Scaffold Split*
    - **Metrik Model**:
      - $R^2$: **0.7297**
      - $RMSE$: **0.6317**
    """)
    st.markdown("---")
    st.markdown("### 📚 Klasifikasi Bioaktivitas")
    st.markdown("""
    - 🟢 **Aktif**: $pActivity > 6.0$ ($IC_{50} < 1.000$ nM)
    - 🟡 **Intermediate**: $5.0 < pActivity \le 6.0$
    - 🔴 **Tidak Aktif**: $pActivity \le 5.0$ ($IC_{50} > 10.000$ nM)
    """)
    st.markdown("---")
    st.caption("Dikembangkan untuk Riset Drug Discovery AI - Prof. Arry")

# --- Model Loading ---
@st.cache_resource
def load_models():
    base_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    model_path = os.path.join(base_dir, 'models', 'rf_regressor_model.pkl')
    scaler_path = os.path.join(base_dir, 'models', 'scaler.pkl')
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError(f"File model atau scaler tidak ditemukan di {base_dir}/models.")
        
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

try:
    model, scaler = load_models()
except Exception as e:
    st.error(f"⚠️ Gagal memuat model machine learning. Error: {e}")
    st.stop()

# --- Helper Functions ---
def get_features(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, None, None
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hdon = Lipinski.NumHDonors(mol)
    hacc = Lipinski.NumHAcceptors(mol)
    num_features = np.array([[mw, logp, hdon, hacc]])
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
    fp_array = np.array(list(fp)).reshape(1, -1)
    return fp_array, num_features, mol

def predict_activity(fp_array, num_features):
    num_scaled = scaler.transform(num_features)
    X = np.hstack([fp_array, num_scaled])
    pred = float(model.predict(X)[0])
    # Konversi pActivity ke IC50 (nM)
    # pActivity = -log10(IC50_Molar) -> IC50_Molar = 10^(-pActivity)
    # IC50_nM = IC50_Molar * 1e9
    ic50_nm = float((10 ** (-pred)) * 1e9)
    return pred, ic50_nm

# --- Preset Molecules ---
PRESETS = {
    "Dapagliflozin (SGLT2 Inhibitor Komersial)": "CC1=C(C=C(C=C1)CC2=C(C=CC(=C2)Cl)OCC)C3C(C(C(C(O3)CO)O)O)O",
    "Empagliflozin (SGLT2 Inhibitor Komersial)": "C1=CC(=C(C=C1CC2=C(C=CC(=C2)Cl)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O)Cl",
    "Canagliflozin (SGLT2 Inhibitor Komersial)": "CC1=CC(=CC=C1)CC2=CC=C(S2)C3C(C(C(C(O3)CO)O)O)O",
    "Metformin (Golongan Biguanid)": "CN(C)C(=NC(=N)N)N",
    "Aspirin (Kontrol Negatif)": "CC(=O)OC1=CC=CC=C1C(=O)O"
}

# --- Application Tabs ---
tab1, tab2, tab3 = st.tabs([
    "🧬 Single Molecule Prediction", 
    "🗂️ Batch Screening (CSV)",
    "📖 Metodologi & Petunjuk"
])

# ==========================================
# TAB 1: Single Molecule Prediction
# ==========================================
with tab1:
    st.subheader("Prediksi Senyawa Tunggal")
    
    # Preset Selector
    selected_preset = st.selectbox(
        "Pilih contoh senyawa acuan atau masukkan SMILES Anda sendiri:",
        options=["(Ketik SMILES kustom di bawah)"] + list(PRESETS.keys())
    )
    
    default_smiles = PRESETS["Dapagliflozin (SGLT2 Inhibitor Komersial)"]
    if selected_preset != "(Ketik SMILES kustom di bawah)":
        default_smiles = PRESETS[selected_preset]
        
    smiles_input = st.text_input("Representasi SMILES:", value=default_smiles)
    
    if st.button("🚀 Analisis Senyawa", type="primary", use_container_width=False):
        if not smiles_input.strip():
            st.warning("Silakan masukkan representasi SMILES terlebih dahulu.")
        else:
            fp_array, num_features, mol = get_features(smiles_input.strip())
            if mol is None:
                st.error("❌ Format struktur SMILES tidak valid. Mohon periksa kembali input Anda.")
            else:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("### 🔬 Struktur 2D")
                    img = Draw.MolToImage(mol, size=(340, 340))
                    st.image(img, use_container_width=True)
                
                with col2:
                    pred, ic50_nm = predict_activity(fp_array, num_features)
                    
                    st.markdown("### 📊 Hasil Prediksi Bioaktivitas")
                    mc1, mc2 = st.columns(2)
                    mc1.metric(label="Prediksi pActivity (pIC50)", value=f"{pred:.2f}")
                    
                    if ic50_nm < 1000:
                        ic50_display = f"{ic50_nm:.2f} nM"
                    elif ic50_nm < 1_000_000:
                        ic50_display = f"{(ic50_nm/1000):.2f} µM"
                    else:
                        ic50_display = f"{(ic50_nm/1_000_000):.2f} mM"
                    mc2.metric(label="Estimasi Nilai IC50", value=ic50_display, help="Semakin kecil nilai IC50, semakin poten senyawanya.")
                    
                    if pred > 6.0:
                        st.success("✅ Status: **POTENSIAL AKTIF** (Kandidat Kuat Inhibitor SGLT2)")
                        status = "Potensial Aktif"
                    elif pred > 5.0:
                        st.warning("⚠️ Status: **POTENSI MENENGAH** (Intermediate Activity)")
                        status = "Intermediate"
                    else:
                        st.error("❌ Status: **TIDAK AKTIF** (Inhibisi Rendah / Negatif)")
                        status = "Tidak Aktif"
                        
                    st.markdown("#### 🧪 Validasi Lipinski's Rule of Five")
                    mw, logp, hdon, hacc = num_features[0]
                    
                    v_mw = "✅ Lolos" if mw <= 500 else "❌ Melanggar (> 500)"
                    v_logp = "✅ Lolos" if logp <= 5 else "❌ Melanggar (> 5)"
                    v_hdon = "✅ Lolos" if hdon <= 5 else "❌ Melanggar (> 5)"
                    v_hacc = "✅ Lolos" if hacc <= 10 else "❌ Melanggar (> 10)"
                    
                    c_lip1, c_lip2 = st.columns(2)
                    with c_lip1:
                        st.write(f"- **Molecular Weight**: `{mw:.2f}` ({v_mw})")
                        st.write(f"- **LogP**: `{logp:.2f}` ({v_logp})")
                    with c_lip2:
                        st.write(f"- **H-Donors**: `{int(hdon)}` ({v_hdon})")
                        st.write(f"- **H-Acceptors**: `{int(hacc)}` ({v_hacc})")
                    
                    # Download Report
                    report_df = pd.DataFrame([{
                        "SMILES": smiles_input.strip(),
                        "Prediksi_pActivity": round(pred, 2),
                        "Estimasi_IC50_nM": round(ic50_nm, 2),
                        "Status": status,
                        "Molecular_Weight": round(mw, 2),
                        "LogP": round(logp, 2),
                        "H_Donors": int(hdon),
                        "H_Acceptors": int(hacc)
                    }])
                    csv_data = report_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Unduh Laporan Prediksi (.csv)",
                        data=csv_data,
                        file_name="sglt2_single_prediction_report.csv",
                        mime="text/csv"
                    )

# ==========================================
# TAB 2: Batch Virtual Screening
# ==========================================
with tab2:
    st.subheader("Skrining Massal Senyawa (Batch Screening via CSV)")
    st.markdown("Unggah file CSV yang memuat daftar senyawa dengan kolom **`smiles`** atau **`canonical_smiles`**.")
    
    # Download sample batch CSV
    sample_df = pd.DataFrame([
        {"compound_name": "Dapagliflozin", "smiles": "CC1=C(C=C(C=C1)CC2=C(C=CC(=C2)Cl)OCC)C3C(C(C(C(O3)CO)O)O)O"},
        {"compound_name": "Empagliflozin", "smiles": "C1=CC(=C(C=C1CC2=C(C=CC(=C2)Cl)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O)Cl"},
        {"compound_name": "Metformin", "smiles": "CN(C)C(=NC(=N)N)N"},
        {"compound_name": "Aspirin", "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O"},
        {"compound_name": "Caffeine", "smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"}
    ])
    sample_csv = sample_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Unduh Contoh Format File CSV Pengujian",
        data=sample_csv,
        file_name="sample_batch_sglt2.csv",
        mime="text/csv"
    )
    
    uploaded_file = st.file_uploader("Pilih file CSV dari komputer Anda", type="csv")
    
    if uploaded_file is not None:
        try:
            df_batch = pd.read_csv(uploaded_file)
            smiles_col = None
            for col in df_batch.columns:
                if col.strip().lower() in ['smiles', 'canonical_smiles']:
                    smiles_col = col
                    break
                    
            if smiles_col is None:
                st.error("❌ Berkas CSV harus memiliki kolom bernama **`smiles`** atau **`canonical_smiles`**.")
            else:
                st.info(f"Ditemukan **{len(df_batch)} baris senyawa** pada kolom `{smiles_col}`.")
                if st.button("⚡ Jalankan Batch Screening", type="primary"):
                    progress_bar = st.progress(0)
                    results = []
                    total = len(df_batch)
                    
                    for idx, row in df_batch.iterrows():
                        s = str(row[smiles_col]).strip()
                        fp_array, num_features, mol = get_features(s)
                        
                        if mol is not None:
                            pred, ic50_nm = predict_activity(fp_array, num_features)
                            status = "Aktif" if pred > 6.0 else ("Intermediate" if pred > 5.0 else "Tidak Aktif")
                            mw, logp, hdon, hacc = num_features[0]
                            
                            violations = 0
                            if mw > 500: violations += 1
                            if logp > 5: violations += 1
                            if hdon > 5: violations += 1
                            if hacc > 10: violations += 1
                            
                            results.append({
                                "SMILES": s,
                                "Prediksi_pActivity": round(pred, 2),
                                "Estimasi_IC50_nM": round(ic50_nm, 2),
                                "Status": status,
                                "MW": round(mw, 2),
                                "LogP": round(logp, 2),
                                "H_Donors": int(hdon),
                                "H_Acceptors": int(hacc),
                                "Lipinski_Violations": violations
                            })
                        else:
                            results.append({
                                "SMILES": s,
                                "Prediksi_pActivity": np.nan,
                                "Estimasi_IC50_nM": np.nan,
                                "Status": "SMILES Tidak Valid",
                                "MW": np.nan,
                                "LogP": np.nan,
                                "H_Donors": np.nan,
                                "H_Acceptors": np.nan,
                                "Lipinski_Violations": np.nan
                            })
                        progress_bar.progress((idx + 1) / total)
                        
                    df_res = pd.DataFrame(results)
                    st.success(f"🎉 Skrining selesai untuk {total} senyawa!")
                    st.dataframe(df_res, use_container_width=True)
                    
                    csv_batch = df_res.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Unduh Seluruh Hasil Batch Screening (.csv)",
                        data=csv_batch,
                        file_name="sglt2_batch_screening_results.csv",
                        mime="text/csv"
                    )
        except Exception as e:
            st.error(f"Gagal memproses file CSV: {e}")

# ==========================================
# TAB 3: Methodology & Instructions
# ==========================================
with tab3:
    st.subheader("📖 Metodologi & Panduan Penggunaan")
    st.markdown("""
    ### 1. Definisi Nilai Prediksi
    - **$pActivity$ ($pIC_{50}$)**: $-\log_{10}(IC_{50} \text{ Molar})$.
    - **$IC_{50}$ (nM)**: Konsentrasi molar yang diperlukan untuk menghambat 50% aktivitas SGLT2 in vitro. Semakin rendah nilai $IC_{50}$, semakin poten senyawa tersebut.
    
    ### 2. Aturan Lima Lipinski (*Lipinski's Rule of Five*)
    Parameter empiris untuk memprediksi bioavailabilitas oral suatu molekul:
    - **Molecular Weight (MW)**: $\le 500 \text{ Da}$
    - **LogP (Lipofilisitas)**: $\le 5$
    - **H-Bond Donors (HBD)**: $\le 5$
    - **H-Bond Acceptors (HBA)**: $\le 10$
    
    ### 3. Arsitektur Machine Learning
    - **Fitur Masukan**: Penggabungan 2.048 bit Morgan Fingerprints (ECFP4) dan 4 deskriptor numerik terstandarisasi.
    - **Pemisahan Data**: *Bemis-Murcko Scaffold Split* memastikan molekul pada kelompok uji (*test set*) memiliki kerangka kimiawi yang berbeda dari kelompok latih (*train set*), menguji kemampuan generalisasi sejati model.
    """)
