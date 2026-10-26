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
import glob

# 1. Pastikan folder repo (tempat joblib dibundel) menjadi prioritas utama sys.path
current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 2. Registrasi dinamis seluruh direktori site-packages di lingkungan Cloud (Streamlit / Linux)
for pattern in [
    "/home/**/site-packages",
    "/home/**/dist-packages",
    "/mount/**/site-packages",
    "/usr/local/**/site-packages",
    "/usr/local/**/dist-packages",
]:
    try:
        for p in glob.glob(pattern, recursive=True):
            if os.path.isdir(p) and p not in sys.path:
                sys.path.insert(0, p)
    except Exception:
        pass

# 3. Impor pustaka Machine Learning & Kimia Komputasi
import datetime
import streamlit.components.v1 as components
import joblib
import pandas as pd
import numpy as np
import sklearn
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, AllChem, Draw
from pdf_report import generate_single_pdf_report, generate_batch_pdf_report, get_printable_html
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
                st.session_state["single_result"] = None
            else:
                pred, ic50_nm = predict_activity(fp_array, num_features)
                if pred > 6.0:
                    status = "Potensial Aktif"
                elif pred > 5.0:
                    status = "Intermediate"
                else:
                    status = "Tidak Aktif"
                
                mw, logp, hdon, hacc = num_features[0]
                v_mw = "✅ Lolos" if mw <= 500 else "❌ Melanggar (> 500)"
                v_logp = "✅ Lolos" if logp <= 5 else "❌ Melanggar (> 5)"
                v_hdon = "✅ Lolos" if hdon <= 5 else "❌ Melanggar (> 5)"
                v_hacc = "✅ Lolos" if hacc <= 10 else "❌ Melanggar (> 10)"

                compound_name = selected_preset if selected_preset != "(Ketik SMILES kustom di bawah)" else "Senyawa Uji Kustom"

                st.session_state["single_result"] = {
                    "smiles": smiles_input.strip(),
                    "compound_name": compound_name,
                    "pred": pred,
                    "ic50_nm": ic50_nm,
                    "status": status,
                    "mw": mw,
                    "logp": logp,
                    "hdon": hdon,
                    "hacc": hacc,
                    "mol": mol,
                    "v_mw": v_mw,
                    "v_logp": v_logp,
                    "v_hdon": v_hdon,
                    "v_hacc": v_hacc
                }

    # Render Hasil Analisis dari Session State
    res = st.session_state.get("single_result", None)
    if res is not None and res.get("mol") is not None:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### 🔬 Struktur 2D")
            img = Draw.MolToImage(res["mol"], size=(340, 340))
            st.image(img, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Hasil Prediksi Bioaktivitas")
            mc1, mc2 = st.columns(2)
            mc1.metric(label="Prediksi pActivity (pIC50)", value=f"{res['pred']:.2f}")
            
            ic50_nm = res["ic50_nm"]
            if ic50_nm < 1000:
                ic50_display = f"{ic50_nm:.2f} nM"
            elif ic50_nm < 1_000_000:
                ic50_display = f"{(ic50_nm/1000):.2f} µM"
            else:
                ic50_display = f"{(ic50_nm/1_000_000):.2f} mM"
            mc2.metric(label="Estimasi Nilai IC50", value=ic50_display, help="Semakin kecil nilai IC50, semakin poten senyawanya.")
            
            if res["status"] == "Potensial Aktif":
                st.success("✅ Status: **POTENSIAL AKTIF** (Kandidat Kuat Inhibitor SGLT2)")
            elif res["status"] == "Intermediate":
                st.warning("⚠️ Status: **POTENSI MENENGAH** (Intermediate Activity)")
            else:
                st.error("❌ Status: **TIDAK AKTIF** (Inhibisi Rendah / Negatif)")
                
            st.markdown("#### 🧪 Validasi Lipinski's Rule of Five")
            c_lip1, c_lip2 = st.columns(2)
            with c_lip1:
                st.write(f"- **Molecular Weight**: `{res['mw']:.2f}` ({res['v_mw']})")
                st.write(f"- **LogP**: `{res['logp']:.2f}` ({res['v_logp']})")
            with c_lip2:
                st.write(f"- **H-Donors**: `{int(res['hdon'])}` ({res['v_hdon']})")
                st.write(f"- **H-Acceptors**: `{int(res['hacc'])}` ({res['v_hacc']})")

        # --- Bagian Ekspor Laporan PDF Lengkap & Fitur Cetak ---
        st.markdown("---")
        st.markdown("### 📑 Ekspor Laporan Resmi & Cetak Dokumen")
        st.caption("Unduh berkas laporan komprehensif berformat PDF atau cetak langsung ke printer:")

        col_exp1, col_exp2, col_exp3 = st.columns([1.2, 1, 1.2])

        with col_exp1:
            try:
                pdf_bytes = generate_single_pdf_report(
                    smiles=res["smiles"],
                    pred=res["pred"],
                    ic50_nm=res["ic50_nm"],
                    status=res["status"],
                    mw=res["mw"],
                    logp=res["logp"],
                    hdon=res["hdon"],
                    hacc=res["hacc"],
                    mol=res["mol"],
                    compound_name=res["compound_name"]
                )
                ts_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="📑 Unduh Laporan PDF Lengkap",
                    data=pdf_bytes,
                    file_name=f"Laporan_SGLT2_{ts_str}.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
            except Exception as err:
                st.error(f"Gagal memformat PDF: {err}")

        with col_exp2:
            report_df = pd.DataFrame([{
                "SMILES": res["smiles"],
                "Prediksi_pActivity": round(res["pred"], 2),
                "Estimasi_IC50_nM": round(res["ic50_nm"], 2),
                "Status": res["status"],
                "Molecular_Weight": round(res["mw"], 2),
                "LogP": round(res["logp"], 2),
                "H_Donors": int(res["hdon"]),
                "H_Acceptors": int(res["hacc"])
            }])
            csv_data = report_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Unduh Data (.csv)",
                data=csv_data,
                file_name="sglt2_single_prediction_report.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_exp3:
            show_print = st.toggle("🖨️ Pratinjau & Cetak Laporan", value=False)

        if show_print:
            st.markdown("#### 🖨️ Pratinjau Dokumen Cetak")
            st.info("💡 Klik tombol **'🖨️ Cetak / Print Sekarang'** di pojok kanan atas formulir pratinjau untuk membuka dialog cetak printer bawaan browser Anda.")
            html_print = get_printable_html(
                smiles=res["smiles"],
                pred=res["pred"],
                ic50_nm=res["ic50_nm"],
                status=res["status"],
                mw=res["mw"],
                logp=res["logp"],
                hdon=res["hdon"],
                hacc=res["hacc"],
                mol=res["mol"],
                compound_name=res["compound_name"]
            )
            components.html(html_print, height=680, scrolling=True)

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
                    st.session_state["batch_results"] = df_res
                    st.success(f"🎉 Skrining selesai untuk {total} senyawa!")

                if "batch_results" in st.session_state and st.session_state["batch_results"] is not None:
                    df_res = st.session_state["batch_results"]
                    st.dataframe(df_res, use_container_width=True)
                    
                    st.markdown("---")
                    st.markdown("### 📑 Ekspor Hasil Penapisan Massal (Batch)")
                    col_b_pdf, col_b_csv = st.columns(2)
                    with col_b_pdf:
                        try:
                            batch_pdf_bytes = generate_batch_pdf_report(df_res)
                            ts_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            st.download_button(
                                label="📑 Unduh Rekapitulasi PDF Batch Screening",
                                data=batch_pdf_bytes,
                                file_name=f"Rekap_Batch_SGLT2_{ts_str}.pdf",
                                mime="application/pdf",
                                type="primary",
                                use_container_width=True
                            )
                        except Exception as err:
                            st.error(f"Gagal memformat PDF Batch: {err}")
                    with col_b_csv:
                        csv_batch = df_res.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Unduh Data Lengkap (.csv)",
                            data=csv_batch,
                            file_name="sglt2_batch_screening_results.csv",
                            mime="text/csv",
                            use_container_width=True
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
