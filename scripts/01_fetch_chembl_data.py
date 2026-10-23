import pandas as pd
from chembl_webresource_client.new_client import new_client
import os

def fetch_sglt2_data():
    print("Mencari data target SGLT2 di ChEMBL...")
    target = new_client.target
    target_query = target.search('SGLT2')
    targets = pd.DataFrame.from_dict(target_query)
    
    # Pilih target SGLT2 manusia (CHEMBL3884)
    selected_target = targets[targets['target_chembl_id'] == 'CHEMBL3884'].iloc[0]
    chembl_id = selected_target['target_chembl_id']
    print(f"Target yang dipilih: {selected_target['pref_name']} ({chembl_id})")

    # Mengambil semua data bioaktivitas untuk target ini (semua metrik)
    print("Mengunduh data bioaktivitas...")
    activity = new_client.activity
    res = activity.filter(target_chembl_id=chembl_id)
    
    df = pd.DataFrame.from_dict(res)
    print(f"Total data bioaktivitas yang diunduh: {len(df)}")
    
    # Membuat direktori data jika belum ada
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Menyimpan data mentah ke CSV
    output_path = os.path.join(data_dir, '01_sglt2_raw_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Data mentah berhasil disimpan di: {output_path}")

if __name__ == "__main__":
    fetch_sglt2_data()
