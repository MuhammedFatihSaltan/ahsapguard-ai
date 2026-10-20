from pathlib import Path
import numpy as np
from sklearn.neighbors import NearestNeighbors
import torch
import torch.nn as nn
from torchvision.models import ResNet18_Weights, resnet18

from src.ahsapguard.goruntu.isleyici import goruntu_yukle_ve_islemden_gecir


class PatchCoreModel:
    """Ahşap ve kereste yüzeyleri için PatchCore tabanlı anomali tespit sınıfı."""

    def __init__(self, coreset_orani: float = 0.2):
        self.coreset_orani = coreset_orani
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        # Ön eğitimli ResNet18 omurgası
        backbone = resnet18(weights=ResNet18_Weights.DEFAULT)
        self.feature_extractor = nn.Sequential(
            backbone.conv1,
            backbone.bn1,
            backbone.relu,
            backbone.maxpool,
            backbone.layer1,
            backbone.layer2,
            backbone.layer3,  # Orta seviye görsel öznitelikler
        ).to(self.device)
        self.feature_extractor.eval()

        self.memory_bank = None
        self.nn_search = None

    def _oznitelik_cikart(self, x: torch.Tensor) -> np.ndarray:
        """Görüntüden lokal yamaların (patch) öznitelik vektörlerini çıkartır."""
        with torch.no_grad():
            features = self.feature_extractor(x.to(self.device))

        b, c, h, w = features.shape
        features = features.permute(0, 2, 3, 1).reshape(-1, c)
        return features.cpu().numpy()

    def egit(self, egitim_klasoru: str):
        """Kusursuz eğitim görsellerini analiz ederek Memory Bank oluşturur."""
        klasor = Path(egitim_klasoru)
        gorseller = list(klasor.glob("*.png")) + list(klasor.glob("*.jpg"))

        if not gorseller:
            raise FileNotFoundError(
                f"Eğitim klasöründe görsel bulunamadı: {egitim_klasoru}"
            )

        tum_yamalar = []
        for g_yolu in gorseller:
            tensor_img = goruntu_yukle_ve_islemden_gecir(str(g_yolu))
            yamalar = self._oznitelik_cikart(tensor_img)
            tum_yamalar.append(yamalar)

        self.memory_bank = np.vstack(tum_yamalar)

        # CoreSet örnekleme
        if self.coreset_orani < 1.0:
            secilecek_sayi = int(len(self.memory_bank) * self.coreset_orani)
            indices = np.random.choice(
                len(self.memory_bank),
                size=max(50, secilecek_sayi),
                replace=False,
            )
            self.memory_bank = self.memory_bank[indices]

        # En yakın komşu arama indeksini kur
        self.nn_search = NearestNeighbors(n_neighbors=1, metric="minkowski")
        self.nn_search.fit(self.memory_bank)
        print(
            f"✅ Model Eğitildi. Memory Bank yama sayısı: {len(self.memory_bank)}"
        )

    def tahmin_et(self, goruntu_yolu: str) -> dict:
        """Test görseli üzerinde anomali skoru ve haritası hesaplar."""
        if self.memory_bank is None or self.nn_search is None:
            raise RuntimeError(
                "Model henüz eğitilmedi! Önce egit() metodunu çağırın."
            )

        tensor_img = goruntu_yukle_ve_islemden_gecir(goruntu_yolu)
        test_yamalari = self._oznitelik_cikart(tensor_img)

        # En yakın kusursuz yamaya olan mesafeleri bul
        mesafeler, _ = self.nn_search.kneighbors(test_yamalari)

        # Anomali skoru (en yüksek 5 yama mesafesinin ortalaması)
        anomali_skoru = float(np.mean(np.sort(mesafeler.flatten())[-5:]))

        anomali_haritasi = mesafeler.reshape(14, 14)

        return {
            "goruntu_yolu": goruntu_yolu,
            "anomali_skoru": anomali_skoru,
            "anomali_haritasi": anomali_haritasi,
        }


if __name__ == "__main__":
    print("PatchCore model testi başlatılıyor...")
    model = PatchCoreModel(coreset_orani=0.2)
    model.egit("veri/wood/train/good")

    # Normal ve anormal iki test resmi üzerinde çıkarım testi
    normal_test = model.tahmin_et("veri/wood/test/good/000.png")
    anormal_test = model.tahmin_et("veri/wood/test/hole/000.png")

    print(f"\n[Normal Görsel] Anomali Skoru: {normal_test['anomali_skoru']:.4f}")
    print(
        f"[Anormal Görsel - Delik] Anomali Skoru: {anormal_test['anomali_skoru']:.4f}"
    )