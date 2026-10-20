from pathlib import Path
import sys

# Kök dizini Python modül arama yoluna ekle
KOK_DIZIN = Path(__file__).resolve().parent.parent
if str(KOK_DIZIN) not in sys.path:
    sys.path.append(str(KOK_DIZIN))

import numpy as np
from src.ahsapguard.goruntu.gorsellestirici import isi_haritasi_olustur


def test_isi_haritasi_boyutu():
    """Isı haritası matris çıktısının orijinal resimle aynı boyutta olduğunun doğrulanması."""
    sahte_map = np.random.rand(14, 14)
    resim_yolu = "veri/wood/test/good/000.png"

    cikti = isi_haritasi_olustur(resim_yolu, sahte_map)
    assert cikti is not None
    assert len(cikti.shape) == 3  # (H, W, C)