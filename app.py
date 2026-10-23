import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import math
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, AllChem
from rdkit.Chem import Draw

st.set_page_config(page_title="SGLT2 Virtual Screening", layout="wide")

st.title("SGLT2 Inhibitor - Virtual Screening App")
st.markdown("Aplikasi web canggih untuk memprediksi potensi bioaktivitas (*SGLT2 Inhibition*) dari suatu senyawa baru menggunakan model *Machine Learning*.")

@st.cache_resource
def load_models():
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, 'models', 'rf_regressor_model.pkl')
    scaler_path = os.path.join(base_dir, 'models', 'scaler.pkl')
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

try:
    model, scaler = load_models()
except Exception as e:
    st.error(f"Gagal memuat model. Error: {e}")
    st.stop()

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
    pred = model.predict(X)[0]
    # Konversi pActivity ke IC50 (nM)
    # pActivity = -log10(IC50_Molar) -> IC50_Molar = 10^(-pActivity)
    # IC50_nM = IC50_Molar * 1e9
    ic50_nm = (10 ** (-pred)) * 1e9
    return pred, ic50_nm

tab1, tab2 = st.tabs(["🧬 Single Molecule Prediction", "🗂️ Batch Prediction (CSV)"])

with tab1:
    st.subheader("Input Senyawa (SMILES)")
    smiles_input = st.text_input("Masukkan representasi SMILES:", "CC1=C(C=C(C=C1)CC2=C(C=CC(=C2)Cl)OCC)C3C(C(C(C(O3)CO)O)O)O")
    
    if st.button("Analisis Senyawa", type="primary"):
        if smiles_input:
            fp_array, num_features, mol = get_features(smiles_input)
            if mol is None:
                st.error("Struktur SMILES tidak valid.")
            else:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("### Struktur 2D")
                    st.image(Draw.MolToImage(mol, size=(300, 300)), use_container_width=False)
                
                with col2:
                    pred, ic50_nm = predict_activity(fp_array, num_features)
                    
                    st.markdown("### Hasil Analisis")
                    mc1, mc2 = st.columns(2)
                    mc1.metric(label="Prediksi pActivity", value=f"{pred:.2f}")
                    mc2.metric(label="Estimasi IC50 (nM)", value=f"{ic50_nm:.2f} nM", help="Semakin kecil nilai IC50, semakin poten senyawanya.")
                    
                    if pred > 6.0:
                        st.success("Status: **POTENSIAL AKTIF** (SGLT2 Inhibitor)")
                        status = "Aktif"
                    elif pred > 5.0:
                        st.warning("Status: **POTENSI MENENGAH** (Intermediate)")
                        status = "Intermediate"
                    else:
                        st.error("Status: **TIDAK AKTIF**")
                        status = "Tidak Aktif"
                        
                    st.markdown("#### Validasi Lipinski's Rule of Five")
                    mw, logp, hdon, hacc = num_features[0]
                    
                    # Lipinski checks visual
                    v_mw = "✅" if mw <= 500 else "❌ (Batas: <= 500)"
                    v_logp = "✅" if logp <= 5 else "❌ (Batas: <= 5)"
                    v_hdon = "✅" if hdon <= 5 else "❌ (Batas: <= 5)"
                    v_hacc = "✅" if hacc <= 10 else "❌ (Batas: <= 10)"
                    
                    st.write(f"- **Molecular Weight**: {mw:.2f} {v_mw}")
                    st.write(f"- **LogP**: {logp:.2f} {v_logp}")
                    st.write(f"- **H-Donors**: {hdon:.0f} {v_hdon}")
                    st.write(f"- **H-Acceptors**: {hacc:.0f} {v_hacc}")
                    
                    # Download Report
                    report_df = pd.DataFrame([{
                        "SMILES": smiles_input,
                        "pActivity": pred,
                        "IC50_nM": ic50_nm,
                        "Status": status,
                        "Molecular_Weight": mw,
                        "LogP": logp,
                        "H_Donors": hdon,
                        "H_Acceptors": hacc
                    }])
                    csv_data = report_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Report (.csv)",
                        data=csv_data,
                        file_name="single_prediction_report.csv",
                        mime="text/csv"
                    )

with tab2:
    st.subheader("Unggah File CSV (Batch Screening)")
    st.info("File CSV harus memiliki minimal satu kolom bernama **`canonical_smiles`** atau **`smiles`**.")
    uploaded_file = st.file_uploader("Pilih file CSV dari komputer Anda", type="csv")
    
    if uploaded_file is not None:
        df_batch = pd.read_csv(uploaded_file)
        
        # Cari kolom smiles
        smiles_col = None
        for col in df_batch.columns:
            if col.lower() in ['smiles', 'canonical_smiles']:
                smiles_col = col
                break
                
        if smiles_col is None:
            st.error("File CSV tidak memiliki kolom bernama 'smiles' atau 'canonical_smiles'.")
        else:
            st.write(f"Ditemukan **{len(df_batch)} baris data** yang siap diproses.")
            if st.button("Mulai Batch Screening", type="primary"):
                with st.spinner("Mengekstraksi fitur dan melakukan prediksi pada seluruh senyawa..."):
                    results = []
                    for idx, row in df_batch.iterrows():
                        s = row[smiles_col]
                        fp_array, num_features, mol = get_features(str(s))
                        
                        if mol is not None:
                            pred, ic50_nm = predict_activity(fp_array, num_features)
                            status = "Aktif" if pred > 6.0 else ("Intermediate" if pred > 5.0 else "Tidak Aktif")
                            res_row = {
                                "SMILES": s,
                                "Prediksi_pActivity": round(pred, 2),
                                "Estimasi_IC50_nM": round(ic50_nm, 2),
                                "Status": status,
                                "MW": round(num_features[0][0], 2),
                                "LogP": round(num_features[0][1], 2),
                                "Lipinski_Violations": 0
                            }
                            # Hitung pelanggaran Lipinski
                            violations = 0
                            if res_row["MW"] > 500: violations += 1
                            if res_row["LogP"] > 5: violations += 1
                            if num_features[0][2] > 5: violations += 1
                            if num_features[0][3] > 10: violations += 1
                            res_row["Lipinski_Violations"] = violations
                            
                            results.append(res_row)
                        else:
                            results.append({
                                "SMILES": s,
                                "Status": "SMILES Tidak Valid"
                            })
                    
                    df_res = pd.DataFrame(results)
                    st.success("Batch Screening Selesai!")
                    st.dataframe(df_res)
                    
                    csv_batch = df_res.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Seluruh Hasil (.csv)",
                        data=csv_batch,
                        file_name="batch_screening_results.csv",
                        mime="text/csv"
                    )
