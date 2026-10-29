---
marp: true
theme: default
paginate: true
size: 16:9
backgroundColor: #f8fafc
---

# 🧬 SGLT2 Inhibitor Drug Discovery Platform
**Platform Prediksi Bioaktivitas In-Silico Berbasis Machine Learning & Aplikasi Web Interaktif untuk Penemuan Kandidat Obat Diabetes Melitus Tipe 2**

- **Peneliti & Pengembang**: Hanna Christina Ginting (NPM: 2506713353) — Universitas Indonesia
- **Dosen Pengampu / Pembimbing**: Prof. Arry
- **Target Biologis**: SGLT2 (*SLC5A2* / `CHEMBL1808`) — 1.760 Senyawa Terkurasi
- **Performa Model**: *Random Forest Regressor* ($R^2 = 0.7297$, $\text{RMSE} = 0.6317$, *Bemis-Murcko Scaffold Split*)
- **Repositori**: `github.com/hannachristina51-gif/SGLT2_Drug_Discovery`

---

## 1. Latar Belakang & Arsitektur End-to-End Aplikasi

### 🎯 Mengapa Target SGLT2 (*SLC5A2*)?
- Bertanggung jawab atas **>90% reabsorpsi glukosa** di tubulus proksimal ginjal.
- Inhibisi SGLT2 memicu ekskresi glukosa urin (*glukosuria*) secara **independen dari insulin** (minim risiko hipoglikemia) serta memberikan efek kardioprotektif & nefroprotektif.

### 🔄 6 Tahap End-to-End Pipeline
1. **Akuisisi Data ChEMBL**: Ekstraksi 4.114 data bioaktivitas mentah (`CHEMBL1808`).
2. **Kurasi & Standardisasi**: Sanitasi SMILES, deduplikasi $\rightarrow$ **1.760 senyawa bersih** ($pActivity = -\log_{10} IC_{50}$).
3. **Feature Engineering**: Penggabungan **2.048-bit Morgan Fingerprints (ECFP4)** + **4 Deskriptor Lipinski**.
4. **Pemodelan & Validasi ML**: *Random Forest Regressor* + *Bemis-Murcko Scaffold Split* (70:30) + *GridSearchCV*.
5. **Aplikasi Web Streamlit (`app.py`)**: Prediksi molekul tunggal, preset obat acuan, visualisasi 2D, & *Batch Screening CSV*.
6. **Pelaporan & Cloud Deployment**: Ekspor Laporan PDF Resmi A4 (`pdf_report.py`), *One-Click Print*, Streamlit Cloud & HF Spaces.

---

## 2. Akuisisi Data, Kurasi & Exploratory Data Analysis (EDA)

- **Data Mentah**: 4.114 entri bioaktivitas dari ChEMBL Database (`CHEMBL1808`).
- **Data Terkurasi**: **1.760 senyawa unik** dengan struktur SMILES kanonik valid.
- **Standar Klasifikasi Bioaktivitas**:
  - 🟢 **Aktif (Poten)**: $pActivity > 6.0$ ($IC_{50} < 1.000\text{ nM}$)
  - 🟡 **Intermediate**: $5.0 < pActivity \le 6.0$ ($IC_{50}: 1.000 - 10.000\text{ nM}$)
  - 🔴 **Tidak Aktif**: $pActivity \le 5.0$ ($IC_{50} > 10.000\text{ nM}$)
- **3 Analisis Visual EDA (`plots/`)**:
  1. Distribusi Kelas Bioaktivitas (`01_bioactivity_distribution.png`)
  2. Pemetaan Ruang Kimia MW vs LogP (`02_chemical_space_mw_logp.png`)
  3. Sebaran Statistik Boxplot $pActivity$ (`03_pActivity_boxplot.png`)

---

## 3. Rekayasa Fitur Molekuler (*Hybrid Feature Engineering*)

Menggabungkan informasi topologi sub-struktur mikro dan sifat fisikokimia makroskopik:

1. **Morgan Fingerprints (ECFP4, `radius=2`)**:
   - Representasi vektor biner lingkungan atomik sirkular menggunakan RDKit.
   - Diekstraksi pada resolusi **1.024-bit** (`curated_features_and_fingerprints.csv`) dan ditingkatkan menjadi **2.048-bit** pada model produksi untuk meminimalkan *bit collision*.
