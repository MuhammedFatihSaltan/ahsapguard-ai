# AhşapGuard AI --- Geliştirme Günlüğü

Bu belge, proje boyunca tamamlanan aşamaları, çalıştırılan komutları, alınan test sonuçlarını ve karşılaşılan sorunları kronolojik olarak kaydeder.

---

## [Aşama 0] --- Ortam ve GitHub Hazırlığı

- **Tarih:** 2026-10-20
- **Durum:** Devam Ediyor / Doğrulama Bekleniyor

### Yapılan İşlemler
1. GitHub üzerinde `ahsapguard-ai` deposu oluşturuldu.
2. Yerel geliştirme ortamında Python 3.11.9 ve Git 2.47.1 sürümleri kontrol edildi.
3. `D:\ahsapguard-ai` proje klasör yapısı ve modül dizinleri oluşturuldu.
4. `.venv` Python sanal ortamı kuruldu ve aktif edildi.
5. Veri setlerinin ve model ağırlıklarının Git'e yüklenmesini engelleyen `.gitignore` yapılandırıldı.
6. Başlangıç geliştirme günlüğü oluşturuldu.

## [Aşama 1] --- Veri Kümesi Hazırlığı

- **Tarih:** 2026-10-20
- **Durum:** Tamamlandı

### Yapılan İşlemler
1. `src/ahsapguard/veri/veri_indir.py` ile MVTec AD `wood` yapısında veri hazırlama altyapısı kuruldu.
2. `src/ahsapguard/veri/veri_kontrol.py` yazılarak veri kümesi klasör yapısı ve görsel sayıları doğrulandı.
3. `docs/VERI_KUMESI.md` teknik dokümantasyonu oluşturuldu.
4. Veri kümesinin test ve doğrulama aşamaları başarıyla tamamlandı.

## [Aşama 2] --- Model Ortamı ve İlk Tahmin

- **Tarih:** 2026-10-20
- **Durum:** Tamamlandı

### Yapılan İşlemler
1. PyTorch, torchvision, scikit-learn ve görüntü işleme kütüphaneleri yüklendi.
2. `src/ahsapguard/goruntu/isleyici.py` modülü ile ImageNet uyumlu görüntü dönüşüm hattı kuruldu.
3. `src/ahsapguard/model/patchcore.py` modülü ile PatchCore anomali tespit mimarisi yazıldı.
4. Normal görsel (0.5389) ve kusurlu delik görseli (6.7080) skorları başarıyla elde edildi.

## [Aşama 3] --- Görselleştirme ve Değerlendirme

- **Tarih:** 2026-10-20
- **Durum:** Tamamlandı

### Yapılan İşlemler
1. `src/ahsapguard/goruntu/gorsellestirici.py` modülü yazılarak OpenCV JET renk haritası ile anomali görselleştirmesi sağlandı.
2. `src/ahsapguard/degerlendirme/degerlendirici.py` yazılarak test seti üzerinde toplu çıkarım ve AUROC hesabı yapıldı.
3. Görüntü düzeyinde AUROC skoru 1.0000 olarak ölçüldü ve `ciktilar/` dizinine ısı haritaları aktarıldı.
4. `docs/MODEL_DEGERLENDIRME.md` teknik dokümanı oluşturuldu.

## [Aşama 4] --- Web Uygulaması (Streamlit)

- **Tarih:** 2026-10-20
- **Durum:** Tamamlandı

### Yapılan İşlemler
1. Streamlit web çatısı projeye dahil edildi.
2. `app/arayuz.py` modülü geliştirilerek kullanıcı dostu kalite kontrol arayüzü sunuldu.
3. Model yükleme süreci `@st.cache_resource` ile optimize edildi.
4. `docs/KULLANIM_KILAVUZU.md` oluşturuldu.