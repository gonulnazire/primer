# DEVAM.md — nerede kaldık

**Son güncelleme:** 2026-11-01 · **Commit:** `6bf9fe5` · **Teslim:** 6 Kasım 2026, 23:59

Bu dosya ara verip döndüğünde bağlamı kurtarmak için. Kararların gerekçeleri ilgili belgelerde; burada yalnız **durum** ve **sıradaki komutlar** var.

---

## Tek cümlede durum

v2'nin kod ve belge tarafı bitti, yayında çalışıyor ve 34/34 test geçiyor; **modelin gerçek veriyle yeniden eğitilmesi bekleniyor**, çünkü ilk toplanan veri kullanılamaz çıktı.

## Biten

| Kalem | Durum |
|---|---|
| spec.md §10 model gereksinimi + AC11–AC13 | ✅ eşik eğitimden önce yazıldı |
| `data/SOZLUK.md`, `sozlesme.py` | ✅ |
| `train.py` + eval kapısı | ✅ `--esik 0.99` ile kapının kapattığı doğrulandı (çıkış 2, `model/` değişmez) |
| `model/` artefakt + sözleşme + model kartı | ✅ 553 bayt, bayt düzeyinde tekrarlanabilir |
| `RELEASE.md` ödünleşim matrisi + shadow/canary/rollback | ✅ |
| `SINAV_TASARIMI.md` | ✅ |
| `web/index.html` + GitHub Pages yayını | ✅ <https://gonulnazire.github.io/primer/web/> |
| Testler | ✅ **34/34** — v1 20 test AI Studio'ya, v2 14 test **canlı Pages'e** karşı |

## Bekleyen (sırayla)

| # | İş | Kimde | Not |
|---|---|---|---|
| 1 | **Dengeleyici veri toplama** | kullanıcı | 15–20 oturum, metni **okuyarak**. Mesaj aşağıda |
| 2 | Gerçek veriyle yeniden eğitim | ajan | Veri gelince, aşağıdaki 5 komut |
| 3 | Hugging Face hesabı + write token | kullanıcı | Paralel yürütülebilir, veriyi beklemez |
| 4 | HF yayını + commit pin → `web/site.json` | ajan | `RELEASE.md` §3 |
| 5 | Demo video 60–90 sn | kullanıcı | `site.json`'da `golge:false`, `devreye_alma_orani:1.0` |
| 6 | Teslim formu (4 link) | kullanıcı | <https://forms.gle/pr9QVEfLJuaFiXw39> |

---

## 1. Veri sorunu — neden yeniden toplanıyor

İlk toplama 52 oturum / 156 karar getirdi (`data/ham/oturumlar-5619d1a4.csv`). Sayıca ödevin istediği 15 oturumun üstünde, **ama kullanılamaz**:

| Ölçüm | Değer |
|---|---|
| Refleks etiketli | **156 / 156 = %100** |
| Ortanca karar süresi | **0.49 sn** (metni okumak ~15 sn) |
| `okuma_orani ≥ 0.4` olan karar | **0 adet** |

Enstrümantasyon doğrulandı (görünür süre / karar süresi oranı 1.007, imkânsız satır yok) — ölçüm değil, **toplama biçimi** sorunlu. Veri tek sınıfa çöktüğü için modele hiçbir ayrım bilgisi vermiyor.

Bu bulguyu yakalayan denetim `data/veri_derle.py` → `etiket_dengesi_uyar()` içinde kalıcı.

**Profil çeşitliliği de zayıf:** 141 satır `sinif=1-2` / 15 satır `3-4`; `rol` dağılımı 129 `bilmiyorum`, 27 `frontend`, **0 `backend`**.

### Arkadaşlara gönderilecek mesaj

> Link: https://gonulnazire.github.io/primer/web/
>
> Önemli: **senaryo metnini ve üç şıkkı gerçekten oku, sonra seç.** Acele etme — bir karar için 10–15 saniye normal. Amaç hangi şıkkın "doğru" olduğunu bulmak değil, metni okuyup kendi kararını vermen.
>
> 1. Sayfanın altındaki **"Katılımcı kodu"** alanına **`k4`** yaz (sana özel)
> 2. Üç soruyu cevapla → senaryo seç → üç kararı **okuyarak** ver → sonucu gör
> 3. "Baştan başla" ile **5 oturum** oyna, farklı senaryolar seç
> 4. Arada sayfayı yenileyip **profili değiştir** — özellikle bir kere **3-4. sınıf**, bir kere **Backend** seç
> 5. **Sadece en sonda, bir kez** "CSV indir"e bas ve dosyayı gönder

