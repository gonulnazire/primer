# DEVAM.md — nerede kaldık

**Son güncelleme:** 2026-11-04 · **Teslim:** 6 Kasım 2026, 23:59

Bu dosya ara verip döndüğünde bağlamı kurtarmak için. Kararların gerekçeleri ilgili belgelerde; burada yalnız **durum** ve **sıradaki komutlar** var.

---

## Tek cümlede durum

Teknik tarafın tamamı bitti: model gerçek veriyle yeniden eğitildi (**AUC 0.8341**), Hugging Face'e yayınlanıp commit'e pin'lendi, **34/34 test canlı yayına karşı geçiyor**. Kalan iş yalnız **devreye alma + demo video + teslim formu**.

## Biten

| Kalem | Durum |
|---|---|
| spec.md §10 model gereksinimi + AC11–AC13 | ✅ eşik eğitimden önce yazıldı |
| `data/SOZLUK.md`, `sozlesme.py` | ✅ |
| `train.py` + eval kapısı | ✅ `--esik 0.99` ile kapının kapattığı doğrulandı (çıkış 2, `model/` değişmez) |
| `model/` artefakt + sözleşme + model kartı | ✅ 553 bayt |
| `RELEASE.md` ödünleşim matrisi + shadow/canary/rollback | ✅ |
| `SINAV_TASARIMI.md` | ✅ |
| `web/index.html` + GitHub Pages yayını | ✅ <https://gonulnazire.github.io/primer/web/> |
| **Dengeleyici veri toplama** | ✅ 3 yeni CSV · 17 oturum / 51 karar · 7 "düşünerek" satırı |
| **Gerçek veriyle yeniden eğitim** | ✅ **AUC 0.8341 ≥ 0.70** · `model/` ve `tests/parite.json` yenilendi |
| Belgeler yeni ölçümlere göre güncel | ✅ `model/README.md` §3–§5, `README.md`, `spec.md` §11, `RELEASE.md` §3/§5 |
| **Hugging Face yayını + commit pin** | ✅ <https://huggingface.co/gonulnazire/primer-refleks-onnx> · commit `1e02139d1968b4cbad05a6893f32f7a570300a63` · `site.json`'da pin'li |
| **Çalışma zamanı CDN'i unpkg'a alındı** | ✅ jsdelivr bu ağdan inmiyordu (§3'teki tuzak) |
| **Testler (canlı yayına karşı)** | ✅ **34/34** · 1 dk 26 sn · `golge:false`/oran `1.0` haline karşı · videolar bu koşumdan |
| **Devreye alma (RELEASE.md §4)** | ✅ 4 kademe, 4 commit · terfi kapısı ölçüldü (kesinlik 1.0000, 65 oturum) · iki çekincesi §4'te yazılı |

## Bekleyen (sırayla)

| # | İş | Kimde | Not |
|---|---|---|---|
| 1 | Demo video 60–90 sn | kullanıcı | Uygulama hazır: `golge:false`, oran `1.0`, model müdahale ediyor. Hızlı tıklayınca yansıma duraklaması açılır |
| 2 | Teslim formu (4 link) | kullanıcı | <https://forms.gle/pr9QVEfLJuaFiXw39> · hangi dört link istendiğini formda doğrula |
| 3 | HF token'larını iptal et | kullanıcı | İki token da sohbete düştü: <https://huggingface.co/settings/tokens> |

**`surum` alanı açık kalem:** `site.json` → `"surum": "v0"`. Bu alan toplanan her CSV satırının `surum` sütununa geçiyor. Yeni veri toplanacaksa anlamlı bir etikete çevrilmeli (ör. `v2.0.0`), yoksa gelecekteki satırlar hangi model devredeyken üretildiğini yanlış söyler. `RELEASE.md` §3 bunu istemediği için değiştirilmedi.

---

## 1. Veri: iki tur, ne oldu

**Birinci tur kullanılamadı.** 52 oturum / 156 karar (`data/ham/oturumlar-5619d1a4.csv`), **156/156 refleks**, ortanca karar süresi 0.49 sn. Enstrümantasyon doğruydu (görünür süre / karar süresi oranı 1.007); sorun toplama biçimiydi — kimse metni okumadı. Bu bulguyu yakalayan denetim `data/veri_derle.py` → `etiket_dengesi_uyar()` içinde kalıcı.

**İkinci tur kurtardı, ama hedefin altında kaldı.** Üç yeni dosya:

| Dosya | Oturum | Karar | Düşünerek | Ort. karar süresi |
|---|---|---|---|---|
| `oturumlar-189075e2.csv` | 4 | 12 | 1 | 1.47 sn |
| `oturumlar-87f40b49.csv` | 7 | 21 | 0 | 1.00 sn |
| `oturumlar-d2dbd7bb.csv` | 6 | 18 | **6** | 4.13 sn |
| **birleşik gerçek** | **69** | **207** | **7 (%3.4)** | — |

Hedef ~45 "düşünerek" satırıydı; 7 geldi. Pratikte yalnız bir katılımcı (`d2dbd7bb`) talimatı okuyarak uyguladı. Profil çeşitliliği yine de düzeldi: artık `backend` rolü ve `3-4. sınıf` temsil ediliyor (birinci turda 0 `backend` vardı).

**Sonuç ve dürüstlük notu:** kapı 0.8341 ile açıldı, ama 39 "düşünerek" satırının 32'si sentetik. Yani AUC'nin bir kısmı sentetik üreticinin yapısını ölçüyor. Bu, `model/README.md` §5'in 1. sınırı olarak ve `README.md`'de açıkça raporlanıyor — saklanmadı.

Üç yeni dosyada `kisi_kodu` **boş** (katılımcılar kodu girmedi). Boru hattını bozmuyor — gruplama `oturum_id` üzerinden — ama kişi düzeyinde gruplama artık veriden kurulamaz; bu da model kartına sınır olarak yazıldı.

---

## 2. Koşulan komutlar (2026-11-04, hepsi geçti)

```bash
.venv/Scripts/python.exe data/veri_derle.py --sentetik 20   # 267 satır (207 gerçek + 60 sentetik)
.venv/Scripts/python.exe train.py                           # AUC 0.8341 -> kapı açık
.venv/Scripts/python.exe tests/parite.py --yaz               # model değişti, referans yenilendi
```

Kalan (push ve HF pin sonrası):

```bash
npx cypress run -x v2Url=https://gonulnazire.github.io/primer/web/
```

`--sentetik 20` neden: ~207 gerçek satır yanına 60 sentetik koyar, gerçek veri çoğunlukta kalır. Sentetik veri etiket dengesini sağlamlaştırmak için var, çoğunluk olmak için değil — ve **kapıyı geçirmek için artırılmaz.**

---

## 3. Tuzaklar — bunlara dikkat

| Tuzak | Ne olur | Çaresi |
|---|---|---|
| **pandas 3.1.0 + Smart App Control** | `train.py` şu hatayla patlar: `DLL load failed while importing reshape: Uygulama Denetimi ilkesi bu dosyayı engelledi`. Windows Smart App Control zorlanıyor durumda (`VerifiedAndReputablePolicyState=1`) ve pandas 3.1.0'ın `reshape.cp314-win_amd64.pyd` dosyasını hash bazında engelliyor | venv'de **`pandas==3.0.5`** kullan. Aynı sürümü yeniden kurmak işe yaramaz (dosya bayt bayt aynı → aynı verdikt). `pip install -U pandas` yapma. **Smart App Control'ü kapatma** — geri alınamaz, yeniden açmak Windows kurulumu gerektirir |
| **Eval kapısı kapanırsa eşiği düşürme** | Eşik eğitimden önce yazıldı; sonradan düşürmek ödevin tek kuralını ihlal eder | Daha çok veri topla; geçmezse `RELEASE.md`'ye "eşik tutmadı, yayınlanmadı" yaz |
| **`parite.py --yaz` atlanırsa** | `tests/parite.py` modelin sha256'sını karşılaştırıp **durur** | Model her değiştiğinde referansı yenile |
| **Cypress `--spec` ile alt küme koşmak** | `videosFolder` koşumdan önce boşaltılır → koşulmayan spec'lerin **commit'li videoları silinir** | Videoları yenilerken tüm takımı koş; silindiyse `git checkout -- cypress/videos/` |
| **Push etmeden Cypress koşmak** | Testler canlı Pages'e karşı koşuyor; push edilmemiş model test edilmez, videolar eski modeli gösterir | Önce push, sonra test. Pages'in yayması ~40–100 sn sürüyor; canlı dosyayı yoklayarak doğrula |
| **CDN yavaşlığı testleri düşürür** | `onnxruntime-web` ~11 MB wasm indiriyor. 2026-11-04'te jsdelivr'dan 2.8 MB dosya 120 sn'de inmedi → model hiç "hazır" olmadı → AC12 + üç AC13 testi 30 sn'de zaman aşımına düştü (30/34). Uygulama müdahalesiz çalışmaya devam ettiği için hata **sessiz** | Host unpkg'a alındı (`web/index.html`, sürüm pin'i korundu). Testler yine düşerse önce CDN hızını ölç, modeli suçlama |
| **`web/site.json`'ı veri toplarken değiştirme** | `golge:true` olmalı; müdahale açıkken toplanan veri modelin kendi etkisini içerir | Demo videosuna kadar gölgede kalsın |
| **Konsol kodlaması** | Windows cp1254, betikler UTF-8'e zorluyor | `PYTHONUTF8=1` ile koş |

