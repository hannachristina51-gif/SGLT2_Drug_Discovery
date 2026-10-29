import os
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from rdkit import Chem
from rdkit.Chem import Draw

# ==============================================================================
# KONFIGURASI TEMA & PALET WARNA MODERN (MEDICAL AI / BIOINFORMATICS THEME)
# ==============================================================================
C_NAVY_DARK   = RGBColor(15, 23, 42)     # #0F172A - Slate 900 (Header / Dark Bg)
C_NAVY_MED    = RGBColor(30, 58, 138)    # #1E3A8A - Blue 900 (Primary Brand)
C_BLUE_ACCENT = RGBColor(2, 132, 199)    # #0284C7 - Sky 600 (Secondary Accent)
C_TEAL_ACCENT = RGBColor(13, 148, 136)   # #0D9488 - Teal 600 (Bio/Chem Accent)
C_GREEN_PASS  = RGBColor(22, 163, 74)    # #16A34A - Green 600 (Success / Active)
C_AMBER_WARN  = RGBColor(217, 119, 6)    # #D97706 - Amber 600 (Medium / Phase 2)
C_RED_HIGH    = RGBColor(220, 38, 38)    # #DC2626 - Red 600 (High Priority)
C_PURPLE_DL   = RGBColor(124, 58, 237)   # #7C3AED - Violet 600 (Deep Learning)

C_BG_LIGHT    = RGBColor(248, 250, 252)  # #F8FAFC - Slate 50 (Slide Background)
C_CARD_WHITE  = RGBColor(255, 255, 255)  # #FFFFFF - Pure White Card
C_CARD_SOFT   = RGBColor(241, 245, 249)  # #F1F5F9 - Slate 100
C_BORDER      = RGBColor(203, 213, 225)  # #CBD5E1 - Slate 300
C_TEXT_DARK   = RGBColor(15, 23, 42)     # #0F172A - Main Text
C_TEXT_MUTED  = RGBColor(71, 85, 105)    # #475569 - Secondary Text
C_WHITE       = RGBColor(255, 255, 255)  # #FFFFFF
C_GOLD_LIGHT  = RGBColor(254, 243, 199)  # #FEF3C7


def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header_banner(slide, title_text, subtitle_text, slide_num, total_slides=14):
    """Menambahkan header konsisten bergaya profesional di bagian atas slide."""
    # Top bar background
    banner = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15)
    )
    banner.fill.solid()
    banner.fill.fore_color.rgb = C_NAVY_DARK
    banner.line.fill.background()

    # Accent stripe di bawah banner
    stripe = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.12), Inches(13.333), Inches(0.06)
    )
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = C_TEAL_ACCENT
    stripe.line.fill.background()

    # Title & Subtitle
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.14), Inches(11.3), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.font.name = "Calibri"

    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.size = Pt(12)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.font.name = "Calibri"

    # Nomor Slide Badge
    badge = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(12.0), Inches(0.32), Inches(0.85), Inches(0.45)
    )
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_NAVY_MED
    badge.line.color.rgb = C_BLUE_ACCENT
    badge.line.width = Pt(1)
    btf = badge.text_frame
    btf.word_wrap = False
    bp = btf.paragraphs[0]
    bp.text = f"{slide_num} / {total_slides}"
    bp.alignment = PP_ALIGN.CENTER
    bp.font.size = Pt(11)
    bp.font.bold = True
    bp.font.color.rgb = C_WHITE
    bp.font.name = "Calibri"

    # Footer
    ftb = slide.shapes.add_textbox(Inches(0.5), Inches(7.15), Inches(12.333), Inches(0.3))
    ftf = ftb.text_frame
    fp = ftf.paragraphs[0]
    fp.text = "SGLT2 Inhibitor Virtual Screening & Drug Discovery Platform  |  Hanna Christina Ginting (2506713353) — Riset AI Prof. Arry (Universitas Indonesia)"
    fp.font.size = Pt(9.5)
    fp.font.color.rgb = C_TEXT_MUTED
    fp.font.name = "Calibri"


def add_card(slide, left, top, width, height, bg_color=C_CARD_WHITE, border_color=C_BORDER, accent_top_color=None):
    """Membuat kartu (card container) dengan opsional garis aksen di atasnya."""
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    card.adjustments[0] = 0.02
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()

    if accent_top_color:
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.08)
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent_top_color
        bar.line.fill.background()
    return card


def add_card_text(slide, left, top, width, height, heading, items, heading_color=C_NAVY_MED, heading_size=15, body_size=12):
    """Menambahkan teks berformat rapi (heading + bullet points) di dalam area kartu."""
    tb = slide.shapes.add_textbox(Inches(left + 0.18), Inches(top + 0.14), Inches(width - 0.36), Inches(height - 0.24))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p0 = tf.paragraphs[0]
    p0.text = heading
    p0.font.size = Pt(heading_size)
    p0.font.bold = True
    p0.font.color.rgb = heading_color
    p0.font.name = "Calibri"
    p0.space_after = Pt(6)

    for item in items:
        p = tf.add_paragraph()
        if isinstance(item, tuple):
            # (bold_prefix, rest_text)
            p.space_after = Pt(4)
            run_b = p.add_run()
            run_b.text = "• " + item[0] + ": "
            run_b.font.bold = True
            run_b.font.size = Pt(body_size)
            run_b.font.color.rgb = C_TEXT_DARK
            run_b.font.name = "Calibri"

            run_r = p.add_run()
            run_r.text = item[1]
            run_r.font.bold = False
            run_r.font.size = Pt(body_size)
            run_r.font.color.rgb = C_TEXT_MUTED
            run_r.font.name = "Calibri"
        else:
            p.text = "• " + item
            p.font.size = Pt(body_size)
            p.font.color.rgb = C_TEXT_DARK
            p.font.name = "Calibri"
            p.space_after = Pt(4)


