from pathlib import Path
import sys

# Kök dizini Python modül arama yoluna ekle
KOK_DIZIN = Path(__file__).resolve().parent.parent
if str(KOK_DIZIN) not in sys.path:
    sys.path.append(str(KOK_DIZIN))

import pytest
from src.ahsapguard.goruntu.isleyici import goruntu_yukle_ve_islemden_gecir
from src.ahsapguard.veri.veri_kontrol import veri_kumesi_kontrol_et


def test_veri_kumesi_yapisi():
    """Veri kümesi klasör yapısının ve görsel varlığının doğrulanması."""
    sonuc = veri_kumesi_kontrol_et("veri/wood")
    assert sonuc["durum"] is True
    assert sonuc["train_good_sayisi"] > 0


def test_gecersiz_goruntu_yolu():
    """Olmayan görüntü dosyasında hata fırlatma kontrolü."""
    with pytest.raises(ValueError):
        goruntu_yukle_ve_islemden_gecir("veri/wood/olmayan_resim.png")