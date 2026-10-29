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

## 24 Oktober 2026 - Stabilisasi Streamlit Cloud, Resolusi Runtime, & Sinkronisasi Repositori
- **Aktivitas**: Mengoptimasi dan menstabilkan peluncuran aplikasi pada Streamlit Community Cloud serta memperbarui seluruh dokumentasi teknis proyek.
- **Detail Implementasi**:
  - **Resolusi Dependency `joblib` & RDKit**: Mengatasi *ModuleNotFoundError* di lingkungan container cloud Linux dengan memprioritaskan urutan instalasi `joblib>=1.3.0` dan `scikit-learn` pada `requirements.txt`.
  - **Penyediaan Linux System Packages**: Menambahkan file `packages.txt` di root repositori berisi pustaka grafis Debian (`libxrender1`, `libxext6`) agar RDKit dapat merender struktur kimia 2D tanpa *shared object error*.
  - **Perbaikan Urutan Eksekusi Streamlit**: Memperbaiki `app.py` dengan menempatkan `st.set_page_config()` pada baris teratas skrip sebelum pemanggilan modul Streamlit lainnya guna mengeliminasi *StreamlitSetPageConfigMustBeFirstCommandError*.
  - **Mekanisme Dynamic Self-Healing Fallback**: Memasang penanganan impor dinamis yang secara otomatis mengunduh pustaka esensial dan menjalankan `st.rerun()` apabila terjadi anomali cache container cloud.
  - **Integrasi GitHub Dev Container**: Menyinkronkan konfigurasi `.devcontainer/devcontainer.json` untuk dukungan penuh pada GitHub Codespaces.
  - **Sinkronisasi Dokumen Terpadu**: Memperbarui dokumen `README.md`, `TODO.md`, `README.txt`, dan `hf_space/README.md` untuk menyelaraskan status terkini proyek sebelum diunggah kembali ke GitHub.

## 26 Oktober 2026 - Resolusi Komprehensif Runtime Streamlit Cloud (Bundling Joblib & Dynamic Path Discovery)
- **Aktivitas**: Mengatasi kendala runtime `ModuleNotFoundError: No module named 'joblib'` dan `subprocess.CalledProcessError` pada Streamlit Community Cloud (`sglt2-drug-discovery.streamlit.app`).
- **Detail Implementasi**:
  - **Analisis Akar Masalah**: Container Linux Streamlit Cloud menjalankan Python 3.14 / Debian Bookworm yang menerapkan proteksi PEP 668 (*externally-managed-environment*), sehingga perintah fallback `pip install` via runtime `subprocess.check_call` otomatis ditolak oleh kernel OS (`CalledProcessError`). Selain itu, direktori `site-packages` virtual environment Streamlit (`/home/adminuser/venv/...`) belum terpetakan ke dalam `sys.path` saat container meluncurkan interpreter sistem.
  - **Pembundelan Pustaka `joblib` Murni**: Membundel pustaka `joblib` (100% *pure Python*, ~1.3 MB tanpa binary C) langsung ke dalam repositori aplikasi (`./joblib/` dan `hf_space/joblib/`). Pendekatan ini menjamin ketersediaan `joblib` secara instan tanpa ketergantungan pada koneksi paket eksternal.
  - **Pencarian Dinamis Site-Packages**: Menambahkan pemindaian otomatis `glob.glob` untuk seluruh lokasi direktori `site-packages` Linux (`/home/**/site-packages`, `/mount/**/site-packages`, `/usr/local/**/site-packages`) di bagian inisialisasi awal skrip.
  - **Pembersihan Kode Subprocess**: Menghapus seluruh eksekusi runtime `pip install` via `subprocess` pada `app.py` dan `hf_space/app.py` agar aplikasi berjalan stabil, aman, dan kompatibel penuh dengan Debian Linux PEP 668.
  - **Pengujian & Deployment**: Menguji impor lokal hingga berstatus sukses tanpa error (`app.py imported successfully!`), menyematkan versi pada `.python-version` (3.11), serta memublikasikan pembaruan ke repositori GitHub pada branch `main`.


