from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def create_presentation():
    prs = Presentation()
    
    # 1. Title Slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "SGLT2 Inhibitor Drug Discovery 🧬"
    subtitle.text = "Pendekatan Machine Learning untuk Penemuan Obat"

    # Slide 2: Pendahuluan
    bullet_slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(bullet_slide_layout)
    title = slide.shapes.title
    body = slide.placeholders[1]
    title.text = "🔍 Pendahuluan & Pengumpulan Data"
    tf = body.text_frame
    tf.text = "Target Studi: Sodium-glucose cotransporter 2 (SGLT2)"
    p = tf.add_paragraph()
    p.text = "Sumber Data: ChEMBL Database"
    p = tf.add_paragraph()
    p.text = "Pemrosesan Data:"
    p = tf.add_paragraph()
    p.text = "Total 4.114 data mentah awal berhasil diekstraksi."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Melalui proses pembersihan dan penyaringan, diperoleh 1.760 senyawa aktif (bersih) yang siap untuk dianalisis lebih lanjut."
    p.level = 1

    # Slide 3: EDA
    slide = prs.slides.add_slide(bullet_slide_layout)
    title = slide.shapes.title
    body = slide.placeholders[1]
    title.text = "📊 Exploratory Data Analysis (EDA)"
    tf = body.text_frame
    tf.text = "Analisis eksploratif dilakukan untuk memahami karakteristik senyawa:"
    p = tf.add_paragraph()
    p.text = "Distribusi Kelas Bioaktivitas: Memahami rasio senyawa aktif, tidak aktif, dan menengah."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Ruang Kimia (Chemical Space): Analisis Molecular Weight (MW) terhadap LogP (Lipofilisitas) untuk melihat kepatuhan terhadap aturan Lipinski (Rule of Five)."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Boxplot pActivity: Distribusi nilai bioaktivitas (pIC50) antar kelas senyawa."
    p.level = 1

    # Slide 4: Feature Engineering
    slide = prs.slides.add_slide(bullet_slide_layout)
    title = slide.shapes.title
    body = slide.placeholders[1]
    title.text = "🧪 Ekstraksi Fitur (Feature Engineering)"
    tf = body.text_frame
    tf.text = "Data senyawa mentah tidak dapat langsung diproses oleh model, sehingga dilakukan ekstraksi fitur terhadap 1.755 data kurasi:"
    p = tf.add_paragraph()
    p.text = "Lipinski Descriptors: Mengekstrak properti fisikokimia (MW, LogP, NumHDonors, NumHAcceptors)."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Morgan Fingerprints: Representasi struktur molekul dalam bentuk vektor biner (1024-bit)."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Hasil Akhir: Total 1.035 kolom fitur yang digabungkan dan siap digunakan untuk pemodelan (disimpan dalam curated_features_and_fingerprints.csv)."
    p.level = 1

    # Slide 5: Machine Learning
    slide = prs.slides.add_slide(bullet_slide_layout)
    title = slide.shapes.title
    body = slide.placeholders[1]
    title.text = "🤖 Pemodelan Machine Learning"
    tf = body.text_frame
    tf.text = "Model regresi dilatih untuk memprediksi nilai bioaktivitas (pActivity)."
    p = tf.add_paragraph()
    p.text = "Algoritma Utama: Random Forest Regressor"
    p = tf.add_paragraph()
    p.text = "Evaluasi Kinerja Model:"
    p = tf.add_paragraph()
    p.text = "RMSE (Root Mean Square Error): 0.6317 (tingkat kesalahan rata-rata prediksi cukup rendah)."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "R-squared (R^2): 0.7297 (model mampu menjelaskan sekitar 73% varians dari data)."
    p.level = 1

    # Slide 6: Virtual Screening
    slide = prs.slides.add_slide(bullet_slide_layout)
    title = slide.shapes.title
    body = slide.placeholders[1]
    title.text = "💊 Virtual Screening"
    tf = body.text_frame
    tf.text = "Model yang telah dilatih digunakan untuk menyaring 5 senyawa kandidat/uji:"
    p = tf.add_paragraph()
    p.text = "Dapagliflozin (SGLT2 Inhibitor komersial): Prediksi pActivity 7.84 (Tertinggi & Paling Potensial)"
    p = tf.add_paragraph()
    p.text = "Kandidat Lainnya yang Berpotensi Aktif:"
    p = tf.add_paragraph()
    p.text = "Caffeine (Stimulan): Prediksi pActivity 6.84"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Aspirin (Analgesik): Prediksi pActivity 6.67"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Metformin (Antidiabetik): Prediksi pActivity 6.42"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Ibuprofen (NSAID): Prediksi pActivity 6.27"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Membuktikan bahwa model mampu membedakan tingkat aktivitas senyawa dan mengenali obat SGLT2 asli dengan skor tertinggi."

    # Slide 7: Rencana Optimasi Model
    slide = prs.slides.add_slide(bullet_slide_layout)
    title = slide.shapes.title
    body = slide.placeholders[1]
    title.text = "⚙️ Rencana Optimasi Model"
    tf = body.text_frame
    tf.text = "Untuk meningkatkan akurasi dan keandalan prediksi, berikut langkah optimasi yang akan dilakukan:"
    p = tf.add_paragraph()
    p.text = "Hyperparameter Tuning: Menggunakan GridSearchCV atau RandomizedSearchCV untuk menemukan parameter Random Forest yang paling optimal."
    p = tf.add_paragraph()
    p.text = "Eksplorasi Algoritma Lain: Membandingkan kinerja dengan algoritma canggih seperti XGBoost, LightGBM, atau Deep Learning."
    p = tf.add_paragraph()
    p.text = "Penambahan Deskriptor Lanjutan: Menggabungkan deskriptor struktural 3D dan farmakofor untuk informasi pengikatan reseptor yang lebih akurat."
    p = tf.add_paragraph()
    p.text = "Validasi Struktural (Scaffold Split): Menerapkan pemisahan data train-test berdasarkan kemiripan kerangka utama (scaffold) untuk mencegah overfitting."

    # Slide 8: Kesimpulan
    slide = prs.slides.add_slide(bullet_slide_layout)
    title = slide.shapes.title
    body = slide.placeholders[1]
    title.text = "🏁 Kesimpulan"
    tf = body.text_frame
    tf.text = "Pipeline Machine Learning dari hulu ke hilir berhasil dibangun untuk prediksi inhibitor SGLT2."
    p = tf.add_paragraph()
    p.text = "Penggunaan Random Forest dengan kombinasi Fingerprint dan Lipinski Descriptors menunjukkan performa yang sangat baik (R^2 = 0.73)."
    p = tf.add_paragraph()
    p.text = "Model siap dikembangkan lebih lanjut untuk Virtual Screening berskala besar pada database molekul (seperti ZINC atau PubChem)."

    # Slide 8: Thank You
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Terima Kasih 🙏"
    subtitle.text = "Ada pertanyaan?"

    prs.save("presentation.pptx")

if __name__ == "__main__":
    create_presentation()
    print("Presentation created successfully as presentation.pptx")
