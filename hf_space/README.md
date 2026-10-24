---
title: SGLT2 Inhibitor Virtual Screening
emoji: 🧬
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
license: mit
---

# SGLT2 Inhibitor - Virtual Screening & Drug Discovery Platform 🧬

Aplikasi *Machine Learning* interaktif untuk penemuan obat kandidat inhibitor **Sodium-Glucose Cotransporter 2 (SGLT2)**, target terapi utama pada pengobatan Diabetes Melitus Tipe 2.

## 🔬 Informasi Target & Data
- **Target Biologis**: Human Sodium-Glucose Cotransporter 2 (SGLT2 / *SLC5A2*)
- **Sumber Data Bioaktivitas**: Database ChEMBL (Target ID: `CHEMBL1808`)
- **Jumlah Senyawa Terkurasi**: 1.760 senyawa aktif terstandardisasi.
- **Representasi Fitur**:
  - *Morgan Fingerprints* (Radius 2, 2.048-bit ECFP4)
  - *Lipinski Physicochemical Descriptors* (Molecular Weight, LogP, H-Bond Donors, H-Bond Acceptors)

## 🤖 Kinerja Model Machine Learning
- **Algoritma**: Random Forest Regressor
- **Validasi Struktural**: *Bemis-Murcko Scaffold Split* (70% Train, 30% Test) untuk mencegah kebocoran informasi (*data leakage*) antar kerangka molekul.
- **Hyperparameter Tuning**: `n_estimators=300`, `max_depth=None`, `min_samples_split=2`.
- **Metrik Evaluasi**: $R^2 \approx 0.73$, $RMSE \approx 0.63$.
- **Validasi Dunia Nyata**: Senyawa komersial *Dapagliflozin* berhasil diidentifikasi secara tepat sebagai kandidat teratas dengan skor bioaktivitas tertinggi ($pActivity = 7.84$).

## ⚙️ Fitur Aplikasi
1. **Single Molecule Prediction**: Prediksi nilai bioaktivitas ($pActivity$) dan estimasi $IC_{50}$ (nM) dari representasi SMILES.
2. **Menu Preset Molekul Acuan**: Pilihan cepat 1-klik untuk senyawa komersial (*Dapagliflozin, Empagliflozin, Canagliflozin, Metformin, Aspirin*).
3. **Visualisasi Struktur 2D**: Rendering otomatis konformasi 2D molekul menggunakan RDKit.
4. **Validasi Lipinski's Rule of Five**: Analisis kelayakan *drug-likeness* secara instan.
5. **Batch Virtual Screening**: Skrining massal hingga ratusan senyawa via unggah file CSV.
6. **Unduh Contoh File CSV**: Fasilitas instan untuk mengunduh template CSV pengujian.
7. **Ekspor Laporan**: Unduh hasil analisis langsung dalam format CSV.
8. **Tab Metodologi**: Penjelasan teoritis mengenai target, rumus bioaktivitas, dan arsitektur model.