## 26 Oktober 2026 - Investigasi & Analisis Diagnostik Runtime `ModuleNotFoundError: No module named 'sklearn'`
- **Aktivitas**: Melakukan penelusuran mendalam terkait kendala *ModuleNotFoundError: No module named 'sklearn'* pada baris 40 `app.py` di lingkungan Streamlit Community Cloud (`sglt2-drug-discovery.streamlit.app`).
- **Hasil Investigasi & Detail Analisis**:
  - **Status Eksekusi Sebelum Baris 40**:
    - Baris 4 `st.set_page_config()`: Berhasil dieksekusi sebagai perintah Streamlit pertama.
    - Baris 37 `import joblib`: Berhasil 100% menggunakan pustaka *pure Python* `joblib` yang telah dibundel lokal di root repositori.
    - Baris 38–39 `pandas` & `numpy`: Berhasil diimpor (paket bawaan dasar platform Streamlit).
    - Baris 40 `import sklearn`: Memicu `ModuleNotFoundError`.
  - **Identifikasi Akar Masalah**:
    1. **Cache Virtual Environment Belum Ter-refresh (*Stale Cache*)**: Pada commit sebelumnya, file `requirements.txt` tidak mengalami modifikasi hash. Sistem CI/CD Streamlit Community Cloud mengabaikan eksekusi ulang `pip install` dan menggunakan cache environment lama yang sebelumnya mengalami kegagalan instalasi.
    2. **Pengabaian Konfigurasi Runtime oleh Streamlit Cloud**: Berdasarkan spesifikasi resmi platform, Streamlit Community Cloud mengabaikan berkas `runtime.txt` dan `.python-version`. Penentuan interpreter Python sepenuhnya dikontrol via menu antarmuka *Advanced settings* pada dashboard Streamlit Cloud.
    3. **Ketersediaan Binary Wheels**: Paket `scikit-learn` dan `rdkit` mengandalkan ekstensi terkompilasi C/C++. Jika container cloud berjalan pada versi Python yang belum memiliki roda distribusi (*pre-compiled binary wheels* seperti Python 3.14), proses instalasi saat *initial build* otomatis gagal dan dilewati oleh sistem cloud.
  - **Urgensi Library**: Modul `sklearn` mutlak dibutuhkan oleh `joblib.load()` pada baris 110–111 untuk merekonstruksi kelas `sklearn.preprocessing._data.StandardScaler` dan `sklearn.ensemble._forest.RandomForestRegressor`.
  - **Rencana Tindak Lanjut Terarah**: Menyelaraskan versi runtime pada menu *Advanced Settings* Streamlit Cloud ke Python 3.11/3.12 yang stabil, memperbarui file dependensi untuk memaksa proses *re-build*, serta melakukan *Clear cache and reboot* dari dashboard aplikasi.

## 26 Oktober 2026 - Implementasi Fitur Ekspor Laporan PDF Lengkap & Cetak Dokumen
- **Aktivitas**: Mengembangkan dan mengintegrasikan modul generator laporan PDF komprehensif (`pdf_report.py`) dan fitur cetak interaktif pada aplikasi Streamlit (`app.py`).
- **Detail Implementasi**:
  - **Generator PDF Mandiri (`pdf_report.py`)**:
    - Membangun template dokumen A4 resmi berbasis pustaka *pure Python* `fpdf2` yang dibundel langsung ke repositori (`./fpdf/`).
    - Laporan senyawa tunggal (`generate_single_pdf_report`) memuat: gambar struktur kimia 2D resolusi tinggi via RDKit, formula & berat molekul, metrik bioaktivitas ($pActivity$ dan $IC_{50}$ nM), badge klasifikasi potensi farmakologis, tabel evaluasi 4 parameter *Lipinski's Rule of Five*, ringkasan metodologi AI (Random Forest, Morgan Fingerprints, Scaffold Split), serta *scientific disclaimer*.
    - Laporan massal (`generate_batch_pdf_report`) menyajikan rekapitulasi statistik (persentase senyawa aktif, intermediate, tidak aktif) dan tabel 20 kandidat inhibitor SGLT2 teratas hasil penapisan.
  - **Fitur Pratinjau & Cetak Interaktif (`window.print()`)**:
    - Mengembangkan template HTML ramah-cetak (`get_printable_html`) dengan aturan CSS `@media print` untuk menghasilkan tata letak cetak dokumen A4 yang bersih dan rapi.
    - Menambahkan tombol interaktif yang membuka dialog cetak browser langsung (*print to printer / save as PDF*).
  - **Optimasi State Antarmuka Streamlit**:
    - Mengintegrasikan penyimpanan hasil prediksi ke dalam `st.session_state` sehingga interaksi pengunduhan dokumen PDF/CSV dan tombol cetak tidak mereset tampilan hasil analisis.
  - **Penyelarasan Repositori & Dokumentasi**:
    - Menambahkan `fpdf2>=2.8.0` pada `requirements.txt`.
    - Menyinkronkan pembaruan kode ke direktori `hf_space/`.
    - Memperbarui status tugas nomor 15 pada `TODO.md` menjadi selesai.

