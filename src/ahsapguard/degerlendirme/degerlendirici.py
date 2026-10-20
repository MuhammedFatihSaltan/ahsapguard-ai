from pathlib import Path
import numpy as np
from sklearn.metrics import roc_auc_score

from src.ahsapguard.goruntu.gorsellestirici import isi_haritasi_olustur
from src.ahsapguard.model.patchcore import PatchCoreModel


def modeli_degerlendir(
    veri_yolu: str = "veri/wood", cikti_klasoru: str = "ciktilar"
):
    """Tüm test veri kümesini analiz eder, AUROC metriğini hesaplar ve görsel çıktıları kaydeder."""
    print("=" * 60)
    print("AHŞAPGUARD AI --- MODEL PERFORMANS DEĞERLENDİRMESİ")
    print("=" * 60)

    model = PatchCoreModel(coreset_orani=0.2)
    model.egit(f"{veri_yolu}/train/good")

    test_dizin = Path(veri_yolu) / "test"

    gercek_etiketler = []  # 0: Normal, 1: Anormal
    tahmin_skorlari = []

    goruntu_sayaci = 0

    for kat in test_dizin.iterdir():
        if not kat.is_dir():
            continue

        is_anomalous = 0 if kat.name == "good" else 1

        for g_yolu in kat.glob("*.png"):
            sonuc = model.tahmin_et(str(g_yolu))

            gercek_etiketler.append(is_anomalous)
            tahmin_skorlari.append(sonuc["anomali_skoru"])

            # Isı haritası görselleştirmesini ciktilar/ klasörüne kaydet
            kayit_yolu = (
                f"{cikti_klasoru}/{kat.name}_{g_yolu.stem}_heatmap.png"
            )
            isi_haritasi_olustur(
                str(g_yolu), sonuc["anomali_haritasi"], cikti_yolu=kayit_yolu
            )

            goruntu_sayaci += 1

    # AUROC Metriği Hesaplama
    auroc = roc_auc_score(gercek_etiketler, tahmin_skorlari)

    print(f"\n📊 Toplam Analiz Edilen Test Görseli: {goruntu_sayaci}")
    print(f"🎯 Görüntü Düzeyinde AUROC Skoru: {auroc:.4f}")
    print(f"📁 Isı haritaları '{cikti_klasoru}/' klasörüne kaydedildi.\n")

    return {"toplam_test": goruntu_sayaci, "auroc": auroc}


if __name__ == "__main__":
    modeli_degerlendir()