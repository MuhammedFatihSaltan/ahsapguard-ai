from pathlib import Path
import sys

# Proje kök dizinini Python modül arama yoluna ekle
KOK_DIZIN = Path(__file__).resolve().parent.parent
if str(KOK_DIZIN) not in sys.path:
    sys.path.append(str(KOK_DIZIN))

import os
import time
import cv2
import numpy as np
from PIL import Image
import streamlit as st

from src.ahsapguard.goruntu.gorsellestirici import isi_haritasi_olustur
from src.ahsapguard.model.patchcore import PatchCoreModel

# Sayfa Yapılandırması
st.set_page_config(
    page_title="AhşapGuard AI --- Kalite Kontrol Sistemi",
    page_icon="🪵",
    layout="wide",
)


@st.cache_resource
def modeli_yukle_ve_egit():
    """Modeli bir kez yükler ve ön belleğe alır."""
    model = PatchCoreModel(coreset_orani=0.2)
    model.egit("veri/wood/train/good")
    return model


st.title("🪵 AhşapGuard AI --- Endüstriyel Anomali Tespiti")
st.markdown(
    "Yapay zekâ ve **PatchCore** mimarisi ile ahşap/kereste yüzeylerindeki otomatik kusur ve anomali tespiti."
)
st.divider()

# Yan Menü (Sidebar)
st.sidebar.header("⚙️ Ayarlar ve Bilgiler")
karar_esigi = st.sidebar.slider(
    "Karar Eşiği (Anomali Skoru)",
    min_value=1.0,
    max_value=10.0,
    value=2.5,
    step=0.1,
    help="Bu eşiğin üzerindeki skorlar 'ANORMAL / KUSURLU' olarak sınıflandırılır.",
)

st.sidebar.info(
    "💡 **Skor Açıklaması:** Anomali skoru bir yüzde değildir. Modelin Memory Bank'teki kusursuz ahşap yama özniteliklerine olan mesafesini ifade eder."
)

# Model Eğitimi Yüklemesi
with st.spinner("Model hazırlanıyor ve eğitiliyor..."):
    model = modeli_yukle_ve_egit()

st.success("✅ Model hazır! Analiz etmek istediğiniz ahşap görselini yükleyin.")

# Görüntü Yükleme Alanı
yuklenen_dosya = st.file_uploader(
    "Görüntü seçin veya sürükleyip bırakın (PNG, JPG, JPEG)",
    type=["png", "jpg", "jpeg"],
)

if yuklenen_dosya is not None:
    # Geçici kaydetme
    gecici_dizin = Path("ciktilar/gecici")
    gecici_dizin.mkdir(parents=True, exist_ok=True)
    gecici_yol = gecici_dizin / yuklenen_dosya.name

    with open(gecici_yol, "wb") as f:
        f.write(yuklenen_dosya.getbuffer())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🖼️ Yüklenen Orijinal Görüntü")
        st.image(
            Image.open(gecici_yol),
            use_column_width=True,
            caption=f"Dosya: {yuklenen_dosya.name}",
        )

    if st.button("🔍 Analizi Başlat", type="primary"):
        baslangic = time.time()
        with st.spinner("Yüzey taranıyor ve anomali haritası çıkarılıyor..."):
            sonuc = model.tahmin_et(str(gecici_yol))
            sure = time.time() - baslangic

            skor = sonuc["anomali_skoru"]
            harita = sonuc["anomali_haritasi"]

            isi_haritasi_img = isi_haritasi_olustur(str(gecici_yol), harita)
            # BGR -> RGB dönüşümü Streamlit için
            isi_haritasi_rgb = cv2.cvtColor(isi_haritasi_img, cv2.COLOR_BGR2RGB)

        with col2:
            st.subheader("🔥 Anomali Isı Haritası")
            st.image(
                isi_haritasi_rgb,
                use_column_width=True,
                caption="Kırmızı/Sarı bölgeler anomali yoğunluğunu gösterir.",
            )

        st.divider()
        st.subheader("📊 Analiz Sonucu")

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Anomali Skoru", f"{skor:.4f}")
        metric_col2.metric("Karar Eşiği", f"{karar_esigi:.1f}")
        metric_col3.metric("Analiz Süresi", f"{sure:.3f} saniye")

        if skor >= karar_esigi:
            st.error(
                f"🚨 **SONUÇ: ANORMAL / KUSURLU YÜZEY DETEKTEDİ**\n\nAnomali skoru ({skor:.4f}) belirlenen karar eşiğinin ({karar_esigi}) üzerindedir."
            )
        else:
            st.success(
                f"✅ **SONUÇ: NORMAL / KUSURSUZ YÜZEY**\n\nAnomali skoru ({skor:.4f}) karar eşiğinin ({karar_esigi}) altındadır."
            )