import pandas as pd
import numpy as np
import os

def preprocess_data():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    input_path = os.path.join(data_dir, '01_sglt2_raw_data.csv')
    
    if not os.path.exists(input_path):
        print(f"File tidak ditemukan: {input_path}")
        return
        
    print(f"Memuat data mentah dari {input_path}")
    df = pd.read_csv(input_path)
    print(f"Jumlah data awal: {len(df)}")
    
    # Memfilter data yang tidak memiliki standard_value atau canonical_smiles
    df2 = df[df.standard_value.notna()]
    df2 = df2[df2.canonical_smiles.notna()]
    
    # Hanya ambil kolom yang penting
    selection = ['molecule_chembl_id', 'canonical_smiles', 'standard_type', 'standard_value', 'standard_units']
    df3 = df2[selection].copy()
    
    # Hapus duplikat berdasarkan canonical_smiles
    df3 = df3.drop_duplicates(subset=['canonical_smiles'])
    print(f"Jumlah data setelah dibersihkan: {len(df3)}")
    
    # Konversi standard_value ke numerik dan tangani nilai-nilai ekstrem
    df3['standard_value'] = pd.to_numeric(df3['standard_value'], errors='coerce')
    df3 = df3.dropna(subset=['standard_value'])
    
    # Menghitung pIC50 (-log10(IC50 dalam Molar))
    # Nilai dari ChEMBL biasanya dalam nM (nanomolar), jadi kita ubah ke Molar
    def pIC50(value):
        # Mencegah log(0) atau nilai negatif/terlalu kecil
        molar = value * 10**-9
        if molar > 0:
            return -np.log10(molar)
        return None

    print("Menghitung pActivity (-log10(value dalam Molar))...")
    df3['pActivity'] = df3['standard_value'].apply(pIC50)
    df3 = df3.dropna(subset=['pActivity'])
    
    # Mengklasifikasikan bioaktivitas
    # Threshold yang umum digunakan:
    # Aktif: Activity < 1000 nM (pActivity > 6)
    # Tidak Aktif: Activity >= 10000 nM (pActivity <= 5)
    # Intermediate: 1000 nM <= Activity < 10000 nM
    def classify_activity(pact):
        if pact > 6.0:
            return 'active'
        elif pact <= 5.0:
            return 'inactive'
        else:
            return 'intermediate'
            
    df3['bioactivity_class'] = df3['pActivity'].apply(classify_activity)
    
    print(f"Distribusi kelas bioaktivitas:\n{df3['bioactivity_class'].value_counts()}")
    
    # Menyimpan data yang sudah diproses ke CSV
    output_path = os.path.join(data_dir, '02_sglt2_processed_data.csv')
    df3.to_csv(output_path, index=False)
    print(f"Data yang diproses berhasil disimpan di: {output_path}")

if __name__ == "__main__":
    preprocess_data()
