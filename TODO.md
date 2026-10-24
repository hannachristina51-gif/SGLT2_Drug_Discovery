# 📋 Rencana Pengembangan & To-Do List: SGLT2 Drug Discovery App

Dokumen ini memetakan peta jalan (*roadmap*) dan daftar tugas (*to-do list*) strategis untuk pengembangan aplikasi **SGLT2 Inhibitor Virtual Screening & Drug Discovery** ke depannya. Rencana ini disusun secara modular berdasarkan prioritas dan fase pengembangan.

---

## 🎯 Ringkasan Status Saat Ini (Baseline v1.0)
- [x] Ekstraksi data ChEMBL target SGLT2 (*Target ID: CHEMBL1808*, 1.760 senyawa terkurasi).
- [x] Ekstraksi deskriptor Lipinski (MW, LogP, HBD, HBA) dan Morgan Fingerprints (1024 & 2048-bit).
- [x] Pelatihan model *Random Forest Regressor* dengan *Bemis-Murcko Scaffold Split* dan *Hyperparameter Tuning*.
- [x] Validasi senyawa kontrol dunia nyata (*Dapagliflozin* terdeteksi dengan pActivity tertinggi 7.84).
- [x] Aplikasi Web Streamlit interaktif (`app.py`): *Single Molecule Prediction*, *Rule of 5 validation*, *Batch Screening CSV*, dan ekspor laporan CSV.
- [x] Menu *preset* molekul kontrol komersial (*Dapagliflozin, Empagliflozin, Canagliflozin, Metformin, Aspirin*).
- [x] Fasilitas unduhan berkas CSV contoh untuk pengujian *batch screening*.
- [x] Tab khusus *Metodologi & Petunjuk Sains*.
- [x] Paket siap-deploy ke Hugging Face Spaces (`hf_space/`) & skrip otomatis `deploy_to_hf.py`.
- [x] Kompatibilitas deployment penuh ke Streamlit Community Cloud (`packages.txt` & `requirements.txt` Linux ready) dan GitHub Codespaces (`.devcontainer`).


---

## 🚀 Fase 1: Jangka Pendek (Peningkatan Kualitas Prediksi & UI/UX)
*Fokus: Memperkuat validitas ilmiah prediksi, keandalan model, dan kemudahan interaksi pengguna.*

### 1.1 Evaluasi & Validasi Ilmiah Model (OECD QSAR Guidelines)
- [ ] **Applicability Domain (AD) Filter** `[PRIORITAS TINGGI]`
  - Implementasikan perhitungan *Applicability Domain* berbasis *Tanimoto Similarity* (k-NN) atau *Leverage / Williams Plot*.
  - Memberikan peringatan (*warning badge*) di web app jika molekul input berada di luar domain latih data ChEMBL (*unreliable prediction*).
- [ ] **Uncertainty Quantification / Prediction Interval** `[PRIORITAS TINGGI]`
  - Manfaatkan varians pohon keputusan pada *Random Forest* atau *Conformal Prediction* untuk menampilkan rentang ketidakpastian (contoh: $pActivity = 7.20 \pm 0.35$).
- [ ] **Model Explainability & Feature Importance (SHAP / Feature Attribution)** `[SEDANG]`
  - Integrasikan analisis SHAP (*SHapley Additive exPlanations*) atau visualisasi sub-struktur molekul (*Morgan fingerprint bit visualization*) untuk menunjukkan atom/gugus fungsi mana yang berkontribusi positif/negatif terhadap inhibisi SGLT2.

### 1.2 Penyempurnaan Antarmuka Pengguna (Web App Streamlit)
- [ ] **Molecular Sketcher Canvas (Ketcher / JSME)** `[PRIORITAS TINGGI]`
  - Tambahkan komponen kanvas gambar molekul (`streamlit-ketcher` atau iframe JSME) agar pengguna/peneliti dapat menggambar struktur 2D tanpa perlu menghafal atau mencari string SMILES manual.