2. **4 Deskriptor Fisikokimia Lipinski (*Rule of Five*)**:
   - *Molecular Weight (MW)*, *LogP (Lipofilisitas)*, *NumHDonors (HBD)*, *NumHAcceptors (HBA)*.
   - Dinormalisasi menggunakan `StandardScaler` (`models/scaler.pkl`).
3. **Vektor Masukan Model Produksi**:
   - $\mathbf{X} = \text{hstack}([\text{ECFP4}_{2048}, \text{Scaled\_Lipinski}_4]) \rightarrow \mathbf{2.052\text{ Fitur / Molekul}}$.

---

## 4. Pemodelan Machine Learning, Validasi Scaffold Split & Komparasi

- **Bemis-Murcko Scaffold Split (70% Train : 30% Test)**: Mengelompokkan kerangka cincin inti molekul agar *Test Set* menguji kemampuan generalisasi pada struktur baru (*mencegah data leakage*).
- **Isolasi Eksklusif Dapagliflozin**: Senyawa kontrol positif ditempatkan 100% di *Test Set*.

| Konfigurasi Model | Metode Optimasi | Skor $R^2$ | Catatan Evaluasi |
|:---|:---|:---:|:---|
| **Random Forest Regressor (Utama)** | Baseline Optimal | **0.7297** | **RMSE = 0.6317 (Model Terbaik ✅)** |
| RF + Hybrid 2052 Fitur | `RandomizedSearchCV` | 0.7255 | 10 iterasi Cross-Validation |
| RF + Hybrid 2052 Fitur | `GridSearchCV` (81 fit) | 0.7233 | `n_estimators=300, max_depth=None` |
| HistGradientBoosting Regressor | `GridSearchCV` | 0.7044 | `learning_rate=0.2, max_depth=9` |

> *Ensambel paralel (Random Forest) terbukti lebih tangguh menangani matriks biner renggang (sparse 2.048-bit) dibanding Gradient Boosting.*

---

## 5. Hasil Virtual Screening & Validasi Senyawa Kontrol

Pengujian model pada kandidat molekul dan obat referensi komersial (`data/04_virtual_screening_results.csv`):

| Peringkat | Nama Senyawa Uji | Prediksi $pActivity$ | Estimasi $IC_{50}$ | Status Klasifikasi |
|:---:|:---|:---:|:---:|:---:|
| **#1 🏆** | **Dapagliflozin (Inhibitor SGLT2 Komersial)** | **7.84** | **14.33 nM** | **Potensial Aktif** |
| #2 | Caffeine (Stimulan SSP) | 6.84 | 144.33 nM | Potensial Aktif |
| #3 | Aspirin (Analgesik / Kontrol) | 6.67 | 215.55 nM | Potensial Aktif |
| #4 | Metformin (Antidiabetik Biguanid) | 6.42 | 378.52 nM | Potensial Aktif |
| #5 | Ibuprofen (NSAID) | 6.27 | 533.66 nM | Potensial Aktif |

- **Temuan Kunci**: Model mengenali **Dapagliflozin** dengan afinitas tertinggi (>10x lebih kuat dalam skala nM dibanding senyawa lain).

---

## 6. Arsitektur Aplikasi Web Interaktif (`app.py` — Streamlit)

Antarmuka pengguna berbasis web yang dirancang modular dan intuitif:

- **🧭 Sidebar Informasi Proyek & Model**: Menampilkan metadata target `CHEMBL1808`, metrik model ($R^2 = 0.7297$, $\text{RMSE} = 0.6317$), serta panduan klasifikasi bioaktivitas.
- **🧬 Tab 1 — Single Molecule Prediction**: Prediksi bioaktivitas instan dari input SMILES, menu *preset* senyawa referensi 1-klik, visualisasi struktur 2D RDKit, evaluasi *Lipinski's Rule of Five*, serta ekspor laporan.
- **🗂️ Tab 2 — Batch Virtual Screening (CSV)**: Unggah berkas CSV berisi ratusan/ribuan molekul untuk penapisan paralel lengkap dengan *progress bar*, deteksi pelanggaran Lipinski, dan unduhan contoh CSV pengujian.
- **📖 Tab 3 — Metodologi & Petunjuk Sains**: Dokumentasi rumus $pActivity$, $IC_{50}$, kriteria Lipinski, dan arsitektur Machine Learning.

