from pathlib import Path
import sys

# Proje kök dizinini Python yoluna ekle
KOK_DIZIN = Path(__file__).resolve().parent.parent
if str(KOK_DIZIN) not in sys.path:
    sys.path.append(str(KOK_DIZIN))

import os
import time
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st

from src.ahsapguard.goruntu.gorsellestirici import isi_haritasi_olustur
from src.ahsapguard.model.patchcore import PatchCoreModel
from src.ahsapguard.raporlama.gecmis_yonetici import AnalizGecmisYonetici
from src.ahsapguard.raporlama.pdf_ureteci import pdf_raporu_olustur

st.set_page_config(
    page_title="AhşapGuard AI --- Kalite Kontrol Sistemi",
    page_icon="🪵",
    layout="wide",
)


@st.cache_resource
def modeli_yukle_ve_egit():
    model = PatchCoreModel(coreset_orani=0.2)
    model.egit("veri/wood/train/good")
    return model


gecmis_db = AnalizGecmisYonetici()

st.title("🪵 AhşapGuard AI --- Endüstriyel Anomali Tespiti")
st.markdown(
    "Yapay zekâ ve **PatchCore** mimarisi ile ahşap/kereste yüzeylerindeki otomatik kusur ve anomali tespiti."
)
st.divider()

# Sekmeli Yapı
sekme1, sekme2 = st.tabs(["🔍 Canlı Kalite Kontrol", "📜 Analiz Geçmişi & Raporlar"])

with sekme1:
    st.sidebar.header("⚙️ Ayarlar")
    karar_esigi = st.sidebar.slider(
        "Karar Eşiği (Anomali Skoru)", 1.0, 10.0, 2.5, 0.1
    )

    with st.spinner("Model yükleniyor..."):
        model = modeli_yukle_ve_egit()

    yuklenen_dosya = st.file_uploader(
        "Görüntü Yükleyin (PNG, JPG)", type=["png", "jpg", "jpeg"]
    )

    if yuklenen_dosya is not None:
        gecici_dizin = Path("ciktilar/gecici")
        gecici_dizin.mkdir(parents=True, exist_ok=True)
        gecici_yol = gecici_dizin / yuklenen_dosya.name

        with open(gecici_yol, "wb") as f:
            f.write(yuklenen_dosya.getbuffer())

        dosya_stem = Path(yuklenen_dosya.name).stem

        col1, col2 = st.columns(2)
        with col1:
            st.image(
                Image.open(gecici_yol),
                use_container_width=True,
                caption="Orijinal Yüzey",
            )

        if st.button("🔍 Analizi Başlat", type="primary"):
            baslangic = time.time()
            sonuc = model.tahmin_et(str(gecici_yol))
            sure = time.time() - baslangic

            skor = sonuc["anomali_skoru"]
            harita = sonuc["anomali_haritasi"]

            isi_yolu = f"ciktilar/gecici/{dosya_stem}_heatmap.png"
            isi_haritasi_img = isi_haritasi_olustur(
                str(gecici_yol), harita, cikti_yolu=isi_yolu
            )
            isi_haritasi_rgb = cv2.cvtColor(isi_haritasi_img, cv2.COLOR_BGR2RGB)

            with col2:
                st.image(
                    isi_haritasi_rgb,
                    use_container_width=True,
                    caption="Anomali Isı Haritası",
                )

            durum_metni = (
                "ANORMAL / KUSURLU" if skor >= karar_esigi else "NORMAL / KUSURSUZ"
            )

            # Geçmişe Kaydet
            gecmis_db.kayit_ekle(
                yuklenen_dosya.name, skor, karar_esigi, durum_metni, sure
            )

            st.divider()
            if skor >= karar_esigi:
                st.error(f"🚨 **SONUÇ: {durum_metni}** (Skor: {skor:.4f})")
            else:
                st.success(f"✅ **SONUÇ: {durum_metni}** (Skor: {skor:.4f})")

            # PDF Oluşturma ve İndirme
            pdf_yolu = f"ciktilar/gecici/{dosya_stem}_rapor.pdf"
            pdf_raporu_olustur(
                str(gecici_yol),
                isi_yolu,
                yuklenen_dosya.name,
                skor,
                karar_esigi,
                durum_metni,
                cikti_pdf_yolu=pdf_yolu,
            )

            with open(pdf_yolu, "rb") as f:
                st.download_button(
                    "📄 PDF Kalite Raporunu İndir",
                    f,
                    file_name=f"Kalite_Raporu_{dosya_stem}.pdf",
                    mime="application/pdf",
                )

with sekme2:
    st.subheader("📊 Analiz Geçmişi Dökümü")
    gecmis_listesi = gecmis_db.gecmisi_getir()
    if gecmis_listesi:
        df = pd.DataFrame(gecmis_listesi)
        st.dataframe(df, use_container_width=True)

        # CSV İndirme
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Tüm Geçmişi CSV Olarak İndir",
            csv_data,
            "analiz_gecmisi.csv",
            "text/csv",
        )
    else:
        st.info("Henüz kaydedilmiş analiz geçmişi bulunmamaktadır.")