- [ ] **Visualisasi Interaktif Konformasi 3D** `[SEDANG]`
  - Tambahkan tab visualisasi 3D interaktif menggunakan `py3Dmol` / `stmol` dengan kalkulasi konformasi energi rendah (*MMFF94 / UFF force field via RDKit*).
- [ ] **Radar / Spider Chart Properti Fisikokimia** `[SEDANG]`
  - Tampilkan diagram radar untuk *Lipinski Properties* (MW, LogP, H-Donors, H-Acceptors, TPSA, Rotatable Bonds) agar pengguna dapat melihat profil *drug-likeness* secara visual dan intuitif.
- [ ] **Ekspor Laporan Komprehensif (PDF/Excel)** `[SEDANG]`
  - Sediakan tombol unduh laporan lengkap dalam format PDF (mencakup struktur molekul, metrik bioaktivitas, status Lipinski, dan disclaimer ilmiah) serta Excel format `.xlsx`.

---

## 🔬 Fase 2: Jangka Menengah (Profil Farmasi Lanjutan & Eksplorasi Data)
*Fokus: Mengembangkan fungsionalitas komputasi kimia medisinal dan ekspansi pustaka senyawa.*

### 2.1 Profil Selektivitas Target (SGLT2 vs SGLT1)
- [ ] **Dual-Target Prediction: Rasio Selektivitas SGLT2/SGLT1** `[PRIORITAS TINGGI]`
  - Latih model pendamping untuk memprediksi bioaktivitas terhadap SGLT1 (*SLC5A1*).
  - *Urgensi Farmakologi*: Inhibisi SGLT1 di saluran cerna dapat memicu efek samping diare berat; inhibitor ideal (seperti Empagliflozin/Dapagliflozin) memiliki selektivitas tinggi SGLT2 > SGLT1 (>1000x).
  - Tambahkan kalkulasi *Selectivity Index* pada hasil analisis aplikasi.

### 2.2 Profil Toksisitas & ADMET In-Silico
- [ ] **Skrining ADMET & Toksisitas Bawaan** `[PRIORITAS TINGGI]`
  - Prediksi absorpsi intestinal (*HIA*), ikatan protein plasma (*PPB*), klirens ginjal, dan permeabilitas membran (*Caco-2 / PAMPA*).
  - Prediksi keamanan kardiovaskular: *hERG channel inhibition* (risiko aritmia jantung).
  - Prediksi hepatotoksisitas dan uji mutagenisitas *Ames Test*.
- [ ] **Synthetic Accessibility Score (SA Score)** `[SEDANG]`
  - Tambahkan estimasi kemudahan sintesis kimiawi (*SA Score* 1-10) untuk menyaring molekul hasil screening yang realistis disintesis di laboratorium basah.

### 2.3 Skrining Basis Data Bahan Alam Indonesia (Herbal / Phytochemicals)
- [ ] **Database Pre-Loaded Senyawa Bahan Alam Indonesia** `[SEDANG]`
  - Sediakan pustaka bawaan (*preset screening library*) berisi metabolit sekunder dari tanaman antidiabetes herbal Indonesia (contoh: daun salam, pare, temulawak, kayu manis, mahkota dewa) dari database COCONUT / KNApSAcK / HerbalDB.
  - Memfasilitasi riset fitofarmaka lokal untuk menemukan alternatif inhibitor alami (seperti sejarah penemuan *Phlorizin*).

