"""Primer v2 — tekrarlanabilir eğitim ve EVAL KAPISI.

Tek komut:
    python train.py

Sırası:
  1. data/oturumlar.csv okunur ve SÖZLEŞME DOĞRULANIR (etiket yeniden türetilir).
  2. StandardScaler + LogisticRegression, sabit tohumla eğitilir.
  3. Gruplu çapraz doğrulama (aynı oturum aynı katta) ile ROC-AUC ölçülür.
  4. KAPI: AUC eşiğin altındaysa betik sıfırdan farklı çıkış koduyla durur ve
     model/ altındaki hiçbir dosyaya DOKUNULMAZ (spec.md AC11).
  5. Eşik geçilirse ONNX'e aktarılır, sklearn ile farkı 1e-4 altında olduğu
     doğrulanır, model/model.onnx + model/config.json yazılır.

Tekrarlanabilirlik: tüm rastgelelik `--tohum` (varsayılan 42) ile sabit.
Aynı CSV ve aynı tohumla başka bir makinede birebir aynı metrik çıkar.

Eşiği sınamak için (kapının gerçekten kapattığını görmek):
    python train.py --esik 0.99
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
import skl2onnx
import onnxruntime as ort
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Windows konsolu varsayılan olarak cp1254 kullanıyor ve Türkçe olmayan tek bir
# işaret (ör. bir ok karakteri) betiği UnicodeEncodeError ile düşürebiliyor.
# Çıktı kodlaması burada sabitleniyor; errors="replace" ile hiçbir yazdırma
# işlemi eğitimi düşürmez.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

KOK = Path(__file__).resolve().parent
sys.path.insert(0, str(KOK))
sys.path.insert(0, str(KOK / "data"))

from sozlesme import (  # noqa: E402
    ETIKET,
    EVAL_KAPISI_AUC,
    KARAR_ESIGI,
    OKUMA_HIZI_KELIME_DK,
    OZELLIKLER,
    REFLEKS_ORAN_ESIGI,
    SINIF_ETIKETLERI,
)
# Doğrulama fonksiyonu veri derleyicisiyle PAYLAŞILIR: eğitim, derlemenin
# kabul ettiğinden farklı bir şeyi kabul etmemeli.
from veri_derle import dogrula  # noqa: E402

VARSAYILAN_VERI = KOK / "data" / "oturumlar.csv"
MODEL_DIZIN = KOK / "model"
HEDEF_OPSET = 18  # onnxruntime-web 1.20.1 bunu güvenle yükler


def veri_yukle(yol: Path) -> pd.DataFrame:
    if not yol.exists():
        raise SystemExit(
            f"HATA: {yol} yok.\n"
            "Önce veriyi derle:  python data/veri_derle.py --sentetik 60"
        )

    cerceve = pd.read_csv(yol, encoding="utf-8")
    dogrula(cerceve.to_dict(orient="records"))

    eksik = [a for a in OZELLIKLER + [ETIKET, "oturum_id"] if a not in cerceve.columns]
    if eksik:
        raise SystemExit(f"HATA: {yol} içinde eksik sütun(lar): {eksik}")

    return cerceve


def boru_hatti(tohum: int) -> Pipeline:
    """StandardScaler + LogisticRegression.

    Neden lojistik regresyon: ödev küçük tabular model istiyor; 180 satır ve 6
    özellikte ağaç toplulukları ezberler. Ayrıca katsayıları okunabilir —
    model kartında hangi sinyalin ne yönde çalıştığını yazabiliyoruz.

    Neden StandardScaler: özelliklerin ölçekleri çok farklı (sahne_no 1-3,
    oturum_gecen_sure_sn 0-120). Ölçeklemeden lbfgs yavaş yakınsar ve
    katsayılar karşılaştırılamaz hale gelir.
    """
    return Pipeline([
        ("olcek", StandardScaler()),
        ("sinif", LogisticRegression(
            max_iter=2000,
            random_state=tohum,
            class_weight="balanced",
        )),
    ])


def gruplu_oof_olasilik(X, y, gruplar, tohum: int) -> tuple[np.ndarray, list[float]]:
    """Kat dışı (out-of-fold) olasılıklar, AYNI OTURUM AYNI KATTA.

    Bu, ölçümün en önemli ayrıntısı. Satır birimi karar noktası olduğu için bir
    oturum üç satır üretiyor ve bu üç satır bağımsız değil (aynı kişi, aynı
    profil, aynı dikkat düzeyi). Sıradan StratifiedKFold bu satırları farklı
    katlara dağıtır; model eğitimde gördüğü oturumun kardeş satırını testte
    tahmin eder ve AUC olduğundan iyi çıkar.

    StratifiedGroupKFold oturumu bölünmez tutar. Aşağıda ikisi birden
    raporlanıyor ki farkın büyüklüğü görünür olsun; KAPI gruplu olana bakar.
    """
    kat = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=tohum)
    oof = np.zeros(len(y), dtype=float)
    kat_auc: list[float] = []

    for egitim_i, test_i in kat.split(X, y, groups=gruplar):
        boru = boru_hatti(tohum)
        boru.fit(X[egitim_i], y[egitim_i])
        p = boru.predict_proba(X[test_i])[:, 1]
        oof[test_i] = p
        if len(np.unique(y[test_i])) > 1:
            kat_auc.append(float(roc_auc_score(y[test_i], p)))

    return oof, kat_auc


def naif_oof_olasilik(X, y, tohum: int) -> np.ndarray:
    """Gruplamayı YOK SAYAN ölçüm — yalnız karşılaştırma için raporlanır."""
    kat = StratifiedKFold(n_splits=5, shuffle=True, random_state=tohum)
    oof = np.zeros(len(y), dtype=float)
    for egitim_i, test_i in kat.split(X, y):
        boru = boru_hatti(tohum)
        boru.fit(X[egitim_i], y[egitim_i])
        oof[test_i] = boru.predict_proba(X[test_i])[:, 1]
    return oof


def onnx_aktar(boru: Pipeline, X: np.ndarray, gecici: Path) -> tuple[Path, float]:
    """ONNX'e aktarır ve sklearn ile farkı ölçer.

    zipmap=False ZORUNLU: skl2onnx varsayılanı olasılıkları `seq(map(...))`
    olarak verir, onnxruntime-web bu tipi kullanamaz. Düz tensör gerekiyor.
    """
    onx = convert_sklearn(
        boru,
        initial_types=[("girdi", FloatTensorType([None, X.shape[1]]))],
        target_opset=HEDEF_OPSET,
        options={id(boru.named_steps["sinif"]): {"zipmap": False}},
    )

    # skl2onnx graph adına rastgele bir UUID yazıyor; ağırlıklar aynı olsa bile
    # dosya her koşumda farklı baytlar üretiyordu. Adı sabitlemek artefaktı
    # (veri + tohum) başına bayt düzeyinde tekrarlanabilir yapıyor — commit'e
    # sabitlenen bir model için bu, pin'in gerçekten tek bir dosyayı
    # işaret ettiği anlamına geliyor.
    onx.graph.name = "primer-refleks"

    yol = gecici / "model.onnx"
    yol.write_bytes(onx.SerializeToString())

    oturum = ort.InferenceSession(str(yol), providers=["CPUExecutionProvider"])
    cikti_adlari = [c.name for c in oturum.get_outputs()]
    olasilik_adi = next((a for a in cikti_adlari if "probab" in a.lower()), cikti_adlari[-1])

    onnx_p = np.asarray(
        oturum.run([olasilik_adi], {"girdi": X.astype(np.float32)})[0]
    )
    if onnx_p.ndim != 2:
        raise SystemExit(
            f"HATA: ONNX olasılık çıktısı düz tensör değil (biçim {onnx_p.shape}). "
            "zipmap=False uygulanmamış olabilir."
        )

    sklearn_p = boru.predict_proba(X)
    fark = float(np.max(np.abs(onnx_p - sklearn_p)))

    if fark > 1e-4:
        raise SystemExit(
            f"HATA: ONNX ile sklearn farkı {fark:.3e} > 1e-4. Artefakt yayınlanmadı."
        )

    return yol, fark


def main() -> None:
    ap = argparse.ArgumentParser(description="Primer v2 eğitim ve eval kapısı")
    ap.add_argument("--veri", type=Path, default=VARSAYILAN_VERI)
    ap.add_argument("--tohum", type=int, default=42)
    ap.add_argument("--esik", type=float, default=EVAL_KAPISI_AUC,
                    help=f"eval kapısı AUC eşiği (spec.md §10.5: {EVAL_KAPISI_AUC})")
    ap.add_argument("--cikti", type=Path, default=MODEL_DIZIN)
    a = ap.parse_args()

    cerceve = veri_yukle(a.veri)

    X = cerceve[OZELLIKLER].to_numpy(dtype=np.float64)
    y = cerceve[ETIKET].to_numpy(dtype=int)
    gruplar = cerceve["oturum_id"].to_numpy()

    if len(np.unique(y)) < 2:
        raise SystemExit("HATA: veride tek sınıf var; model eğitilemez.")

    print(f"veri: {a.veri.name} · {len(cerceve)} satır · "
          f"{len(np.unique(gruplar))} oturum · refleks oranı %{100 * y.mean():.1f}")
    print(f"özellikler ({len(OZELLIKLER)}): {', '.join(OZELLIKLER)}")

    # ---- ölçüm ----
    oof, kat_auc = gruplu_oof_olasilik(X, y, gruplar, a.tohum)
    auc_gruplu = float(roc_auc_score(y, oof))
    auc_naif = float(roc_auc_score(y, naif_oof_olasilik(X, y, a.tohum)))

    tahmin = (oof >= KARAR_ESIGI).astype(int)
    dengeli = float(balanced_accuracy_score(y, tahmin))
    kesinlik = float(precision_score(y, tahmin, zero_division=0))
    duyarlilik = float(recall_score(y, tahmin, zero_division=0))
    f1 = float(f1_score(y, tahmin, zero_division=0))
    km = confusion_matrix(y, tahmin, labels=[0, 1]).tolist()

    cogunluk_dogruluk = float(max(y.mean(), 1 - y.mean()))

    # Tek özellikli taban çizgisi: modelin altı özelliği gerçekten bir şey
    # katıyor mu, yoksa her şey "önceki refleks sayısı" mı?
    tek_i = OZELLIKLER.index("onceki_refleks_sayisi")
    oof_tek, _ = gruplu_oof_olasilik(X[:, [tek_i]], y, gruplar, a.tohum)
    auc_tek = float(roc_auc_score(y, oof_tek))

    print()
    print(f"ROC-AUC (gruplu, kat dışı)  : {auc_gruplu:.4f}   <- KAPI bu sayıya bakar")
    print(f"ROC-AUC (gruplamasız, naif) : {auc_naif:.4f}   (yalnız karşılaştırma)")
    print(f"ROC-AUC (tek özellik taban) : {auc_tek:.4f}   (onceki_refleks_sayisi)")
    print(f"kat kat AUC                 : {', '.join(f'{v:.3f}' for v in kat_auc)}")
    print(f"dengeli doğruluk @{KARAR_ESIGI}      : {dengeli:.4f}")
    print(f"kesinlik / duyarlılık / F1  : {kesinlik:.3f} / {duyarlilik:.3f} / {f1:.3f}")
    print(f"çoğunluk sınıfı doğruluğu   : {cogunluk_dogruluk:.4f}")
    print(f"karmaşıklık matrisi [[TN,FP],[FN,TP]] : {km}")

    # ---- EVAL KAPISI (spec.md AC11) ----
    if auc_gruplu < a.esik:
        print()
        print(f"EVAL KAPISI KAPALI: AUC {auc_gruplu:.4f} < eşik {a.esik:.2f}")
        print("Artefakt YAYINLANMADI; model/ dizinine dokunulmadı.")
        print("Yapılacak: veriyi büyüt (eşiği düşürmek değil).")
        raise SystemExit(2)

    print()
    print(f"EVAL KAPISI AÇIK: AUC {auc_gruplu:.4f} >= eşik {a.esik:.2f}")

    # ---- tam veriyle son model + ONNX ----
    boru = boru_hatti(a.tohum)
    boru.fit(X, y)

    with tempfile.TemporaryDirectory() as gecici_ad:
        gecici = Path(gecici_ad)
        onnx_yol, fark = onnx_aktar(boru, X, gecici)
        print(f"ONNX / sklearn en büyük fark: {fark:.3e}  (sınır 1e-4)")

        katsayilar = {
            ad: float(k) for ad, k in zip(OZELLIKLER, boru.named_steps["sinif"].coef_[0])
        }

        config = {
            "ad": "primer-refleks",
            "surum": "2.0.0",
            "olusturulma": date.today().isoformat(),
            "amac": "Bir karar noktasına girildiğinde o kararın refleksle verilme "
                    "olasılığını tahmin eder. Çıktı yalnızca yansıma duraklamasını "
                    "tetikler; hangi seçeneğin seçileceğine dair hiçbir yetkisi yok.",

            "girdi": {
                "ad": "girdi",
                "tip": "float32",
                "bicim": [None, len(OZELLIKLER)],
                "ozellikler": OZELLIKLER,
            },
            "cikti": {
                "sinif_etiketleri": SINIF_ETIKETLERI,
                "olasilik_indeksi": 1,
                "aciklama": "olasılık tensörünün 1. indeksi p(refleks)",
            },

            "karar_esigi": KARAR_ESIGI,
            "etiket_kurali": {
                "refleks": f"okuma_orani < {REFLEKS_ORAN_ESIGI}",
                "okuma_orani": "min(1, metin_gorunur_sure_sn / (yeni_kelime_sayisi/"
                               f"{OKUMA_HIZI_KELIME_DK}*60))",
            },

            "eval": {
                "kapi_metrigi": "roc_auc_gruplu_kat_disi",
                "kapi_esigi": a.esik,
                "sonuc": round(auc_gruplu, 4),
                "gecti": True,
                "gruplama": "oturum_id (StratifiedGroupKFold, 5 kat)",
            },
            "metrikler": {
                "roc_auc_gruplu": round(auc_gruplu, 4),
                "roc_auc_gruplamasiz": round(auc_naif, 4),
                "roc_auc_tek_ozellik_taban": round(auc_tek, 4),
                "kat_kat_auc": [round(v, 4) for v in kat_auc],
                "dengeli_dogruluk": round(dengeli, 4),
                "kesinlik": round(kesinlik, 4),
                "duyarlilik": round(duyarlilik, 4),
                "f1": round(f1, 4),
                "cogunluk_sinifi_dogrulugu": round(cogunluk_dogruluk, 4),
                "karmasiklik_matrisi": km,
            },

            "veri": {
                "dosya": str(a.veri.relative_to(KOK)).replace("\\", "/"),
                "satir": int(len(cerceve)),
                "oturum": int(len(np.unique(gruplar))),
                "gercek_satir": int((cerceve["kaynak"] == "gercek").sum()),
                "sentetik_satir": int((cerceve["kaynak"] == "sentetik").sum()),
                "gercek_oturum": int(
                    cerceve.loc[cerceve["kaynak"] == "gercek", "oturum_id"].nunique()
                ),
                "refleks_orani": round(float(y.mean()), 4),
            },

            "egitim": {
                "model": "StandardScaler + LogisticRegression(class_weight=balanced)",
                "tohum": a.tohum,
                "target_opset": HEDEF_OPSET,
                "katsayilar": katsayilar,
                "kesisim": float(boru.named_steps["sinif"].intercept_[0]),
                "surumler": {
                    "python": platform.python_version(),
                    "scikit-learn": sklearn.__version__,
                    "skl2onnx": skl2onnx.__version__,
                    "onnxruntime": ort.__version__,
                },
            },

            "onnx_sklearn_max_fark": fark,
        }

        # Artefaktlar YALNIZCA kapı geçildikten ve ONNX doğrulandıktan sonra
        # yerine taşınır. Kapı kapalıysa buraya hiç gelinmiyor.
        a.cikti.mkdir(parents=True, exist_ok=True)
        shutil.copy2(onnx_yol, a.cikti / "model.onnx")
        (a.cikti / "config.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(f"yazıldı: {(a.cikti / 'model.onnx').relative_to(KOK)}")
    print(f"yazıldı: {(a.cikti / 'config.json').relative_to(KOK)}")
    print()
    print("katsayılar (ölçeklenmiş özelliklerde, + = refleks olasılığını artırır):")
    for ad, k in sorted(katsayilar.items(), key=lambda t: -abs(t[1])):
        print(f"  {ad:28s} {k:+.4f}")


if __name__ == "__main__":
    main()
