"""Primer v2 — veri derleme: gerçek oturumlar + sentetik takviye -> data/oturumlar.csv

Tek komut:
    python data/veri_derle.py --sentetik 60

Ne yapar:
  1. `data/ham/` altındaki gerçek CSV'leri okur (uygulamadan indirilen dosyalar).
  2. Sabit tohumla sentetik satır üretir (`kaynak=sentetik`).
  3. İkisini birleştirir, SÖZLEŞMEYİ DOĞRULAR (sütunlar, etiket tutarlılığı, KVKK).
  4. `data/oturumlar.csv` yazar ve özet basar.

Neden ayrı bir "sadece üret" betiği değil: gerçek ve sentetik satırların aynı
şemada, aynı ölçekte ve aynı etiket kuralıyla durduğunu garanti eden yer tek
olmalı. İki ayrı betik olsaydı ikisinin şeması sessizce ayrışabilirdi.

SENTETİK VERİ ÜRETİCİ KURALI (README.md'de de yazılı):
  - Her sentetik "kişi"nin bir `dikkat` tabanı var (Beta(2.2, 2.0)); oturum
    başına bu tabana gürültü eklenir. Dikkat, metnin ekranda görünür kaldığı
    süreyi belirler.
  - Sahne ilerledikçe %12 yorgunluk düşüşü uygulanır.
  - `acele` çarpanı lognormal(0, 0.35) — aynı kişinin oturumları arasındaki
    dalgalanma.
  - Karar süresi = görünür süre + Exp(1.2) (okuma dışı karar verme payı).
  - Etiket, GERÇEK veriyle aynı fonksiyondan geçer: sozlesme.refleks_mi().
  - Seçenek etiketi refleks kararlarda daha sık `riskli` çıkar; bu bir özellik
    değil, yalnız veriyi gerçekçi tutmak için.

Tohum varsayılan 42; `--tohum` ile değiştirilebilir ama teslimde 42 kullanıldı.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sozlesme import (  # noqa: E402
    HEDEFLER,
    OZELLIKLER,
    ROLLER,
    SENARYOLAR,
    SINIFLAR,
    SUTUNLAR,
    YENI_KELIME,
    okuma_orani,
    refleks_mi,
    sinif_kodu,
    tahmini_okuma_suresi_sn,
)

KOK = Path(__file__).resolve().parents[1]
HAM_DIZIN = KOK / "data" / "ham"
CIKTI = KOK / "data" / "oturumlar.csv"

# data/SOZLUK.md — KVKK: bu adlarda sütun ASLA olmamalı
YASAK_SUTUNLAR = {
    "ad", "isim", "soyad", "eposta", "e_posta", "email", "mail", "telefon",
    "ogrenci_no", "ogrenci_numarasi", "ip", "konum", "lat", "lon",
    "cihaz", "cihaz_id", "user_agent", "zaman", "zaman_damgasi", "timestamp",
}


# ---------------------------------------------------------------- gerçek veri

def gercek_satirlari_oku() -> list[dict]:
    """data/ham/*.csv -> satır listesi. Dizin yoksa boş döner."""
    if not HAM_DIZIN.exists():
        return []

    satirlar: list[dict] = []
    for yol in sorted(HAM_DIZIN.glob("*.csv")):
        with yol.open("r", encoding="utf-8-sig", newline="") as f:
            okuyucu = csv.DictReader(f)
            eksik = set(SUTUNLAR) - set(okuyucu.fieldnames or [])
            if eksik:
                raise SystemExit(
                    f"HATA {yol.name}: eksik sütun(lar): {sorted(eksik)}\n"
                    "Bu dosya farklı bir uygulama sürümünden indirilmiş olabilir."
                )
            fazla = set(okuyucu.fieldnames or []) & YASAK_SUTUNLAR
            if fazla:
                raise SystemExit(
                    f"HATA {yol.name}: KVKK ihlali — yasak sütun(lar): {sorted(fazla)}"
                )
            for s in okuyucu:
                s["kaynak"] = "gercek"
                satirlar.append(s)
    return satirlar


# -------------------------------------------------------------- sentetik veri

def sentetik_uret(n_oturum: int, tohum: int) -> list[dict]:
    rng = np.random.default_rng(tohum)

    # Sentetik "kişiler": oturumlar bir kişiye bağlı olmalı, yoksa gerçek
    # veride var olan kişi içi korelasyon sentetikte kaybolur.
    n_kisi = max(3, n_oturum // 5)
    kisi_dikkat = rng.beta(2.2, 2.0, size=n_kisi)

    satirlar: list[dict] = []
    oturum_sayaci = {i: 0 for i in range(n_kisi)}

    for o in range(n_oturum):
        kisi = o % n_kisi
        oturum_sayaci[kisi] += 1

        oturum_id = f"{int(rng.integers(0, 16 ** 8)):08x}"
        senaryo = SENARYOLAR[int(rng.integers(len(SENARYOLAR)))]
        rol = ROLLER[int(rng.integers(len(ROLLER)))]
        hedef = HEDEFLER[int(rng.integers(len(HEDEFLER)))]
        sinif = SINIFLAR[int(rng.integers(len(SINIFLAR)))]

        dikkat = float(np.clip(kisi_dikkat[kisi] + rng.normal(0, 0.12), 0.03, 1.4))
        kelimeler = YENI_KELIME[(senaryo, rol)]

        gecen = float(rng.uniform(0.1, 0.6))
        onceki_sure = 0.0
        onceki_oran = 0.0
        refleks_sayisi = 0

        for k in range(3):
            yorgunluk = 1.0 - 0.12 * k
            acele = float(rng.lognormal(0.0, 0.35))
            yeni_kelime = int(kelimeler[k])
            tahmini = tahmini_okuma_suresi_sn(yeni_kelime)

            gorunur = max(0.3, tahmini * dikkat * yorgunluk * acele)
            karar_suresi = gorunur + float(rng.exponential(1.2))
            oran = okuma_orani(gorunur, yeni_kelime)
            refleks = refleks_mi(oran)

            if refleks:
                olasiliklar = [0.15, 0.25, 0.60]
            else:
                olasiliklar = [0.50, 0.28, 0.22]
            etiket = ["saglam", "orta", "riskli"][
                int(rng.choice(3, p=olasiliklar))
            ]

            satirlar.append({
                "oturum_id": oturum_id,
                "kisi_kodu": f"s{kisi + 1}",
                "oturum_sira": oturum_sayaci[kisi],
                "senaryo": senaryo,
                "sahne_no": k + 1,
                "sinif": sinif,
                "sinif_kodu": sinif_kodu(sinif),
                "rol": rol,
                "hedef": hedef,
                "onceki_karar_suresi_sn": round(onceki_sure, 2),
                "onceki_okuma_orani": round(onceki_oran, 4),
                "onceki_refleks_sayisi": refleks_sayisi,
                "oturum_gecen_sure_sn": round(gecen, 2),
                "karar_suresi_sn": round(karar_suresi, 2),
                "metin_gorunur_sure_sn": round(gorunur, 2),
                "yeni_kelime_sayisi": yeni_kelime,
                "okuma_orani": round(oran, 4),
                "vazgecilen_dokunma": int(rng.poisson(0.15)),
                "secenek_etiketi": etiket,
                "refleks": refleks,
                "golge_tahmin": "",
                "kaynak": "sentetik",
                "surum": f"sentetik-t{tohum}",
            })

            gecen += karar_suresi + 1.5
            onceki_sure = karar_suresi
            onceki_oran = oran
            refleks_sayisi += refleks

    return satirlar


# ---------------------------------------------------------------- doğrulama

def dogrula(satirlar: list[dict]) -> None:
    """Sözleşme denetimi. Hata varsa sıfırdan farklı çıkış kodu."""
    hatalar: list[str] = []

    for i, s in enumerate(satirlar):
        eksik = [k for k in SUTUNLAR if k not in s]
        if eksik:
            hatalar.append(f"satır {i}: eksik sütun {eksik}")
            continue

        try:
            gorunur = float(s["metin_gorunur_sure_sn"])
            kelime = float(s["yeni_kelime_sayisi"])
            oran_csv = float(s["okuma_orani"])
            refleks_csv = int(float(s["refleks"]))
        except (TypeError, ValueError) as e:
            hatalar.append(f"satır {i}: sayıya çevrilemedi ({e})")
            continue

        # Denetim zinciri (data/SOZLUK.md): 15 ÷ (16/200×60) -> 17 -> eşik -> 20
        oran_yeniden = okuma_orani(gorunur, kelime)
        if abs(oran_yeniden - oran_csv) > 1e-3:
            hatalar.append(
                f"satır {i}: okuma_orani tutmuyor — CSV {oran_csv}, "
                f"yeniden hesap {oran_yeniden:.4f}"
            )
        if refleks_mi(oran_csv) != refleks_csv:
            hatalar.append(
                f"satır {i}: refleks etiketi kuralla tutmuyor — "
                f"oran {oran_csv}, CSV etiketi {refleks_csv}"
            )

        for ad in OZELLIKLER:
            try:
                float(s[ad])
            except (TypeError, ValueError):
                hatalar.append(f"satır {i}: özellik '{ad}' sayısal değil: {s[ad]!r}")

    if hatalar:
        print(f"\nDOĞRULAMA BAŞARISIZ — {len(hatalar)} sorun:", file=sys.stderr)
        for h in hatalar[:20]:
            print("  -", h, file=sys.stderr)
        if len(hatalar) > 20:
            print(f"  … ve {len(hatalar) - 20} tane daha", file=sys.stderr)
        raise SystemExit(1)


# ---------------------------------------------------------------------- ana

def main() -> None:
    ap = argparse.ArgumentParser(description="Primer v2 veri derleyici")
    ap.add_argument("--sentetik", type=int, default=0,
                    help="üretilecek sentetik OTURUM sayısı (her oturum 3 satır)")
    ap.add_argument("--tohum", type=int, default=42, help="sentetik üretici tohumu")
    ap.add_argument("--cikti", type=Path, default=CIKTI)
    a = ap.parse_args()

    gercek = gercek_satirlari_oku()
    sentetik = sentetik_uret(a.sentetik, a.tohum) if a.sentetik > 0 else []
    hepsi = gercek + sentetik

    if not hepsi:
        raise SystemExit(
            "HATA: hiç satır yok.\n"
            f"Gerçek veri için indirilen CSV'leri {HAM_DIZIN} altına koy, "
            "ya da --sentetik N ver."
        )

    dogrula(hepsi)

    a.cikti.parent.mkdir(parents=True, exist_ok=True)
    with a.cikti.open("w", encoding="utf-8", newline="") as f:
        yazici = csv.DictWriter(f, fieldnames=SUTUNLAR, extrasaction="ignore")
        yazici.writeheader()
        yazici.writerows(hepsi)

    # ---- özet ----
    g_oturum = len({s["oturum_id"] for s in gercek})
    g_kisi = len({s["kisi_kodu"] for s in gercek if s.get("kisi_kodu")})
    refleks = sum(int(float(s["refleks"])) for s in hepsi)

    print(f"yazıldı: {a.cikti.relative_to(KOK)}")
    print(f"  satır        : {len(hepsi)}  (gerçek {len(gercek)} + sentetik {len(sentetik)})")
    print(f"  gerçek oturum: {g_oturum}  ({g_kisi} farklı katılımcı kodu)")
    print(f"  etiket dengesi: refleks={refleks}  dusunerek={len(hepsi) - refleks}"
          f"  (refleks oranı %{100 * refleks / len(hepsi):.1f})")

    if g_oturum < 15:
        print(f"\nUYARI: ödev en az 15 GERÇEK oturum istiyor, şu an {g_oturum} var.")
        print("Yalnız sentetik veriyle Veri kaleminin yarısı alınır.")


if __name__ == "__main__":
    main()