## 27 Oktober 2026 - Pembaruan Menyeluruh LogBook, Sinkronisasi Dokumentasi, & Publikasi Repositori GitHub
- **Aktivitas**: Mengonsolidasikan seluruh log pembaruan terkini (fitur ekspor PDF, pratinjau cetak interaktif, pembundelan pustaka mandiri, serta stabilisasi deployment), menyelaraskan dokumentasi proyek, dan memublikasikan seluruh pembaruan ke repositori GitHub.
- **Detail Pembaruan & Integrasi**:
  - **Sinkronisasi Dokumen Teknis**:
    - Memperbarui `README.md` dengan penambahan deskripsi fitur ekspor laporan resmi PDF, pratinjau cetak satu klik (*one-click browser print*), serta pembaruan diagram pohon struktur repositori yang mencakup `pdf_report.py`, `joblib/`, dan `fpdf/`.
    - Memperbarui berkas `hf_space/README.md` untuk menyelaraskan daftar fitur siap-deploy pada platform Hugging Face Spaces.
    - Memastikan status tugas #15 pada roadmap strategis `TODO.md` telah terverifikasi selesai (*completed*).
  - **Verifikasi Kesiapan Kode & Dependensi**:
    - Memastikan seluruh modul utama (`app.py`, `pdf_report.py`) dan pustaka pendukung (`joblib/`, `fpdf/`) berada dalam kondisi bersih, teruji lokal tanpa galat (*zero syntax error*).
    - Memastikan dependensi `requirements.txt` dan `packages.txt` sinkron antara root proyek dan direktori `hf_space/`.
  - **Publikasi ke Repositori GitHub**:
    - Melakukan `git add`, `git commit`, dan `git push` seluruh pembaruan ke branch `main` repositori publik GitHub (`hannachristina51-gif/SGLT2_Drug_Discovery`).
    - Melakukan sanitasi kredensial URL remote Git demi menjaga keamanan akses repositori.

## 29 Oktober 2026 - Pembaruan Materi Presentasi PowerPoint Terbaru (14 Slide Widescreen)
- **Aktivitas**: Merombak dan memperbarui skrip generator presentasi (`create_pptx.py`), materi Markdown (`presentation.md`), serta berkas PowerPoint (`presentation.pptx` dan `Presentasi_SGLT2_Drug_Discovery_Terbaru.pptx`) agar mencerminkan seluruh fitur terkini aplikasi.
- **Detail Pembaruan**:
  - Memperluas cakupan presentasi menjadi **14 slide Widescreen (16:9)** dengan desain visual profesional bertema *Medical AI / Bioinformatics*.
  - Menyematkan langsung 3 grafik analisis EDA dari folder `plots/` dan merender struktur kimia 2D senyawa inhibitor SGLT2 komersial (*Dapagliflozin* & *Empagliflozin*) menggunakan RDKit ke dalam slide.
  - Menambahkan pembahasan arsitektur aplikasi web interaktif Streamlit (`app.py`), fitur preset molekul acuan 1-klik, validasi otomatis *Lipinski's Rule of Five*, modul generator laporan PDF resmi A4 (`pdf_report.py` berbasis `fpdf2`), fitur pratinjau cetak langsung (*one-click browser print*), kesiapan deployment multi-platform (Streamlit Community Cloud & Hugging Face Spaces), serta peta jalan strategis (*Roadmap* Fase 1, 2, dan 3).
