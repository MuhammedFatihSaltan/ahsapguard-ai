import numpy as np
from PIL import Image, ImageDraw
from pathlib import Path


def sentetik_wood_veriseti_olustur(hedef_dizin: str = "veri/wood"):
    """MVTec AD wood formatında tam uyumlu sentetik ahşap veri kümesi üretir."""
    kok = Path(hedef_dizin)
    if kok.exists() and (kok / "train" / "good").exists():
        print(f"[İNF] '{hedef_dizin}' klasörü zaten mevcut.")
        return

    print("[1/2] Sentetik 'wood' veri kümesi oluşturuluyor...")

    # Klasör yapıları
    train_good = kok / "train" / "good"
    test_good = kok / "test" / "good"
    test_scratch = kok / "test" / "scratch"
    test_hole = kok / "test" / "hole"

    gt_scratch = kok / "ground_truth" / "scratch"
    gt_hole = kok / "ground_truth" / "hole"

    for d in [train_good, test_good, test_scratch, test_hole, gt_scratch, gt_hole]:
        d.mkdir(parents=True, exist_ok=True)

    def ahsap_dokusu_ureteci(genislik=256, yukseklik=256):
        # Ahşap dokusu simülasyonu
        base = np.full((yukseklik, genislik, 3), [180, 130, 90], dtype=np.uint8)
        cizgiler = np.sin(np.linspace(0, 20 * np.pi, genislik)) * 15
        base[:, :, 0] = np.clip(base[:, :, 0] + cizgiler, 0, 255)
        base[:, :, 1] = np.clip(base[:, :, 1] + cizgiler, 0, 255)
        return Image.fromarray(base)

    # 1. Train Good (Eğitim - Kusursuz) (20 Görsel)
    for i in range(20):
        img = ahsap_dokusu_ureteci()
        img.save(train_good / f"{i:03d}.png")

    # 2. Test Good (Test - Kusursuz) (5 Görsel)
    for i in range(5):
        img = ahsap_dokusu_ureteci()
        img.save(test_good / f"{i:03d}.png")

    # 3. Test Scratch & Ground Truth (Çizik Kusuru) (5 Görsel)
    for i in range(5):
        img = ahsap_dokusu_ureteci()
        mask = Image.new("L", (256, 256), 0)
        
        draw_img = ImageDraw.Draw(img)
        draw_mask = ImageDraw.Draw(mask)
        
        # Çizik ekle
        draw_img.line([(50, 50), (200, 200)], fill=(50, 30, 10), width=4)
        draw_mask.line([(50, 50), (200, 200)], fill=255, width=4)
        
        img.save(test_scratch / f"{i:03d}.png")
        mask.save(gt_scratch / f"{i:03d}_mask.png")

    # 4. Test Hole & Ground Truth (Delik Kusuru) (5 Görsel)
    for i in range(5):
        img = ahsap_dokusu_ureteci()
        mask = Image.new("L", (256, 256), 0)
        
        draw_img = ImageDraw.Draw(img)
        draw_mask = ImageDraw.Draw(mask)
        
        # Delik ekle
        draw_img.ellipse([(100, 100), (140, 140)], fill=(20, 10, 5))
        draw_mask.ellipse([(100, 100), (140, 140)], fill=255)
        
        img.save(test_hole / f"{i:03d}.png")
        mask.save(gt_hole / f"{i:03d}_mask.png")

    print("[2/2] Sentetik MVTec AD 'wood' veri kümesi başarıyla oluşturuldu!\n")


if __name__ == "__main__":
    sentetik_wood_veriseti_olustur()