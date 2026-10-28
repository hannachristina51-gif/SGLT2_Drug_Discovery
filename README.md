# SGLT2 Inhibitor - Virtual Screening & Drug Discovery Platform 🧬

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=hannachristina51-gif/SGLT2_Drug_Discovery&branch=main&mainModule=app.py)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![RDKit](https://img.shields.io/badge/RDKit-Cheminformatics-brightgreen.svg)](https://www.rdkit.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4+-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Aplikasi *in-silico* dan *machine learning* komprehensif untuk menyaring (*virtual screening*) dan memprediksi potensi bioaktivitas kandidat obat inhibitor **Sodium-Glucose Cotransporter 2 (SGLT2)** dalam terapi pengobatan Diabetes Melitus Tipe 2.

Proyek ini mencakup alur lengkap (*end-to-end pipeline*):
1. **Ekstraksi Data Biologis**: Penarikan data mentah bioaktivitas dari ChEMBL Database (Target ID: `CHEMBL1808`).
2. **Prapemrosesan & Kurasi**: Standardisasi struktur molekul, eliminasi duplikat, dan kalkulasi nilai bioaktivitas $pActivity$ ($-\log_{10} IC_{50}$).
3. **Rekayasa Fitur**: Ekstraksi *Morgan Fingerprints* (ECFP4, 2.048-bit) dan *Lipinski Physicochemical Descriptors* (MW, LogP, HBD, HBA).
4. **Pemodelan Machine Learning**: Pelatihan model *Random Forest Regressor* dengan *Bemis-Murcko Scaffold Split* dan *Hyperparameter Tuning* ($R^2 \approx 0.73$).
5. **Antarmuka Pengguna Interaktif (Web App)**: Aplikasi berbasis web dengan framework *Streamlit* untuk prediksi instan, visualisasi struktur 2D molekuler, dan skrining massal via CSV.

---

## 🚀 Fitur Utama Aplikasi

- **🧬 Single Molecule Prediction**: Masukkan representasi string SMILES dari senyawa baru untuk memperoleh prediksi nilai bioaktivitas ($pActivity$) dan estimasi nilai $IC_{50}$ dalam satuan nanomolar (nM).
- **🎯 Menu Preset Molekul Acuan**: Pilihan cepat 1-klik untuk molekul kontrol komersial (*Dapagliflozin, Empagliflozin, Canagliflozin, Metformin, Aspirin*) tanpa perlu mengetik string SMILES manual.
- **🔬 Visualisasi Struktur Molekuler 2D**: Rendering visual otomatis konformasi dua dimensi senyawa menggunakan mesin kimia komputasi RDKit.
- **🧪 Validasi Aturan Lima Lipinski (*Rule of Five*)**: Pengecekan otomatis parameter kelayakan sifat fisikokimia (*drug-likeness*) obat oral:
  - *Molecular Weight (MW) $\le 500$ Da*
  - *LogP (Lipofilisitas) $\le 5$*
  - *H-Bond Donors (HBD) $\le 5$*
  - *H-Bond Acceptors (HBA) $\le 10$*
- **🗂️ Batch Virtual Screening**: Fasilitas unggah berkas CSV berisi ratusan hingga ribuan senyawa sekaligus untuk diskrining secara paralel dan massal.
- **📄 Unduh Contoh Berkas CSV**: Tersedia tombol instan untuk mengunduh contoh berkas CSV pengujian bagi reviewer atau pengguna baru.
- **📑 Ekspor Laporan PDF Lengkap**: Unduh berkas laporan resmi A4 format PDF yang memuat rendering struktur 2D beresolusi tinggi via RDKit, nilai afinitas ($pIC_{50}$ & $IC_{50}$), tabel evaluasi 4 parameter *Lipinski's Rule of Five*, ringkasan metodologi AI, dan *scientific disclaimer*.
- **🖨️ Fitur Cetak Dokumen Langsung (*One-Click Browser Print*)**: Pratinjau cetak interaktif dengan tata letak rapi CSS `@media print` untuk mencetak dokumen langsung ke printer fisik atau menyimpan sebagai file PDF bawaan sistem.
- **📥 Ekspor Data Tabular (.csv)**: Unduh seluruh data hasil prediksi senyawa tunggal maupun rekapitulasi massal (batch) dalam format berkas `.csv`.
- **📖 Tab Metodologi Sains**: Penjelasan terperinci mengenai metrik bioaktivitas, rumus perhitungan $IC_{50}$, aturan Lipinski, dan arsitektur model.

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
├── .devcontainer/              # Konfigurasi container development (GitHub Codespaces)
├── app.py                      # Aplikasi web interaktif utama (Streamlit)
├── pdf_report.py               # Generator laporan PDF resmi & template cetak interaktif
├── joblib/                     # Pustaka serialisasi model (dibundel lokal cloud-ready)
├── fpdf/                       # Pustaka generator PDF (dibundel lokal cloud-ready)
├── packages.txt                # Dependensi pustaka sistem Linux Debian (libxrender1, libxext6)
├── requirements.txt            # Dependensi pustaka Python cloud-ready (termasuk fpdf2)
├── LogBook.md                  # Buku log historis progres riset mingguan
├── TODO.md                     # Roadmap pengembangan strategis & to-do list
├── run_windows.bat             # Skrip launcher cepat untuk Windows
├── create_pptx.py              # Generator presentasi otomatis
├── presentation.md             # Bahan materi slide presentasi (Marp format)
├── presentation.pptx           # Slide presentasi PowerPoint
├── eval_metrics.py             # Evaluasi metrik kinerja model
├── deploy_to_hf.py             # Skrip otomatisasi deployment ke Hugging Face Spaces
├── hf_space/                   # Bundel mandiri siap-deploy ke Hugging Face Spaces
│   ├── app.py
│   ├── pdf_report.py
│   ├── joblib/
│   ├── fpdf/
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
- Python 3.9 – 3.12
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

## 🌐 Deployment Cloud

### Opsi 1: Streamlit Community Cloud (Rekomendasi Utama)
Aplikasi ini sudah dioptimasi secara penuh untuk Streamlit Cloud (dengan `packages.txt` dan `requirements.txt` yang bersih). Anda dapat meluncurkannya dengan 1-klik:
👉 **[Deploy ke Streamlit Cloud](https://share.streamlit.io/deploy?repository=hannachristina51-gif/SGLT2_Drug_Discovery&branch=main&mainModule=app.py)**

### Opsi 2: Hugging Face Spaces
Paket mandiri siap-deploy tersedia di folder `hf_space/`. Untuk mengunggah secara otomatis:
```bash
python deploy_to_hf.py
```
Atau drag & drop seluruh isi folder `hf_space/` ke Hugging Face Space baru bertipe **Streamlit**.

---

## 👥 Tim & Pengembang
- **Peneliti**: Hanna Christina Ginting (NPM: 2506713353) — Universitas Indonesia
- **Pembimbing / Dosen Pengampu**: Prof. Arry
