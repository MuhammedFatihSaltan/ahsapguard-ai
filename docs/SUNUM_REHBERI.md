# AhşapGuard AI --- Proje Sunum ve Demo Rehberi

## 🎯 Proje Kısa Özeti (30 Saniyelik Pitch)
AhşapGuard AI; kereste ve ahşap üretim hatlarında insan gözünden kaçabilecek yüzey kusurlarını (çizik, delik, renk değişimi) yapay zekâ ve **PatchCore** anomali tespiti mimarisiyle milisaniyeler içinde tespit eden, anomali ısı haritaları çıkartan ve resmi PDF kalite kontrol raporları üreten endüstriyel bir yazılım sistemidir.

## 🚀 Öne Çıkan Özellikler
1. **Etiketleme Gerektirmez (Unsupervised):** Yalnızca kusursuz ahşap yüzeyleriyle eğitilir, daha önce görülmemiş kusur türlerini tespit eder.
2. **Piksel Düzeyinde Isı Haritası:** Kusurun tam konumunu renkli halkalarla görselleştirir.
3. **Milisaniyelik Çıkarım:** Görsel başına ~0.18 saniye analiz süresi.
4. **Endüstriyel Raporlama:** Otomatik PDF raporu ve CSV veri aktarımı.

## 📹 Demo Senaryosu
1. Web arayüzünü açın (`streamlit run app/arayuz.py`).
2. "Canlı Kalite Kontrol" sekmesinde normal bir ahşap resmi yükleyip analizi başlatın (Normal kararı gösterin).
3. Ardından kusurlu (delik/çizik) bir resim yükleyip analizi başlatın (Kırmızı anomali ısı haritasını ve yüksek skoru gösterin).
4. "📄 PDF Kalite Raporunu İndir" butonuna basarak indirilen resmi belgeyi sunun.