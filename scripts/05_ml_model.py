import pandas as pd
import numpy as np
import os
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Scaffolds import MurckoScaffold
from collections import defaultdict
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
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

def generate_scaffolds(df):
    scaffolds = defaultdict(list)
    for idx, smiles in enumerate(df['canonical_smiles']):
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            try:
                scaffold = MurckoScaffold.MurckoScaffoldSmiles(mol=mol, includeChirality=False)
                scaffolds[scaffold].append(idx)
            except:
                scaffolds[''].append(idx)
        else:
            scaffolds[''].append(idx)
    return scaffolds

def scaffold_split(df, frac_train=0.7):
    scaffolds = generate_scaffolds(df)
    # Urutkan scaffold dari yang anggotanya paling banyak
    scaffold_sets = [scaffolds[scaffold] for scaffold in sorted(scaffolds, key=lambda k: len(scaffolds[k]), reverse=True)]
    
    train_idx = []
    test_idx = []
    
    train_cutoff = int(len(df) * frac_train)
    
    for scaffold_set in scaffold_sets:
        if len(train_idx) + len(scaffold_set) > train_cutoff:
            test_idx.extend(scaffold_set)
        else:
            train_idx.extend(scaffold_set)
            
    return train_idx, test_idx

def run_ml_training():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, 'data', '03_sglt2_with_descriptors.csv')
    model_dir = os.path.join(base_dir, 'models')
    
    if not os.path.exists(data_path):
        print(f"Data tidak ditemukan di {data_path}")
        return
        
    print("Memuat dataset...")
    df = pd.read_csv(data_path)
    
    # Hapus baris dengan nilai kosong
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
    df_others = df[~df['is_dapa']].reset_index(drop=True)
    
    print(f"Ditemukan {len(df_dapa)} baris Dapagliflozin yang akan dimasukkan ke Test Set secara eksklusif.")
    
    # Scaffold Split
    print("Melakukan Scaffold Split (70% Train, 30% Test) untuk meminimalkan overfitting...")
    train_idx, test_idx = scaffold_split(df_others, frac_train=0.7)
    
    df_train = df_others.iloc[train_idx]
    df_test_part = df_others.iloc[test_idx]
    
    # Menyiapkan fitur
    num_cols = ['MW', 'LogP', 'NumHDonors', 'NumHAcceptors']
    
    X_train_num = df_train[num_cols].values
    X_test_num = df_test_part[num_cols].values
    Y_train = df_train['pActivity'].values
    Y_test_part = df_test_part['pActivity'].values
    
    print("Menghitung Morgan Fingerprints...")
    X_train_fp = get_morgan_fingerprints(df_train['canonical_smiles'].values)
    X_test_fp = get_morgan_fingerprints(df_test_part['canonical_smiles'].values)
    
    # Scaling fitur numerik (fit pada train, transform pada train dan test)
    scaler = StandardScaler()
    X_train_num_scaled = scaler.fit_transform(X_train_num)
    X_test_num_scaled = scaler.transform(X_test_num)
    
    # Gabungkan Fingerprints + Lipinski (Scaled)
    X_train = np.hstack([X_train_fp, X_train_num_scaled])
    X_test_part_combined = np.hstack([X_test_fp, X_test_num_scaled])
    
    # Proses Dapagliflozin (Masukkan ke Test Set)
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
    
    print(f"Jumlah Training Set (Scaffold, 70%): {len(X_train)} senyawa, {X_train.shape[1]} fitur")
    print(f"Jumlah Testing Set (Scaffold, 30% + Dapagliflozin): {len(X_test)} senyawa, {X_test.shape[1]} fitur")
    
    print("\nMulai Hyperparameter Tuning menggunakan GridSearchCV...")
    rf = RandomForestRegressor(random_state=42)
    
    # Parameter grid full
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10]
    }
    
    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=3, 
        verbose=2, 
        n_jobs=-1
    )
    
    grid_search.fit(X_train, Y_train)
    print(f"\nParameter Terbaik Ditemukan: {grid_search.best_params_}")
    
    best_model = grid_search.best_estimator_
    print("Mengevaluasi model final...")
    Y_pred = best_model.predict(X_test)
    
    mse = mean_squared_error(Y_test, Y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(Y_test, Y_pred)
    
    print(f"Model Performance (Setelah Scaffold Split & Tuning):")
    print(f"RMSE: {rmse:.4f}")
    print(f"R-squared: {r2:.4f}")
    
    # Simpan model dan scaler
    model_path = os.path.join(model_dir, 'rf_regressor_model.pkl')
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    joblib.dump(best_model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Model dan Scaler berhasil disimpan di folder {model_dir}")

if __name__ == "__main__":
    run_ml_training()
