SGLT2 Inhibitor - Virtual Screening & Drug Discovery Platform

=== DESKRIPSI ===
Proyek ini berisi pipeline Drug Discovery lengkap dari awal pengumpulan data (ChEMBL Target ID: CHEMBL1808, 4.114 data mentah -> 1.760 senyawa terkurasi bersih), prapemrosesan, ekstraksi fitur hibrida (4 Lipinski Descriptors & 2.048-bit Morgan Fingerprints ECFP4 = 2.052 fitur), analisis ruang kimia (Chemical Space), pelatihan model Machine Learning (Random Forest Regressor, R^2 = 0.7297, RMSE = 0.6317) via Bemis-Murcko Scaffold Split & Hyperparameter Tuning (GridSearchCV), hingga pembentukan Aplikasi Web Interaktif.

Model final diintegrasikan ke dalam Aplikasi Web Interaktif (End-User App) menggunakan framework Streamlit (app.py) untuk memfasilitasi skrining virtual molekul obat antidiabetes (mencakup Single Molecule Prediction, 5 Preset Molekul Kontrol 1-Klik, rendering struktur 2D molekul via RDKit, validasi Aturan Lima Lipinski, konversi otomatis pActivity ke IC50 nM/uM/mM, Batch Screening CSV, Generator Laporan PDF Resmi A4 via pdf_report.py, serta fitur Cetak Dokumen 1-Klik).

=== PERSIAPAN LINGKUNGAN (CARA MENJALANKAN LOKAL) ===
Aplikasi ini memerlukan sistem Python 3.9 - 3.12. Untuk menjalankan aplikasi di komputer lokal:

1. Buka Terminal (Mac/Linux) atau Command Prompt / PowerShell (Windows).
2. Arahkan direktori terminal ke dalam folder repositori ini:
   cd SGLT2_Drug_Discovery

3. Buat dan aktifkan Virtual Environment:
   python3 -m venv venv
   source venv/bin/activate       (untuk Mac/Linux)
   venv\Scripts\activate          (untuk Windows)

4. Instal dependensi paket:
   pip install -r requirements.txt

=== MELUNCURKAN APLIKASI ===
Setelah proses instalasi selesai, jalankan perintah berikut di terminal:

   streamlit run app.py

Aplikasi (Web App) akan otomatis terbuka di browser pada alamat:
http://localhost:8501

=== DEPLOYMENT CLOUD ===
- Streamlit Community Cloud:
  Buka tautan: https://share.streamlit.io/deploy?repository=hannachristina51-gif/SGLT2_Drug_Discovery&branch=main&mainModule=app.py
- Hugging Face Spaces:
  Jalankan perintah: python deploy_to_hf.py

=== PANDUAN STRUKTUR PROYEK ===
- app.py: File utama untuk meluncurkan antarmuka pengguna Streamlit.
- pdf_report.py: Modul generator Laporan PDF Resmi A4 (Single & Batch) dan template cetak interaktif.
- joblib/ & fpdf/: Pustaka pure-Python yang dibundel lokal untuk stabilitas deployment cloud Linux (PEP 668).
- packages.txt: Pustaka sistem Linux Debian (libxrender1, libxext6) untuk dependensi grafis RDKit di cloud.
- requirements.txt: Daftar dependensi pustaka Python cloud-ready.
- .devcontainer/: Konfigurasi container untuk GitHub Codespaces.
- models/: Menyimpan file model Random Forest (rf_regressor_model.pkl) dan StandardScaler (scaler.pkl).
- data/: Berisi data mentah, kurasi bersih, deskriptor, hingga hasil virtual screening (Dapagliflozin peringkat #1: pActivity 7.84).
- plots/: Grafik visualisasi Exploratory Data Analysis (EDA).
- scripts/: Koleksi skrip pengolahan bertahap 01 s/d 06.
- LogBook.md: Buku log historis detail seluruh progres dan pembaruan proyek.
- TODO.md: Peta jalan (roadmap) pengembangan strategis Fase 1, 2, dan 3.
- hf_space/: Direktori mandiri berisi seluruh berkas siap-deploy ke Hugging Face Spaces.
- deploy_to_hf.py: Skrip otomatisasi unggah aplikasi ke Hugging Face Spaces.
- Presentasi_SGLT2_Drug_Discovery_Terbaru.pptx & presentation.pptx: Slide materi presentasi proyek terbaru (14 slide Widescreen 16:9).
- presentation.md & create_pptx.py: Materi Markdown dan skrip generator otomatis presentasi PowerPoint.