def add_metric_box(slide, left, top, width, height, value_str, label_str, sub_str, accent_color):
    """Menambahkan kotak KPI / metrik dengan angka besar yang menonjol."""
    add_card(slide, left, top, width, height, bg_color=C_CARD_WHITE, border_color=C_BORDER, accent_top_color=accent_color)
    tb = slide.shapes.add_textbox(Inches(left + 0.12), Inches(top + 0.14), Inches(width - 0.24), Inches(height - 0.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p1 = tf.paragraphs[0]
    p1.text = value_str
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = accent_color
    p1.font.name = "Calibri"
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = label_str
    p2.font.size = Pt(11.5)
    p2.font.bold = True
    p2.font.color.rgb = C_TEXT_DARK
    p2.font.name = "Calibri"
    p2.alignment = PP_ALIGN.CENTER

    if sub_str:
        p3 = tf.add_paragraph()
        p3.text = sub_str
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = C_TEXT_MUTED
        p3.font.name = "Calibri"
        p3.alignment = PP_ALIGN.CENTER


def render_smiles_png_stream(smiles, size=(320, 240)):
    """Merender struktur kimia 2D dari SMILES ke BytesIO PNG menggunakan RDKit."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    img = Draw.MolToImage(mol, size=size)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return bio


def style_table_cell(cell, text, font_size=11, bold=False, text_color=C_TEXT_DARK, bg_color=None, align=PP_ALIGN.LEFT):
    cell.text = str(text)
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    if bg_color:
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_color
    p = cell.text_frame.paragraphs[0]
    p.alignment = align
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = text_color
    p.font.name = "Calibri"


def create_presentation():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(base_dir, "plots")

    prs = Presentation()
    # Set Widescreen 16:9 (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    TOTAL_SLIDES = 14

    # ==========================================================================
    # SLIDE 1: COVER / TITLE SLIDE
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_NAVY_DARK)

    # Decorative geometric accent bars
    bar_left = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.35), Inches(7.5))
    bar_left.fill.solid()
    bar_left.fill.fore_color.rgb = C_TEAL_ACCENT
    bar_left.line.fill.background()

    bar_top = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), Inches(0), Inches(12.983), Inches(0.12))
    bar_top.fill.solid()
    bar_top.fill.fore_color.rgb = C_BLUE_ACCENT
    bar_top.line.fill.background()

    # Pill Badge
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(0.8), Inches(5.6), Inches(0.45))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 41, 59)
    pill.line.color.rgb = C_TEAL_ACCENT
    pill.line.width = Pt(1.5)
    ptf = pill.text_frame
    pp = ptf.paragraphs[0]
    pp.text = "🧬 AI-DRIVEN DRUG DISCOVERY & VIRTUAL SCREENING PLATFORM"
    pp.font.size = Pt(11)
    pp.font.bold = True
    pp.font.color.rgb = RGBColor(45, 212, 191)
    pp.alignment = PP_ALIGN.CENTER

    # Main Title & Subtitle
    tb1 = s1.shapes.add_textbox(Inches(0.9), Inches(1.45), Inches(11.6), Inches(2.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_title = tf1.paragraphs[0]
    p_title.text = "SGLT2 Inhibitor Drug Discovery"
    p_title.font.size = Pt(44)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE
    p_title.font.name = "Calibri"
    p_title.space_after = Pt(8)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Platform Prediksi Bioaktivitas In-Silico Berbasis Machine Learning & Aplikasi Web Interaktif untuk Penemuan Kandidat Obat Diabetes Melitus Tipe 2"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = RGBColor(186, 230, 253)
    p_sub.font.name = "Calibri"

    # 4 Highlight Metric Cards on Cover
    cover_metrics = [
        ("CHEMBL1808", "Target Biologis SGLT2", "1.760 Senyawa Terkurasi", C_TEAL_ACCENT),
        ("2.052 Fitur", "Hybrid Representation", "2048-bit ECFP4 + 4 Lipinski", C_BLUE_ACCENT),
        ("R² = 0.7297", "Random Forest Regressor", "RMSE = 0.6317 | Scaffold Split", C_GREEN_PASS),
        ("Web & Cloud", "Streamlit + PDF Export", "Streamlit Cloud & HF Spaces", C_AMBER_WARN),
    ]
    for idx, (val, lbl, sub, col) in enumerate(cover_metrics):
        left_pos = 0.9 + idx * 2.95
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(4.15), Inches(2.75), Inches(1.45))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(30, 41, 59)
        card.line.color.rgb = col
        card.line.width = Pt(1.5)
        ctf = card.text_frame
        ctf.word_wrap = True

        cp1 = ctf.paragraphs[0]
        cp1.text = val
        cp1.font.size = Pt(21)
        cp1.font.bold = True
        cp1.font.color.rgb = C_WHITE
        cp1.alignment = PP_ALIGN.CENTER

        cp2 = ctf.add_paragraph()
        cp2.text = lbl
        cp2.font.size = Pt(11.5)
        cp2.font.bold = True
        cp2.font.color.rgb = RGBColor(148, 163, 184)
        cp2.alignment = PP_ALIGN.CENTER

        cp3 = ctf.add_paragraph()
        cp3.text = sub
        cp3.font.size = Pt(9.5)
        cp3.font.color.rgb = RGBColor(203, 213, 225)
        cp3.alignment = PP_ALIGN.CENTER

    # Author & Institution Box
    auth_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(5.95), Inches(11.55), Inches(1.05))
    auth_box.fill.solid()
    auth_box.fill.fore_color.rgb = RGBColor(15, 35, 66)
    auth_box.line.color.rgb = RGBColor(51, 65, 85)
    atf = auth_box.text_frame
    atf.word_wrap = True
    ap1 = atf.paragraphs[0]
    ap1.text = "👩‍🔬 Peneliti & Pengembang: Hanna Christina Ginting (NPM: 2506713353) — Universitas Indonesia"
    ap1.font.size = Pt(14)
    ap1.font.bold = True
    ap1.font.color.rgb = C_WHITE
    ap2 = atf.add_paragraph()
    ap2.text = "👨‍🏫 Dosen Pengampu / Pembimbing: Prof. Arry   |   🌐 Publikasi: github.com/hannachristina51-gif/SGLT2_Drug_Discovery   |   Update Terbaru: Oktober 2026"
    ap2.font.size = Pt(12)
    ap2.font.color.rgb = RGBColor(148, 163, 184)

    # ==========================================================================
    # SLIDE 2: LATAR BELAKANG FARMAKOLOGI & END-TO-END PIPELINE
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, C_BG_LIGHT)
    add_header_banner(
        s2,
        "1. Latar Belakang & Arsitektur End-to-End Aplikasi",
        "Peran strategis inhibisi SGLT2 pada terapi Diabetes Melitus Tipe 2 dan alur kerja komputasi hulu ke hilir",
        2, TOTAL_SLIDES
    )

    # Left Card: Urgensi Klinis SGLT2
    add_card(s2, 0.5, 1.4, 5.9, 3.1, accent_top_color=C_NAVY_MED)
    add_card_text(
        s2, 0.5, 1.48, 5.9, 3.0,
        "🎯 Mengapa Target SGLT2 (SLC5A2)?",
        [
            ("Mekanisme Fisiologis", "Protein kotransporter natrium-glukosa 2 (SGLT2) bertanggung jawab atas >90% reabsorpsi glukosa dari filtrat glomerulus di tubulus proksimal ginjal."),
            ("Keunggulan Terapi", "Inhibisi SGLT2 memicu ekskresi glukosa urin (glukosuria) dan menurunkan hiperglikemia secara independen dari sekresi insulin (risiko hipoglikemia rendah)."),
            ("Manfaat Kardiorenal", "Terbukti klinis memberikan efek kardioprotektif (gagal jantung) dan nefroprotektif pada pasien Diabetes Melitus Tipe 2."),
            ("Obat Referensi", "Gliflozin (Dapagliflozin, Empagliflozin, Canagliflozin) berbasis kerangka C-aryl glucoside.")
        ],
        heading_color=C_NAVY_MED, heading_size=15, body_size=11.5
    )

    # Right Card: Solusi AI In-Silico
    add_card(s2, 6.65, 1.4, 6.18, 3.1, accent_top_color=C_TEAL_ACCENT)
    add_card_text(
        s2, 6.65, 1.48, 6.18, 3.0,
        "💡 Solusi Aplikasi Virtual Screening Berbasis AI",
        [
            ("Akselerasi Penemuan Obat", "Menyaring ribuan molekul kandidat secara in-silico sebelum uji laboratorium basah (in-vitro) yang mahal dan memakan waktu."),
            ("Prediksi Kuantitatif QSAR", "Memprediksi afinitas pengikatan langsung dalam skala pActivity (-log10 IC50) serta estimasi konsentrasi IC50 (nM)."),
            ("Evaluasi Kepatuhan Obat Oral", "Mengintegrasikan pemeriksaan otomatis aturan fisikokimia Lipinski's Rule of Five."),
            ("Aksesibilitas Peneliti", "Dikemas dalam Web App Streamlit interaktif dengan fitur ekspor Laporan PDF Resmi A4, Cetak Langsung, dan Batch CSV.")
        ],
        heading_color=C_TEAL_ACCENT, heading_size=15, body_size=11.5
    )

    # Bottom Section: 6-Stage Pipeline Flowchart
    lbl_pipe = s2.shapes.add_textbox(Inches(0.5), Inches(4.62), Inches(12.3), Inches(0.35))
    p_lp = lbl_pipe.text_frame.paragraphs[0]
    p_lp.text = "🔄 Alur Arsitektur End-to-End Pipeline (6 Tahap Terintegrasi)"
    p_lp.font.size = Pt(14)
    p_lp.font.bold = True
    p_lp.font.color.rgb = C_NAVY_DARK

    stages = [
        ("Tahap 1", "Akuisisi Data ChEMBL", "Target CHEMBL1808\n4.114 data mentah IC50", C_NAVY_MED),
        ("Tahap 2", "Kurasi & Pre-processing", "Sanitasi SMILES, deduplikasi\n1.760 senyawa bersih", C_BLUE_ACCENT),
        ("Tahap 3", "Feature Engineering", "2048-bit Morgan FP +\n4 Lipinski Descriptors", C_TEAL_ACCENT),
        ("Tahap 4", "Pemodelan & Validasi", "Random Forest + GridSearchCV\nBemis-Murcko Scaffold Split", C_GREEN_PASS),
        ("Tahap 5", "Aplikasi Web Streamlit", "Single & Batch Screening\nStruktur 2D & Rule of 5", C_AMBER_WARN),
        ("Tahap 6", "Pelaporan & Cloud", "Generator PDF A4 & Print\nStreamlit Cloud & HF Spaces", C_PURPLE_DL),
    ]
    for i, (st_num, st_title, st_desc, st_col) in enumerate(stages):
        x = 0.5 + i * 2.08
        add_card(s2, x, 5.0, 1.95, 1.95, bg_color=C_CARD_WHITE, border_color=st_col, accent_top_color=st_col)
        tb_s = s2.shapes.add_textbox(Inches(x + 0.08), Inches(5.12), Inches(1.79), Inches(1.75))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True

        ps1 = tf_s.paragraphs[0]
        ps1.text = st_num
        ps1.font.size = Pt(10)
        ps1.font.bold = True
        ps1.font.color.rgb = st_col
        ps1.alignment = PP_ALIGN.CENTER

        ps2 = tf_s.add_paragraph()
        ps2.text = st_title
        ps2.font.size = Pt(12)
        ps2.font.bold = True
        ps2.font.color.rgb = C_TEXT_DARK
        ps2.alignment = PP_ALIGN.CENTER
        ps2.space_after = Pt(6)

        ps3 = tf_s.add_paragraph()
        ps3.text = st_desc
        ps3.font.size = Pt(10)
        ps3.font.color.rgb = C_TEXT_MUTED
        ps3.alignment = PP_ALIGN.CENTER

    # ==========================================================================
    # SLIDE 3: AKUISISI DATA, KURASI & EXPLORATORY DATA ANALYSIS (EDA)
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, C_BG_LIGHT)
    add_header_banner(
        s3,
        "2. Akuisisi Data ChEMBL, Kurasi & Exploratory Data Analysis (EDA)",
        "Penyaringan ketat bioaktivitas CHEMBL1808 dan pemetaan ruang kimia (Chemical Space) senyawa inhibitor SGLT2",
        3, TOTAL_SLIDES
    )

    # Top Summary Cards
    add_metric_box(s3, 0.5, 1.35, 2.9, 1.25, "4.114", "Data Mentah ChEMBL", "Target ID: CHEMBL1808 (IC50)", C_NAVY_MED)
    add_metric_box(s3, 3.6, 1.35, 2.9, 1.25, "1.760", "Senyawa Terkurasi Bersih", "Bebas duplikat & SMILES valid", C_TEAL_ACCENT)

    # Classification Threshold Card
    add_card(s3, 6.7, 1.35, 6.13, 1.25, accent_top_color=C_GREEN_PASS)
    add_card_text(
        s3, 6.7, 1.4, 6.13, 1.15,
        "📏 Standar Klasifikasi Bioaktivitas — pActivity = -log10(IC50 Molar)",
        [
            ("🟢 Aktif (Poten)", "pActivity > 6.0  (setara IC50 < 1.000 nM)"),
            ("🟡 Intermediate (Menengah)", "5.0 < pActivity ≤ 6.0  (IC50: 1.000 – 10.000 nM)"),
            ("🔴 Tidak Aktif", "pActivity ≤ 5.0  (setara IC50 > 10.000 nM)")
        ],
        heading_color=C_NAVY_DARK, heading_size=12.5, body_size=10.5
    )

    # 3 Embedded EDA Plots from ./plots/
    plot_specs = [
        ("01_bioactivity_distribution.png", "Distribusi Kelas Bioaktivitas", "Proporsi senyawa Aktif, Intermediate, dan Tidak Aktif"),
        ("02_chemical_space_mw_logp.png", "Ruang Kimia (MW vs LogP)", "Kepatuhan terhadap Lipinski's Rule of Five"),
        ("03_pActivity_boxplot.png", "Distribusi pActivity (pIC50)", "Sebaran statistik nilai pActivity antarkelas"),
    ]
    for idx, (fname, ptitle, psub) in enumerate(plot_specs):
        x_pos = 0.5 + idx * 4.2
        add_card(s3, x_pos, 2.78, 3.95, 4.2, accent_top_color=C_BLUE_ACCENT)
        tb_p = s3.shapes.add_textbox(Inches(x_pos + 0.12), Inches(2.88), Inches(3.7), Inches(0.55))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True
        pp1 = tf_p.paragraphs[0]
        pp1.text = ptitle
        pp1.font.size = Pt(12.5)
        pp1.font.bold = True
        pp1.font.color.rgb = C_NAVY_MED
        pp1.alignment = PP_ALIGN.CENTER

        pp2 = tf_p.add_paragraph()
        pp2.text = psub
        pp2.font.size = Pt(9.5)
        pp2.font.color.rgb = C_TEXT_MUTED
        pp2.alignment = PP_ALIGN.CENTER

        img_path = os.path.join(plots_dir, fname)
        if os.path.exists(img_path):
            s3.shapes.add_picture(img_path, Inches(x_pos + 0.18), Inches(3.48), width=Inches(3.58))

    # ==========================================================================
    # SLIDE 4: REKAYASA FITUR MOLEKULER (FEATURE ENGINEERING)
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, C_BG_LIGHT)
    add_header_banner(
        s4,
        "3. Rekayasa Fitur Molekuler (Hybrid Feature Engineering)",
        "Penggabungan representasi sub-struktur topologi Morgan Fingerprints (ECFP4) dan deskriptor fisikokimia Lipinski",
        4, TOTAL_SLIDES
    )

    # Left Card: Morgan Fingerprints
    add_card(s4, 0.5, 1.4, 6.0, 4.1, accent_top_color=C_NAVY_MED)
    add_card_text(
        s4, 0.5, 1.48, 6.0, 3.9,
        "🧬 1. Morgan Fingerprints (ECFP4 — Extended Connectivity)",
        [
            ("Algoritma RDKit", "AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)."),
            ("Lingkungan Atomik Sirkular", "Mengkodekan keberadaan gugus fungsi dan fragmen sub-struktur kimia dalam radius 2 ikatan kovalen di sekitar setiap atom."),
            ("Evolusi Dimensi Fitur", "Eksplorasi awal menggunakan vektor 1.024-bit (disimpan pada curated_features_and_fingerprints.csv dengan 1.035 kolom), kemudian ditingkatkan menjadi 2.048-bit pada model produksi untuk meminimalkan bit collision."),
            ("Karakteristik Matriks", "Vektor biner (0/1) berdimensi tinggi dan bersifat renggang (sparse binary matrix).")
        ],
        heading_color=C_NAVY_MED, heading_size=15, body_size=11.5
    )

    # Right Card: Lipinski Descriptors
    add_card(s4, 6.8, 1.4, 6.0, 4.1, accent_top_color=C_TEAL_ACCENT)
    add_card_text(
        s4, 6.8, 1.48, 6.0, 3.9,
        "⚖️ 2. Deskriptor Fisikokimia Lipinski (Rule of Five)",
        [
            ("Molecular Weight (MW)", "Berat molekul senyawa (batas ideal obat oral ≤ 500 Dalton)."),
            ("LogP (Koefisien Partisi Oktanol-Air)", "Indikator lipofilisitas & kemampuan menembus membran sel (ideal ≤ 5)."),
            ("NumHDonors (HBD)", "Jumlah donor ikatan hidrogen seperti gugus -OH dan -NH (ideal ≤ 5)."),
            ("NumHAcceptors (HBA)", "Jumlah akseptor ikatan hidrogen seperti atom O dan N (ideal ≤ 10)."),
            ("Standardisasi Numerik", "Keempat fitur kontinu dinormalisasi menggunakan StandardScaler (mean=0, std=1) yang disimpan pada models/scaler.pkl agar seimbang saat digabung dengan fingerprint.")
        ],
        heading_color=C_TEAL_ACCENT, heading_size=15, body_size=11.5
    )

    # Bottom Fusion Formula Banner
    add_card(s4, 0.5, 5.7, 12.3, 1.25, bg_color=C_NAVY_DARK, border_color=C_BLUE_ACCENT)
    tb_f = s4.shapes.add_textbox(Inches(0.7), Inches(5.82), Inches(11.9), Inches(1.0))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True
    pf1 = tf_f.paragraphs[0]
    pf1.text = "🔗 Vektor Masukan Model Produksi:  X = np.hstack([ Morgan_FP (2.048 bit)  +  StandardScaler(MW, LogP, HBD, HBA) (4 fitur) ])  ➔  Total 2.052 Fitur / Molekul"
    pf1.font.size = Pt(14)
    pf1.font.bold = True
    pf1.font.color.rgb = C_WHITE
    pf1.alignment = PP_ALIGN.CENTER

    pf2 = tf_f.add_paragraph()
    pf2.text = "Sinergi fitur mikro-struktural (fragmen pengikatan reseptor SGLT2) dan sifat makro-fisikokimia (kelarutan, ukuran, dan permeabilitas obat)."
    pf2.font.size = Pt(11.5)
    pf2.font.color.rgb = RGBColor(148, 163, 184)
    pf2.alignment = PP_ALIGN.CENTER

    # ==========================================================================
    # SLIDE 5: PEMODELAN MACHINE LEARNING, SCAFFOLD SPLIT & KOMPARASI ALGORITMA
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, C_BG_LIGHT)
    add_header_banner(
        s5,
        "4. Pemodelan Machine Learning, Validasi Scaffold Split & Komparasi Algoritma",
        "Strategi pencegahan overfitting berbasis kerangka molekul dan evaluasi komparatif ensambel pohon keputusan",
        5, TOTAL_SLIDES
    )

    # Left Column: Validation Strategy
    add_card(s5, 0.5, 1.4, 5.6, 5.55, accent_top_color=C_NAVY_MED)
    add_card_text(
        s5, 0.5, 1.48, 5.6, 5.3,
        "🛡️ Validasi Ilmiah & Strategi Pelatihan",
        [
            ("Bemis-Murcko Scaffold Split (70% Train : 30% Test)", "Menggunakan rdkit.Chem.Scaffolds.MurckoScaffold untuk mengelompokkan kerangka cincin inti molekul. Memastikan molekul di Test Set memiliki kerangka baru yang belum pernah dilihat saat training (mencegah data leakage)."),
            ("Isolasi Eksklusif Dapagliflozin", "Senyawa kontrol positif Dapagliflozin dipisahkan dari data latih dan ditempatkan 100% di Test Set sebagai blind validation."),
            ("Hyperparameter Tuning (GridSearchCV)", "Eksplorasi 81 kombinasi parameter dengan Cross-Validation. Parameter optimal: n_estimators=300, max_depth=None, min_samples_split=2."),
            ("Mengapa Random Forest Unggul?", "Algoritma ensambel paralel (bagging) terbukti jauh lebih stabil menghadapi matriks biner renggang (sparse 2.048-bit) tanpa mengalami over-spesialisasi dibanding Gradient Boosting.")
        ],
        heading_color=C_NAVY_MED, heading_size=14.5, body_size=11.2
    )

    # Right Top: KPI Metrics
    add_metric_box(s5, 6.35, 1.4, 3.1, 1.45, "R² = 0.7297", "Koefisien Determinasi", "Menjelaskan ~73% varians bioaktivitas", C_GREEN_PASS)
    add_metric_box(s5, 9.7, 1.4, 3.1, 1.45, "RMSE = 0.6317", "Root Mean Square Error", "Galat prediksi rendah (skala log pIC50)", C_BLUE_ACCENT)

    # Right Bottom: Experiment Comparison Table
    add_card(s5, 6.35, 3.05, 6.45, 3.9, accent_top_color=C_TEAL_ACCENT)
    tb_t5 = s5.shapes.add_textbox(Inches(6.55), Inches(3.18), Inches(6.1), Inches(0.4))
    pt5 = tb_t5.text_frame.paragraphs[0]
    pt5.text = "📊 Tabel Perbandingan Eksperimen Pemodelan (LogBook Riset)"
    pt5.font.size = Pt(13.5)
    pt5.font.bold = True
    pt5.font.color.rgb = C_NAVY_DARK

    table_shape5 = s5.shapes.add_table(5, 4, Inches(6.52), Inches(3.62), Inches(6.1), Inches(3.1))
    t5 = table_shape5.table
    t5.columns[0].width = Inches(2.25)
    t5.columns[1].width = Inches(1.45)
    t5.columns[2].width = Inches(0.95)
    t5.columns[3].width = Inches(1.45)

    headers5 = ["Konfigurasi Model", "Metode Tuning", "Skor R²", "Catatan Evaluasi"]
    for c_idx, h in enumerate(headers5):
        style_table_cell(t5.cell(0, c_idx), h, font_size=10.5, bold=True, text_color=C_WHITE, bg_color=C_NAVY_MED, align=PP_ALIGN.CENTER)

    rows5 = [
        ["Random Forest Regressor (Model Utama)", "Baseline Optimal", "0.7297", "RMSE 0.6317 (Terbaik ✅)"],
        ["RF + Hybrid 2052 Fitur (RandomSearch)", "RandomizedSearchCV", "0.7255", "10 iterasi CV"],
        ["RF + Hybrid 2052 Fitur (GridSearch)", "GridSearchCV (81 fit)", "0.7233", "n_estimators = 300"],
        ["HistGradientBoosting Regressor", "GridSearchCV", "0.7044", "lr=0.2, max_depth=9"],
    ]
    for r_idx, r_data in enumerate(rows5, start=1):
        bg = C_CARD_SOFT if r_idx % 2 == 1 else C_CARD_WHITE
        if r_idx == 1:
            bg = RGBColor(220, 252, 231)  # Highlight best row
        for c_idx, val in enumerate(r_data):
            al = PP_ALIGN.CENTER if c_idx == 2 else PP_ALIGN.LEFT
            bld = True if (r_idx == 1 or c_idx == 2) else False
            style_table_cell(t5.cell(r_idx, c_idx), val, font_size=10, bold=bld, bg_color=bg, align=al)

    # ==========================================================================
    # SLIDE 6: HASIL VIRTUAL SCREENING & VALIDASI OBAT KONTROL KOMERSIAL
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, C_BG_LIGHT)
    add_header_banner(
        s6,
        "5. Hasil Virtual Screening & Validasi Senyawa Kontrol Dunia Nyata",
        "Pengujian kemampuan model mengenali inhibitor SGLT2 komersial (Gliflozin) dibandingkan senyawa kelas terapi lain",
        6, TOTAL_SLIDES
    )

    # Left: Screening Table
    add_card(s6, 0.5, 1.4, 7.25, 5.55, accent_top_color=C_GREEN_PASS)
    tb_t6 = s6.shapes.add_textbox(Inches(0.7), Inches(1.52), Inches(6.9), Inches(0.7))
    tf_t6 = tb_t6.text_frame
    tf_t6.word_wrap = True
    pt6 = tf_t6.paragraphs[0]
    pt6.text = "💊 Hasil Penapisan Virtual (data/04_virtual_screening_results.csv)"
    pt6.font.size = Pt(14)
    pt6.font.bold = True
    pt6.font.color.rgb = C_NAVY_DARK
    pt6_sub = tf_t6.add_paragraph()
    pt6_sub.text = "Dapagliflozin berhasil diidentifikasi sebagai kandidat paling poten dengan skor pActivity tertinggi (7.84 / IC50 ≈ 14.3 nM)."
    pt6_sub.font.size = Pt(11)
    pt6_sub.font.color.rgb = C_TEXT_MUTED

    table_shape6 = s6.shapes.add_table(6, 5, Inches(0.68), Inches(2.28), Inches(6.9), Inches(3.25))
    t6 = table_shape6.table
    t6.columns[0].width = Inches(0.6)
    t6.columns[1].width = Inches(2.35)
    t6.columns[2].width = Inches(1.25)
    t6.columns[3].width = Inches(1.3)
    t6.columns[4].width = Inches(1.4)

    headers6 = ["Rank", "Nama Senyawa Uji", "Prediksi pActivity", "Estimasi IC50", "Status Klasifikasi"]
    for c_idx, h in enumerate(headers6):
        style_table_cell(t6.cell(0, c_idx), h, font_size=10.5, bold=True, text_color=C_WHITE, bg_color=C_NAVY_MED, align=PP_ALIGN.CENTER)

    rows6 = [
        ["#1 🏆", "Dapagliflozin (Inhibitor SGLT2)", "7.84", "14.33 nM", "Potensial Aktif"],
        ["#2", "Caffeine (Stimulan SSP)", "6.84", "144.33 nM", "Potensial Aktif"],
        ["#3", "Aspirin (Analgesik / Kontrol)", "6.67", "215.55 nM", "Potensial Aktif"],
        ["#4", "Metformin (Antidiabetik Biguanid)", "6.42", "378.52 nM", "Potensial Aktif"],
        ["#5", "Ibuprofen (NSAID)", "6.27", "533.66 nM", "Potensial Aktif"],
    ]
    for r_idx, r_data in enumerate(rows6, start=1):
        bg = RGBColor(220, 252, 231) if r_idx == 1 else (C_CARD_SOFT if r_idx % 2 == 1 else C_CARD_WHITE)
        for c_idx, val in enumerate(r_data):
            al = PP_ALIGN.LEFT if c_idx == 1 else PP_ALIGN.CENTER
            bld = True if r_idx == 1 else False
            style_table_cell(t6.cell(r_idx, c_idx), val, font_size=10.5, bold=bld, bg_color=bg, align=al)

    # Bottom note inside Left card
    tb_n6 = s6.shapes.add_textbox(Inches(0.7), Inches(5.68), Inches(6.9), Inches(1.1))
    tf_n6 = tb_n6.text_frame
    tf_n6.word_wrap = True
    pn6 = tf_n6.paragraphs[0]
    pn6.text = "💡 Catatan Validasi Ilmiah & Urgensi Applicability Domain:"
    pn6.font.size = Pt(11.5)
    pn6.font.bold = True
    pn6.font.color.rgb = C_NAVY_MED
    pn6_2 = tf_n6.add_paragraph()
    pn6_2.text = "Skor Dapagliflozin (7.84) unggul >1.0 unit logaritmik (10x lebih kuat dalam skala nM) dibanding molekul lain. Prediksi moderat pada molekul kecil non-SGLT2 (seperti Aspirin/Caffeine) menegaskan pentingnya penambahan filter Applicability Domain (AD) pada Fase 1 Roadmap."
    pn6_2.font.size = Pt(10.5)
    pn6_2.font.color.rgb = C_TEXT_MUTED

    # Right: Rendered 2D Chemical Structures of Commercial SGLT2 Inhibitors via RDKit
    add_card(s6, 7.95, 1.4, 4.88, 5.55, accent_top_color=C_TEAL_ACCENT)
    tb_r6 = s6.shapes.add_textbox(Inches(8.1), Inches(1.52), Inches(4.6), Inches(0.5))
    pr6 = tb_r6.text_frame.paragraphs[0]
    pr6.text = "🔬 Struktur 2D Inhibitor SGLT2 (Dirender via RDKit)"
    pr6.font.size = Pt(13)
    pr6.font.bold = True
    pr6.font.color.rgb = C_TEAL_ACCENT
    pr6.alignment = PP_ALIGN.CENTER

    gliflozins = [
        ("Dapagliflozin (pIC50 = 7.84)", "CC1=C(C=C(C=C1)CC2=C(C=CC(=C2)Cl)OCC)C3C(C(C(C(O3)CO)O)O)O"),
        ("Empagliflozin (Preset Acuan)", "C1=CC(=C(C=C1CC2=C(C=CC(=C2)Cl)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O)Cl"),
    ]
    for g_idx, (g_name, g_smiles) in enumerate(gliflozins):
        y_top = 2.05 + g_idx * 2.4
        bio_img = render_smiles_png_stream(g_smiles, size=(420, 230))
        if bio_img:
            s6.shapes.add_picture(bio_img, Inches(8.65), Inches(y_top), width=Inches(3.45))
        lbl_g = s6.shapes.add_textbox(Inches(8.1), Inches(y_top + 1.9), Inches(4.6), Inches(0.35))
        pg = lbl_g.text_frame.paragraphs[0]
        pg.text = g_name
        pg.font.size = Pt(11)
        pg.font.bold = True
        pg.font.color.rgb = C_NAVY_DARK
        pg.alignment = PP_ALIGN.CENTER

    # ==========================================================================
    # SLIDE 7: ARSITEKTUR APLIKASI WEB INTERAKTIF (STREAMLIT APP.PY)
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, C_BG_LIGHT)
    add_header_banner(
        s7,
        "6. Arsitektur Aplikasi Web Interaktif (Streamlit — app.py)",
        "Antarmuka pengguna modern yang membungkus model Machine Learning ke dalam 3 modul fungsional terpadu",
        7, TOTAL_SLIDES
    )

    # Sidebar Architecture Card (Left)
    add_card(s7, 0.5, 1.4, 3.1, 5.55, bg_color=C_NAVY_DARK, border_color=C_TEAL_ACCENT, accent_top_color=C_TEAL_ACCENT)
    tb_sb = s7.shapes.add_textbox(Inches(0.68), Inches(1.58), Inches(2.74), Inches(5.2))
    tf_sb = tb_sb.text_frame
    tf_sb.word_wrap = True
    psb = tf_sb.paragraphs[0]
    psb.text = "🧭 Sidebar Panel Informasi"
    psb.font.size = Pt(14)
    psb.font.bold = True
    psb.font.color.rgb = RGBColor(45, 212, 191)
    psb.space_after = Pt(8)

    sb_items = [
        "Target Biologis: SGLT2 (SLC5A2)",
        "Dataset: ChEMBL (CHEMBL1808)",
        "Data Terkurasi: 1.760 senyawa",
        "Algoritma: Random Forest Regressor",
        "Validasi: Bemis-Murcko Scaffold Split",
        "Metrik Model: R² = 0.7297 | RMSE = 0.6317",
        "Panduan Ambang Bioaktivitas:\n  🟢 Aktif (> 6.0)\n  🟡 Intermediate (5.0–6.0)\n  🔴 Tidak Aktif (≤ 5.0)",
        "Caching Model Cerdas:\n  @st.cache_resource menjamin pemuatan model .pkl instan tanpa reload berulang."
    ]
    for item in sb_items:
        p = tf_sb.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_WHITE
        p.space_after = Pt(5)

    # 3 Main Tabs Cards (Right)
    tabs_info = [
        (
            "Tab 1: 🧬 Single Molecule Prediction",
            C_NAVY_MED,
            [
                ("Preset Molekul Kontrol 1-Klik", "Pilihan instan Dapagliflozin, Empagliflozin, Canagliflozin, Metformin, & Aspirin."),
                ("Input SMILES Kustom & Validasi RDKit", "Sanitasi otomatis struktur kimia; mendeteksi string SMILES tidak valid."),
                ("Visualisasi Struktur 2D & Metrik Afinitas", "Gambar 2D molekul (340x340 px), skor pActivity (pIC50), dan konversi otomatis IC50 (nM / µM / mM)."),
                ("Evaluasi Lipinski & Ekspor Laporan", "Indikator Rule of Five (✅/❌) serta tombol unduh Laporan PDF Resmi, CSV, & Cetak Langsung.")
            ]
        ),
        (
            "Tab 2: 🗂️ Batch Virtual Screening (CSV)",
            C_TEAL_ACCENT,
            [
                ("Unduh Contoh CSV Pengujian", "Tersedia tombol unduh sample_batch_sglt2.csv berisi 5 senyawa referensi untuk uji cepat."),
                ("Unggah & Deteksi Kolom Otomatis", "Mendukung berkas CSV dengan nama kolom smiles atau canonical_smiles."),
                ("Pemrosesan Massal Paralel", "Dilengkapi progress bar real-time, kalkulasi pActivity, IC50 (nM), dan jumlah pelanggaran Lipinski."),
                ("Ekspor Rekapitulasi Batch", "Unduh Rekapitulasi PDF Batch Screening (Statistik + Top 20 Kandidat) dan tabel lengkap (.csv).")
            ]
        ),
        (
            "Tab 3: 📖 Metodologi & Petunjuk Sains",
            C_PURPLE_DL,
            [
                ("Transparansi Rumus Kimia Medisinal", "Penjelasan matematis hubungan logaritmik pActivity (pIC50) dan konsentrasi molar IC50 (nM)."),
                ("Kriteria Lipinski's Rule of Five", "Rincian 4 syarat kelayakan bioavailabilitas obat oral (MW, LogP, HBD, HBA)."),
                ("Dokumentasi Arsitektur AI", "Penjelasan penggabungan 2.048-bit ECFP4 + 4 deskriptor terstandarisasi dan uji generalisasi Scaffold Split.")
            ]
        )
    ]
    for idx, (t_title, t_col, t_bullets) in enumerate(tabs_info):
        y_pos = 1.4 + idx * 1.9
        add_card(s7, 3.85, y_pos, 8.98, 1.75, accent_top_color=t_col)
        add_card_text(s7, 3.85, y_pos + 0.04, 8.98, 1.68, t_title, t_bullets, heading_color=t_col, heading_size=13.5, body_size=10.5)

    # ==========================================================================
    # SLIDE 8: FITUR UNGGULAN 1 — PREDIKSI MOLEKUL TUNGGAL & VALIDASI LIPINSKI
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, C_BG_LIGHT)
    add_header_banner(
        s8,
        "7. Fitur Unggulan 1: Single Molecule Prediction & Lipinski's Rule of Five",
        "Detail alur inferensi senyawa tunggal, konversi satuan farmakologi otomatis, dan evaluasi kelayakan obat oral",
        8, TOTAL_SLIDES
    )

    # Left Card: Preset & Mathematical Conversion
    add_card(s8, 0.5, 1.4, 6.0, 5.55, accent_top_color=C_NAVY_MED)
    add_card_text(
        s8, 0.5, 1.48, 6.0, 5.3,
        "⚡ Alur Inferensi Instan & Preset Molekul Acuan",
        [
            ("5 Preset Senyawa Referensi Terintegrasi", "Memudahkan pengguna/reviewer menguji akurasi aplikasi dalam 1 klik tanpa mengetik SMILES manual:\n   1. Dapagliflozin (SGLT2 Inhibitor Komersial)\n   2. Empagliflozin (SGLT2 Inhibitor Komersial)\n   3. Canagliflozin (SGLT2 Inhibitor Komersial)\n   4. Metformin (Antidiabetik Golongan Biguanid)\n   5. Aspirin (Kontrol Negatif / NSAID)"),
            ("Transformasi Satuan IC50 Otomatis", "Menghitung IC50_nM = 10^(-pActivity) × 10^9 dan memformat tampilan secara adaptif ke satuan nM (<1.000 nM), µM (<10^6 nM), atau mM agar intuitif bagi farmasis."),
            ("Persistensi State (st.session_state)", "Hasil prediksi disimpan di memori sesi sehingga tampilan tidak ter-reset saat pengguna menekan tombol unduh PDF/CSV atau membuka pratinjau cetak.")
        ],
        heading_color=C_NAVY_MED, heading_size=14.5, body_size=11.2
    )

    # Right Card: Lipinski's Rule of Five Table & Example
    add_card(s8, 6.75, 1.4, 6.08, 5.55, accent_top_color=C_TEAL_ACCENT)
    tb_l8 = s8.shapes.add_textbox(Inches(6.95), Inches(1.52), Inches(5.7), Inches(0.8))
    tf_l8 = tb_l8.text_frame
    tf_l8.word_wrap = True
    pl8 = tf_l8.paragraphs[0]
    pl8.text = "🧪 Evaluasi Otomatis Lipinski's Rule of Five"
    pl8.font.size = Pt(14.5)
    pl8.font.bold = True
    pl8.font.color.rgb = C_TEAL_ACCENT
    pl8_s = tf_l8.add_paragraph()
    pl8_s.text = "Menilai apakah kandidat inhibitor SGLT2 memenuhi syarat sifat fisikokimia untuk diserap dengan baik melalui pemberian oral (Contoh: Profil Dapagliflozin):"
    pl8_s.font.size = Pt(11)
    pl8_s.font.color.rgb = C_TEXT_MUTED

    table_shape8 = s8.shapes.add_table(5, 4, Inches(6.95), Inches(2.4), Inches(5.68), Inches(2.6))
    t8 = table_shape8.table
    t8.columns[0].width = Inches(1.85)
    t8.columns[1].width = Inches(1.3)
    t8.columns[2].width = Inches(1.25)
    t8.columns[3].width = Inches(1.28)

    headers8 = ["Parameter Fisikokimia", "Batas Lipinski", "Dapagliflozin", "Status Validasi"]
    for c_idx, h in enumerate(headers8):
        style_table_cell(t8.cell(0, c_idx), h, font_size=10.5, bold=True, text_color=C_WHITE, bg_color=C_TEAL_ACCENT, align=PP_ALIGN.CENTER)

    rows8 = [
        ["Molecular Weight (MW)", "≤ 500 Da", "408.88 Da", "✅ Lolos"],
        ["LogP (Lipofilisitas)", "≤ 5.0", "2.14", "✅ Lolos"],
        ["H-Bond Donors (HBD)", "≤ 5", "4", "✅ Lolos"],
        ["H-Bond Acceptors (HBA)", "≤ 10", "6", "✅ Lolos"],
    ]
    for r_idx, r_data in enumerate(rows8, start=1):
        bg = C_CARD_SOFT if r_idx % 2 == 1 else C_CARD_WHITE
        for c_idx, val in enumerate(r_data):
            al = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
            style_table_cell(t8.cell(r_idx, c_idx), val, font_size=10.5, bold=(c_idx == 3), bg_color=bg, align=al)

    # Bottom Box inside Right Card
    add_card(s8, 6.95, 5.2, 5.68, 1.5, bg_color=RGBColor(240, 253, 244), border_color=C_GREEN_PASS)
    tb_b8 = s8.shapes.add_textbox(Inches(7.1), Inches(5.3), Inches(5.4), Inches(1.3))
    tf_b8 = tb_b8.text_frame
    tf_b8.word_wrap = True
    pb8 = tf_b8.paragraphs[0]
    pb8.text = "✅ Output Analisis Komprehensif Dapagliflozin di Aplikasi:"
    pb8.font.size = Pt(12)
    pb8.font.bold = True
    pb8.font.color.rgb = C_GREEN_PASS
    pb8_2 = tf_b8.add_paragraph()
    pb8_2.text = "• Prediksi pActivity: 7.84  |  Estimasi IC50: 14.33 nM\n• Status Bioaktivitas: POTENSIAL AKTIF (Kandidat Kuat Inhibitor SGLT2)\n• Kepatuhan Lipinski: 4/4 Parameter Lolos (0 Pelanggaran — Ideal sebagai obat oral)"
    pb8_2.font.size = Pt(10.5)
    pb8_2.font.color.rgb = C_TEXT_DARK

    # ==========================================================================
    # SLIDE 9: FITUR UNGGULAN 2 — EKSPOR LAPORAN PDF RESMI, CETAK & BATCH CSV
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, C_BG_LIGHT)
    add_header_banner(
        s9,
        "8. Fitur Unggulan Terbaru: Generator Laporan PDF Resmi & Cetak Dokumen",
        "Modul pelaporan laboratorium otomatis (pdf_report.py berbasis fpdf2) untuk dokumentasi riset dan publikasi",
        9, TOTAL_SLIDES
    )

    # 3 Columns for PDF Single, PDF Batch, and One-Click Print
    col_specs9 = [
        (
            "📑 1. Laporan PDF Senyawa Tunggal",
            C_NAVY_MED,
            [
                ("Format Dokumen Resmi A4", "Dihasilkan secara dinamis oleh fungsi generate_single_pdf_report() menggunakan pustaka fpdf2 murni."),
                ("Visualisasi Struktur 2D Resolusi Tinggi", "Menyematkan gambar 2D molekul (450x450 px) beserta Rumus Kimia (Molecular Formula) & Berat Molekul."),
                ("Ringkasan Eksekutif Bioaktivitas", "Menampilkan pActivity, IC50 (nM/µM), dan badge status berwarna sesuai klasifikasi potensi."),
                ("Tabel Evaluasi Lipinski & Metodologi", "Tabel lengkap 4 parameter Rule of Five, deskripsi arsitektur Random Forest, dan Scientific Disclaimer.")
            ]
        ),
        (
            "🗂️ 2. Rekapitulasi PDF Batch Screening",
            C_TEAL_ACCENT,
            [
                ("Statistik Penapisan Massal", "Fungsi generate_batch_pdf_report() merangkum total senyawa diuji, jumlah & persentase senyawa Aktif, Intermediate, dan Tidak Aktif."),
                ("Tabel 20 Kandidat Inhibitor Teratas", "Mengurutkan senyawa secara otomatis dari nilai pActivity tertinggi lengkap dengan SMILES, IC50 (nM), MW, LogP, dan jumlah pelanggaran Lipinski."),
                ("Ekspor Data Tabular (.csv)", "Tersedia tombol pendamping untuk mengunduh seluruh baris hasil batch screening dalam format CSV.")
            ]
        ),
        (
            "🖨️ 3. Pratinjau & Cetak 1-Klik (Print)",
            C_AMBER_WARN,
            [
                ("Template HTML Ramah-Cetak", "Fungsi get_printable_html() menyusun halaman pratinjau berformat A4 dengan aturan CSS @media print."),
                ("Integrasi Struktur Base64", "Gambar struktur molekul 2D dikodekan langsung ke Base64 PNG sehingga tampil tajam di semua browser."),
                ("Dialog Cetak Langsung (window.print)", "Tombol interaktif membuka dialog printer bawaan sistem operasi untuk mencetak ke kertas atau Save as PDF.")
            ]
        )
    ]

    for idx, (c_title, c_col, c_items) in enumerate(col_specs9):
        x_pos = 0.5 + idx * 4.2
        add_card(s9, x_pos, 1.4, 3.95, 5.55, accent_top_color=c_col)
        add_card_text(s9, x_pos, 1.48, 3.95, 5.35, c_title, c_items, heading_color=c_col, heading_size=14, body_size=11)

    # ==========================================================================
    # SLIDE 10: ARSITEKTUR CLOUD-READY & DEPLOYMENT MULTI-PLATFORM
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, C_BG_LIGHT)
    add_header_banner(
        s10,
        "9. Arsitektur Cloud-Ready, Ketahanan Runtime & Deployment Multi-Platform",
        "Rekayasa perangkat lunak untuk menjamin stabilitas aplikasi di Streamlit Cloud, Hugging Face Spaces, dan GitHub",
        10, TOTAL_SLIDES
    )

    # Top Row: 2 Cards (Streamlit Cloud Engineering & Hugging Face Spaces)
    add_card(s10, 0.5, 1.4, 6.0, 2.7, accent_top_color=C_NAVY_MED)
    add_card_text(
        s10, 0.5, 1.48, 6.0, 2.55,
        "☁️ 1. Optimasi Khusus Streamlit Community Cloud",
        [
            ("Self-Contained Library Bundling (./joblib & ./fpdf)", "Membundel pustaka pure-Python joblib dan fpdf2 langsung di repositori untuk melewati pembatasan PEP 668 pada container Debian Linux / Python 3.11–3.14."),
            ("Dynamic Site-Packages Discovery", "Pemindaian otomatis direktori site-packages Linux via glob.glob saat startup."),
            ("Dukungan Grafis Sistem (packages.txt)", "Menyertakan libxrender1 & libxext6 agar RDKit dapat merender gambar 2D di server headless.")
        ],
        heading_color=C_NAVY_MED, heading_size=14, body_size=10.8
    )

    add_card(s10, 6.8, 1.4, 6.0, 2.7, accent_top_color=C_TEAL_ACCENT)
    add_card_text(
        s10, 6.8, 1.48, 6.0, 2.55,
        "🤗 2. Bundel Mandiri Hugging Face Spaces (hf_space/)",
        [
            ("Direktori Siap-Deploy Lengkap", "Folder hf_space/ memuat app.py, pdf_report.py, models/, joblib/, fpdf/, requirements.txt, packages.txt, dan YAML frontmatter README."),
            ("Otomatisasi Deployment 1-Perintah", "Skrip deploy_to_hf.py berbasis huggingface_hub membuat repository Space dan mengunggah seluruh file (termasuk Git LFS model .pkl) secara otomatis.")
        ],
        heading_color=C_TEAL_ACCENT, heading_size=14, body_size=10.8
    )

    # Bottom Row: 2 Cards (GitHub + Codespaces & Local Multi-OS)
    add_card(s10, 0.5, 4.3, 6.0, 2.65, accent_top_color=C_PURPLE_DL)
    add_card_text(
        s10, 0.5, 4.38, 6.0, 2.5,
        "🐙 3. Publikasi GitHub & Dukungan GitHub Codespaces",
        [
            ("Repositori Publik Terdokumentasi", "Tersedia di github.com/hannachristina51-gif/SGLT2_Drug_Discovery lengkap dengan README.md, LogBook.md, dan TODO.md."),
            ("Cloud Development (.devcontainer)", "Dilengkapi konfigurasi devcontainer.json untuk menjalankan lingkungan pengembangan instan di GitHub Codespaces.")
        ],
        heading_color=C_PURPLE_DL, heading_size=14, body_size=10.8
    )

    add_card(s10, 6.8, 4.3, 6.0, 2.65, accent_top_color=C_GREEN_PASS)
    add_card_text(
        s10, 6.8, 4.38, 6.0, 2.5,
        "💻 4. Kemudahan Eksekusi Lokal Lintas Sistem Operasi",
        [
            ("Launcher Cepat Windows (run_windows.bat)", "Skrip eksekusi 1-klik untuk mengaktifkan virtual environment dan membuka aplikasi di http://localhost:8501."),
            ("Dukungan macOS & Linux", "Lingkungan terisolasi venv dengan dependensi terstandarisasi (scikit-learn, rdkit, streamlit, pandas, numpy, fpdf2).")
        ],
        heading_color=C_GREEN_PASS, heading_size=14, body_size=10.8
    )

    # ==========================================================================
    # SLIDE 11: ROADMAP PENGEMBANGAN FASE 1 (JANGKA PENDEK)
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, C_BG_LIGHT)
    add_header_banner(
        s11,
        "10. Peta Jalan Pengembangan (Roadmap) — Fase 1: Jangka Pendek",
        "Fokus: Peningkatan validitas ilmiah model sesuai pedoman OECD QSAR dan penyempurnaan interaktivitas UI/UX",
        11, TOTAL_SLIDES
    )

    # Left Card: OECD QSAR Model Validation
    add_card(s11, 0.5, 1.4, 6.0, 5.55, accent_top_color=C_RED_HIGH)
    add_card_text(
        s11, 0.5, 1.48, 6.0, 5.35,
        "🔬 1.1 Evaluasi & Validasi Ilmiah Model (OECD QSAR)",
        [
            ("Applicability Domain (AD) Filter [PRIORITAS TINGGI 🔴]", "Mengimplementasikan perhitungan kemiripan struktural Tanimoto Similarity (k-NN) atau Leverage (Williams Plot) terhadap data latih ChEMBL.\n   ➔ Menampilkan peringatan (warning badge) jika molekul uji berada di luar domain kimia model (mencegah positif palsu pada molekul seperti Aspirin/Caffeine)."),
            ("Uncertainty Quantification / Prediction Interval [TINGGI 🔴]", "Memanfaatkan varians antar-pohon keputusan (300 trees) pada Random Forest atau Conformal Prediction untuk menyajikan rentang ketidakpastian (contoh: pActivity = 7.84 ± 0.28)."),
            ("Model Explainability / SHAP & Bit Attribution [SEDANG 🟡]", "Visualisasi sub-struktur molekul (Morgan fingerprint bit highlighting) untuk memetakan atom/gugus fungsi yang berkontribusi positif atau negatif terhadap inhibisi SGLT2.")
        ],
        heading_color=C_RED_HIGH, heading_size=14.5, body_size=11
    )

    # Right Card: UI/UX Enhancements
    add_card(s11, 6.8, 1.4, 6.0, 5.55, accent_top_color=C_BLUE_ACCENT)
    add_card_text(
        s11, 6.8, 1.48, 6.0, 5.35,
        "🎨 1.2 Penyempurnaan Antarmuka Pengguna (Web App)",
        [
            ("Molecular Sketcher Canvas (Ketcher / JSME) [TINGGI 🔴]", "Menambahkan kanvas gambar struktur 2D interaktif (streamlit-ketcher) agar peneliti dapat menggambar atau memodifikasi molekul langsung di layar tanpa mengetik string SMILES."),
            ("Visualisasi Konformasi 3D Interaktif [SEDANG 🟡]", "Integrasi py3Dmol / stmol dengan optimasi geometri medan gaya MMFF94/UFF via RDKit untuk inspeksi ruang 3 dimensi."),
            ("Radar / Spider Chart Properti Fisikokimia [SEDANG 🟡]", "Visualisasi poligon profil drug-likeness (MW, LogP, HBD, HBA, TPSA, Rotatable Bonds)."),
            ("Ekspor Laporan Komprehensif PDF & Cetak [SELESAI 🟢]", "Telah berhasil diimplementasikan penuh melalui modul pdf_report.py (Laporan PDF A4 Single & Batch + One-Click Browser Print).")
        ],
        heading_color=C_BLUE_ACCENT, heading_size=14.5, body_size=11
    )

    # ==========================================================================
    # SLIDE 12: ROADMAP PENGEMBANGAN FASE 2 (JANGKA MENENGAH)
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, C_BG_LIGHT)
    add_header_banner(
        s12,
        "11. Peta Jalan Pengembangan — Fase 2: Profil Farmasi & Polifarmakologi",
        "Fokus: Selektivitas SGLT2/SGLT1, profil ADMET-Toksisitas, Fitofarmaka Indonesia, dan Multi-Target Antidiabetes",
        12, TOTAL_SLIDES
    )

    # 2x2 Grid of Cards for Phase 2
    p2_cards = [
        (
            0.5, 1.4, 6.0, 2.65,
            "⚖️ 2.1 Dual-Target: Selektivitas SGLT2 vs SGLT1 [🔴 Tinggi]",
            C_NAVY_MED,
            [
                ("Urgensi Klinis", "Inhibisi SGLT1 (SLC5A1) di saluran cerna memicu malabsorpsi glukosa-galaktosa dan diare osmotik berat."),
                ("Selectivity Index", "Melatih model pendamping SGLT1 untuk menghitung rasio selektivitas SGLT2/SGLT1 (inhibitor ideal >1.000x selektif terhadap SGLT2).")
            ]
        ),
        (
            6.8, 1.4, 6.0, 2.65,
            "🛡️ 2.2 Skrining ADMET In-Silico & SA Score [🔴 Tinggi]",
            C_TEAL_ACCENT,
            [
                ("Farmakokinetik & Keamanan", "Prediksi absorpsi intestinal (HIA), permeabilitas Caco-2, ikatan protein plasma (PPB), risiko aritmia jantung (hERG), hepatotoksisitas, & uji mutagenisitas Ames."),
                ("Synthetic Accessibility (SA Score)", "Skor 1–10 untuk menilai kemudahan sintesis molekul di laboratorium basah.")
            ]
        ),
        (
            0.5, 4.25, 6.0, 2.7,
            "🌿 2.3 Database Bahan Alam / Herbal Indonesia [🟡 Sedang]",
            C_GREEN_PASS,
            [
                ("Eksplorasi Fitofarmaka Lokal", "Pustaka bawaan metabolit sekunder tanaman antidiabetes Indonesia (daun salam, pare, temulawak, kayu manis, mahkota dewa) dari COCONUT / KNApSAcK / HerbalDB."),
                ("Inspirasi Phlorizin", "Mendukung penemuan kandidat glikosida alami baru seperti sejarah penemuan Phlorizin dari kulit pohon apel.")
            ]
        ),
        (
            6.8, 4.25, 6.0, 2.7,
            "💊 2.4 Profiling Lintas Golongan Antidiabetes (MTDL) [🔴 Tinggi]",
            C_AMBER_WARN,
            [
                ("Pustaka Standar 6 Golongan Antidiabetes", "Biguanid (Metformin), Sulfonilurea (Glimepirid), AGI (Akarbosa), DPP-4 Inhibitor (Sitagliptin), TZD (Pioglitazone), & GLP-1 RA."),
                ("Multi-Target QSAR & Tanimoto Similarity", "Prediksi polifarmakologi terhadap DPP-4 (CHEMBL284), Alpha-Glucosidase (CHEMBL340), & PPAR-γ (CHEMBL235) beserta Spider Plot komparatif.")
            ]
        )
    ]
    for (x, y, w, h, title, col, items) in p2_cards:
        add_card(s12, x, y, w, h, accent_top_color=col)
        add_card_text(s12, x, y + 0.05, w, h - 0.1, title, items, heading_color=col, heading_size=13.5, body_size=10.5)

    # ==========================================================================
    # SLIDE 13: ROADMAP PENGEMBANGAN FASE 3 (JANGKA PANJANG)
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, C_BG_LIGHT)
    add_header_banner(
        s13,
        "12. Peta Jalan Pengembangan — Fase 3: Deep Learning, Docking & Produksi",
        "Fokus: Arsitektur Graph Neural Networks (GNN), integrasi struktur 3D SGLT2, dan layanan API skala institusi",
        13, TOTAL_SLIDES
    )

    col_specs13 = [
        (
            "🧬 3.1 Graph Neural Networks (GNN) & ChemBERTa",
            C_PURPLE_DL,
            [
                ("Representasi Graf Molekuler Langsung", "Menguji arsitektur Directed Message Passing Neural Network (Chemprop), GCN, dan GAT yang belajar langsung dari topologi atom (node) dan ikatan kimia (edge)."),
                ("Transformer Kimia (ChemBERTa)", "Memanfaatkan model bahasa kimia pre-trained pada jutaan string SMILES."),
                ("Benchmark Komprehensif", "Membandingkan akurasi, kalibrasi ketidakpastian, dan generalisasi scaffold terhadap baseline Random Forest.")
            ]
        ),
        (
            "🧲 3.2 Integrasi Automated Molecular Docking",
            C_RED_HIGH,
            [
                ("Struktur Cryo-EM SGLT2 Manusia", "Menghubungkan pipeline dengan struktur kompleks protein SGLT2 beresolusi tinggi (PDB ID: 7VSI atau 7BOV)."),
                ("Simulasi AutoDock Vina / GNINA", "Menjalankan penambatan molekul otomatis untuk 5 kandidat teratas hasil skrining ML guna menghitung energi bebas ikatan (ΔG kkal/mol)."),
                ("Pemetaan Interaksi Residu Kunci", "Menganalisis ikatan hidrogen & hidrofobik pada kantong aktif SGLT2 (Phe98, Glu99, Val157, Trp291).")
            ]
        ),
        (
            "⚙️ 3.3 Orkestrasi Produksi (Docker, FastAPI & CI/CD)",
            C_NAVY_MED,
            [
                ("Cloud Hosting (Streamlit & HF Spaces) [SELESAI 🟢]", "Telah selesai dikonfigurasi dan berjalan stabil di cloud publik."),
                ("REST API Headless (FastAPI Engine)", "Memisahkan mesin inferensi ke layanan mikro RESTful agar dapat diakses oleh skrip eksternal, workflow KNIME, atau kluster kampus."),
                ("Containerization & Automated Testing", "Penyediaan Dockerfile, docker-compose.yml, serta unit testing pytest untuk CI/CD pipeline.")
            ]
        )
    ]
    for idx, (c_title, c_col, c_items) in enumerate(col_specs13):
        x_pos = 0.5 + idx * 4.2
        add_card(s13, x_pos, 1.4, 3.95, 5.55, accent_top_color=c_col)
        add_card_text(s13, x_pos, 1.48, 3.95, 5.35, c_title, c_items, heading_color=c_col, heading_size=13.5, body_size=11)

    # ==========================================================================
    # SLIDE 14: KESIMPULAN & PENUTUP
    # ==========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, C_NAVY_DARK)

    # Top & Left Accent Bars
    b14_l = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.35), Inches(7.5))
    b14_l.fill.solid()
    b14_l.fill.fore_color.rgb = C_TEAL_ACCENT
    b14_l.line.fill.background()

    tb14_h = s14.shapes.add_textbox(Inches(0.85), Inches(0.45), Inches(11.8), Inches(1.0))
    tf14_h = tb14_h.text_frame
    p14_h = tf14_h.paragraphs[0]
    p14_h.text = "🏁 Kesimpulan & Ringkasan Capaian Aplikasi (Baseline v1.0)"
    p14_h.font.size = Pt(28)
    p14_h.font.bold = True
    p14_h.font.color.rgb = C_WHITE

    p14_s = tf14_h.add_paragraph()
    p14_s.text = "Platform End-to-End Penemuan Obat Inhibitor SGLT2 Berbasis Machine Learning & Web Interaktif"
    p14_s.font.size = Pt(14)
    p14_s.font.color.rgb = RGBColor(45, 212, 191)

    # 4 Summary Pillars on Slide 14
    summary_pillars = [
        (
            "1. Pipeline Data & Fitur Kuat",
            "Kurasi 1.760 senyawa aktif SGLT2 dari ChEMBL (CHEMBL1808) dengan ekstraksi fitur hibrida 2.048-bit Morgan Fingerprints (ECFP4) dan 4 deskriptor fisikokimia Lipinski terstandarisasi.",
            C_TEAL_ACCENT
        ),
        (
            "2. Model ML Tervalidasi Ilmiah",
            "Random Forest Regressor mencapai performa R² = 0.7297 & RMSE = 0.6317, dilengkapi validasi Bemis-Murcko Scaffold Split dan terbukti akurat mengenali Dapagliflozin (pActivity 7.84).",
            C_GREEN_PASS
        ),
        (
            "3. Aplikasi Web & Pelaporan PDF",
            "Aplikasi Streamlit interaktif dengan prediksi senyawa tunggal, preset obat kontrol, skrining massal CSV, evaluasi Rule of Five, serta ekspor Laporan PDF Resmi A4 & Cetak 1-Klik.",
            C_BLUE_ACCENT
        ),
        (
            "4. Siap Cloud & Ekspansi Riset",
            "Telah siap di-deploy ke Streamlit Community Cloud & Hugging Face Spaces, dengan peta jalan terstruktur menuju ADMET, multi-target antidiabetes, GNN, dan Molecular Docking.",
            C_AMBER_WARN
        ),
    ]
    for idx, (sp_title, sp_desc, sp_col) in enumerate(summary_pillars):
        row = idx // 2
        col = idx % 2
        x_pos = 0.85 + col * 5.95
        y_pos = 1.65 + row * 1.95
        card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x_pos), Inches(y_pos), Inches(5.7), Inches(1.75))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(30, 41, 59)
        card.line.color.rgb = sp_col
        card.line.width = Pt(1.5)

        ctf = card.text_frame
        ctf.word_wrap = True
        cp1 = ctf.paragraphs[0]
        cp1.text = sp_title
        cp1.font.size = Pt(15)
        cp1.font.bold = True
        cp1.font.color.rgb = C_WHITE
        cp1.space_after = Pt(6)

        cp2 = ctf.add_paragraph()
        cp2.text = sp_desc
        cp2.font.size = Pt(11.5)
        cp2.font.color.rgb = RGBColor(203, 213, 225)

    # Thank You Banner at Bottom
    ty_box = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(5.65), Inches(11.65), Inches(1.3))
    ty_box.fill.solid()
    ty_box.fill.fore_color.rgb = C_NAVY_MED
    ty_box.line.color.rgb = C_TEAL_ACCENT
    ty_box.line.width = Pt(1.5)
    ty_tf = ty_box.text_frame
    ty_tf.word_wrap = True

    pty1 = ty_tf.paragraphs[0]
    pty1.text = "Terima Kasih 🙏  |  Sesi Diskusi & Tanya Jawab"
    pty1.font.size = Pt(22)
    pty1.font.bold = True
    pty1.font.color.rgb = C_WHITE
    pty1.alignment = PP_ALIGN.CENTER

    pty2 = ty_tf.add_paragraph()
    pty2.text = "Hanna Christina Ginting (NPM: 2506713353)  •  Pembimbing: Prof. Arry  •  Universitas Indonesia"
    pty2.font.size = Pt(12.5)
    pty2.font.color.rgb = RGBColor(186, 230, 253)
    pty2.alignment = PP_ALIGN.CENTER

    # Save to both presentation.pptx and Presentasi_SGLT2_Drug_Discovery_Terbaru.pptx
    out_main = os.path.join(base_dir, "presentation.pptx")
    out_named = os.path.join(base_dir, "Presentasi_SGLT2_Drug_Discovery_Terbaru.pptx")
    prs.save(out_main)
    prs.save(out_named)
    print(f"Berhasil membuat presentasi terbaru (14 slide widescreen): {out_main}")
    print(f"Salinan bernama juga disimpan di: {out_named}")


if __name__ == "__main__":
    create_presentation()
