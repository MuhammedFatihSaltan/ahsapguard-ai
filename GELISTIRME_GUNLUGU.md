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