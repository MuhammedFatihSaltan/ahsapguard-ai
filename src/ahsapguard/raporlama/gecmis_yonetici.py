from datetime import datetime
import json
from pathlib import Path
import pandas as pd


class AnalizGecmisYonetici:
    """Kalite kontrol analiz sonuçlarını saklar, CSV ve JSON olarak dışa aktarır."""

    def __init__(self, kayit_dosyasi: str = "ciktilar/analiz_gecmisi.json"):
        self.kayit_dosyasi = Path(kayit_dosyasi)
        self.kayit_dosyasi.parent.mkdir(parents=True, exist_ok=True)
        if not self.kayit_dosyasi.exists():
            with open(self.kayit_dosyasi, "w", encoding="utf-8") as f:
                json.dump([], f)

    def kayit_ekle(
        self, dosya_adi: str, skor: float, esik: float, durum: str, sure: float
    ):
        yeni_kayit = {
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dosya_adi": dosya_adi,
            "anomali_skoru": round(skor, 4),
            "karar_esigi": round(esik, 2),
            "durum": durum,
            "analiz_suresi_saniye": round(sure, 3),
        }

        with open(self.kayit_dosyasi, "r", encoding="utf-8") as f:
            gecmis = json.load(f)

        gecmis.append(yeni_kayit)

        with open(self.kayit_dosyasi, "w", encoding="utf-8") as f:
            json.dump(gecmis, f, ensure_ascii=False, indent=2)

    def gecmisi_getir(self) -> list:
        with open(self.kayit_dosyasi, "r", encoding="utf-8") as f:
            return json.load(f)

    def csv_donustur(self) -> bytes:
        with open(self.kayit_dosyasi, "r", encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        return df.to_csv(index=False).encode("utf-8")