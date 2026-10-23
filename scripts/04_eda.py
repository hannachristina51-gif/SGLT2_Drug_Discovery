import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, 'data', '03_sglt2_with_descriptors.csv')
    plots_dir = os.path.join(base_dir, 'plots')
    
    if not os.path.exists(data_path):
        print(f"Data tidak ditemukan di {data_path}")
        return
        
    print(f"Memuat data dari {data_path}...")
    df = pd.read_csv(data_path)
    
    # 1. Plot Distribusi Kelas Bioaktivitas
    plt.figure(figsize=(8, 6))
    sns.countplot(x='bioactivity_class', data=df, edgecolor='black', palette='viridis')
    plt.title('Distribusi Kelas Bioaktivitas SGLT2', fontsize=14)
    plt.xlabel('Kelas Bioaktivitas', fontsize=12)
    plt.ylabel('Frekuensi', fontsize=12)
    plot1_path = os.path.join(plots_dir, '01_bioactivity_distribution.png')
    plt.savefig(plot1_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Plot distribusi kelas disimpan di {plot1_path}")
    
    # 2. Scatter Plot: MW vs LogP
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='MW', y='LogP', data=df, hue='bioactivity_class', size='pActivity', alpha=0.7, palette='Set1')
    plt.title('Ruang Kimia: Berat Molekul (MW) vs LogP', fontsize=14)
    plt.xlabel('Molecular Weight (MW)', fontsize=12)
    plt.ylabel('LogP', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plot2_path = os.path.join(plots_dir, '02_chemical_space_mw_logp.png')
    plt.savefig(plot2_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Plot scatter ruang kimia disimpan di {plot2_path}")
    
    # 3. Boxplot pActivity berdasarkan kelas
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='bioactivity_class', y='pActivity', data=df, palette='Set2')
    plt.title('Distribusi Nilai pActivity per Kelas', fontsize=14)
    plt.xlabel('Kelas Bioaktivitas', fontsize=12)
    plt.ylabel('pActivity (-log(Molar))', fontsize=12)
    plot3_path = os.path.join(plots_dir, '03_pActivity_boxplot.png')
    plt.savefig(plot3_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Plot boxplot pActivity disimpan di {plot3_path}")
    
    print("EDA selesai.")

if __name__ == "__main__":
    run_eda()
