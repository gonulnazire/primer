"""Primer v2 — TEST KAHİNİ (oracle) ve parite denetimi.

Diferansiyel testin Python tarafı. Aynı `model/model.onnx`'i çalıştırır ve beş
referans girdi için olasılıkları üretir; Cypress bu değerleri tarayıcıdaki
onnxruntime-web çıkarımıyla karşılaştırır (spec.md AC12, tolerans 1e-4).

İki kip:
    python tests/parite.py --yaz   # referans olasılıkları yeniden üretir
    python tests/parite.py         # kayıtlı değerlerle tutarlılığı denetler

Neden "kahin": iki bağımsız uygulamanın (Python onnxruntime ve tarayıcıdaki
onnxruntime-web) aynı girdide aynı cevabı vermesi, tek bir uygulamanın kendi
kendini test etmesinden farklı bir şey kanıtlar — sözleşmenin uygulamadan
bağımsız olduğunu. Birinde özellik sırası kayarsa veya tip dönüşümü bozulursa
tek taraflı test bunu göremez; parite testi görür.

`parite.json` modelin sha256'sını da taşır: model yeniden eğitilip referans
dosyası güncellenmezse bu betik DURUR. Sessizce bayat referansla karşılaştırmak,
test etmemekten daha kötüdür.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import onnxruntime as ort

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from sozlesme import OZELLIKLER  # noqa: E402

MODEL = KOK / "model" / "model.onnx"
CONFIG = KOK / "model" / "config.json"
REFERANS = Path(__file__).resolve().parent / "parite.json"
TOLERANS = 1e-4

# Beş referans girdi. Uç ve orta durumları birlikte örnekliyorlar; ikisi eylem
# eşiğinin (0.60) üstünde, ikisi altında, biri sınırda olacak şekilde seçildi —
# parite testi yalnız "aynı sayı mı" demekle kalmayıp eşiğin iki yanını da
# kapsamalı.
GIRDILER = [
    {
        "aciklama": "1. karar noktası, 1-2. sınıf, geçmiş yok — taban oran",
        "sahne_no": 1, "sinif_kodu": 0,
        "onceki_karar_suresi_sn": 0.0, "onceki_okuma_orani": 0.0,
        "onceki_refleks_sayisi": 0, "oturum_gecen_sure_sn": 0.4,
    },
    {
        "aciklama": "2. karar noktası, önceki karar hızlı ve okunmamış — refleks eğilimi",
        "sahne_no": 2, "sinif_kodu": 0,
        "onceki_karar_suresi_sn": 2.1, "onceki_okuma_orani": 0.12,
        "onceki_refleks_sayisi": 1, "oturum_gecen_sure_sn": 4.0,
    },
    {
        "aciklama": "2. karar noktası, önceki karar yavaş ve okunmuş — düşünerek eğilimi",
        "sahne_no": 2, "sinif_kodu": 1,
        "onceki_karar_suresi_sn": 24.5, "onceki_okuma_orani": 1.0,
        "onceki_refleks_sayisi": 0, "oturum_gecen_sure_sn": 27.0,
    },
    {
        "aciklama": "3. karar noktası, iki refleks karar arkasında — en yüksek olasılık",
        "sahne_no": 3, "sinif_kodu": 0,
        "onceki_karar_suresi_sn": 1.4, "onceki_okuma_orani": 0.05,
        "onceki_refleks_sayisi": 2, "oturum_gecen_sure_sn": 9.5,
    },
    {
        "aciklama": "3. karar noktası, iki dikkatli karar ve uzun oturum — en düşük olasılık",
        "sahne_no": 3, "sinif_kodu": 1,
        "onceki_karar_suresi_sn": 18.0, "onceki_okuma_orani": 0.95,
        "onceki_refleks_sayisi": 0, "oturum_gecen_sure_sn": 61.0,
    },
]


def model_sha256() -> str:
    return hashlib.sha256(MODEL.read_bytes()).hexdigest()


def kahin_olasiliklari(girdiler: list[dict]) -> list[float]:
    """model.onnx'i Python onnxruntime ile çalıştırır."""
    if not MODEL.exists():
        raise SystemExit(f"HATA: {MODEL} yok. Önce: python train.py")

    oturum = ort.InferenceSession(str(MODEL), providers=["CPUExecutionProvider"])
    girdi_adi = oturum.get_inputs()[0].name
    cikti_adlari = [c.name for c in oturum.get_outputs()]
    olasilik_adi = next((a for a in cikti_adlari if "probab" in a.lower()), cikti_adlari[-1])

    # Özellik sırası SÖZLEŞMEDEN okunur, girdi sözlüğünün anahtar sırasından
    # değil. Sözlük sırasına güvenmek, sözleşmeyi sessizce kaybetmenin yoludur.
    X = np.array(
        [[float(g[ad]) for ad in OZELLIKLER] for g in girdiler],
        dtype=np.float32,
    )

    cikti = oturum.run([olasilik_adi], {girdi_adi: X})[0]
    olasilik = np.asarray(cikti)
    if olasilik.ndim != 2 or olasilik.shape[1] < 2:
        raise SystemExit(
            f"HATA: olasılık çıktısı beklenen biçimde değil: {olasilik.shape}"
        )
    return [float(p) for p in olasilik[:, 1]]