---

## 4. Değişmeyecek kararlar (gerekçeleri belgelerde)

- **Model yalnız *ne zaman durulacağını* söyler, *ne seçileceğini* söylemez.** Müdahale cevap-nötr (`spec.md` §10.2, AC13 testi bunu doğruluyor).
- **v1 test dosyalarına dokunulmaz** (`cypress/e2e/primer.cy.js`, `sohbet.cy.js`) — regresyon kanıtının değeri aynı kalmalarından geliyor (`spec.md` §8).
- **Etiket kuralı:** `refleks = okuma_orani < 0.4`, veriden sonra değişmez (`spec.md` §10.4).
- **İki eşik karıştırılmaz:** eval kapısı 0.70 (AUC) ≠ eylem eşiği 0.60 (olasılık).
- **Model katmanı Pages'te, v1 AI Studio'da** — ölçülmüş CORS kısıtı yüzünden (`RELEASE.md` §2).
- **Sentetik veri oranı kapıyı geçirmek için artırılmaz.**

## 5. Ortam

```bash
# Python 3.14.2 + .venv
# scikit-learn 1.9.1 / skl2onnx 1.20.0 / onnxruntime 1.31.1 / pandas 3.0.5 (3.1.0 DEĞİL — §3)
.venv/Scripts/python.exe -c "import sklearn, skl2onnx, onnx, onnxruntime, pandas; print('ok')"

npm run v2     # yerel sunucu: http://localhost:4173/web/  (Pages varken gerekmez)
```

Not: Smart App Control bazı dosyaları ilk yüklemede engelleyip birkaç dakika sonra serbest bırakıyor (sklearn'de böyle oldu), bazılarında kalıcı engelliyor (pandas 3.1.0). Bir ithal hatası görürsen bir kez tekrar dene; ısrar ediyorsa §3'e bak.