---

## 7. Fitur Unggulan 1: Prediksi Molekul Tunggal & Evaluasi Lipinski

- **🎯 Menu Preset Molekul Kontrol 1-Klik**:
  - *Dapagliflozin*, *Empagliflozin*, *Canagliflozin* (Inhibitor SGLT2 Komersial), *Metformin* (Biguanid), dan *Aspirin* (Kontrol Negatif).
- **⚡ Kalkulasi & Konversi Satuan Adaptif**:
  - Menghitung $IC_{50}\text{ (nM)} = 10^{-pActivity} \times 10^9$ dan otomatis memformat ke satuan **nM**, **µM**, atau **mM**.
- **🧪 Validasi Otomatis *Lipinski's Rule of Five*** (Contoh: Dapagliflozin):
  - **Molecular Weight (MW)**: `408.88 Da` ($\le 500\text{ Da}$ $\rightarrow$ ✅ Lolos)
  - **LogP (Lipofilisitas)**: `2.14` ($\le 5.0$ $\rightarrow$ ✅ Lolos)
  - **H-Bond Donors (HBD)**: `4` ($\le 5$ $\rightarrow$ ✅ Lolos)
  - **H-Bond Acceptors (HBA)**: `6` ($\le 10$ $\rightarrow$ ✅ Lolos)

---

## 8. Fitur Unggulan 2: Generator Laporan PDF Resmi & Cetak 1-Klik

Modul pelaporan laboratorium mandiri (`pdf_report.py` berbasis `fpdf2`):

1. **📑 Laporan PDF Senyawa Tunggal (`generate_single_pdf_report`)**:
   - Dokumen A4 resmi memuat gambar struktur kimia 2D resolusi tinggi via RDKit, rumus molekul, metrik $pActivity$ & $IC_{50}$, badge status bioaktivitas, tabel evaluasi 4 parameter Lipinski, metodologi AI, dan *scientific disclaimer*.
2. **🗂️ Laporan PDF Rekapitulasi Batch (`generate_batch_pdf_report`)**:
   - Merangkum statistik skrining massal (proporsi senyawa Aktif, Intermediate, Tidak Aktif) dan **Tabel 20 Kandidat Inhibitor SGLT2 Teratas**.
3. **🖨️ Pratinjau & Cetak Dokumen Langsung (`get_printable_html`)**:
   - Template HTML/CSS `@media print` dengan tombol interaktif `window.print()` untuk cetak langsung ke printer atau *Save as PDF*.

---

## 9. Arsitektur Cloud-Ready & Deployment Multi-Platform

1. **☁️ Streamlit Community Cloud (`sglt2-drug-discovery.streamlit.app`)**:
   - **Self-Contained Bundling**: Pustaka *pure-Python* `joblib/` dan `fpdf/` dibundel langsung di repositori untuk kompatibilitas penuh dengan proteksi PEP 668 pada Linux Debian Bookworm.
   - **Dynamic Path Discovery**: Pemindaian otomatis `site-packages` via `glob.glob` & dukungan `packages.txt` (`libxrender1`, `libxext6`).
2. **🤗 Hugging Face Spaces (`hf_space/` & `deploy_to_hf.py`)**:
   - Bundel mandiri lengkap dengan konfigurasi Git LFS model `.pkl` dan skrip deployment otomatis 1-perintah.
3. **🐙 GitHub Repository & Codespaces**:
   - Publikasi di `github.com/hannachristina51-gif/SGLT2_Drug_Discovery` beserta `.devcontainer/devcontainer.json` dan `run_windows.bat`.

---

## 10. Peta Jalan Pengembangan (Roadmap) — Fase 1 (Jangka Pendek)

*Fokus: Validitas Ilmiah Prediksi (Standar OECD QSAR) & Peningkatan Interaktivitas UI/UX*

- 🔴 **Applicability Domain (AD) Filter** `[Prioritas Tinggi]`
  - Perhitungan *Tanimoto Similarity* (k-NN) / *Leverage* untuk memberi *warning badge* jika molekul uji berada di luar domain latih ChEMBL.
