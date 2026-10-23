import pandas as pd
import numpy as np
import os
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, AllChem

def get_lipinski_descriptors(smiles_list):
    moldata = []
    for elem in smiles_list:
        mol = Chem.MolFromSmiles(elem)
        moldata.append(mol)
       
    baseData = np.empty((0, 4))
    for mol in moldata:        
        if mol is not None:
            desc_MolWt = Descriptors.MolWt(mol)
            desc_MolLogP = Descriptors.MolLogP(mol)
            desc_NumHDonors = Lipinski.NumHDonors(mol)
            desc_NumHAcceptors = Lipinski.NumHAcceptors(mol)
            row = np.array([[desc_MolWt, desc_MolLogP, desc_NumHDonors, desc_NumHAcceptors]])   
            baseData = np.vstack([baseData, row])
        else:
            baseData = np.vstack([baseData, np.array([[np.nan, np.nan, np.nan, np.nan]])])
            
    columnNames = ["MW", "LogP", "NumHDonors", "NumHAcceptors"]   
    descriptors = pd.DataFrame(data=baseData, columns=columnNames)
    return descriptors

def get_morgan_fingerprints(smiles_list, radius=2, nBits=1024):
    fingerprints = []
    for smiles in smiles_list:
        mol = Chem.MolFromSmiles(smiles)
        if mol is not None:
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=nBits)
            fingerprints.append(list(fp))
        else:
            fingerprints.append([np.nan] * nBits)
            
    fp_columns = [f"FP_{i}" for i in range(nBits)]
    df_fp = pd.DataFrame(fingerprints, columns=fp_columns)
    return df_fp

def extract_all_features():
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(os.path.dirname(current_dir), 'data', '02_sglt2_processed_data.csv')
    output_path = os.path.join(current_dir, 'curated_features_and_fingerprints.csv')
    
    if not os.path.exists(data_path):
        print(f"Data tidak ditemukan di {data_path}")
        return
        
    print(f"Memuat data kurasi dari {data_path}...")
    df = pd.read_csv(data_path)
    
    # Hapus baris dengan SMILES kosong
    df = df.dropna(subset=['canonical_smiles']).reset_index(drop=True)
    
    print("Menghitung Lipinski Descriptors (MW, LogP, HDonors, HAcceptors)...")
    df_lipinski = get_lipinski_descriptors(df['canonical_smiles'])
    
    # Gunakan 1024 bit untuk fingerprint agar file tidak terlalu besar
    print("Menghitung Morgan Fingerprints (1024 bit)...")
    df_fp = get_morgan_fingerprints(df['canonical_smiles'], nBits=1024)
    
    print("Menggabungkan seluruh data...")
    # Gabungkan data asli, deskriptor, dan fingerprint
    df_combined = pd.concat([df, df_lipinski, df_fp], axis=1)
    
    print(f"Menyimpan hasil ekstraksi fitur ({df_combined.shape[0]} baris, {df_combined.shape[1]} kolom)...")
    df_combined.to_csv(output_path, index=False)
    print(f"Proses selesai. File tersimpan di: {output_path}")

if __name__ == "__main__":
    extract_all_features()
