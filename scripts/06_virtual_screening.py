import pandas as pd
import numpy as np
import os
from rdkit import Chem
from rdkit.Chem import AllChem
import joblib

def get_morgan_fingerprints(smiles_list, radius=2, nBits=2048):
    fingerprints = []
    for smiles in smiles_list:
        mol = Chem.MolFromSmiles(smiles)
        if mol is not None:
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=nBits)
            fingerprints.append(np.array(fp))
        else:
            fingerprints.append(np.zeros(nBits))
    return np.array(fingerprints)

def run_virtual_screening():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(base_dir, 'models', 'rf_regressor_model.pkl')
    results_dir = os.path.join(base_dir, 'data')
    
    if not os.path.exists(model_path):
        print(f"Model tidak ditemukan di {model_path}. Harap latih model terlebih dahulu.")
        return
        
    print("Memuat model Random Forest Regressor...")
    model = joblib.load(model_path)
    
    # Kumpulan Senyawa Contoh (Compound Library) untuk Screening
    # Kita menggunakan beberapa senyawa terkenal termasuk Dapagliflozin (SGLT2 inhibitor)
    sample_library = [
        {"Name": "Dapagliflozin (SGLT2 Inhibitor)", "SMILES": "CC1=C(C=C(C=C1)CC2=C(C=CC(=C2)Cl)OCC)C3C(C(C(C(O3)CO)O)O)O"},
        {"Name": "Metformin (Antidiabetik)", "SMILES": "CN(C)C(=NC(=N)N)N"},
        {"Name": "Aspirin (Analgesik)", "SMILES": "CC(=O)OC1=CC=CC=C1C(=O)O"},
        {"Name": "Caffeine (Stimulan)", "SMILES": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"},
        {"Name": "Ibuprofen (NSAID)", "SMILES": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"}
    ]
    
    df_screening = pd.DataFrame(sample_library)
    print(f"Memulai Virtual Screening untuk {len(df_screening)} senyawa...")
    
    # Hitung Fingerprints
    X_screen = get_morgan_fingerprints(df_screening['SMILES'].values)
    
    # Prediksi
    print("Memprediksi pActivity...")
    predictions = model.predict(X_screen)
    df_screening['Predicted_pActivity'] = predictions
    
    # Tentukan apakah berpotensi aktif (Threshold pActivity > 6.0)
    df_screening['Potensi'] = df_screening['Predicted_pActivity'].apply(lambda x: 'Potensial Aktif' if x > 6.0 else 'Tidak Aktif')
    
    # Urutkan berdasarkan potensi tertinggi
    df_screening = df_screening.sort_values(by='Predicted_pActivity', ascending=False)
    
    print("\n=== HASIL VIRTUAL SCREENING ===")
    print(df_screening[['Name', 'Predicted_pActivity', 'Potensi']].to_string(index=False))
    
    # Simpan hasil screening ke CSV
    output_path = os.path.join(results_dir, '04_virtual_screening_results.csv')
    df_screening.to_csv(output_path, index=False)
    print(f"\nHasil screening berhasil disimpan di: {output_path}")

if __name__ == "__main__":
    run_virtual_screening()
