from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def pdf_raporu_olustur(
    orijinal_resim_yolu: str,
    isi_haritasi_yolu: str,
    dosya_adi: str,
    skor: float,
    esik: float,
    durum: str,
    cikti_pdf_yolu: str = "ciktilar/kalite_kontrol_raporu.pdf",
) -> str:
    """Tekil analiz için resmi PDF Kalite Kontrol Raporu üretir."""
    Path(cikti_pdf_yolu).parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(cikti_pdf_yolu, pagesize=letter)

    # Başlık
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "AHSAPGUARD AI --- KALITE KONTROL RAPORU")

    c.setFont("Helvetica", 10)
    c.drawString(50, 735, "Endustriyel Anomali ve Kusur Tespit Sistemi")
    c.line(50, 725, 550, 725)

    # Özet Bilgiler
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 695, "ANALIZ METRIKLERI")

    c.setFont("Helvetica", 10)
    c.drawString(50, 675, f"Gorsel Dosya Adi: {dosya_adi}")
    c.drawString(50, 660, f"Anomali Skoru: {skor:.4f}")
    c.drawString(50, 645, f"Karar Esigi: {esik:.2f}")

    if "ANORMAL" in durum:
        c.setFillColorRGB(0.8, 0.1, 0.1)
    else:
        c.setFillColorRGB(0.1, 0.6, 0.1)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 625, f"KALITE SONUCU: {durum}")

    # Siyah renge dön
    c.setFillColorRGB(0, 0, 0)

    # Resimleri Yan Yana Çizdir
    c.drawString(50, 580, "GORSEL KARSILASTIRMA")
    if Path(orijinal_resim_yolu).exists():
        c.drawImage(
            orijinal_resim_yolu, 50, 360, width=220, height=200, preserveAspectRatio=True
        )
    if Path(isi_haritasi_yolu).exists():
        c.drawImage(
            isi_haritasi_yolu, 290, 360, width=220, height=200, preserveAspectRatio=True
        )

    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 340, "Sol: Orijinal Yuzey | Sag: PatchCore Anomali Isi Haritasi")

    c.line(50, 320, 550, 320)
    c.drawString(50, 300, "AhsapGuard AI Otomatik Sistem Raporudur.")

    c.save()
    return cikti_pdf_yolu