### 2.4 Fasilitas Pemeriksaan & Profiling Lintas Golongan Obat Antidiabetes (Multi-Class Antidiabetic Profiling)
- [ ] **Pustaka Obat Kontrol & Senyawa Standar Antidiabetes (Benchmark Reference Library)** `[PRIORITAS TINGGI]`
  - Integrasikan pustaka molekul obat antidiabetes komersial (terverifikasi FDA/BPOM) dari berbagai golongan farmakologis ke dalam sistem sebagai standar pembanding:
    * **Biguanid**: Metformin, Fenformin, Buformin (Target: jalur aktivasi AMPK & penurunan glukoneogenesis hepatik).
    * **Sulfonilurea**: Glibenklamid (*Glyburide*), Glimepirid, Glipizid, Gliklazid (Target: reseptor SUR1 / penutupan kanal $K_{ATP}$ sel $\beta$ pankreas untuk stimulasi insulin).
    * **Alpha-Glucosidase Inhibitors (AGIs)**: Akarbosa, Miglitol, Voglibose (Target: enzim $\alpha$-glukosidase di usus halus untuk menunda absorpsi karbohidrat).
    * **DPP-4 Inhibitors (Gliptin)**: Sitagliptin, Vildagliptin, Linagliptin, Saksagliptin (Target: enzim Dipeptidyl Peptidase-4 untuk memperpanjang bioaktivitas hormon inkretin GLP-1/GIP).
    * **Thiazolidinediones (TZDs / Glitazones)**: Pioglitazone, Rosiglitazone (Target: agonis reseptor nuklear PPAR-$\gamma$ untuk meningkatkan sensitivitas insulin perifer).
    * **GLP-1 Receptor Agonists (GLP-1 RA)**: Semaglutide, Liraglutide, dan molekul kecil non-peptida oral (*oral small-molecule GLP-1 agonists*).
- [ ] **Panel Prediksi Multi-Target QSAR Antidiabetes (Multi-Target Directed Ligands - MTDL)** `[PRIORITAS TINGGI]`
  - Latih dan hubungkan model QSAR untuk target-target antidiabetes utama lainnya dari ChEMBL:
    * *DPP-4* (ChEMBL Target: `CHEMBL284`)
    * *Alpha-Glucosidase* (ChEMBL Target: `CHEMBL340`)
    * *PPAR-gamma* (ChEMBL Target: `CHEMBL235`)
    * *Kanal SUR1 / Kir6.2* (Target Sulfonilurea)
  - Memungkinkan peneliti memetakan apakah suatu senyawa baru bekerja murni sebagai inhibitor SGLT2 atau memiliki potensi aksi ganda (*dual-action antidiabetic / polypharmacology*) yang sinergis.
- [ ] **Dashboard Komparasi Farmakologi & Kemiripan Struktur Antargolongan** `[SEDANG]`
  - Sediakan fitur komparasi interaktif di Web App: Menghitung skor kemiripan struktural (*Tanimoto Similarity*) molekul uji terhadap prototipe obat dari masing-masing golongan antidiabetes.
  - Tampilkan diagram spider/radar profil farmakologi multi-mekanisme untuk membandingkan potensi, sifat fisikokimia Lipinski, dan mekanisme aksi dalam satu tampilan visual terpadu.

---

## 🧬 Fase 3: Jangka Panjang (Deep Learning, Struktur 3D & Sistem Terintegrasi)
*Fokus: Integrasi Graph AI, Molecular Docking, dan deployment skala riset institusi.*

### 3.1 Pemodelan Lanjutan (Deep Learning & Graph Neural Networks)
- [ ] **Eksplorasi Graph Neural Networks (GNN) / ChemBERTa** `[SEDANG]`
  - Uji arsitektur berbasis graf (*Directed Message Passing Neural Network - Chemprop*, GCN, atau GAT) yang langsung belajar dari representasi topologi molekuler tanpa *fixed-length fingerprints*.
  - Bandingkan performa secara *benchmark* dengan *Random Forest* baseline.

### 3.2 Integrasi Molecular Docking Otomatis
- [ ] **Penyambungan Molecular Docking (AutoDock Vina / GNINA Integration)** `[PRIORITAS TINGGI]`
  - Hubungkan struktur kristal/cryo-EM kompleks SGLT2 manusia (PDB ID: `7VSI` atau `7BOV`).
  - Untuk 5 senyawa teratas hasil virtual screening ML, jalankan simulasi *docking* otomatis untuk mengukur energi bebas pengikatan ($\Delta G$ kkal/mol) dan interaksi residu asam amino kunci (*Glu99, Phe98, Val157, Trp291*).

