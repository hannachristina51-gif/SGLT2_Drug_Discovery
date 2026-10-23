import pandas as pd
import numpy as np
import os
import joblib
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Scaffolds import MurckoScaffold
from collections import defaultdict
from sklearn.metrics import mean_squared_error, r2_score

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

def main():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, 'data', '03_sglt2_with_descriptors.csv')
    model_path = os.path.join(base_dir, 'models', 'rf_regressor_model.pkl')
    scaler_path = os.path.join(base_dir, 'models', 'scaler.pkl')
    
    df = pd.read_csv(data_path).dropna(subset=['pActivity', 'MW', 'LogP', 'NumHDonors', 'NumHAcceptors'])
    
    dapa_smiles = "O[C@H]1[C@H](C2=CC(CC3=CC=C(OCC)C=C3)=C(Cl)C=C2)O[C@H](CO)[C@@H](O)[C@@H]1O"
    dapa_mol = Chem.MolFromSmiles(dapa_smiles)
    dapa_canonical = Chem.MolToSmiles(dapa_mol) if dapa_mol else dapa_smiles

    def is_dapa(s):
        mol = Chem.MolFromSmiles(s)
        return Chem.MolToSmiles(mol) == dapa_canonical if mol else False
        
    df['is_dapa'] = df['canonical_smiles'].apply(is_dapa)
    df_dapa = df[df['is_dapa']]
    df_others = df[~df['is_dapa']].reset_index(drop=True)
    
    train_idx, test_idx = scaffold_split(df_others, frac_train=0.7)
    
    df_train = df_others.iloc[train_idx]
    df_test_part = df_others.iloc[test_idx]
    
    num_cols = ['MW', 'LogP', 'NumHDonors', 'NumHAcceptors']
    
    X_train_num = df_train[num_cols].values
    X_test_num = df_test_part[num_cols].values
    Y_train = df_train['pActivity'].values
    Y_test_part = df_test_part['pActivity'].values
    
    X_train_fp = get_morgan_fingerprints(df_train['canonical_smiles'].values)
    X_test_fp = get_morgan_fingerprints(df_test_part['canonical_smiles'].values)
    
    scaler = joblib.load(scaler_path)
    X_train_num_scaled = scaler.transform(X_train_num)
    X_test_num_scaled = scaler.transform(X_test_num)
    
    X_train = np.hstack([X_train_fp, X_train_num_scaled])
    X_test_part_combined = np.hstack([X_test_fp, X_test_num_scaled])
    
    if len(df_dapa) > 0:
        X_dapa_num = df_dapa[num_cols].values
        X_dapa_num_scaled = scaler.transform(X_dapa_num)
        X_dapa_fp = get_morgan_fingerprints(df_dapa['canonical_smiles'].values)
        X_dapa = np.hstack([X_dapa_fp, X_dapa_num_scaled])
        Y_dapa = df_dapa['pActivity'].values
        
        X_test = np.vstack([X_test_part_combined, X_dapa])
        Y_test = np.concatenate([Y_test_part, Y_dapa])
    else:
        X_test = X_test_part_combined
        Y_test = Y_test_part
        
    model = joblib.load(model_path)
    
    # Evaluasi Train
    Y_train_pred = model.predict(X_train)
    rmse_train = np.sqrt(mean_squared_error(Y_train, Y_train_pred))
    r2_train = r2_score(Y_train, Y_train_pred)
    
    # Evaluasi Test
    Y_test_pred = model.predict(X_test)
    rmse_test = np.sqrt(mean_squared_error(Y_test, Y_test_pred))
    r2_test = r2_score(Y_test, Y_test_pred)
    
    print("--- HASIL EVALUASI MODEL ---")
    print(f"Training Set (n={len(X_train)}):")
    print(f"  RMSE: {rmse_train:.4f}")
    print(f"  R^2 : {r2_train:.4f}")
    print(f"\nTest Set (n={len(X_test)}):")
    print(f"  RMSE: {rmse_test:.4f}")
    print(f"  R^2 : {r2_test:.4f}")

if __name__ == "__main__":
    main()
