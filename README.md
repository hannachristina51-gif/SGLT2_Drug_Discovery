# SGLT2 Inhibitor - Virtual Screening & Drug Discovery Platform 🧬

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=hannachristina51-gif/SGLT2_Drug_Discovery&branch=main&mainModule=app.py)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![RDKit](https://img.shields.io/badge/RDKit-Cheminformatics-brightgreen.svg)](https://www.rdkit.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4+-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Platform *in-silico* dan *machine learning* komprehensif untuk menyaring (*virtual screening*) serta memprediksi potensi bioaktivitas kandidat obat inhibitor **Sodium-Glucose Cotransporter 2 (SGLT2 / *SLC5A2*)** dalam terapi pengobatan Diabetes Melitus Tipe 2.

Proyek ini mencakup alur kerja hulu ke hilir (*6-Stage End-to-End Pipeline*):
1. **Akuisisi Data Biologis ChEMBL**: Penarikan 4.114 data mentah bioaktivitas $IC_{50}$ dari ChEMBL Database (Target ID: `CHEMBL1808`).
2. **Prapemrosesan & Kurasi Data**: Sanitasi struktur SMILES kanonik, eliminasi duplikat, dan transformasi logaritmik nilai bioaktivitas $pActivity = -\log_{10}(IC_{50}\text{ Molar})$ menghasilkan **1.760 senyawa bersih**.
3. **Rekayasa Fitur Molekuler (*Hybrid Feature Engineering*)**: Penggabungan **2.048-bit Morgan Fingerprints** (ECFP4, `radius=2`) dan **4 Deskriptor Fisikokimia Lipinski** (MW, LogP, HBD, HBA) terstandarisasi (`StandardScaler`) $\rightarrow$ total **2.052 fitur/molekul**.
4. **Pemodelan & Validasi Machine Learning**: Pelatihan *Random Forest Regressor* dengan validasi struktural *Bemis-Murcko Scaffold Split* (70% Train : 30% Test), isolasi eksklusif *Dapagliflozin* di *Test Set*, dan optimasi *GridSearchCV* ($R^2 = 0.7297$, $\text{RMSE} = 0.6317$).
5. **Aplikasi Web Interaktif (`app.py`)**: Antarmuka berbasis *Streamlit* untuk prediksi molekul tunggal, menu *preset* obat kontrol 1-klik, visualisasi struktur 2D RDKit, evaluasi *Lipinski's Rule of Five*, serta penapisan massal (*Batch Screening*) via CSV.
6. **Pelaporan Resmi & Deployment Cloud**: Modul generator laporan PDF A4 mandiri (`pdf_report.py` berbasis `fpdf2`), fitur cetak dokumen langsung (*One-Click Browser Print*), serta paket siap-deploy untuk **Streamlit Community Cloud** dan **Hugging Face Spaces**.

---

## 🚀 Fitur Utama Aplikasi

- **🧬 Single Molecule Prediction**: Masukkan representasi string SMILES dari senyawa baru untuk memperoleh prediksi nilai bioaktivitas ($pActivity$ / $pIC_{50}$) dan konversi otomatis estimasi konsentrasi $IC_{50}$ dalam satuan adaptif (**nM**, **µM**, atau **mM**).
- **🎯 Menu Preset Molekul Acuan (1-Klik)**: Pilihan cepat untuk menguji molekul kontrol komersial (*Dapagliflozin, Empagliflozin, Canagliflozin, Metformin, Aspirin*) tanpa perlu mengetik string SMILES manual.
- **🔬 Visualisasi Struktur Molekuler 2D**: Rendering visual otomatis konformasi dua dimensi senyawa menggunakan mesin cheminformatics RDKit.
- **🧪 Validasi Aturan Lima Lipinski (*Rule of Five*)**: Pengecekan otomatis 4 parameter kelayakan sifat fisikokimia (*drug-likeness*) obat oral lengkap dengan indikator lulus/melanggar (✅/❌):
  - *Molecular Weight (MW)* $\le 500\text{ Da}$
  - *LogP (Lipofilisitas)* $\le 5.0$
  - *H-Bond Donors (HBD)* $\le 5$
  - *H-Bond Acceptors (HBA)* $\le 10$
- **🗂️ Batch Virtual Screening (CSV)**: Fasilitas unggah berkas CSV berisi puluhan hingga ribuan senyawa sekaligus (`smiles` atau `canonical_smiles`) untuk diskrining secara paralel lengkap dengan *progress bar* dan penghitungan jumlah pelanggaran Lipinski.
- **📄 Unduh Contoh Berkas CSV**: Tersedia tombol instan untuk mengunduh berkas template `sample_batch_sglt2.csv` bagi penguji atau pengguna baru.
- **📑 Ekspor Laporan PDF Lengkap (Single & Batch)**:
  - **Laporan PDF Senyawa Tunggal (A4 Resmi)**: Memuat gambar struktur 2D beresolusi tinggi via RDKit, rumus & berat molekul, metrik afinitas ($pActivity$ & $IC_{50}$), badge klasifikasi potensi farmakologis, tabel evaluasi 4 parameter *Lipinski's Rule of Five*, ringkasan metodologi AI, dan *scientific disclaimer*.
  - **Laporan PDF Rekapitulasi Batch Screening**: Menyajikan ringkasan statistik penapisan massal (proporsi senyawa Aktif, Intermediate, Tidak Aktif) serta **Tabel 20 Kandidat Inhibitor SGLT2 Teratas**.
- **🖨️ Fitur Cetak Dokumen Langsung (*One-Click Browser Print*)**: Pratinjau cetak interaktif berformat A4 dengan tata letak CSS `@media print` (`window.print()`) untuk mencetak langsung ke printer fisik atau menyimpan sebagai PDF.
- **📥 Ekspor Data Tabular (`.csv`)**: Unduh seluruh hasil prediksi senyawa tunggal maupun rekapitulasi batch dalam format `.csv`.
- **📖 Tab Metodologi & Petunjuk Sains**: Penjelasan terperinci mengenai rumus bioaktivitas, kriteria *Rule of Five*, dan arsitektur Machine Learning.

---

## 📊 Kinerja Model Machine Learning & Hasil Eksperimen

### 1. Ringkasan Metrik Evaluasi Utama
| Parameter / Metrik | Nilai Capaian | Keterangan Ilmiah |
|:---|:---|:---|
| **Algoritma Utama** | *Random Forest Regressor* | Ensambel pohon keputusan paralel yang tangguh terhadap matriks biner renggang (*sparse* 2.048-bit). |
| **Pemisahan Data** | *Bemis-Murcko Scaffold Split* | 70% Train, 30% Test berdasarkan kerangka cincin inti untuk mencegah *data leakage* & *overfitting*. |
| **R-squared ($R^2$)** | **0.7297** | Model mampu menerangkan $\approx 73\%$ variabilitas bioaktivitas senyawa. |
| **RMSE** | **0.6317** | Rata-rata deviasi galat prediksi rendah pada skala logaritmik $pIC_{50}$. |
| **Hyperparameter Optimal** | `n_estimators=300` | Ditemukan melalui `GridSearchCV` (`max_depth=None`, `min_samples_split=2`). |

### 2. Perbandingan Eksperimen Algoritma
| Konfigurasi Model | Metode Optimasi | Skor $R^2$ | Catatan Evaluasi |
|:---|:---|:---:|:---|
| **Random Forest Regressor (Model Utama)** | Baseline Optimal | **0.7297** | **RMSE = 0.6317 (Performa Terbaik ✅)** |
| RF + Hybrid 2.052 Fitur | `RandomizedSearchCV` (10 iter) | 0.7255 | Kombinasi 2048-bit ECFP4 + 4 Scaled Lipinski |
| RF + Hybrid 2.052 Fitur | `GridSearchCV` (81 fit) | 0.7233 | `n_estimators=300, max_depth=None` |
| HistGradientBoosting Regressor | `GridSearchCV` | 0.7044 | `learning_rate=0.2, max_depth=9, max_iter=100` |

### 3. Validasi Virtual Screening Senyawa Kontrol (`data/04_virtual_screening_results.csv`)
| Peringkat | Nama Senyawa Uji | Prediksi $pActivity$ | Estimasi $IC_{50}$ | Status Klasifikasi |
|:---:|:---|:---:|:---:|:---:|
| **#1 🏆** | **Dapagliflozin (Inhibitor SGLT2 Komersial)** | **7.84** | **14.33 nM** | **Potensial Aktif** |
| #2 | Caffeine (Stimulan SSP) | 6.84 | 144.33 nM | Potensial Aktif |
| #3 | Aspirin (Analgesik / Kontrol) | 6.67 | 215.55 nM | Potensial Aktif |
| #4 | Metformin (Antidiabetik Biguanid) | 6.42 | 378.52 nM | Potensial Aktif |
| #5 | Ibuprofen (NSAID) | 6.27 | 533.66 nM | Potensial Aktif |

---

## 🖥️ Materi Presentasi Proyek (PowerPoint 14 Slide Widescreen 16:9)

Repositori ini dilengkapi dengan slide presentasi komprehensif terbaru (**14 slide Widescreen 16:9**) yang mencakup latar belakang farmakologi SGLT2, grafik EDA asli, rekayasa fitur, komparasi model ML, struktur 2D RDKit, bedah fitur aplikasi web & generator PDF, arsitektur cloud, hingga peta jalan (*roadmap*) pengembangan Fase 1–3:
- 📊 **[Presentasi_SGLT2_Drug_Discovery_Terbaru.pptx](Presentasi_SGLT2_Drug_Discovery_Terbaru.pptx)** — Berkas PowerPoint terbaru siap presentasi.
- 📊 **[presentation.pptx](presentation.pptx)** — Salinan utama slide presentasi PowerPoint.
- 📝 **[presentation.md](presentation.md)** — Materi presentasi dalam format Markdown / Marp.
- 🐍 **[create_pptx.py](create_pptx.py)** — Skrip Python otomatis (`python-pptx` + `RDKit`) untuk membangun ulang slide presentasi.

---

## 📁 Struktur Repositori

```text
├── .devcontainer/                                    # Konfigurasi container development (GitHub Codespaces)
├── app.py                                            # Aplikasi web interaktif utama (Streamlit)
├── pdf_report.py                                     # Generator laporan PDF resmi A4 & template cetak interaktif
├── joblib/                                           # Pustaka serialisasi model (dibundel lokal cloud-ready)
├── fpdf/                                             # Pustaka generator PDF fpdf2 (dibundel lokal cloud-ready)
├── packages.txt                                      # Dependensi pustaka sistem Linux Debian (libxrender1, libxext6)
├── requirements.txt                                  # Dependensi pustaka Python cloud-ready (termasuk fpdf2)
├── README.md                                         # Dokumentasi utama repositori
├── README.txt                                        # Panduan ringkas teks polos (plain-text)
├── LogBook.md                                        # Buku log historis progres riset & pengembangan
├── TODO.md                                           # Peta jalan (roadmap) pengembangan strategis Fase 1–3
├── Presentasi_SGLT2_Drug_Discovery_Terbaru.pptx      # Slide presentasi PowerPoint terbaru (14 slide Widescreen 16:9)
├── presentation.pptx                                 # Slide presentasi PowerPoint utama
├── presentation.md                                   # Materi slide presentasi (Marp Markdown format)
├── create_pptx.py                                    # Skrip generator presentasi PowerPoint otomatis
├── run_windows.bat                                   # Skrip launcher cepat 1-klik untuk Windows
├── eval_metrics.py                                   # Skrip evaluasi metrik kinerja model (Train & Test)
├── deploy_to_hf.py                                   # Skrip otomatisasi deployment ke Hugging Face Spaces
├── hf_space/                                         # Bundel mandiri siap-deploy ke Hugging Face Spaces
│   ├── app.py
│   ├── pdf_report.py
│   ├── joblib/
│   ├── fpdf/
│   ├── README.md
│   ├── requirements.txt
│   ├── packages.txt
│   └── models/
├── data/                                             # Dataset mentah, kurasi bersih, deskriptor, & hasil screening
├── feature_extraction/                               # Modul dan hasil ekstraksi fitur molekuler (1.035 kolom)
├── models/                                           # Model Random Forest (rf_regressor_model.pkl) & StandardScaler
├── plots/                                            # Grafik visualisasi EDA (distribusi bioaktivitas & chemical space)
└── scripts/                                          # Pipeline modul skrip Python 01 s/d 06 (termasuk HGB & XGB)
```

---

## 🗺️ Ringkasan Peta Jalan Pengembangan (`TODO.md`)

1. **🚀 Fase 1 — Jangka Pendek (Validasi OECD QSAR & UI/UX)**:
   - *Applicability Domain (AD) Filter* berbasis *Tanimoto Similarity* / *Leverage*, *Uncertainty Quantification* (interval kepercayaan prediksi), *Model Explainability (SHAP / Morgan Bit Attribution)*, kanvas gambar molekul 2D interaktif (*Ketcher / JSME*), visualisasi konformasi 3D (`py3Dmol`), *Radar Chart* fisikokimia, serta fitur **Ekspor Laporan PDF & Cetak (Selesai ✅)**.
2. **🔬 Fase 2 — Jangka Menengah (Profil Farmasi Lanjutan & Polifarmakologi)**:
   - Dual-target rasio selektivitas **SGLT2 vs SGLT1** (*Selectivity Index*), skrining **ADMET & Toksisitas In-Silico** (*hERG*, *Caco-2*, *Ames test*, *SA Score*), **Database Bahan Alam / Herbal Indonesia** (*COCONUT / HerbalDB*), serta **Multi-Class Antidiabetic Profiling (MTDL)** lintas 6 golongan obat diabetes (*Biguanid, Sulfonilurea, AGI, DPP-4 Inhibitor, TZD, GLP-1 RA*).
3. **🧬 Fase 3 — Jangka Panjang (Deep Learning, Struktur 3D & Produksi)**:
   - Eksplorasi **Graph Neural Networks (GNN / Chemprop & ChemBERTa)**, integrasi **Automated Molecular Docking** (*AutoDock Vina / GNINA* pada struktur cryo-EM SGLT2 `PDB: 7VSI`), serta kontainerisasi **Docker & REST API Headless (`FastAPI`)**.

> Lihat rincian lengkap pada dokumen **[TODO.md](TODO.md)** dan riwayat perubahan pada **[LogBook.md](LogBook.md)**.

---

## 💻 Panduan Menjalankan Secara Lokal

### Prasyarat
- Python 3.9 – 3.12
- Git

### Langkah Instalasi
```bash
# 1. Clone repositori ini
git clone https://github.com/hannachristina51-gif/SGLT2_Drug_Discovery.git
cd SGLT2_Drug_Discovery

# 2. Buat dan aktifkan Virtual Environment
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# atau
venv\Scripts\activate           # Windows (atau klik 2x file run_windows.bat)

# 3. Instal dependensi
pip install -r requirements.txt

# 4. Jalankan aplikasi web Streamlit
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser lokal Anda pada alamat: `http://localhost:8501`.

---

## 🌐 Deployment Cloud

### Opsi 1: Streamlit Community Cloud (Rekomendasi Utama)
Aplikasi ini telah dioptimasi penuh untuk Streamlit Community Cloud (dilengkapi pembundelan lokal `joblib/` & `fpdf/` untuk kompatibilitas Debian Linux PEP 668, pemindaian dinamis `site-packages`, serta `packages.txt`). Luncurkan dengan 1-klik:
👉 **[Deploy ke Streamlit Cloud](https://share.streamlit.io/deploy?repository=hannachristina51-gif/SGLT2_Drug_Discovery&branch=main&mainModule=app.py)**

### Opsi 2: Hugging Face Spaces
Paket mandiri siap-deploy tersedia di folder `hf_space/`. Untuk mengunggah secara otomatis:
```bash
python deploy_to_hf.py
```
Atau *drag & drop* seluruh isi folder `hf_space/` ke Hugging Face Space baru bertipe **Streamlit**.

---

## 👥 Tim & Pengembang
- **Peneliti & Pengembang**: Hanna Christina Ginting (NPM: 2506713353) — Universitas Indonesia
- **Dosen Pengampu / Pembimbing**: Prof. Arry