### 3.3 Skalabilitas Arsitektur & Deployment Produksi
- [x] **Cloud Hosting & Deployment (Streamlit Cloud & Hugging Face Spaces)** `[SELESAI]`
  - Konfigurasi repositori siap-pakai di Streamlit Community Cloud (dukungan `packages.txt` & `requirements.txt`).
  - Pembuatan bundel mandiri `hf_space/` dan skrip otomatis `deploy_to_hf.py` untuk Hugging Face Spaces.
  - Penambahan `.devcontainer/devcontainer.json` untuk dukungan langsung di GitHub Codespaces.
- [ ] **Containerization Mandiri (Dockerfile & docker-compose.yml)** `[SEDANG]`
  - Buat image Docker mandiri untuk lingkungan kluster lokal atau on-premise kampus.

- [ ] **REST API Headless (FastAPI Engine)** `[SEDANG]`
  - Pisahkan mesin inferensi ke dalam RESTful API (`FastAPI`) agar pipeline virtual screening dapat diakses via skrip Python eksternal, workflow KNIME, atau platform komputasi kluster.
- [ ] **Automated Testing & CI/CD Pipeline** `[SEDANG]`
  - Tulis *unit test* (`pytest`) untuk validasi sanitasi SMILES, ekstraksi fitur, konsistensi output model, dan penanganan input anomali.

---

## 📊 Matriks Ringkasan Rencana Kerja

| No | Modul / Fitur | Kategori | Prioritas | Estimasi Target |
|:---|:---|:---|:---|:---|
| 1 | **Applicability Domain (AD) Filter** | Validasi ML | 🔴 Tinggi | Fase 1 |
| 2 | **Uncertainty Quantification (Prediction Interval)** | Validasi ML | 🔴 Tinggi | Fase 1 |
| 3 | **Interactive Molecular Sketcher (Ketcher Canvas)** | UI/UX Web | 🔴 Tinggi | Fase 1 |
| 4 | **Dual-Target: Selektivitas SGLT2 vs SGLT1** | Farmakologi AI | 🔴 Tinggi | Fase 2 |
| 5 | **Pustaka Pembanding Golongan Antidiabetes (Biguanid, SU, AGI, DPP-4)** | Farmakologi Komparatif | 🔴 Tinggi | Fase 2 |
| 6 | **Panel Prediksi Multi-Target QSAR Antidiabetes (MTDL)** | AI & Polifarmakologi | 🔴 Tinggi | Fase 2 |
| 7 | **In-Silico ADMET Profiling (hERG, Caco-2, Ames)** | Farmakokinetik | 🔴 Tinggi | Fase 2 |
| 8 | **Automated Molecular Docking (PDB: 7VSI)** | Kimia Komputasi | 🔴 Tinggi | Fase 3 |
| 9 | **Dashboard Komparasi Farmakologi Antargolongan (Spider Plot)** | UI/UX Web | 🟡 Sedang | Fase 2 |
| 10 | **Visualisasi 3D Interaktif (py3Dmol/stmol)** | UI/UX Web | 🟡 Sedang | Fase 1 |
| 11 | **Synthetic Accessibility (SA) Score** | Kimia Medisinal | 🟡 Sedang | Fase 2 |
| 12 | **Database Senyawa Bahan Alam Indonesia** | Data Presets | 🟡 Sedang | Fase 2 |
| 13 | **Model Graph Neural Network (Chemprop/GNN)** | AI Lanjutan | 🟡 Sedang | Fase 3 |
| 14 | **Containerization Docker & FastAPI Service** | Infrastruktur | 🟡 Sedang | Fase 3 |
| 15 | **Ekspor Laporan PDF Lengkap & Cetak** | Fitur App | 🟡 Sedang | Fase 1 |

---

> [!NOTE]
> Daftar tugas ini bersifat adaptif dan dapat disesuaikan berkala berdasarkan arahan riset Prof. Arry, ketersediaan data biologis baru, serta kebutuhan publikasi ilmiah.
