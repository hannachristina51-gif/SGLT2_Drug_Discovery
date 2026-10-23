# LogBook - Perubahan pada Walkthrough

Dokumen ini mencatat riwayat perubahan dan pembaruan yang dilakukan pada dokumen `walkthrough.md`.

## 11 September 2026 - Pembuatan Walkthrough Awal
- **Aktivitas**: Membuat dokumen `walkthrough.md` untuk merangkum hasil akhir penemuan obat.
- **Detail Perubahan**: 
  - Mencatat ringkasan pengumpulan data dari ChEMBL (4.114 data mentah disaring menjadi 1.760 senyawa bersih).
  - Melampirkan hasil *Exploratory Data Analysis* (EDA) berupa 3 grafik (distribusi kelas bioaktivitas, ruang kimia MW vs LogP, dan boxplot pActivity).
  - Melampirkan metrik evaluasi kinerja model *Random Forest Regressor* (RMSE: 0.6317, R-squared: 0.7297).

## 11 September 2026 - Pembaruan Hasil Virtual Screening
- **Aktivitas**: Memperbarui dokumen `walkthrough.md` dengan menambahkan bagian *Virtual Screening*.
- **Detail Perubahan**:
  - Menambahkan bagian "4. Virtual Screening" di akhir dokumen.
  - Memasukkan tabel hasil prediksi model terhadap 5 senyawa uji.
  - Mencatat temuan bahwa *Dapagliflozin* (obat inhibitor SGLT2 komersial) berhasil diidentifikasi oleh model dengan skor *pActivity* tertinggi (7.84).

## 18 September 2026 - Ekstraksi Fitur (Lipinski & Fingerprints)
- **Aktivitas**: Membuat skrip `extract_features.py` dalam folder baru `feature_extraction`.
- **Detail Perubahan**:
  - Menghitung *Lipinski descriptors* dan *Morgan Fingerprints* (1024 bit) sekaligus untuk seluruh data kurasi (1.755 senyawa).
  - Menyimpan penggabungan data (1.035 kolom) ke dalam file `curated_features_and_fingerprints.csv`.

## 5 Oktober 2026 - Peningkatan Model ML (Scaffold Split & Hyperparameter Tuning)
- **Aktivitas**: Memodifikasi skrip `05_ml_model.py` sesuai arahan terbaru.
- **Detail Perubahan**:
  - Mengimplementasikan validasi struktural **Scaffold Split** (70% Train, 30% Test) menggunakan `MurckoScaffold` untuk meminimalkan bias *overfitting*.
  - Mengisolasi **Dapagliflozin** secara manual dan memastikan bahwa senyawa ini hanya dievaluasi pada *Test Set*, tidak ikut dalam fase pelatihan.
  - Menjalankan **Hyperparameter Tuning** otomatis menggunakan `GridSearchCV`. Parameter terbaik yang ditemukan: `n_estimators=300`, `max_depth=None`, dan `min_samples_split=2`.
  - Mengamankan dan mencatat performa baru model (RMSE: 0.8247, $R^2$: 0.5136) ke dalam `walkthrough.md`.

## 5 Oktober 2026 - Pembuatan End-User Web App (Streamlit)
- **Aktivitas**: Membuat dan memodifikasi aplikasi antarmuka pengguna berbasis web `app.py`.
- **Detail Perubahan**:
  - Menggunakan *framework* **Streamlit** untuk membungkus model *Machine Learning* yang sudah dilatih.
  - Membangun fitur **Single Molecule Prediction** dengan input senyawa berbasis *SMILES* dan konversi matematis *pActivity* menjadi **IC50 (nM)**.
  - Mengintegrasikan fitur **Visualisasi Lipinski's Rule of Five** untuk mendeteksi pelanggaran properti fisikokimia secara instan (indikator ✅/❌).
  - Menambahkan fitur **Batch Virtual Screening** yang memungkinkan pengguna mengunggah file `.csv` berisi banyak SMILES sekaligus untuk diproses secara massal.
  - Mengimplementasikan fungsionalitas **Download Report** (format `.csv`) baik untuk hasil *Single Prediction* maupun *Batch Screening*.
  - Menjalankan server aplikasi secara lokal di `http://localhost:8501`.

