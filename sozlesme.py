"""Primer v2 — veri ve model sözleşmesi.

Bu modül TEK DOĞRU KAYNAKTIR. `data/veri_derle.py`, `train.py` ve
`tests/parite.py` sütun adlarını, özellik sırasını ve etiket kuralını
buradan alır.

Neden ayrı bir modül: aynı tanımı üç betikte tekrarlamak, üretimdeki ML
sistemlerinin klasik hatası olan eğitim-servis sapmasının (train/serve skew)
en ucuz hâlidir. Bir yerde 0.4, başka yerde 0.5 yazdığı an etiket sessizce
ikiye ayrılır ve hiçbir test bunu yakalamaz.

İlgili belgeler: spec.md §10 · data/SOZLUK.md
"""

from __future__ import annotations

# --- Etiket kuralı (spec.md §10.4) — veri görüldükten sonra DEĞİŞTİRİLEMEZ ---
OKUMA_HIZI_KELIME_DK = 200
REFLEKS_ORAN_ESIGI = 0.4

# --- Eval kapısı ve eylem eşiği (spec.md §10.5) ---
# İkisi farklı şeydir: biri modelin yayınlanabilirliğini, diğeri uygulamanın
# müdahale edip etmeyeceğini belirler.
EVAL_KAPISI_AUC = 0.70
KARAR_ESIGI = 0.60

# --- CSV sütun sırası (data/SOZLUK.md) ---
SUTUNLAR = [
    "oturum_id", "kisi_kodu", "oturum_sira", "senaryo", "sahne_no",
    "sinif", "sinif_kodu", "rol", "hedef",
    "onceki_karar_suresi_sn", "onceki_okuma_orani", "onceki_refleks_sayisi",
    "oturum_gecen_sure_sn",
    "karar_suresi_sn", "metin_gorunur_sure_sn", "yeni_kelime_sayisi", "okuma_orani",
    "vazgecilen_dokunma", "secenek_etiketi", "refleks",
    "golge_tahmin", "kaynak", "surum",
]

# --- Özellik sırası (spec.md §10.3) — model/config.json ile AYNI olmalı ---
OZELLIKLER = [
    "sahne_no",
    "sinif_kodu",
    "onceki_karar_suresi_sn",
    "onceki_okuma_orani",
    "onceki_refleks_sayisi",
    "oturum_gecen_sure_sn",
]

ETIKET = "refleks"
SINIF_ETIKETLERI = ["dusunerek", "refleks"]  # 0, 1

# --- Ölçülmüş okuma yükü (kelime) ---
# web/index.html içindeki gerçek senaryo metinlerinden sayıldı (2026-11-01):
#   node ile SENARYOLAR nesnesi okunup kelime sayıldı; 1. sahnede kriz kurulumu
#   + rol eki + soru + üç seçenek, sonraki sahnelerde soru + üç seçenek.
# Sentetik veri üreticisi bu sayıları kullanır ki sentetik satırlar gerçek
# satırlarla aynı ölçekte olsun. Senaryo metni değişirse bu tablo da değişmeli.
YENI_KELIME = {
    ("donem-projesi", "backend"): (55, 30, 26),
    ("donem-projesi", "frontend"): (59, 30, 26),
    ("donem-projesi", "bilmiyorum"): (57, 30, 26),
    ("staj-task", "backend"): (63, 27, 26),
    ("staj-task", "frontend"): (62, 27, 26),
    ("staj-task", "bilmiyorum"): (62, 27, 26),
    ("vize-haftasi", "backend"): (43, 23, 20),
    ("vize-haftasi", "frontend"): (43, 23, 20),
    ("vize-haftasi", "bilmiyorum"): (43, 23, 20),
}

SENARYOLAR = ["donem-projesi", "staj-task", "vize-haftasi"]
ROLLER = ["frontend", "backend", "bilmiyorum"]
HEDEFLER = ["staj", "proje", "ogrenme"]
SINIFLAR = ["1-2", "3-4"]


def tahmini_okuma_suresi_sn(yeni_kelime_sayisi: float) -> float:
    """O karar noktasındaki metni okumak için gereken tahmini süre."""
    return (float(yeni_kelime_sayisi) / OKUMA_HIZI_KELIME_DK) * 60.0


def okuma_orani(metin_gorunur_sure_sn: float, yeni_kelime_sayisi: float) -> float:
    """spec.md §10.4 — 1'de kırpılmış okuma oranı."""
    tahmini = tahmini_okuma_suresi_sn(yeni_kelime_sayisi)
    if tahmini <= 0:
        return 1.0
    return min(1.0, float(metin_gorunur_sure_sn) / tahmini)


def refleks_mi(oran: float) -> int:
    """spec.md §10.4 — tek koşullu etiket kuralı."""
    return 1 if float(oran) < REFLEKS_ORAN_ESIGI else 0


def sinif_kodu(sinif: str) -> int:
    return 1 if str(sinif) == "3-4" else 0
