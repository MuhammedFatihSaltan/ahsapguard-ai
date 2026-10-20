from pathlib import Path


def veri_kumesi_kontrol_et(veri_yolu: str = "veri/wood") -> dict:
    """MVTec AD wood veri kümesinin varlığını ve klasör yapısını doğrulayarak

    görüntü sayılarını raporlar.
    """
    kok_dizin = Path(veri_yolu)

    if not kok_dizin.exists():
        return {
            "durum": False,
            "mesaj": f"HATA: Veri kümesi dizini bulunamadı: '{kok_dizin.resolve()}'",
        }

    train_dizin = kok_dizin / "train" / "good"
    test_dizin = kok_dizin / "test"
    gt_dizin = kok_dizin / "ground_truth"

    if not train_dizin.exists():
        return {
            "durum": False,
            "mesaj": f"HATA: Eğitim klasörü bulunamadı: '{train_dizin}'",
        }

    # Eğitim resimlerini say
    train_resimler = list(train_dizin.glob("*.png"))

    # Test alt klasörlerini ve resimlerini say
    test_ozet = {}
    if test_dizin.exists():
        for alt_klasor in test_dizin.iterdir():
            if alt_klasor.is_dir():
                resimler = list(alt_klasor.glob("*.png"))
                test_ozet[alt_klasor.name] = len(resimler)

    # Ground truth alt klasörlerini ve maskelerini say
    gt_ozet = {}
    if gt_dizin.exists():
        for alt_klasor in gt_dizin.iterdir():
            if alt_klasor.is_dir():
                maskeler = list(alt_klasor.glob("*.png"))
                gt_ozet[alt_klasor.name] = len(maskeler)

    return {
        "durum": True,
        "mesaj": "Veri kümesi yapısı başarıyla doğrulandı.",
        "train_good_sayisi": len(train_resimler),
        "test_kategorileri": test_ozet,
        "ground_truth_kategorileri": gt_ozet,
    }


if __name__ == "__main__":
    sonuc = veri_kumesi_kontrol_et()
    print("=" * 50)
    print(sonuc["mesaj"])
    print("=" * 50)

    if sonuc["durum"]:
        print(f"Eğitim Görüntü Sayısı (good): {sonuc['train_good_sayisi']}")
        print("\nTest Görüntü Sayıları:")
        for kat, sayi in sonuc["test_kategorileri"].items():
            print(f"  - {kat}: {sayi}")
        print("\nGround Truth Maske Sayıları:")
        for kat, sayi in sonuc["ground_truth_kategorileri"].items():
            print(f"  - {kat}: {sayi}")