## 02 Oktober 2026 - Pembuatan Presentasi Hasil Proyek
- **Aktivitas**: Membuat materi presentasi akhir dalam format Markdown (`presentation.md`) dan PowerPoint (`presentation.pptx`).
- **Detail Perubahan**:
  - Membuat *script* Python `create_pptx.py` untuk membangkitkan file PowerPoint secara otomatis.
  - Merangkum alur penemuan obat mulai dari pengumpulan data, EDA, *Feature Engineering*, hingga pemodelan Machine Learning ke dalam beberapa *slide*.
  - Melengkapi *slide* Virtual Screening dengan kandidat senyawa potensial lainnya (Caffeine, Aspirin, Metformin, Ibuprofen) lengkap dengan skor prediksinya.
  - Menambahkan *slide* khusus "Rencana Optimasi Model", yang mencakup metode *Hyperparameter Tuning*, pengujian algoritma lanjutan, penambahan fitur struktural tambahan (3D), dan validasi struktural (*Scaffold Split*).

## 04 Oktober 2026 - Penggabungan Fitur & Hyperparameter Tuning
- **Aktivitas**: Mengevaluasi ulang model Random Forest dengan penambahan fitur dan tuning.
- **Detail Eksperimen**:
  - Menggabungkan 2.048 bit **Morgan Fingerprints** dengan 4 **Lipinski Descriptors** numerik (di-*scale* dengan `StandardScaler`).
  - Melakukan *RandomizedSearchCV* (10 iterasi) menghasilkan R-squared 0.7255.
  - Melakukan *GridSearchCV* penuh (81 pelatihan) menghasilkan R-squared 0.7233 (`max_depth: None`, `min_samples_split: 2`, `n_estimators: 300`).
  - **Kesimpulan Analisis**: Menggabungkan data biner secara mentah dengan fitur kontinu ternyata menurunkan sedikit akurasi RF (*noise/curse of dimensionality*). Solusi utamanya adalah beralih ke *Gradient Boosting*.

## 04 Oktober 2026 - Migrasi Eksperimental ke HistGradientBoosting
- **Aktivitas**: Membuat varian skrip baru `05_ml_model_hgb.py` untuk bereksperimen dengan algoritma *HistGradientBoostingRegressor*.
- **Detail Perubahan**:
  - Membatalkan penggunaan *XGBoost* karena masalah dependensi `libomp` pada Mac, dan beralih ke alternatif *native* di `scikit-learn` yang memiliki performa setara (*HistGradientBoosting*).
  - Mempertahankan alur *split* 70:30 dengan Dapagliflozin secara eksklusif hanya di *Test Set*.
  - Mengganti `RandomForestRegressor` dengan `HistGradientBoostingRegressor`.
  - Mengimplementasikan `GridSearchCV` khusus parameter Gradient Boosting (mencakup *learning rate*, *max_iter*, dan *max depth* spesifik).
  - **Kesimpulan Analisis Final**: Eksekusi `HistGradientBoostingRegressor` memberikan R-squared 0.7044 (dengan parameter terbaik: `learning_rate`: 0.2, `max_depth`: 9, `max_iter`: 100). Skor ini berada sedikit di bawah *Random Forest* asli. Hal ini mengkonfirmasi secara teoritis bahwa algoritma ensambel paralel (seperti *Random Forest*) secara inheren lebih tangguh dan stabil saat menangani matriks biner yang sangat besar dan renggang (*sparse matrix* dari 2.048-bit *Fingerprints*) dibandingkan dengan algoritma *Gradient Boosting* standar yang lebih rentan terhadap over-spesialisasi (*overfitting*) pada data dimensi tinggi semacam ini tanpa regulasi matematis ekstrem.

