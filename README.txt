SGLT2 Inhibitor - Virtual Screening App

=== DESKRIPSI ===
Proyek ini berisi pipeline Drug Discovery lengkap dari awal pengumpulan data (ChEMBL Target ID: CHEMBL1808), prapemrosesan, ekstraksi fitur (Lipinski Descriptors & Morgan Fingerprints 2048-bit), analisis ruang kimia (Chemical Space), pelatihan model Machine Learning (Random Forest Regressor) via Bemis-Murcko Scaffold Split & Hyperparameter Tuning, hingga pembentukan purwarupa (prototype).

Model final kemudian diintegrasikan ke dalam Aplikasi Web Interaktif (End-User App) menggunakan framework Streamlit untuk memfasilitasi kemudahan skrining virtual molekul obat antidiabetes oleh para peneliti biologi molekuler atau farmakolog (termasuk rendering struktur 2D molekul, validasi Aturan Lima Lipinski, dan konversi prediksi pActivity menjadi IC50 secara otomatis).

=== PERSIAPAN LINGKUNGAN (CARA MENJALANKAN LOKAL) ===
Aplikasi ini memerlukan sistem Python 3.9 atau yang lebih baru. Untuk menjalankan aplikasi di komputer lokal (misalnya di komputer penilai/dosen), silakan ikuti panduan berikut:

1. Buka Terminal (Mac/Linux) atau Command Prompt / PowerShell (Windows).
2. Arahkan direktori terminal ke dalam folder repositori ini:
   cd SGLT2_Drug_Discovery

3. Instalasi Paket: Sangat disarankan untuk membuat Virtual Environment baru sebelum menginstal dependensi:
   
   Membuat Virtual Environment:
   python3 -m venv venv
   source venv/bin/activate       (untuk Mac/Linux)
   venv\Scripts\activate          (untuk Windows)

   Melakukan Instalasi Paket:
   pip install -r requirements.txt

=== MELUNCURKAN APLIKASI ===
Setelah proses instalasi selesai, cukup jalankan satu perintah sederhana berikut di terminal:

   streamlit run app.py

Aplikasi (Web App) akan secara otomatis memunculkan tab baru di browser bawaan Anda dengan alamat URL:
http://localhost:8501

=== DEPLOYMENT CLOUD ===
- Streamlit Community Cloud:
  Buka tautan: https://share.streamlit.io/deploy?repository=hannachristina51-gif/SGLT2_Drug_Discovery&branch=main&mainModule=app.py
- Hugging Face Spaces:
  Jalankan perintah: python deploy_to_hf.py

=== PANDUAN STRUKTUR PROYEK ===
- app.py: File utama untuk meluncurkan antarmuka pengguna Streamlit.
- packages.txt: Pustaka sistem Linux Debian untuk dependensi grafis RDKit di cloud.
- requirements.txt: Daftar dependensi pustaka Python cloud-ready.
- .devcontainer/: Konfigurasi container untuk GitHub Codespaces.
- models/: Menyimpan file algoritma dan scaler (Random Forest) hasil training.
- data/: Berisi hasil data mentah, bersih, hingga hasil virtual screening.
- scripts/: Koleksi script pengolahan bertahap mulai dari unduhan data hingga evaluasi model.
- LogBook.md: Buku log mingguan detail seluruh perubahan proyek.
- TODO.md: Rencana pengembangan dan to-do list terstruktur ke depannya.
- hf_space/: Direktori mandiri berisi seluruh berkas siap-deploy ke Hugging Face Spaces.
- deploy_to_hf.py: Skrip otomatisasi unggah aplikasi ke Hugging Face Spaces.
- presentation.pptx: Slide materi presentasi proyek.
