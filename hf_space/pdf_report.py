import io
import os
import base64
import tempfile
import datetime
import pandas as pd
import numpy as np
from fpdf import FPDF
from rdkit import Chem
from rdkit.Chem import Draw, rdMolDescriptors


class SGLT2ReportPDF(FPDF):
    """
    Template PDF Resmi untuk Laporan Riset Penapisan Virtual SGLT2.
    Laboratorium Komputasi Farmasi - Riset Prof. Arry.
    """
    def __init__(self, title_text="LAPORAN HASIL PENAPISAN VIRTUAL SGLT2"):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.title_text = title_text
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        # Header bar dengan warna Navy (#1E3A8A)
        self.set_fill_color(30, 58, 138)
        self.rect(0, 0, 210, 20, "F")
        
        self.set_text_color(255, 255, 255)
        self.set_font("helvetica", "B", 11)
        self.set_xy(10, 4)
        self.cell(190, 6, "SGLT2 DRUG DISCOVERY - AI COMPUTATIONAL SCREENING", align="C")
        
        self.set_font("helvetica", "I", 8)
        self.set_xy(10, 10)
        self.cell(190, 6, "Laboratorium Komputasi Farmasi & Kimia Medisinal", align="C")
        self.ln(12)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(226, 232, 240)
        self.line(10, 283, 200, 283)
        self.set_font("helvetica", "I", 7.5)
        self.set_text_color(100, 116, 139)
        self.cell(95, 8, "Dokumen ini dihasilkan secara otomatis oleh Platform AI SGLT2 Drug Discovery", align="L")
        self.cell(95, 8, f"Halaman {self.page_no()}", align="R")


