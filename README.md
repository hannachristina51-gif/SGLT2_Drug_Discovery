# SGLT2 Inhibitor - Virtual Screening & Drug Discovery Platform 🧬

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io)
[![RDKit](https://img.shields.io/badge/RDKit-Cheminformatics-brightgreen.svg)](https://www.rdkit.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Aplikasi *in-silico* dan *machine learning* komprehensif untuk menyaring (*virtual screening*) dan memprediksi potensi bioaktivitas kandidat obat inhibitor **Sodium-Glucose Cotransporter 2 (SGLT2)** dalam terapi pengobatan Diabetes Melitus Tipe 2.

Proyek ini mencakup alur lengkap (*end-to-end pipeline*):
1. **Ekstraksi Data Biologis**: Penarikan data mentah bioaktivitas dari ChEMBL Database (Target ID: `CHEMBL1808`).
2. **Prapemrosesan & Kurasi**: Standardisasi struktur molekul, penghapusan duplikat, dan kalkulasi $pActivity$ ($-\log_{10} IC_{50}$).
3. **Rekayasa Fitur**: Ekstraksi *Morgan Fingerprints* (ECFP4, 2.048-bit) dan *Lipinski Physicochemical Descriptors* (MW, LogP, HBD, HBA).
4. **Pemodelan Machine Learning**: Pelatihan model *Random Forest Regressor* dengan *Bemis-Murcko Scaffold Split* dan *Hyperparameter Tuning* ($R^2 \approx 0.73$).
5. **Antarmuka Pengguna Interaktif (Web App)**: Aplikasi berbasis web dengan framework *Streamlit* untuk prediksi instan, visualisasi struktur 2D molekuler, dan skrining massal via CSV.

---

## 🚀 Fitur Utama Aplikasi

- **🧬 Single Molecule Prediction**: Masukkan representasi string SMILES dari senyawa baru untuk memperoleh prediksi nilai bioaktivitas ($pActivity$) dan estimasi nilai $IC_{50}$ dalam satuan nanomolar (nM).
- **🔬 Visualisasi Struktur Molekuler 2D**: Rendering visual otomatis konformasi dua dimensi senyawa menggunakan mesin kimia komputasi RDKit.
- **🧪 Validasi Aturan Lima Lipinski (*Rule of Five*)**: Pengecekan otomatis parameter kelayakan sifat fisikokimia (*drug-likeness*) obat oral:
  - *Molecular Weight (MW) $\le 500$ Da*
  - *LogP (Lipofilisitas) $\le 5$*
  - *H-Bond Donors (HBD) $\le 5$*
  - *H-Bond Acceptors (HBA) $\le 10$*
- **🗂️ Batch Virtual Screening**: Fasilitas unggah berkas CSV berisi ratusan hingga ribuan senyawa sekaligus untuk diskrining secara paralel dan massal.
- **📥 Ekspor Laporan Otomatis**: Unduh seluruh hasil analisis baik senyawa tunggal maupun batch ke dalam format berkas `.csv`.

---

## 📊 Kinerja Model Machine Learning

| Metrik Evaluasi | Nilai Capaian | Keterangan |
|:---|:---|:---|
| **Algoritma Utama** | *Random Forest Regressor* | Ensambel pohon keputusan paralel yang tangguh terhadap matriks biner renggang (*sparse*). |
| **Pemisahan Data** | *Bemis-Murcko Scaffold Split* | 70% Train, 30% Test berdasarkan kemiripan kerangka inti untuk mengeliminasi bias *overfitting*. |
| **R-squared ($R^2$)** | **0.7297** | Model mampu menerangkan $\approx 73\%$ variabilitas bioaktivitas senyawa. |
| **RMSE** | **0.6317** | Rata-rata deviasi galat prediksi sangat rendah pada skala logaritmik. |
| **Validasi Kontrol** | *Dapagliflozin* | Obat komersial SGLT2 inhibitor terbukti diprediksi aktif dengan skor tertinggi ($pActivity = 7.84$). |

---

## 📁 Struktur Repositori

```text
├── app.py                      # Aplikasi web interaktif utama (Streamlit)
├── LogBook.md                  # Buku log historis progres riset mingguan
├── TODO.md                     # Roadmap pengembangan strategis & to-do list
├── requirements.txt            # Dependensi pustaka Python
├── run_windows.bat             # Skrip launcher cepat untuk Windows
├── create_pptx.py              # Generator presentasi otomatis
├── presentation.md             # Bahan materi slide presentasi (Marp format)
├── presentation.pptx           # Slide presentasi PowerPoint
├── eval_metrics.py             # Evaluasi metrik kinerja model
├── deploy_to_hf.py             # Skrip otomatisasi deployment ke Hugging Face Spaces
├── hf_space/                   # Bundel mandiri siap-deploy ke Hugging Face Spaces
│   ├── app.py
│   ├── README.md
│   ├── requirements.txt
│   ├── packages.txt
│   └── models/
├── data/                       # Dataset mentah, bersih, dan hasil virtual screening
├── feature_extraction/         # Modul dan hasil ekstraksi fitur molekuler
├── models/                     # Model Random Forest (.pkl) & StandardScaler (.pkl)
├── plots/                      # Grafik visualisasi EDA (bioaktivitas & chemical space)
└── scripts/                    # Pipeline modul Python 01 s/d 06
```

---

## 💻 Panduan Menjalankan Secara Lokal

### Prasyarat
- Python 3.8 – 3.11
- Git

### Langkah Instalasi
```bash
# 1. Clone repositori ini
git clone https://github.com/hannachristina51-gif/SGLT2_Drug_Discovery.git
cd SGLT2_Drug_Discovery

# 2. Buat dan aktifkan Virtual Environment
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
# atau
venv\Scripts\activate           # Windows

# 3. Instal dependensi
pip install -r requirements.txt

# 4. Jalankan aplikasi web
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser lokal Anda pada alamat: `http://localhost:8501`.

---

## 🌐 Deployment Cloud (Hugging Face Spaces)

Aplikasi ini telah dilengkapi bundel siap-deploy di folder `hf_space/`. Untuk mengunggah secara otomatis:
```bash
python deploy_to_hf.py
```
Atau ikuti panduan lengkap pada [TODO.md](TODO.md) dan [LogBook.md](LogBook.md).

---

## 👥 Tim & Pengembang
- **Peneliti**: Hanna Christina Ginting (NPM: 2506713353) — Universitas Indonesia
- **Pembimbing / Dosen Pengampu**: Prof. Arry