Yeni kodlar `k4`, `k5`, `k6` (eskiler K1–K3). Hedef ~15 oturum = 45 "düşünerek" satırı → gerçek verinin ~%22'si karşı sınıf olur.

---

## 2. Veri geldiğinde koşulacak komutlar (SIRA ÖNEMLİ)

Dosyalar `data/ham/` içine konur, sonra:

```bash
# 1) birleştir + tekilleştir + şema/KVKK/etiket dengesi denetimi
.venv/Scripts/python.exe data/veri_derle.py --sentetik 20

# 2) eğit ve eval kapısından geçir
.venv/Scripts/python.exe train.py

# 3) model DEĞİŞTİ -> parite referansını yenile (atlanırsa 4. adım DURUR)
.venv/Scripts/python.exe tests/parite.py --yaz

# 4) tüm takım, canlı Pages'e karşı
npx cypress run -x v2Url=https://gonulnazire.github.io/primer/web/

# 5) belgeleri güncelle: model/README.md §3-§4, README.md ölçüm tablosu, spec.md §11
```

`--sentetik 20` neden: ~200 gerçek satır yanına 60 sentetik koyar, gerçek veri çoğunlukta kalır. Sentetik veri etiket dengesini sağlamlaştırmak için var, çoğunluk olmak için değil.

---

## 3. Tuzaklar — bunlara dikkat

| Tuzak | Ne olur | Çaresi |
|---|---|---|
| **Eval kapısı kapanırsa eşiği düşürme** | Eşik eğitimden önce yazıldı; sonradan düşürmek ödevin tek kuralını ihlal eder | Daha çok veri topla; geçmezse `RELEASE.md`'ye "eşik tutmadı, yayınlanmadı" yaz — ödev dürüstlüğü ödüllendiriyor |
| **`parite.py --yaz` atlanırsa** | `tests/parite.py` modelin sha256'sını karşılaştırıp **durur** | Model her değiştiğinde referansı yenile |
| **Cypress `--spec` ile alt küme koşmak** | `videosFolder` koşumdan önce boşaltılır → koşulmayan spec'lerin **commit'li videoları silinir** | Videoları yenilerken tüm takımı koş; silindiyse `git checkout -- cypress/videos/` |
| **`web/site.json`'ı veri toplarken değiştirme** | `golge:true` olmalı; müdahale açıkken toplanan veri modelin kendi etkisini içerir | Demo videosuna kadar gölgede kalsın |
| **Konsol kodlaması** | Windows cp1254, betikler UTF-8'e zorluyor | Sorun çıkarsa `PYTHONUTF8=1` ile koş |

---

## 4. Değişmeyecek kararlar (gerekçeleri belgelerde)

- **Model yalnız *ne zaman durulacağını* söyler, *ne seçileceğini* söylemez.** Müdahale cevap-nötr (`spec.md` §10.2, AC13 testi bunu doğruluyor).
- **v1 test dosyalarına dokunulmaz** (`cypress/e2e/primer.cy.js`, `sohbet.cy.js`) — regresyon kanıtının değeri aynı kalmalarından geliyor (`spec.md` §8).
- **Etiket kuralı:** `refleks = okuma_orani < 0.4`, veriden sonra değişmez (`spec.md` §10.4).
- **İki eşik karıştırılmaz:** eval kapısı 0.70 (AUC) ≠ eylem eşiği 0.60 (olasılık).
- **Model katmanı Pages'te, v1 AI Studio'da** — ölçülmüş CORS kısıtı yüzünden (`RELEASE.md` §2).

## 5. Ortam

```bash
# Python 3.14.2 + .venv (scikit-learn 1.9.1 / skl2onnx 1.20.0 / onnxruntime 1.31.1)
.venv/Scripts/python.exe -c "import sklearn, skl2onnx, onnx, onnxruntime; print('ok')"

npm run v2     # yerel sunucu: http://localhost:4173/web/  (Pages varken gerekmez)
```
