# AhşapGuard AI --- Model Değerlendirme Raporu

## 🎯 Değerlendirme Yöntemi
PatchCore modeli MVTec AD `wood` kategorisi test seti üzerinde değerlendirilmiştir.

- **Eğitim Seti:** 20 Adet Kusursuz (`good`) Ahşap Görseli
- **Test Seti:** 15 Adet Görsel (Kusursuz, Delik, Çizik)
- **Metrik:** Görüntü Düzeyinde AUROC (Area Under ROC Curve)

## 📊 Performans Sonuçları
- **Görüntü Düzeyinde AUROC:** 1.0000 (%100 Başarı)
- **Ortalama Çıkarım Süresi:** ~0.15 saniye/görsel (CPU ortamında)

## 🔍 Görselleştirme
Model tarafından üretilen piksel düzeyindeki anomali skor matrisleri JET colormap ile ısı haritasına dönüştürülmüş ve `ciktilar/` dizinine kaydedilmiştir.