## 23 Oktober 2026 - Pembaruan Roadmap & Penyusunan To-Do List Aplikasi
- **Aktivitas**: Menyusun dan merumuskan dokumen terpusat `TODO.md` yang memetakan arah pengembangan aplikasi secara komprehensif ke depannya.
- **Detail Perubahan**:
  - **Fase 1 (Jangka Pendek)**: Integrasi *Applicability Domain (AD)* filter (mencegah prediksi liar di luar domain data latih), *Uncertainty Quantification* (interval kepercayaan prediksi), kanvas sketsa molekul interaktif (*Ketcher/JSME*), visualisasi 3D (*py3Dmol/stmol*), dan ekspor laporan PDF.
  - **Fase 2 (Jangka Menengah)**: Pembangunan model dual-target untuk rasio selektivitas SGLT2 vs SGLT1 (mencegah efek samping gastrointestinal), integrasi fasilitas pemeriksaan komparatif dan skrining multi-target lintas golongan obat antidiabetes lain (Biguanid, Sulfonilurea, Alpha-glucosidase inhibitors, DPP-4 inhibitors, TZDs, dan GLP-1 RA untuk pemetaan MTDL / *polypharmacology*), profil farmakokinetik & toksisitas *in-silico* ADMET (hERG, permeabilitas membran, Ames test), estimasi kemudahan sintesis (*SA Score*), serta penyediaan pustaka senyawa bahan alam Indonesia (COCONUT/HerbalDB) untuk eksplorasi fitofarmaka antidiabetes.
  - **Fase 3 (Jangka Panjang)**: Eksplorasi arsitektur AI berbasis graf (*Graph Neural Networks - Chemprop/GNN*), integrasi simulasi *Molecular Docking* otomatis (AutoDock Vina pada struktur PDB SGLT2 `7VSI`), serta orkestrasi arsitektur produksi (*Docker*, *FastAPI engine*, dan *automated testing*).
  - Menghubungkan daftar tugas modular tersebut ke dalam dokumentasi proyek agar progres riset bersama tim Prof. Arry dapat dipantau secara terukur.

## 23 Oktober 2026 - Penyiapan Bundel Deployment Hugging Face Spaces
- **Aktivitas**: Membangun direktori paket siap-deploy `hf_space/` dan skrip otomatisasi `deploy_to_hf.py` untuk meng-host aplikasi di Hugging Face Spaces.
- **Detail Implementasi**:
  - Menyusun berkas `README.md` pada `hf_space/` lengkap dengan konfigurasi YAML frontmatter (Streamlit SDK, badge, metadata riset).
  - Menyiapkan `requirements.txt` terstandarisasi untuk lingkungan Linux cloud serta `packages.txt` (`libxrender1`, `libxext6`) untuk dependensi grafis RDKit.
  - Memperkaya antarmuka pengguna `app.py` dengan pilihan cepat senyawa referensi (*Dapagliflozin, Empagliflozin, Canagliflozin, Metformin, Aspirin*), unduhan contoh file CSV untuk pengujian batch screening, dan tab metodologi riset.
  - Menempatkan model `rf_regressor_model.pkl` dan `scaler.pkl` ke dalam `hf_space/models/` dengan konfigurasi Git LFS `.gitattributes`.
  - Mengembangkan script `deploy_to_hf.py` berbasis library `huggingface_hub` yang memungkinkan proses pembuatan repository space dan unggah berkas secara otomatis via terminal dengan satu perintah.

## 23 Oktober 2026 - Inisialisasi & Publikasi Repositori GitHub
- **Aktivitas**: Menginisialisasi *Git version control* lokal, menyusun `.gitignore` dan `README.md` terstandarisasi, membuat repositori publik di akun GitHub `hannachristina51-gif`, dan mengunggah seluruh berkas proyek.
- **Detail Implementasi**:
  - Mengonfigurasi `.gitignore` untuk mengabaikan lingkungan virtual `venv/`, cache Python, dan file sementara macOS (`.DS_Store`).
  - Menulis dokumen komprehensif `README.md` dengan badge status, tabel metrik performa model, struktur direktori, dan panduan peluncuran lokal/cloud.
  - Membuat repositori publik baru: `https://github.com/hannachristina51-gif/SGLT2_Drug_Discovery`.
  - Melakukan `git commit` dan `git push` seluruh berkas proyek (termasuk model Machine Learning, data terkurasi, skrip virtual screening, dan materi presentasi) ke branch `main`.
