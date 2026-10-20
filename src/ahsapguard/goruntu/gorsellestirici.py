from pathlib import Path
import cv2
import numpy as np


def isi_haritasi_olustur(
    orijinal_goruntu_yolu: str,
    anomali_haritasi: np.ndarray,
    cikti_yolu: str = None,
) -> np.ndarray:
    """Anomali haritasını orijinal görüntü boyutuna ölçekler ve renkli ısı haritası olarak üst üste bindirir."""
    # Orijinal görüntüyü BGR olarak oku
    orig_img = cv2.imread(orijinal_goruntu_yolu)
    if orig_img is None:
        raise FileNotFoundError(
            f"Görüntü bulunamadı: {orijinal_goruntu_yolu}"
        )

    h, w, _ = orig_img.shape

    # Anomali haritasını [0, 255] aralığına normalize et
    map_min, map_max = anomali_haritasi.min(), anomali_haritasi.max()
    if map_max - map_min > 0:
        norm_map = (anomali_haritasi - map_min) / (map_max - map_min)
    else:
        norm_map = np.zeros_like(anomali_haritasi)

    norm_map = (norm_map * 255).astype(np.uint8)

    # Orijinal boyuta büyük (Bicubic interpolation)
    resized_map = cv2.resize(norm_map, (w, h), interpolation=cv2.INTER_CUBIC)

    # Renk haritası uygula (JET colormap)
    heatmap = cv2.applyColorMap(resized_map, cv2.COLORMAP_JET)

    # Orijinal resim ile ısı haritasını harmanla (%70 Orijinal + %30 Isı Haritası)
    cikis_resmi = cv2.addWeighted(orig_img, 0.7, heatmap, 0.3, 0)

    if cikti_yolu:
        Path(cikti_yolu).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(cikti_yolu, cikis_resmi)

    return cikis_resmi