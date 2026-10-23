import pandas as pd
import numpy as np
import os
from rdkit import Chem
from rdkit.Chem import AllChem
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import warnings
warnings.filterwarnings('ignore')

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

def run_ml_training():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, 'data', '03_sglt2_with_descriptors.csv')
    model_dir = os.path.join(base_dir, 'models')
    
    if not os.path.exists(data_path):
        print(f"Data tidak ditemukan di {data_path}")
        return
        
    print("Memuat dataset...")
    df = pd.read_csv(data_path)
    
    # Hapus baris dengan nilai kosong di target atau deskriptor numerik
    df = df.dropna(subset=['pActivity', 'MW', 'LogP', 'NumHDonors', 'NumHAcceptors'])
    
    dapa_smiles = "O[C@H]1[C@H](C2=CC(CC3=CC=C(OCC)C=C3)=C(Cl)C=C2)O[C@H](CO)[C@@H](O)[C@@H]1O"
    
    # Standarisasi SMILES Dapagliflozin dengan RDKit
    dapa_mol = Chem.MolFromSmiles(dapa_smiles)
    dapa_canonical = Chem.MolToSmiles(dapa_mol) if dapa_mol else dapa_smiles

    def is_dapa(s):
        mol = Chem.MolFromSmiles(s)
        if mol:
            return Chem.MolToSmiles(mol) == dapa_canonical
        return False
        
    print("Mencari senyawa Dapagliflozin di dataset...")
    df['is_dapa'] = df['canonical_smiles'].apply(is_dapa)
    
    df_dapa = df[df['is_dapa']]
    df_others = df[~df['is_dapa']]
    
    print(f"Ditemukan {len(df_dapa)} baris Dapagliflozin yang akan dimasukkan ke Test Set secara eksklusif.")
    
    # Menyiapkan fitur numerik (Lipinski descriptors)
    num_cols = ['MW', 'LogP', 'NumHDonors', 'NumHAcceptors']
    
    X_others_num = df_others[num_cols].values
    Y_others = df_others['pActivity'].values
    
    print("Menghitung Morgan Fingerprints...")
    X_others_fp = get_morgan_fingerprints(df_others['canonical_smiles'].values)
    
    # Split data sisanya menjadi training (70%) dan testing (30%)
    X_train_num, X_test_num, X_train_fp, X_test_fp, Y_train, Y_test_part = train_test_split(
        X_others_num, X_others_fp, Y_others, test_size=0.3, random_state=42
    )
    
    # Scaling fitur numerik (fit pada train, transform pada train dan test)
    scaler = StandardScaler()
    X_train_num_scaled = scaler.fit_transform(X_train_num)
    X_test_num_scaled = scaler.transform(X_test_num)
    
    # Gabungkan Fingerprints + Lipinski (Scaled)
    X_train = np.hstack([X_train_fp, X_train_num_scaled])
    X_test_part_combined = np.hstack([X_test_fp, X_test_num_scaled])
    
    if len(df_dapa) > 0:
        X_dapa_num = df_dapa[num_cols].values
        X_dapa_num_scaled = scaler.transform(X_dapa_num)
        X_dapa_fp = get_morgan_fingerprints(df_dapa['canonical_smiles'].values)
        X_dapa = np.hstack([X_dapa_fp, X_dapa_num_scaled])
        Y_dapa = df_dapa['pActivity'].values
        
        # Gabungkan Dapagliflozin HANYA ke Test Set
        X_test = np.vstack([X_test_part_combined, X_dapa])
        Y_test = np.concatenate([Y_test_part, Y_dapa])
    else:
        X_test = X_test_part_combined
        Y_test = Y_test_part
        print("Peringatan: Dapagliflozin tidak ditemukan di dalam data yang sedang diproses.")
    
    print(f"Jumlah Training Set (70%): {len(X_train)} senyawa, {X_train.shape[1]} fitur")
    print(f"Jumlah Testing Set (30% + Dapagliflozin): {len(X_test)} senyawa, {X_test.shape[1]} fitur")
    
    print("\nMulai Full Hyperparameter Tuning menggunakan GridSearchCV untuk HistGradientBoosting...")
    hgb_model = HistGradientBoostingRegressor(random_state=42)
    
    # Parameter grid untuk HistGradientBoosting
    param_grid = {
        'max_iter': [100, 200, 300], # Setara dengan n_estimators
        'max_depth': [3, 6, 9],
        'learning_rate': [0.01, 0.1, 0.2]
    }
    
    grid_search = GridSearchCV(
        estimator=hgb_model,
        param_grid=param_grid,
        cv=3, 
        verbose=2, 
        n_jobs=-1
    )
    
    grid_search.fit(X_train, Y_train)
    print(f"\nParameter Terbaik Ditemukan: {grid_search.best_params_}")
    
    best_model = grid_search.best_estimator_
    print("Mengevaluasi model final HistGradientBoosting...")
    Y_pred = best_model.predict(X_test)
    
    mse = mean_squared_error(Y_test, Y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(Y_test, Y_pred)
    
    print(f"Model Performance HistGradientBoosting:")
    print(f"RMSE: {rmse:.4f}")
    print(f"R-squared: {r2:.4f}")
    
    # Simpan model dan scaler
    model_path = os.path.join(model_dir, 'hgb_regressor_model.pkl')
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    joblib.dump(best_model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Model dan Scaler berhasil disimpan di folder {model_dir}")

if __name__ == "__main__":
    run_ml_training()
