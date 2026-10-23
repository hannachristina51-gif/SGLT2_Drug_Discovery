import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
import os
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

def get_lipinski_descriptors(smiles):
    moldata= []
    for elem in smiles:
        mol=Chem.MolFromSmiles(elem) 
        moldata.append(mol)
       
    baseData= np.arange(1,1)
    i=0  
    for mol in moldata:        
        if mol is not None:
            desc_MolWt = Descriptors.MolWt(mol)
            desc_MolLogP = Descriptors.MolLogP(mol)
            desc_NumHDonors = Lipinski.NumHDonors(mol)
            desc_NumHAcceptors = Lipinski.NumHAcceptors(mol)
           
            row = np.array([desc_MolWt, desc_MolLogP, desc_NumHDonors, desc_NumHAcceptors])   
            if i==0:
                baseData=row
            else:
                baseData=np.vstack([baseData, row])
            i=i+1      
    
    columnNames=["MW","LogP","NumHDonors","NumHAcceptors"]   
    descriptors = pd.DataFrame(data=baseData,columns=columnNames)
    return descriptors

def calculate_descriptors():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    input_path = os.path.join(data_dir, '02_sglt2_processed_data.csv')
    
    if not os.path.exists(input_path):
        print(f"File tidak ditemukan: {input_path}")
        return
        
    print(f"Memuat data dari {input_path}")
    df = pd.read_csv(input_path)
    
    print("Menghitung Lipinski descriptors...")
    df_lipinski = get_lipinski_descriptors(df.canonical_smiles)
    
    # Gabungkan dataframe
    df_combined = pd.concat([df.reset_index(drop=True), df_lipinski.reset_index(drop=True)], axis=1)
    
    # Menyimpan data dengan deskriptor ke CSV
    output_path = os.path.join(data_dir, '03_sglt2_with_descriptors.csv')
    df_combined.to_csv(output_path, index=False)
    print(f"Data dengan deskriptor berhasil disimpan di: {output_path}")

if __name__ == "__main__":
    calculate_descriptors()