- 🔴 **Uncertainty Quantification (Prediction Interval)** `[Prioritas Tinggi]`
  - Menampilkan rentang kepercayaan prediksi dari varians 300 pohon keputusan RF (misal: $pActivity = 7.84 \pm 0.28$).
- 🔴 **Interactive Molecular Sketcher (Ketcher / JSME Canvas)** `[Prioritas Tinggi]`
  - Kanvas gambar struktur 2D interaktif langsung di browser tanpa perlu mengetik string SMILES.
- 🟡 **Model Explainability (SHAP / Morgan Bit Attribution)**, **Visualisasi 3D (`py3Dmol`)**, & **Radar Chart Fisikokimia**.
- 🟢 **Ekspor Laporan PDF Lengkap & Fitur Cetak**: **SELESAI DIIMPLEMENTASIKAN ✅**.

---

## 11. Peta Jalan Pengembangan — Fase 2 (Jangka Menengah)

*Fokus: Selektivitas Target, ADMET-Toksisitas, Fitofarmaka Indonesia & Polifarmakologi Antidiabetes*

- 🔴 **Dual-Target Selektivitas SGLT2 vs SGLT1 (*SLC5A1*)**:
  - Menghitung *Selectivity Index* (mencegah efek samping diare osmotik akibat inhibisi SGLT1 di usus; rasio ideal >1.000x).
- 🔴 **Profil ADMET In-Silico & Synthetic Accessibility (SA) Score**:
  - Prediksi absorpsi HIA, Caco-2, risiko aritmia jantung (*hERG*), hepatotoksisitas, *Ames test*, dan skor kemudahan sintesis (1–10).
- 🔴 **Profiling Lintas Golongan Antidiabetes & Multi-Target QSAR (MTDL)**:
  - Pustaka pembanding & model QSAR untuk **Biguanid**, **Sulfonilurea**, **AGI** (`CHEMBL340`), **DPP-4 Inhibitor** (`CHEMBL284`), **TZD / PPAR-$\gamma$** (`CHEMBL235`), dan **GLP-1 RA**.
- 🟡 **Database Bahan Alam / Herbal Indonesia**:
  - Skrining fitokimia tanaman antidiabetes lokal (daun salam, pare, temulawak, kayu manis, mahkota dewa dari COCONUT/HerbalDB).

---

## 12. Peta Jalan Pengembangan — Fase 3 (Jangka Panjang)

*Fokus: Deep Learning Berbasis Graf, Simulasi Struktur 3D & Infrastruktur Kluster*

- 🔴 **Integrasi Automated Molecular Docking (AutoDock Vina / GNINA)**:
  - Penambatan otomatis 5 kandidat teratas pada struktur cryo-EM SGLT2 manusia (**PDB ID: `7VSI` / `7BOV`**) untuk mengukur energi bebas ikatan ($\Delta G\text{ kkal/mol}$) & interaksi residu kunci (*Phe98, Glu99, Val157, Trp291*).
- 🟡 **Eksplorasi Graph Neural Networks (GNN / Chemprop & ChemBERTa)**:
  - Pembelajaran representasi topologi graf molekul secara langsung dan komparasi terhadap Random Forest.
- 🟡 **Infrastruktur Produksi (`Docker`, `FastAPI` Headless Engine & `pytest` CI/CD)**:
  - Pemisahan layanan mikro REST API untuk integrasi dengan workflow KNIME dan kluster komputasi kampus.

---

# 🏁 Kesimpulan & Terima Kasih 🙏

- **Pipeline End-to-End Teruji**: Mulai dari kurasi 1.760 senyawa ChEMBL, ekstraksi 2.052 fitur hibrida, hingga model *Random Forest* ($R^2 = 0.7297$) tervalidasi *Scaffold Split*.
- **Aplikasi Web Siap Pakai**: Dilengkapi prediksi molekul tunggal, skrining massal CSV, evaluasi Lipinski, serta **Generator Laporan PDF Resmi A4 & Cetak 1-Klik**.
- **Siap Cloud & Ekspansi Riset**: Mendukung penuh Streamlit Cloud & Hugging Face Spaces dengan roadmap jelas menuju ADMET, polifarmakologi antidiabetes, GNN, dan *Molecular Docking*.

**Hanna Christina Ginting (NPM: 2506713353) • Pembimbing: Prof. Arry • Universitas Indonesia**
