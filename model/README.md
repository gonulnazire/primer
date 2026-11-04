---
license: mit
tags:
  - tabular-classification
  - onnx
  - education
language:
  - tr
---

# Primer — Refleks Karar Modeli (`primer-refleks`)

**Sürüm:** 2.0.0 · **Biçim:** ONNX (opset 18) · **Boyut:** ~0.6 KB
**Kaynak depo:** <https://github.com/gonulnazire/primer>
**Sözleşme:** [`config.json`](./config.json) — özellik adları ve sırası, sınıf etiketleri, metrikler

Bu kart [Mitchell vd. (2019), *Model Cards for Model Reporting*](https://arxiv.org/abs/1810.03993) yapısını izler. Sayısal değerlerin tek doğru kaynağı `config.json`'dır; aşağıdaki tablolar `train.py` çıktısından kopyalanmıştır.

---

## 1. Model nedir

Bir öğrenci Primer simülasyonunda bir karar noktasına girdiğinde, **o kararı refleksle verip vermeyeceğini** tahmin eder.

| | |
|---|---|
| Tip | Lojistik regresyon (`StandardScaler` + `LogisticRegression`, `class_weight=balanced`) |
| Girdi | `float32[1, 6]` — sırası `config.json` → `girdi.ozellikler` |
| Çıktı | `p(refleks)` — olasılık tensörünün 1. indeksi |
| Eylem eşiği | **0.60** |
| Tohum | 42 (`random_state`) |

**Neden lojistik regresyon:** 180 satır ve 6 özellikte ağaç toplulukları ezberler. Ayrıca katsayılar okunabilir — hangi sinyalin hangi yönde çalıştığı aşağıda yazılı, ki bu bir öğrenme ürününde modelin ne yaptığını savunabilmek için gerekli.

### Katsayılar (ölçeklenmiş özelliklerde)

| Özellik | Katsayı | Okunuşu |
|---|---|---|
| `onceki_refleks_sayisi` | **+0.93** | Refleks davranış kendini tekrar ediyor — en güçlü sinyal |
| `sahne_no` | **+0.70** | Senaryo ilerledikçe refleks kararlar artıyor |
| `oturum_gecen_sure_sn` | **−0.53** | Oturumda uzun zaman geçirmiş oyuncu daha az refleks veriyor |
| `onceki_okuma_orani` | −0.24 | Önceki sahneyi okuyan, sonrakini de okuyor |
| `sinif_kodu` | +0.17 | 3-4. sınıf hafifçe daha fazla refleks (zayıf) |
| `onceki_karar_suresi_sn` | −0.03 | Neredeyse hiçbir şey katmıyor — ham süre yerine oran bilgilendirici |

İlk üç sinyalin birlikte anlattığı şey tutarlı: **refleks bir alışkanlık, anlık bir hata değil.** Ürün tarafındaki karşılığı şu — müdahale (yansıma duraklaması) oyuncunun ilk hatasında değil, örüntü belirdiğinde devreye giriyor.

---

## 2. Amaçlanan kullanım

**Kullanım alanı:** yalnızca Primer öğrenme simülasyonu içinde, **yansıma duraklamasını** tetiklemek. Eşik geçilirse karar noktasına girişte tek bir Sokratik soru gösterilir ve seçenekler 3 saniye pasif kalır.

**Modelin yetkisi sınırlıdır ve bu kasıtlıdır.** Model yalnızca *ne zaman durulacağını* söyler; *ne seçileceğini* söyleyemez. Primer'ın tek iddiası öğrenciye doğru cevabı vermemek (`spec.md` §1, §6.1); modelin müdahalesi hiçbir seçeneği işaret etmez, öne çıkarmaz veya metni değiştirmez. Bu, bir Cypress testiyle de doğrulanıyor: duraklama metni hiçbir seçeneğin metnini içermemeli (`cypress/e2e/v2-akis.cy.js`, AC13).

### Kullanılmaması gereken durumlar

| Nerede kullanılmamalı | Neden |
|---|---|
| **Notlandırma, değerlendirme, sıralama** | Model dikkat ölçmüyor; ekranda geçen süreyi ölçüyor. Bir öğrenciyi "dikkatsiz" diye etiketlemek için kullanılamaz |
| **Öğrenci hakkında kalıcı profil çıkarmak** | Veri oturum içidir ve simülasyon hiçbir şey saklamaz (`spec.md` §2) |
| **Primer dışındaki herhangi bir uygulama** | Özellikler bu üç senaryonun okuma yüküne göre ölçeklenmiş; başka içerikte `yeni_kelime_sayisi` tabanı farklı olur |
| **İşe alım, akademik yaptırım, disiplin** | Tahmin edici gücü %83 AUC; birey hakkında karar vermeye yakın bile değil |
| **Dikkat eksikliği veya öğrenme güçlüğü göstergesi** | Klinik hiçbir geçerliliği yok. Hızlı okuyan, metni önceden görmüş veya telefonu elinden bırakmış bir öğrenci aynı sinyali üretir |

---

## 3. Veri

| | Değer |
|---|---|
| Dosya | [`data/oturumlar.csv`](../data/oturumlar.csv) · sözlük: [`data/SOZLUK.md`](../data/SOZLUK.md) |
| Satır birimi | **bir karar noktası** (bir oturum = 3 satır) |
| Toplam satır | 267 |
| Gerçek / sentetik | **207 / 60** — aşağıdaki sınıra bakın |
| Oturum | 89 (69 gerçek) |
| Refleks oranı | %85.4 (gerçek veride %96.6) |

**Bu sürüm gerçek veriyle eğitilmiştir** (satırların %77'si gerçek), ancak **azınlık sınıfı hâlâ ağırlıkla sentetiktir** — 39 "düşünerek" satırının 32'si sentetik, yalnız 7'si gerçek. Aşağıdaki 5. bölümün 1. sınırı bunun ne anlama geldiğini açıklıyor. `config.json` → `veri.gercek_oturum` o anki gerçek sayıyı taşır. Bu kartın 3. bölümü her yeniden eğitimde güncellenmelidir.

Sentetik üretici kuralı ve tohumu `data/veri_derle.py` başlığında ve `README.md`'de yazılıdır (tohum 42). Sentetik veri gerçek verinin yerine geçmez: kişi içi korelasyonu taklit eder ama gerçek bir öğrencinin davranış dağılımını bilemez.

### Etiket

```
refleks = 1   eğer   okuma_orani < 0.4
okuma_orani   = min(1, metin_gorunur_sure_sn / (yeni_kelime_sayisi / 200 * 60))
```

200 kelime/dakika Türkçe ortalama okuma hızı **varsayımıdır**, ölçüm değil. Eşik ve kural veri toplanmadan önce sabitlendi (`spec.md` §10.4) ve veriden sonra değiştirilmedi.

---

## 4. Değerlendirme

| Ölçüt | Sonuç | Not |
|---|---|---|
| **ROC-AUC (gruplu, kat dışı)** | **0.8341** | **Eval kapısı bu sayıya bakar** — eşik 0.70 |
| ROC-AUC (gruplamasız) | 0.8429 | Yalnız karşılaştırma için |
| ROC-AUC (tek özellik tabanı) | 0.7634 | Yalnız `onceki_refleks_sayisi` |
| Kat kat AUC | 0.808 / 0.853 / 0.802 / 0.749 / 0.881 | Katlar arası yayılım |
| Dengeli doğruluk @0.60 | 0.7729 | |
| Kesinlik / Duyarlılık / F1 | 0.979 / 0.623 / 0.761 | |
| Çoğunluk sınıfı doğruluğu | 0.8539 | Taban çizgisi |
| Karmaşıklık matrisi | `[[36, 3], [86, 142]]` | `[[TN, FP], [FN, TP]]` |
| ONNX / sklearn en büyük fark | 9.1e-08 | Sınır 1e-4 |

**Gruplama neden önemli:** satır birimi karar noktası olduğu için bir oturum üç satır üretiyor ve bu satırlar bağımsız değil (aynı kişi, aynı profil, aynı dikkat düzeyi). Sıradan `StratifiedKFold` aynı oturumun satırlarını farklı katlara dağıtır; model eğitimde gördüğü oturumun kardeş satırını testte tahmin eder ve AUC olduğundan iyi çıkar. Ölçüm `StratifiedGroupKFold` ile `oturum_id` üzerinden gruplanıyor. Bu veri setinde gruplu AUC gruplamasızdan **düşük** (0.8341 vs 0.8429) — yani gruplama beklendiği yönde çalışıyor ve iyimserliği kırpıyor. Önceki sentetik-yalnız sürümde yön tersiydi (0.7391 vs 0.7314); o da gruplamanın etkisinin veri setine bağlı olduğunu ve yön bilinmeden raporlanamayacağını gösteriyor.

**Model tabanı ne kadar geçiyor:** altı özellikli model 0.8341, tek özellikli (`onceki_refleks_sayisi`) taban 0.7634. Yani diğer beş özellik **+0.071 AUC** katıyor — sentetik-yalnız sürümdeki +0.035'in iki katı, ama hâlâ mütevazı. Dürüst okunuşu değişmiyor: bu modelin öğrendiği şeyin büyük kısmı "refleks davranış tekrar eder"dir.

**Kesinlik duyarlılıktan önce geliyor** ve eşik bu yüzden 0.60, 0.50 değil. Yanlış pozitif, metni gerçekten okuyan bir öğrenciyi boşuna durdurmak demek; bu akışa zarar verir. Bedeli düşük duyarlılık (0.623): refleks kararların yaklaşık %38'i yakalanmıyor. Bu, bilinçli bir ödünleşim.

---

## 5. Sınırlar

1. **Azınlık sınıfı ağırlıkla sentetik (en önemli sınır).** Veri artık %77 gerçek, ama bu çoğunluk sınıfından geliyor: 39 "düşünerek" satırının yalnız **7'si gerçek**, 32'si sentetik. Model "düşünerek" davranışının neye benzediğini büyük ölçüde sentetik üreticiden, yani o davranış hakkındaki *varsayımlarımızdan* öğrendi. 0.8341 AUC bu yüzden yukarı yanlı okunmalıdır: ölçtüğü şeyin bir kısmı modelin sentetik üreticinin yapısını yakalama başarısıdır. Eşiği geçmesi kapıyı formel olarak açar, gerçek öğrenci davranışında aynı başarıyı kanıtlamaz.
2. **Bağımsızlık varsayımı tam karşılanmıyor.** Aynı kişinin birden çok oturumu var; gruplama oturum düzeyinde, kişi düzeyinde değil. Kişi düzeyinde gruplama daha doğru olurdu ama katılımcı sayısı 5 katlı çapraz doğrulama için az. Ayrıca ikinci toplama turunda üç katılımcı **`kisi_kodu` alanını boş bıraktı**, bu yüzden o 51 satırın kişi kimliği yalnız dosya bazında biliniyor — kişi düzeyinde gruplama artık veriden kurulamaz.
3. **1. karar noktasında model neredeyse kör.** Geçmişe dayalı dört özellik 0 olduğu için tahmin, sınıf başına taban orana yakın (~0.44) ve eşiği geçmiyor — yani duraklama pratikte hiç 1. sahnede açılmıyor. Bu kabul edildi: ilk karardan önce müdahale etmek için bir gerekçe de yok.
4. **`okuma_orani` okumayı değil ekranda geçen süreyi ölçüyor.** Telefonu bırakıp dönen, hızlı okuyan veya metni önceden görmüş öğrenci yanlış sınıflanır. `document.visibilityState` sekme arka plandayken sayacı durdurur ama kullanıcı ekrana bakmayı bıraktığını tarayıcıya bildirmez.
5. **`sahne_no` ile `oturum_gecen_sure_sn` korelasyonlu.** Eşdoğrusallık katsayı yorumunu zayıflatıyor; tahmin gücünü değil.
6. **200 kelime/dakika tek bir sabit.** Sınıfa, dile veya kişiye göre uyarlanmıyor.
7. **Dağıtım kayması izlenmiyor.** Senaryo metinleri değişirse `yeni_kelime_sayisi` tabanı değişir ve etiketin anlamı kayar. `sozlesme.py` → `YENI_KELIME` tablosu bu yüzden metinden ölçülerek yazıldı ve metin değişirse güncellenmesi gerekiyor.

---

## 6. Gizlilik

Eğitim verisinde kişisel veri **yok**: ad, e-posta, öğrenci numarası, konum, cihaz kimliği, IP ve zaman damgası hiç toplanmadı. `oturum_id` rastgele üretilir, `kisi_kodu` anonim bir ayrıştırıcıdır (`k1`, `k2`, `k3`) ve hangi kodun kime ait olduğunun hiçbir kaydı yoktur. Veri tarayıcıda üretilir ve kullanıcının kendi indirdiği CSV ile taşınır; sunucuya gönderilmez. Ayrıntı: [`data/SOZLUK.md`](../data/SOZLUK.md).

Zaman damgasının bilinçli olarak toplanmaması bir karardır: sıralama için `oturum_sira` yeterli, zaman damgası ise başka kayıtlarla eşleştirilerek yeniden kimliklendirmeye kapı bırakır.

## 7. Sürüm ve geri alma

Tüketiciler modeli `main` dalından değil **commit'e sabitlenmiş URL'den** indirir. Devreye alma (gölge → kanarya → aşamalı) ve geri alma planı: [`RELEASE.md`](../RELEASE.md).

Artefakt bayt düzeyinde tekrarlanabilirdir: aynı CSV + aynı tohum aynı `model.onnx` baytlarını üretir (`train.py` ONNX graph adını sabitler, çünkü `skl2onnx` oraya rastgele bir UUID yazıyor). Dolayısıyla commit pin'i gerçekten tek bir modeli işaret eder.