def generate_single_pdf_report(smiles, pred, ic50_nm, status, mw, logp, hdon, hacc, mol=None, compound_name="Senyawa Uji"):
    """
    Menghasilkan file PDF resmi untuk penapisan senyawa tunggal (Single Compound).
    """
    pdf = SGLT2ReportPDF(title_text="LAPORAN PREDIKSI SENYAWA TUNGGAL")
    pdf.add_page()
    
    # 1. Judul Laporan & Metadata
    pdf.set_y(26)
    pdf.set_text_color(30, 58, 138)
    pdf.set_font("helvetica", "B", 15)
    pdf.cell(0, 8, "Laporan Prediksi Bioaktivitas Inhibitor SGLT2", new_x="LMARGIN", new_y="NEXT", align="L")
    
    pdf.set_font("helvetica", "", 8.5)
    pdf.set_text_color(100, 116, 139)
    current_time = datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S WIB")
    pdf.cell(0, 5, f"Waktu Analisis: {current_time}  |  Target Biologis: SGLT2 (SLC5A2)  |  Spesies: Human", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_draw_color(203, 213, 225)
    pdf.set_line_width(0.3)
    pdf.line(10, 42, 200, 42)
    pdf.ln(4)

    # 2. Gambar Struktur Kimia 2D & Identitas Molekul
    img_path = None
    if mol is not None:
        try:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                img = Draw.MolToImage(mol, size=(450, 320))
                img.save(tmp.name)
                img_path = tmp.name
        except Exception:
            img_path = None

    y_start_mol = 46
    if img_path and os.path.exists(img_path):
        # Bingkai gambar struktur di sebelah kiri
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(226, 232, 240)
        pdf.rect(10, y_start_mol, 75, 56, "DF")
        pdf.image(img_path, x=11, y=y_start_mol + 1, w=73, h=54)
        try:
            os.remove(img_path)
        except Exception:
            pass
        x_info = 90
        w_info = 110
    else:
        x_info = 10
        w_info = 190

    # Kotak Informasi Identitas Senyawa di sebelah kanan
    pdf.set_xy(x_info, y_start_mol)
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(x_info, y_start_mol, w_info, 56, "DF")
    
    pdf.set_xy(x_info + 4, y_start_mol + 3)
    pdf.set_font("helvetica", "B", 10.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(w_info - 8, 5, f"Identitas Molekul: {compound_name}", new_x="LMARGIN", new_y="NEXT")
    
    mol_formula = rdMolDescriptors.CalcMolFormula(mol) if mol else "N/A"
    
    pdf.set_font("helvetica", "", 8.5)
    pdf.set_text_color(51, 65, 85)
    
    info_items = [
        ("Rumus Molekul", mol_formula),
        ("Berat Molekul (MW)", f"{mw:.2f} Da"),
        ("SMILES Notasi", smiles if len(smiles) <= 50 else smiles[:47] + "..."),
    ]
    
    y_row = y_start_mol + 11
    for label, val in info_items:
        pdf.set_xy(x_info + 4, y_row)
        pdf.set_font("helvetica", "B", 8)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(32, 4.5, label + ":", align="L")
        pdf.set_font("helvetica", "", 8)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(w_info - 40, 4.5, str(val), align="L")
        y_row += 6

    # Full SMILES box jika panjang
    pdf.set_xy(x_info + 4, y_start_mol + 31)
    pdf.set_font("helvetica", "B", 7.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(w_info - 8, 4, "Canonical SMILES Lengkap:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_xy(x_info + 4, y_start_mol + 35)
    pdf.set_font("courier", "", 6.5)
    pdf.set_text_color(30, 41, 59)
    pdf.multi_cell(w_info - 8, 3.2, smiles)

    pdf.set_y(106)

    # 3. Hasil Prediksi Bioaktivitas Machine Learning
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 6, "1. Hasil Prediksi Bioaktivitas Inhibisi SGLT2", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    # Kotak Ringkasan Prediksi
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(10, 114, 190, 28, "DF")

    # Kolom Prediksi pActivity
    pdf.set_xy(14, 116)
    pdf.set_font("helvetica", "", 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(55, 4, "Nilai Bioaktivitas (pActivity / pIC50):", align="L")
    pdf.set_xy(14, 122)
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(55, 7, f"{pred:.2f}", align="L")
    pdf.set_xy(14, 130)
    pdf.set_font("helvetica", "I", 7)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(55, 4, "-log10(IC50 Molar)", align="L")

    # Kolom Estimasi IC50
    pdf.set_xy(75, 116)
    pdf.set_font("helvetica", "", 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(55, 4, "Estimasi IC50 (Potensi Inhibisi):", align="L")
    pdf.set_xy(75, 122)
    pdf.set_font("helvetica", "B", 16)
    if ic50_nm >= 1000:
        pdf.set_text_color(217, 119, 6)
        ic50_str = f"{ic50_nm/1000:.2f} uM"
    else:
        pdf.set_text_color(22, 163, 74)
        ic50_str = f"{ic50_nm:.2f} nM"
    pdf.cell(55, 7, ic50_str, align="L")
    pdf.set_xy(75, 130)
    pdf.set_font("helvetica", "I", 7)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(55, 4, f"Setara {ic50_nm:.2f} nanomolar", align="L")

    # Kolom Status Klasifikasi & Badge
    pdf.set_xy(135, 116)
    pdf.set_font("helvetica", "", 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(60, 4, "Klasifikasi Aktivitas:", align="L")

    if pred > 6.0:
        status_color = (22, 163, 74)      # Emerald
        status_label = "POTENSIAL AKTIF"
        status_desc = "Afinitas Sub-Mikromolar (Inhibitor Kuat)"
    elif pred > 5.0:
        status_color = (217, 119, 6)     # Amber
        status_label = "INTERMEDIATE"
        status_desc = "Potensi Sedang (Perlu Optimasi Struktur)"
    else:
        status_color = (220, 38, 38)     # Red
        status_label = "TIDAK AKTIF"
        status_desc = "Inhibisi Rendah / Afinitas Lemah"

    pdf.set_xy(135, 122)
    pdf.set_fill_color(*status_color)
    pdf.set_draw_color(*status_color)
    pdf.rect(135, 122, 58, 8, "DF")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("helvetica", "B", 9)
    pdf.set_xy(135, 123.5)
    pdf.cell(58, 5, status_label, align="C")

    pdf.set_xy(135, 131)
    pdf.set_font("helvetica", "I", 7)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(58, 4, status_desc, align="C")

    pdf.set_y(147)

    # 4. Validasi Lipinski's Rule of Five
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 6, "2. Profil Drug-Likeness (Lipinski's Rule of Five)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    # Header Tabel Lipinski
    pdf.set_fill_color(226, 232, 240)
    pdf.set_draw_color(203, 213, 225)
    pdf.set_font("helvetica", "B", 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(50, 6, "Deskriptor Fisikokimia", border=1, fill=True, align="L")
    pdf.cell(45, 6, "Nilai Molekul", border=1, fill=True, align="C")
    pdf.cell(45, 6, "Kriteria Lipinski", border=1, fill=True, align="C")
    pdf.cell(50, 6, "Status Evaluasi", border=1, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")

    # Baris Tabel Lipinski
    lipinski_rows = [
        ("Molecular Weight (MW)", f"{mw:.2f} Da", "<= 500 Da", mw <= 500),
        ("LogP (Lipofilisitas)", f"{logp:.2f}", "<= 5.0", logp <= 5.0),
        ("H-Bond Donors (HBD)", f"{int(hdon)}", "<= 5", hdon <= 5),
        ("H-Bond Acceptors (HBA)", f"{int(hacc)}", "<= 10", hacc <= 10),
    ]

    violations = 0
    pdf.set_font("helvetica", "", 8)
    for name, val_str, rule_str, is_pass in lipinski_rows:
        pdf.set_text_color(15, 23, 42)
        pdf.cell(50, 5.5, f" {name}", border=1, align="L")
        pdf.cell(45, 5.5, val_str, border=1, align="C")
        pdf.cell(45, 5.5, rule_str, border=1, align="C")
        if is_pass:
            pdf.set_text_color(22, 163, 74)
            pdf.set_font("helvetica", "B", 8)
            pdf.cell(50, 5.5, "Lolos", border=1, align="C", new_x="LMARGIN", new_y="NEXT")
        else:
            violations += 1
            pdf.set_text_color(220, 38, 38)
            pdf.set_font("helvetica", "B", 8)
            pdf.cell(50, 5.5, "Melanggar", border=1, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 8)

    # Kesimpulan Druglikeness
    pdf.ln(2)
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(10, pdf.get_y(), 190, 10, "DF")
    pdf.set_xy(14, pdf.get_y() + 2)
    pdf.set_font("helvetica", "B", 8)
    pdf.set_text_color(15, 23, 42)
    if violations == 0:
        pdf.cell(0, 6, "Kesimpulan Lipinski: Senyawa mematuhi seluruh Aturan Lima Lipinski (0 Pelanggaran) - Potensi Bioavailabilitas Oral Tinggi.", align="L")
    elif violations == 1:
        pdf.cell(0, 6, f"Kesimpulan Lipinski: Terdapat 1 Pelanggaran Lipinski. Masih dapat ditoleransi dalam rentang drug-like space.", align="L")
    else:
        pdf.cell(0, 6, f"Kesimpulan Lipinski: Terdapat {violations} Pelanggaran Lipinski. Perlu optimasi formulasi / farmakokinetik.", align="L")

    pdf.set_y(190)

    # 5. Metodologi AI & Parameter Model
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 6, "3. Metodologi & Arsitektur AI Model", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    pdf.set_font("helvetica", "", 7.5)
    pdf.set_text_color(51, 65, 85)
    methodology_text = (
        "Model prediksi bioaktivitas menggunakan arsitektur Random Forest Regressor yang dioptimasi pada dataset "
        "bioaktivitas SGLT2 (Target ChEMBL ID: CHEMBL2094248) yang terkurasi. Representasi kimia menggabungkan "
        "2.048-bit Morgan Fingerprints (ECFP4, radius 2) dan deskriptor fisikokimia terstandarisasi. Pemisahan "
        "dataset dilakukan dengan skema Bemis-Murcko Scaffold Split untuk menguji generalisasi molekul sejati."
    )
    pdf.multi_cell(190, 4, methodology_text)

    # 6. Catatan Ilmiah & Disclaimer
    pdf.ln(3)
    pdf.set_fill_color(254, 243, 199)     # Soft amber
    pdf.set_draw_color(251, 191, 36)
    y_disc = pdf.get_y()
    pdf.rect(10, y_disc, 190, 20, "DF")
    
    pdf.set_xy(14, y_disc + 2)
    pdf.set_font("helvetica", "B", 8)
    pdf.set_text_color(180, 83, 9)
    pdf.cell(180, 4, "Catatan Ilmiah & Pernyataan Penyangkalan (Scientific Disclaimer):", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_xy(14, y_disc + 6.5)
    pdf.set_font("helvetica", "", 7)
    pdf.set_text_color(120, 53, 15)
    disclaimer_text = (
        "Laporan ini dihasilkan secara komputasi (in-silico) sebagai alat penapisan awal (virtual screening) "
        "dalam eksplorasi obat antidiabetes inhibitor SGLT2. Nilai prediksi tidak menggantikan pengujian "
        "eksperimental langsung. Validasi basah in-vitro (seperti enzyme inhibition assay) dan karakterisasi "
        "toksikologi laboratorium tetap menjadi syarat mutlak untuk konfirmasi aktivitas farmakologis definitif."
    )
    pdf.multi_cell(182, 3.4, disclaimer_text)

    # 7. Tanda Tangan Verifikasi
    pdf.set_y(y_disc + 23)
    pdf.set_font("helvetica", "I", 7.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(95, 4, f"Diverifikasi oleh: Tim Riset SGLT2 AI", align="L")
    pdf.cell(95, 4, f"Prof. Arry Research Group - Fakultas Farmasi", align="R")

    return bytes(pdf.output())


def generate_batch_pdf_report(df_results, title="Laporan Hasil Batch Virtual Screening SGLT2"):
    """
    Menghasilkan file PDF rekapitulasi untuk penapisan massal (Batch Screening via CSV).
    """
    pdf = SGLT2ReportPDF(title_text="LAPORAN HASIL BATCH VIRTUAL SCREENING")
    pdf.add_page()

    # Header & Metadata
    pdf.set_y(26)
    pdf.set_text_color(30, 58, 138)
    pdf.set_font("helvetica", "B", 15)
    pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT", align="L")

    pdf.set_font("helvetica", "", 8.5)
    pdf.set_text_color(100, 116, 139)
    current_time = datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S WIB")
    total_cmpds = len(df_results)
    pdf.cell(0, 5, f"Waktu Analisis: {current_time}  |  Total Senyawa Dianalisis: {total_cmpds} Senyawa", new_x="LMARGIN", new_y="NEXT")

    pdf.set_draw_color(203, 213, 225)
    pdf.line(10, 42, 200, 42)
    pdf.ln(4)

    # Statistik Ringkasan
    active_cnt = len(df_results[df_results["Status"] == "Aktif"]) if "Status" in df_results.columns else 0
    inter_cnt = len(df_results[df_results["Status"] == "Intermediate"]) if "Status" in df_results.columns else 0
    inactive_cnt = len(df_results[df_results["Status"] == "Tidak Aktif"]) if "Status" in df_results.columns else 0

    pdf.set_y(46)
    pdf.set_font("helvetica", "B", 10.5)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 6, "1. Ringkasan Hasil Penapisan Massal", new_x="LMARGIN", new_y="NEXT")

    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(10, 53, 190, 16, "DF")

    stats_col_w = 47.5
    stats = [
        ("Total Senyawa", str(total_cmpds), (15, 23, 42)),
        ("Potensial Aktif", f"{active_cnt} ({active_cnt/total_cmpds*100:.1f}%)" if total_cmpds > 0 else "0", (22, 163, 74)),
        ("Intermediate", f"{inter_cnt} ({inter_cnt/total_cmpds*100:.1f}%)" if total_cmpds > 0 else "0", (217, 119, 6)),
        ("Tidak Aktif", f"{inactive_cnt} ({inactive_cnt/total_cmpds*100:.1f}%)" if total_cmpds > 0 else "0", (220, 38, 38)),
    ]

    for i, (label, val, col) in enumerate(stats):
        x_pos = 10 + (i * stats_col_w)
        pdf.set_xy(x_pos, 54.5)
        pdf.set_font("helvetica", "", 7.5)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(stats_col_w, 4, label, align="C")
        pdf.set_xy(x_pos, 60)
        pdf.set_font("helvetica", "B", 10)
        pdf.set_text_color(*col)
        pdf.cell(stats_col_w, 6, val, align="C")

    # Tabel Top Candidates (Urutkan dari pActivity tertinggi)
    pdf.set_y(73)
    pdf.set_font("helvetica", "B", 10.5)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 6, "2. Tabel Peringkat Kandidat Teratas (Top Screened Compounds)", new_x="LMARGIN", new_y="NEXT")

    # Sort candidates
    df_sorted = df_results.sort_values(by="Prediksi_pActivity", ascending=False).reset_index(drop=True)
    top_n = min(20, len(df_sorted))

    # Header Tabel
    pdf.set_fill_color(226, 232, 240)
    pdf.set_draw_color(203, 213, 225)
    pdf.set_font("helvetica", "B", 7.5)
    pdf.set_text_color(15, 23, 42)
    
    col_widths = [10, 65, 24, 28, 33, 30]
    headers = ["No", "SMILES (Trunkasi)", "pActivity", "IC50 (nM)", "Status", "Lipinski Viol."]
    
    pdf.set_y(80)
    for w, h in zip(col_widths, headers):
        pdf.cell(w, 6, h, border=1, fill=True, align="C")
    pdf.ln()

    # Baris data
    pdf.set_font("helvetica", "", 7)
    for idx in range(top_n):
        row = df_sorted.iloc[idx]
        smiles_disp = str(row.get("SMILES", ""))
        if len(smiles_disp) > 35:
            smiles_disp = smiles_disp[:32] + "..."
        
        pred_val = row.get("Prediksi_pActivity", 0)
        pred_str = f"{pred_val:.2f}" if not pd.isna(pred_val) else "N/A"
        
        ic50_val = row.get("Estimasi_IC50_nM", 0)
        ic50_str = f"{ic50_val:.2f}" if not pd.isna(ic50_val) else "N/A"
        
        status_val = str(row.get("Status", "N/A"))
        lip_viol = str(row.get("Lipinski_Violations", "0"))
        
        pdf.set_text_color(15, 23, 42)
        pdf.cell(col_widths[0], 5, str(idx + 1), border=1, align="C")
        pdf.cell(col_widths[1], 5, f" {smiles_disp}", border=1, align="L")
        pdf.cell(col_widths[2], 5, pred_str, border=1, align="C")
        pdf.cell(col_widths[3], 5, ic50_str, border=1, align="C")
        
        # Color status
        if status_val == "Aktif":
            pdf.set_text_color(22, 163, 74)
        elif status_val == "Intermediate":
            pdf.set_text_color(217, 119, 6)
        else:
            pdf.set_text_color(220, 38, 38)
        pdf.set_font("helvetica", "B", 7)
        pdf.cell(col_widths[4], 5, status_val, border=1, align="C")
        
        pdf.set_text_color(15, 23, 42)
        pdf.set_font("helvetica", "", 7)
        pdf.cell(col_widths[5], 5, lip_viol, border=1, align="C")
        pdf.ln()

    # Disclaimer di bawah tabel
    pdf.ln(4)
    pdf.set_font("helvetica", "I", 7)
    pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(190, 3.5, "Catatan: Tabel di atas menampilkan 20 kandidat teratas hasil skrining massal. Hasil lengkap dapat diakses melalui berkas CSV. Seluruh prediksi memerlukan uji validasi in-vitro sebelum melangkah ke tahap pengujian farmakologis pra-klinis.")

    return bytes(pdf.output())


def get_printable_html(smiles, pred, ic50_nm, status, mw, logp, hdon, hacc, mol=None, compound_name="Senyawa Uji"):
    """
    Menghasilkan HTML ramah-cetak (Print-friendly HTML template)
    dengan fungsi cetak langsung (window.print()) dan tombol interaktif.
    """
    # Generate image base64 if mol is available
    img_b64 = ""
    if mol is not None:
        try:
            img = Draw.MolToImage(mol, size=(400, 300))
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode()
        except Exception:
            img_b64 = ""

    mol_formula = rdMolDescriptors.CalcMolFormula(mol) if mol else "N/A"
    current_time = datetime.datetime.now().strftime("%d %B %Y, %H:%M WIB")

    if pred > 6.0:
        badge_bg = "#dcfce7"
        badge_text = "#15803d"
        status_label = "POTENSIAL AKTIF"
        status_desc = "Afinitas Sub-Mikromolar (Inhibitor Kuat SGLT2)"
    elif pred > 5.0:
        badge_bg = "#fef3c7"
        badge_text = "#b45309"
        status_label = "INTERMEDIATE"
        status_desc = "Potensi Menengah (Perlu Optimasi Struktur)"
    else:
        badge_bg = "#fee2e2"
        badge_text = "#b91c1c"
        status_label = "TIDAK AKTIF"
        status_desc = "Inhibisi Rendah / Negatif"

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Laporan Hasil Prediksi SGLT2 - {compound_name}</title>
<style>
  @media print {{
    body {{
      margin: 0;
      padding: 15mm;
      color: #0f172a;
      background: #ffffff;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    .no-print {{
      display: none !important;
    }}
    .page-box {{
      border: none !important;
      box-shadow: none !important;
      padding: 0 !important;
    }}
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background-color: #f8fafc;
    margin: 0;
    padding: 20px;
  }}
  .page-box {{
    max-width: 800px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    padding: 32px;
    border: 1px solid #e2e8f0;
  }}
  .header {{
    border-bottom: 2px solid #1e3a8a;
    padding-bottom: 16px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }}
  .header-title {{
    font-size: 20px;
    font-weight: 700;
    color: #1e3a8a;
    margin: 0 0 6px 0;
  }}
  .header-sub {{
    font-size: 12px;
    color: #64748b;
    margin: 0;
  }}
  .print-btn {{
    background-color: #1e3a8a;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 13px;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(30,58,138,0.2);
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }}
  .print-btn:hover {{
    background-color: #172554;
  }}
  .mol-section {{
    display: flex;
    gap: 20px;
    margin-bottom: 24px;
    background: #f8fafc;
    border-radius: 8px;
    padding: 16px;
    border: 1px solid #e2e8f0;
  }}
  .mol-img-box {{
    flex: 0 0 220px;
    background: white;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .mol-img-box img {{
    max-width: 100%;
    height: auto;
  }}
  .mol-info {{
    flex: 1;
  }}
  .results-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
  }}
  .stat-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 14px;
    text-align: center;
  }}
  .stat-val {{
    font-size: 22px;
    font-weight: 700;
    color: #0f172a;
    margin: 4px 0;
  }}
  .stat-lbl {{
    font-size: 11px;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 600;
  }}
  .badge {{
    display: inline-block;
    padding: 6px 14px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 12px;
    background-color: {badge_bg};
    color: {badge_text};
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 24px;
    font-size: 13px;
  }}
  th, td {{
    padding: 10px 12px;
    border: 1px solid #e2e8f0;
    text-align: left;
  }}
  th {{
    background-color: #f1f5f9;
    font-weight: 600;
    color: #334155;
  }}
  .disclaimer {{
    background-color: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 8px;
    padding: 14px;
    font-size: 11px;
    color: #92400e;
    line-height: 1.5;
  }}
</style>
</head>
<body>

<div class="page-box">
  <div class="header">
    <div>
      <h1 class="header-title">Laporan Penapisan Virtual SGLT2</h1>
      <p class="header-sub">Platform AI Drug Discovery | Lab Komputasi Farmasi Prof. Arry | Waktu: {current_time}</p>
    </div>
    <div class="no-print">
      <button class="print-btn" onclick="window.print()">🖨️ Cetak / Print Sekarang</button>
    </div>
  </div>

  <div class="mol-section">
    {'<div class="mol-img-box"><img src="data:image/png;base64,' + img_b64 + '" alt="2D Structure"></div>' if img_b64 else ''}
    <div class="mol-info">
      <h3 style="margin-top:0; color:#1e3a8a;">Identitas Senyawa: {compound_name}</h3>
      <p style="font-size:12px; margin:4px 0;"><strong>Rumus Molekul:</strong> {mol_formula}</p>
      <p style="font-size:12px; margin:4px 0;"><strong>Berat Molekul:</strong> {mw:.2f} Da</p>
      <p style="font-size:11px; margin:4px 0; word-break:break-all;"><strong>SMILES:</strong> <code>{smiles}</code></p>
    </div>
  </div>

  <h3 style="color:#1e3a8a; margin-bottom:12px;">Hasil Prediksi Bioaktivitas Machine Learning</h3>
  <div class="results-grid">
    <div class="stat-card">
      <div class="stat-lbl">Prediksi Bioaktivitas</div>
      <div class="stat-val">{pred:.2f}</div>
      <div style="font-size:10px; color:#64748b;">pActivity (pIC50)</div>
    </div>
    <div class="stat-card">
      <div class="stat-lbl">Estimasi IC50</div>
      <div class="stat-val">{f"{ic50_nm/1000:.2f} uM" if ic50_nm >= 1000 else f"{ic50_nm:.2f} nM"}</div>
      <div style="font-size:10px; color:#64748b;">Kekuatan Inhibisi</div>
    </div>
    <div class="stat-card">
      <div class="stat-lbl">Klasifikasi Status</div>
      <div style="margin: 8px 0;"><span class="badge">{status_label}</span></div>
      <div style="font-size:10px; color:#64748b;">{status_desc}</div>
    </div>
  </div>

  <h3 style="color:#1e3a8a; margin-bottom:12px;">Validasi Lipinski's Rule of Five</h3>
  <table>
    <thead>
      <tr>
        <th>Parameter Fisikokimia</th>
        <th>Nilai Molekul</th>
        <th>Kriteria Lipinski</th>
        <th>Status Kelayakan</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Molecular Weight (MW)</td>
        <td>{mw:.2f} Da</td>
        <td>&le; 500 Da</td>
        <td>{'<span style="color:#15803d; font-weight:600;">✅ Lolos</span>' if mw <= 500 else '<span style="color:#b91c1c; font-weight:600;">❌ Melanggar</span>'}</td>
      </tr>
      <tr>
        <td>LogP (Lipofilisitas)</td>
        <td>{logp:.2f}</td>
        <td>&le; 5.0</td>
        <td>{'<span style="color:#15803d; font-weight:600;">✅ Lolos</span>' if logp <= 5.0 else '<span style="color:#b91c1c; font-weight:600;">❌ Melanggar</span>'}</td>
      </tr>
      <tr>
        <td>H-Bond Donors (HBD)</td>
        <td>{int(hdon)}</td>
        <td>&le; 5</td>
        <td>{'<span style="color:#15803d; font-weight:600;">✅ Lolos</span>' if hdon <= 5 else '<span style="color:#b91c1c; font-weight:600;">❌ Melanggar</span>'}</td>
      </tr>
      <tr>
        <td>H-Bond Acceptors (HBA)</td>
        <td>{int(hacc)}</td>
        <td>&le; 10</td>
        <td>{'<span style="color:#15803d; font-weight:600;">✅ Lolos</span>' if hacc <= 10 else '<span style="color:#b91c1c; font-weight:600;">❌ Melanggar</span>'}</td>
      </tr>
    </tbody>
  </table>

  <div class="disclaimer">
    <strong>Scientific Disclaimer (Pernyataan Penyangkalan):</strong><br>
    Laporan ini dihasilkan secara in-silico menggunakan model AI Random Forest Regressor dan ditujukan untuk penapisan awal senyawa kandidat obat antidiabetes. Hasil prediksi harus dikonfirmasi melalui pengujian laboratorium basah (in-vitro enzyme assay) sebelum melangkah ke tahap validasi biologis lanjutan.
  </div>
</div>

</body>
</html>
"""
    return html