def yaz() -> None:
    olasiliklar = kahin_olasiliklari(GIRDILER)
    surum = "?"
    if CONFIG.exists():
        surum = json.loads(CONFIG.read_text(encoding="utf-8")).get("surum", "?")

    icerik = {
        "_aciklama": "Diferansiyel test referansı. p_kahin değerleri Python "
                     "onnxruntime ile üretildi; tarayıcı çıkarımı bunlardan "
                     "en çok 'tolerans' kadar sapabilir (spec.md AC12).",
        "model": {
            "dosya": "model/model.onnx",
            "sha256": model_sha256(),
            "surum": surum,
        },
        "tolerans": TOLERANS,
        "ozellikler": OZELLIKLER,
        "girdiler": [
            {**g, "p_kahin": round(p, 9)} for g, p in zip(GIRDILER, olasiliklar)
        ],
    }

    REFERANS.write_text(
        json.dumps(icerik, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"yazıldı: tests/{REFERANS.name}  ({len(GIRDILER)} girdi)")
    for g, p in zip(GIRDILER, olasiliklar):
        print(f"  p={p:.6f}  {g['aciklama']}")


def denetle() -> None:
    if not REFERANS.exists():
        raise SystemExit(
            f"HATA: {REFERANS} yok. Önce: python tests/parite.py --yaz"
        )

    kayit = json.loads(REFERANS.read_text(encoding="utf-8"))

    # 1) Model değişmiş mi?
    simdiki = model_sha256()
    kayitli = kayit.get("model", {}).get("sha256")
    if kayitli != simdiki:
        raise SystemExit(
            "HATA: model.onnx referans dosyasındakinden farklı.\n"
            f"  kayıtlı : {kayitli}\n"
            f"  şimdiki : {simdiki}\n"
            "Model yeniden eğitildiyse referansı yenile: python tests/parite.py --yaz"
        )

    # 2) Özellik sırası değişmiş mi?
    if kayit.get("ozellikler") != OZELLIKLER:
        raise SystemExit(
            "HATA: özellik sırası sözleşmeden farklı.\n"
            f"  kayıtlı : {kayit.get('ozellikler')}\n"
            f"  sözleşme: {OZELLIKLER}"
        )

    # 3) Kahin aynı sayıyı veriyor mu?
    girdiler = kayit["girdiler"]
    tolerans = float(kayit.get("tolerans", TOLERANS))
    yeniden = kahin_olasiliklari(girdiler)

    en_buyuk = 0.0
    basarisiz = []
    for i, (g, p) in enumerate(zip(girdiler, yeniden)):
        fark = abs(p - float(g["p_kahin"]))
        en_buyuk = max(en_buyuk, fark)
        durum = "ok" if fark < tolerans else "BAŞARISIZ"
        if fark >= tolerans:
            basarisiz.append((i, g["p_kahin"], p, fark))
        print(f"  [{durum}] girdi {i + 1}: kayıtlı {float(g['p_kahin']):.6f} · "
              f"şimdiki {p:.6f} · fark {fark:.2e}")

    print(f"\nen büyük fark: {en_buyuk:.3e}  (tolerans {tolerans:.0e})")

    if basarisiz:
        print(f"PARİTE BAŞARISIZ: {len(basarisiz)} girdi toleransı aştı", file=sys.stderr)
        raise SystemExit(1)

    print("PARİTE OK — kahin kayıtlı değerlerle tutarlı")


def main() -> None:
    ap = argparse.ArgumentParser(description="Primer v2 parite (diferansiyel test) kahini")
    ap.add_argument("--yaz", action="store_true",
                    help="referans olasılıkları yeniden üret (model değiştiyse)")
    a = ap.parse_args()

    if a.yaz:
        yaz()
    else:
        denetle()


if __name__ == "__main__":
    main()
