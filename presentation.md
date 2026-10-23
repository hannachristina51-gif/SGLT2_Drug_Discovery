---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# SGLT2 Inhibitor Drug Discovery 🧬
**Pendekatan Machine Learning untuk Penemuan Obat**

---

## 🔍 Pendahuluan & Pengumpulan Data
- **Target Studi**: Sodium-glucose cotransporter 2 (SGLT2)
- **Sumber Data**: ChEMBL Database
- **Pemrosesan Data**: 
  - Total **4.114** data mentah awal berhasil diekstraksi.
  - Melalui proses pembersihan dan penyaringan, diperoleh **1.760** senyawa aktif (bersih) yang siap untuk dianalisis lebih lanjut.

---

## 📊 Exploratory Data Analysis (EDA)
Analisis eksploratif dilakukan untuk memahami karakteristik senyawa:
1. **Distribusi Kelas Bioaktivitas**: Memahami rasio senyawa aktif, tidak aktif, dan menengah.
2. **Ruang Kimia (Chemical Space)**: Analisis *Molecular Weight* (MW) terhadap *LogP* (Lipofilisitas) untuk melihat kepatuhan terhadap aturan Lipinski (Rule of Five).
3. **Boxplot pActivity**: Distribusi nilai bioaktivitas (pIC50) antar kelas senyawa.

---

## 🧪 Ekstraksi Fitur (Feature Engineering)
Data senyawa mentah tidak dapat langsung diproses oleh model, sehingga dilakukan ekstraksi fitur terhadap 1.755 data kurasi:
- **Lipinski Descriptors**: Mengekstrak properti fisikokimia (MW, LogP, NumHDonors, NumHAcceptors).
- **Morgan Fingerprints**: Representasi struktur molekul dalam bentuk vektor biner (1024-bit).
- **Hasil Akhir**: Total **1.035** kolom fitur yang digabungkan dan siap digunakan untuk pemodelan (disimpan dalam `curated_features_and_fingerprints.csv`).

---

## 🤖 Pemodelan Machine Learning
Model regresi dilatih untuk memprediksi nilai bioaktivitas (*pActivity*).
- **Algoritma Utama**: Random Forest Regressor
- **Evaluasi Kinerja Model**:
  - **RMSE (Root Mean Square Error)**: **0.6317** (tingkat kesalahan rata-rata prediksi cukup rendah).
  - **R-squared ($R^2$)**: **0.7297** (model mampu menjelaskan sekitar 73% varians dari data).

---

## 💊 Virtual Screening
Model yang telah dilatih digunakan untuk menyaring kandidat obat potensial (Virtual Screening):
- Menguji model terhadap **5 senyawa kandidat/uji**.
- **Hasil Signifikan**: **Dapagliflozin** (obat inhibitor SGLT2 komersial) berhasil diidentifikasi oleh model sebagai kandidat paling potensial dengan skor prediksi *pActivity* tertinggi yaitu **7.84**.
- Membuktikan bahwa model mampu mengenali senyawa obat aktif yang valid secara dunia nyata.

---

## 🏁 Kesimpulan
- Pipeline Machine Learning dari hulu ke hilir berhasil dibangun untuk prediksi inhibitor SGLT2.
- Penggunaan *Random Forest* dengan kombinasi *Fingerprint* dan *Lipinski Descriptors* menunjukkan performa yang sangat baik ($R^2$ = 0.73).
- Model siap dikembangkan lebih lanjut untuk *Virtual Screening* berskala besar pada database molekul (seperti ZINC atau PubChem).

---
# Terima Kasih 🙏
Ada pertanyaan?
