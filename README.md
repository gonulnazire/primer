# Primer

**Yazılım mühendisliği öğrencileri için Sokratik kriz simülasyonu.**

v1 öğrenciye kriz senaryolarında karar verdirip kendi varsayımını sorgulatıyor. **v2** buna, oyuncunun davranışından öğrenen ve bizim eğitip yayınladığımız **553 baytlık bir modeli** ekliyor: refleksle karar verileceğini öngörürse, o karardan önce bir *yansıma duraklaması* açıyor.

## Teslim linkleri — v2

| # | Ne | Link |
|---|---|---|
| 1 | **Repo** | <https://github.com/gonulnazire/primer> |
| 2 | **Hugging Face modeli (commit'li)** | <https://huggingface.co/gonulnazire/primer-refleks-onnx/tree/1e02139d1968b4cbad05a6893f32f7a570300a63> · repo kökü: <https://huggingface.co/gonulnazire/primer-refleks-onnx> |
| 3 | **Canlı uygulama (v2, GitHub Pages)** | <https://gonulnazire.github.io/primer/web/> |
| 4 | **60–90 sn demo video (v2)** | <https://youtube.com/shorts/ZswUKGP096k> |

## Teslim linkleri — v1

| # | Ne | Link |
|---|---|---|
| 1 | **Çalışan uygulama** | <https://primer-1.ai.studio/> |
| 2 | **60 sn demo video** | <https://youtube.com/shorts/akFFeEdus34> |

## Puanlama kalemleri nerede — v2

| Kalem | Puan | Nerede |
|---|---|---|
| Spec ve kabul örnekleri (eşik eğitimden önce tanımlı) | 10 | [`spec.md`](./spec.md) §10 model gereksinimi · §7 **AC11–AC13** |
| Veri (≥15 gerçek oturum), veri sözlüğü, `kaynak` sütunu | 10 | [`data/SOZLUK.md`](./data/SOZLUK.md) · `data/oturumlar.csv` · [`data/ham/`](./data/ham/) |
| Tekrarlanabilir eğitim ve eval kapısı | 15 | [`train.py`](./train.py) — tek komut, tohum 42, **AUC < 0.70 ise durur** |
| Somut artefakt ve sözleşme | 10 | `model/model.onnx` (553 bayt) · [`model/config.json`](./model/config.json) |
| Model kartı | — | [`model/README.md`](./model/README.md) |
| Yayın: HF reposu, commit'e sabit URL, ödünleşim matrisi, shadow/canary, rollback | 15 | [`RELEASE.md`](./RELEASE.md) |
| Uygulamada çıkarım (model kararı oyunun davranışını değiştiriyor) | 15 | [`web/index.html`](./web/index.html) — `onnxruntime-web`, yansıma duraklaması |
| Diferansiyel test (parite + tolerans) ve regresyon E2E | 15 | [`cypress/e2e/parite.cy.js`](./cypress/e2e/parite.cy.js) · [`tests/parite.py`](./tests/parite.py) · [`cypress/e2e/v2-akis.cy.js`](./cypress/e2e/v2-akis.cy.js) |
| Demo video, README, vize sınav tasarımı | 10 | bu dosya · [`SINAV_TASARIMI.md`](./SINAV_TASARIMI.md) |

**Test durumu: 34/34 geçiyor** — v1 regresyonu **20/20** (dosyalar değiştirilmedi) + v2 **14/14**.

Tam takım en son **2026-11-04**'te, **devreye alma tamamlandıktan sonra** koşuldu — yani `web/site.json` `golge: false` / `devreye_alma_orani: 1.0` haldeyken, model gerçekten müdahale ederken. v2'nin 14 testi **canlı GitHub Pages adresine karşı** koşuyor, yerel sunucuya değil: diferansiyel test, yayındaki tarayıcı çıkarımının Python kahiniyle `1e-4` içinde uyuştuğunu gösteriyor. Koşum 1 dk 26 sn sürdü; `cypress/videos/` altındaki videolar bu koşumdan.

```bash
npx cypress run -x v2Url=https://gonulnazire.github.io/primer/web/   # 34 test
```

**Devreye alma tamamlandı (2026-11-04).** Gölge → kanarya (%5) → %25 → %50 → %100; her basamak `web/site.json`'da tek bir sayının değiştiği ayrı bir commit, dolayısıyla her adım geri alınabilir ve git geçmişinde görünür. Kanaryaya terfi koşulu veri görülmeden önce yazılmıştı (eylem eşiğinde kesinlik ≥ 0.70) ve ölçüldü: **kesinlik 1.0000**, 65 oturum. İki çekincesi — temel oranın kesinliği kolaylaştırması ve gölge verisinin **önceki** model sürümünden gelmesi — [`RELEASE.md`](./RELEASE.md) §4'te açıkça yazılı.

## Puanlama kalemleri nerede — v1

| Kalem | Puan | Dosya |
|---|---|---|
| spec.md — problem, kapsam dışı, kabul örnekleri, akış şeması | 20 | [`spec.md`](./spec.md) · §1 problem · §2 kapsam dışı · §3 akış şeması · §7 **10 kabul örneği** |
| Tasarım — Stitch ekranları + DESIGN.md | 15 | [`DESIGN.md`](./DESIGN.md) · §4 ekranlar · §9 üretim notları · `stitch_*/` **7 ekran** |
| Çalışan uygulama — telefonda baştan sona | 20 | <https://primer-1.ai.studio/> |
| Tutor eval — 20 cevap, hata türleri, oran, örnek | 25 | [`TUTOR-EVAL.md`](./TUTOR-EVAL.md) · **%85 kural uyumu** |
| Cypress — tüm yollar E2E + demo video | 10 | [`cypress/e2e/primer.cy.js`](./cypress/e2e/primer.cy.js) · **20/20 geçiyor** (13 simülasyon + 7 sohbet) |
| Ürün kararı — 3 özellik + tek cümle neden | 10 | [Aşağıdaki tablo](#ürün-kararları--yapmadığım-üç-özellik) |

---

## Ne yapar

Öğrenci üç soruluk bir profil doldurur, kendi hayatından üç krizden birini seçer, içinde üç karar verir ve iki sondan birine ulaşır. Sonuç ekranında yapay zekâ **doğru cevabı söylemez** — verdiği kararlara atıf yapıp farkında olmadığı varsayımı sorgulatır.

İlham: Neal Stephenson, *The Diamond Age* — okuyucusuna uyum sağlayan ve cevap vermek yerine düşündüren "Primer".

### Üç senaryo

| Senaryo | Kriz |
|---|---|
| Dönem projesi teslim krizi | Teslime 48 saat, `main` bozuk, takım arkadaşı kayıp |
| İlk staj task'ın | Mentor izinde, düzeltme için canlı veriye dokunmak gerekiyor |
| Vize haftası | Üç sınav, bir grup ödevi ve kopya şüphesi |

### Çözdüğü problem

Öğrenci "kriz anında ne yapılır" **bilgisini** ediniyor ama o bilgiyi kullanacak **muhakemeyi** çalıştırmıyor. Sınav "rollback nedir" diye sorar; hayat "teslime 6 saat var, rollback mi yaparsın kapsamı mı kısarsın, neyi varsayıyorsun" diye sorar. Primer ikincisini sordurtur.

---

## v2 — davranıştan öğrenen uyum katmanı

### Model ne tahmin ediyor

**`refleks`:** öğrenci girdiği karar noktasında, metni okumadan karar verecek mi?

```
okuma_orani = min(1, metin_gorunur_sure_sn / (yeni_kelime_sayisi / 200 * 60))
refleks     = okuma_orani < 0.4
```

Eşik geçilirse uygulama o karardan **önce** tek bir Sokratik soru gösterir ve seçenekleri 3 saniye pasifler: *"Bu kararı vermeden önce: neyi varsayıyorsun?"*

### Neden "ipucu gerekli mi" değil

Başlangıç reposunun örneği *"bu oyuncunun ipucuna ihtiyacı var mı"*ydı. Bu üründe ipucu vermek, doğru cevabı sızdırmak demek — yani Primer'ın tek iddiasını çökertmek (`spec.md` §6.1 S1).

Bu yüzden modelin yetkisi kasıtlı olarak sınırlı: **ne zaman durulacağını söyler, ne seçileceğini söyleyemez.** Duraklama hiçbir seçeneği işaret etmiyor, öne çıkarmıyor, metni değiştirmiyor. Bir Cypress testi bunu doğruluyor: duraklama metni hiçbir seçeneğin metnini içermemeli (AC13).

Hedef seçiminin ikinci gerekçesi veriyle ilgili: satır birimi **karar noktası** olduğu için 15 oturum 45 satır veriyor. Oturum başına tek satır üreten bir hedef (ör. "kötü sona gider mi") 15 satırda kalır ve altı özelliği öğrenemez.

### Model nerede çalışıyor ve neden

Model, repo içindeki `web/index.html` sayfasında **tarayıcıda** çalışıyor (`onnxruntime-web`), v1'in AI Studio uygulamasında değil. Nedeni ölçülmüş bir kısıt: v1'in Sokratik uç noktası (`/api/socratic`) CORS başlığı döndürmüyor, dolayısıyla ayrı origin'deki bir sayfa o uç noktayı çağıramıyor. Ödünleşim matrisi ve üç dağıtım seçeneğinin karşılaştırması [`RELEASE.md`](./RELEASE.md) §2'de.

Sonuç: v1 uygulaması canlı Sokratik katmanı taşımaya devam ediyor, v2 sayfası model katmanını taşıyor ve bu sınır sayfada kullanıcıya açıkça yazılı.

### Ölçüm

| Ölçüt | Sonuç |
|---|---|
| ROC-AUC (gruplu, kat dışı) — **eval kapısı** | **0.8341** · eşik 0.70 |
| ROC-AUC (gruplamasız) | 0.8429 |
| Tek özellik tabanı (`onceki_refleks_sayisi`) | 0.7634 |
| Kesinlik / Duyarlılık @0.60 | 0.979 / 0.623 |
| ONNX / sklearn en büyük fark | 9.1e-08 (sınır 1e-4) |
| Tarayıcı / Python kahini en büyük fark | **< 1e-4** (AC12, Cypress) |

Üç dürüstlük notu, ayrıntısı [`model/README.md`](./model/README.md)'de:

1. **Azınlık sınıfı ağırlıkla sentetik.** Satırların %77'si gerçek (207/267), ama 39 "düşünerek" satırının yalnız 7'si gerçek. AUC bu yüzden yukarı yanlı okunmalı; ayrıntı model kartının 5. bölümünde.
2. **Çapraz doğrulama oturum bazında gruplanıyor.** Bir oturum 3 satır üretiyor ve bu satırlar bağımsız değil; gruplamazsak model eğitimde gördüğü oturumun kardeş satırını testte tahmin eder ve AUC sahte biçimde yükselir.
3. **Altı özelliğin katkısı mütevazı.** Tek özellikli taban 0.7634, tam model 0.8341 — yani öğrenilenin çoğu "refleks davranış tekrar eder".

### Sentetik veri üretici kuralı ve tohumu

**Tohum: 42.** Üretici (`data/veri_derle.py`): her sentetik kişiye `Beta(2.2, 2.0)` dağılımından bir `dikkat` tabanı verilir, oturum başına bu tabana `N(0, 0.12)` gürültü eklenir; sahne ilerledikçe %12 yorgunluk düşüşü ve `lognormal(0, 0.35)` acele çarpanı uygulanır; karar süresi = görünür süre + `Exp(1.2)`. Etiket, gerçek veriyle **aynı fonksiyondan** geçer (`sozlesme.py` → `refleks_mi`). Seçenek etiketi refleks kararlarda daha sık `riskli` çıkar — bu bir özellik değil, yalnız veriyi gerçekçi tutmak için.

Sentetik veri gerçeğin yerine geçmiyor: gerçek öğrenci davranışını değil, o davranış hakkındaki **varsayımlarımızı** kodluyor.

---

## Ürün kararları — yapmadığım üç özellik

| # | Yapmadığım özellik | Tek cümlelik gerekçe |
|---|---|---|
| 1 | Gerçek hesap sistemi (parola, oturum, kimlik doğrulama) | Simülasyonun değeri tek oturumda ortaya çıkıyor; kimlik doğrulamak öğrenmeye hiçbir şey katmazken altyapı maliyetini ve gizlilik yükünü getiriyor. |
| 2 | Sınıf arkadaşıyla skor karşılaştırma | Yarışma, Sokratik sorgulamanın yerini "doğru cevabı bulma" refleksine bıraktırır — ki bu, ürünün çözmeye çalıştığı problemin ta kendisidir. |
| 3 | Senaryo editörü | Üç sabit senaryo on kabul örneğinin tamamını karşılıyor; kimse başka senaryo yazmak istemeden yazma aracı yapmak, çözülmemiş bir problemi çözmektir. |

Üçü de zaman yetmediği için değil, **ürünün amacına ters düştüğü veya hiçbir şey eklemediği için** yapılmadı. Ayrıntılı gerekçeler aşağıda.

### 1. Gerçek hesap sistemi (parola, oturum, kimlik doğrulama)

Simülasyonun değeri tek oturumda, üç dakikada ortaya çıkıyor; kimlik doğrulamak öğrenmeye hiçbir şey katmazken altyapı maliyetini ve gizlilik yükünü getiriyor.

> Sohbette istenen e-posta buna aykırı değil: o bir **kimlik değil etiket**. Parola yok, doğrulama yok, sunucuda hesap yok. Yalnızca sohbet geçmişini tarayıcıda ayrıştırmaya yarıyor. Simülasyon tarafı hiçbir şey saklamıyor ve profil ekranı bunu açıkça söylüyor: *"Simülasyon cevapların kaydedilmiyor."*

### 2. Sınıf arkadaşıyla skor karşılaştırma

Yarışma, Sokratik sorgulamanın yerini "doğru cevabı bulma" refleksine bıraktırır — öğrenci kendi muhakemesini değil başkasının puanını kovalamaya başlar, ki bu ürünün çözmeye çalıştığı problemin ta kendisidir.

### 3. Senaryo editörü

Üç sabit senaryo on kabul örneğinin tamamını karşılıyor; editör, kullanıcısı olmayan bir özellik olurdu — kimse başka senaryo yazmak istemeden önce yazma aracı yapmak, çözülmemiş bir problemi çözmektir.

---

## Fikrimi değiştirdiğim karar: serbest sohbet

Bu bölüm listede değil çünkü **yapmayacağım dediğim ama sonra yaptığım** tek özellik.

**İlk kararım:** Serbest sohbet kapsam dışıydı. Gerekçem şuydu: *"deterministik test edilemez ve Cypress kalemini riske atar."*

**Gerekçenin neresi yanlıştı:** Sohbetin *içeriği* gerçekten deterministik değil — ama test edilmesi gereken şey içerik değil, sözleşme. Bu ayrımı Sokratik geri bildirim için zaten yapmıştım: testler metnin ne dediğine değil, "boş değil, soru içeriyor, yasaklı kalıp yok" kurallarına bakıyor. Aynı yaklaşım sohbete de uygulanabilirdi. Yani kendi mimarimde çözdüğüm bir problemi, başka bir özellik için çözülemez saymıştım.

**Bedeli neydi:** Sohbet, simülasyonun aksine kalıcı veri tutuyor — e-posta ve sohbet geçmişi tarayıcıda (`localStorage`), mesajlar sunucuda işleniyor. Bu, "hiçbir şey saklamıyoruz" iddiasını geçersiz kıldı. Üç şey yapmak zorunda kaldım:

1. Profil ekranındaki *"Cevapların kaydedilmiyor"* cümlesini düzelttim — artık *"Simülasyon cevapların kaydedilmiyor"* diyor, çünkü eski hali artık doğru değildi.
2. Sohbet alanına ne saklandığını söyleyen bir not ekledim.
3. Kullanıcının saklananı silebilmesi için "Sohbeti sıfırla" denetimi koydum.

**Çıkardığım ders:** Bir özelliği "test edilemez" diye kapsam dışı bırakmadan önce, test etmeyi *nasıl* düşündüğümü kontrol etmeliyim. Çoğu zaman test edilemez olan şey özellik değil, benim o an aklımdaki test yöntemi.

---

## Dikkate değer üç tasarım kararı

### Hibrit tutor mimarisi

Ödevin iki gereksinimi birbiriyle gerilimdeydi: değerlendirme canlı bir modelin kural uyumunu ölçmeyi istiyordu, uçtan uca testler ise deterministik davranış. Çözüm, sistemi ikiye ayırmak oldu:

| Katman | Nasıl | Neden |
|---|---|---|
| Dallanma (senaryo, seçenekler, sonlar) | Önceden yazılmış karar ağacı | Testler her koşumda aynı sonucu görmeli |
| Geri bildirim (Sokratik sorular) | Canlı model çağrısı | Ölçülecek bir davranış olmalı |

Testler geri bildirim metnini *içerik olarak* değil *kural olarak* doğruluyor: boş değil, soru içeriyor, yasaklı emir kalıbı yok.

### Seçenekler görsel olarak birebir aynı — ve sırası karışık

Karar ekranındaki üç seçenekte tik, renk, ikon, rozet veya boyut farkı yok **ve konumları sabit değil**.

İkinci kısım bir arkadaş testinden geldi. İlk sürümde yalnızca görsel eşitliği şart koşmuştum ve uygulama buna harfiyen uyuyordu — ama doğru seçenek her zaman ilk sıradaydı. Gerçek bir öğrenciye oynattım, ilk tepkisi şu oldu: *"hep birinci şık doğru oluyor."* Üç karar, kalıbı çözmesine yetti.

**Konum, stil kadar güçlü bir sinyal.** Gerekçe basit: öğrenci doğru cevabı ekrandan okuyabiliyorsa uygulamanın hiçbir anlamı kalmaz. Kural `spec.md`'ye AC10 olarak eklendi, bir Cypress testi yazıldı (önce kırıldı, düzeltmeden sonra geçti) ve seçenekler artık her karar noktasında karıştırılıyor.

### Model cevap veremediğinde ekran Sokratik kalır

Sokratik blok yüklenemezse sabit bir yedek soru gösteriliyor:

> *"Rehber şu an cevap veremedi. Kendine sor: bu kararı verirken neyi varsaydın?"*

Bu süs değil gereklilik çıktı: değerlendirme sırasında uç noktanın hız sınırlı olduğu ölçüldü (bkz. [`TUTOR-EVAL.md`](./TUTOR-EVAL.md) §4.3). Yedek soru olmasaydı yoğun kullanımda kullanıcı boş bir kutu görürdü.

---

## Sonuçlar

| Ölçüt | Sonuç |
|---|---|
| Sokratik kural uyumu | **%85** (17/20 oturum) — eşik %80 |
| Cevap sızdırma (en kritik hata) | **%0** — 20/20 |
| Kişiselleştirme | Profilin üç boyutu da modelin çerçevesini değiştiriyor |
| Uçtan uca test (v1) | **20/20 geçiyor** (13 simülasyon + 7 sohbet), v1'in 10 kabul örneğini karşılıyor |
| Uçtan uca test (v2) | **14/14 geçiyor** (3 parite + 11 akış/uyum), AC11–AC13'ü karşılıyor |
| Model eval kapısı (v2) | **AUC 0.8341** · eşik 0.70 · eşik altı sürüm yayınlanmıyor |
| Diferansiyel test (v2) | Tarayıcı ile Python kahini arasındaki en büyük fark **< 1e-4** |
| Devreye alma (v2) | Gölge → kanarya → **%100**, 4 basamak / 4 commit · terfi kapısı ölçüldü: kesinlik **1.0000** (65 oturum, eşik 0.70) |

Ayrıntı: [`TUTOR-EVAL.md`](./TUTOR-EVAL.md)

---

## Depo haritası

| Dosya | İçerik |
|---|---|
| [`spec.md`](./spec.md) | Problem tanımı, kapsam, mimari, üç senaryonun tam içeriği, **13 kabul örneği**, Sokratik kurallar, §10 model gereksinimi |
| [`DESIGN.md`](./DESIGN.md) | Tasarım ilkeleri, renk/tipografi token'ları, dört ekran, Stitch prompt'ları, üretim notları |
| [`TUTOR-EVAL.md`](./TUTOR-EVAL.md) | 20 oturumluk değerlendirme: etiket dağılımı, hata türleri, alıntılı örnekler |
| [`cypress/e2e/primer.cy.js`](./cypress/e2e/primer.cy.js) | v1 uçtan uca testler (13) — **v2'de değiştirilmedi**, regresyon kanıtı |
| [`cypress/e2e/sohbet.cy.js`](./cypress/e2e/sohbet.cy.js) | Sohbet sözleşmesi testleri (7) — **v2'de değiştirilmedi** |
| `uygulama/` | AI Studio'dan indirilen tek dosyalık sürüm |
| `stitch_.../` | Stitch ekran çıktıları (7 ekran) |
| `calisma/` | Teslim edilmeyen çalışma dosyaları: AI Studio prompt'u, ham eval koşumları |

### v2 dosyaları

| Dosya | İçerik |
|---|---|
| [`RELEASE.md`](./RELEASE.md) | v2.0 değişiklikleri, ödünleşim matrisi, gölge/kanarya/aşamalı geçiş, geri alma planı |
| [`SINAV_TASARIMI.md`](./SINAV_TASARIMI.md) | Vize sınav tasarımı düşünce egzersizi (1 sayfa) |
| [`sozlesme.py`](./sozlesme.py) | **Tek doğru kaynak:** sütun adları, özellik sırası, etiket kuralı, eşikler |
| [`train.py`](./train.py) | Tekrarlanabilir eğitim + eval kapısı + ONNX dışa aktarım |
| [`data/SOZLUK.md`](./data/SOZLUK.md) | Veri sözlüğü: 23 sütun, birimleri, etiket kuralı, KVKK notu |
| [`data/veri_derle.py`](./data/veri_derle.py) | Gerçek + sentetik veriyi birleştirir, şemayı ve etiketi doğrular |
| `data/ham/` | Uygulamadan indirilen ham oturum CSV'leri |
| `model/` | `model.onnx` · `config.json` (sözleşme) · `README.md` (model kartı) |
| [`web/index.html`](./web/index.html) | **Primer v2:** karar akışı + veri toplama modu + `onnxruntime-web` çıkarımı |
| [`web/site.json`](./web/site.json) | Devreye alma yapılandırması: model pin'i, eşik, gölge/kanarya oranı |
| [`tests/parite.py`](./tests/parite.py) | Test kahini (Python referans çıkarımı) |
| `tests/parite.json` | 5 referans girdi + kahinin olasılıkları + model sha256 |
| [`cypress/e2e/parite.cy.js`](./cypress/e2e/parite.cy.js) | Diferansiyel test (3) |
| [`cypress/e2e/v2-akis.cy.js`](./cypress/e2e/v2-akis.cy.js) | v2 akış + uyum katmanı testleri (11) |

---

## Kurulum (3 komut)

```bash
npm install                                   # Cypress
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt   # Linux/mac: .venv/bin/pip
python train.py                               # veri -> eval kapısı -> model/
```

`train.py` için veri gerekiyor; depo veriyle birlikte geliyor. Sıfırdan derlemek istenirse:

```bash
python data/veri_derle.py --sentetik 20       # ham gerçek CSV'ler + sentetik -> data/oturumlar.csv
```

> **Python sürümü:** Başlangıç reposu 3.12 hedefliyor; bu depo **Python 3.14.2** ile kuruldu ve `scikit-learn 1.9.1` / `skl2onnx 1.20.0` / `onnxruntime 1.31.1` sorunsuz çalışıyor. Belgelerdeki tüm ölçümler o yorumlayıcıyla alındı (`model/config.json` → `egitim.surumler`).

> **Windows'ta bir tuzak:** Smart App Control açıkken `pandas 3.1.0`'ın `reshape.cp314-win_amd64.pyd` dosyası hash bazında engellenebiliyor ve `train.py` `DLL load failed while importing reshape` hatasıyla düşüyor. Çare **`pandas==3.0.5`** kurmak; aynı sürümü yeniden kurmak işe yaramaz, çünkü dosya bayt bayt aynı olduğu için aynı verdikti alır. Smart App Control'ü kapatmak geri alınamaz bir işlem olduğu için önerilmiyor. `requirements.txt` pandas'ı kasıtlı olarak sabitlemiyor: pandas yalnız ham CSV'leri birleştiriyor, metriğe etkisi yok — sabitlemek herkesi Windows'a özgü bir engel yüzünden eski sürüme zorlardı.

## Testleri çalıştırma

```bash
# tüm takım (34 test) — videoları yenileyen koşum budur
npx cypress run -x v2Url=https://gonulnazire.github.io/primer/web/
```

> **`--spec` ile alt küme koşmak commit'li videoları siler.** Cypress her koşumdan önce `videosFolder`'ı boşaltıyor (`trashAssetsBeforeRuns` varsayılanı), dolayısıyla alt küme koşumu **koşulmayan spec'lerin videolarını** siler — ki bu depoda videolar teslim kanıtı. Alt kümeyi yalnız videolar umurunda değilken koş; silinirse `git checkout -- cypress/videos/` geri getirir. (`trashAssetsBeforeRuns: false` denendi ve geri alındı: silmeyi durduruyor ama üzerine yazmak yerine `ad (1).mp4` kopyası üretiyor, yani takip edilen videolar bayatlıyor. Gerekçe `cypress.config.js`'te yazılı.)

Alt kümeleri ayrı ayrı koşmak gerekirse:

```bash
# v1 regresyonu — yayındaki AI Studio uygulamasına koşar (20 test)
npx cypress run --spec "cypress/e2e/primer.cy.js,cypress/e2e/sohbet.cy.js"

# v2 — model katmanı testleri (14 test); hedef varsayılan olarak yerel sunucu
npm run v2          # ayrı terminalde: http://localhost:4173/web/
npx cypress run --spec "cypress/e2e/parite.cy.js,cypress/e2e/v2-akis.cy.js"
```

İki ayrı hedef var ve bu kasıtlı: v1 spec'leri `baseUrl` ile **yayındaki uygulamaya**, v2 spec'leri `Cypress.expose('v2Url')` ile **GitHub Pages sayfasına** (veya yerel sunucuya) koşuyor. v1 dosyalarının yayına koşmaya devam etmesi regresyon kanıtının ta kendisi.

Sokratik API çağrısı `cy.intercept` ile sabitlenir — testler modelin o anki metnine değil uygulamanın sözleşmesine bakar. v2'de aynı teknik devreye alma yapılandırması için de kullanılıyor: `site.json` stub'lanarak gölge/kanarya modları test ediliyor, yani uygulamada **test için açılmış bir arka kapı yok**.

Model tarafı doğrulaması:

```bash
python train.py --esik 0.99        # eval kapısının kapattığını gösterir: çıkış kodu 2, model/ değişmez
python tests/parite.py             # test kahini kayıtlı olasılıklarla tutarlı mı
python tests/parite.py --yaz       # model yeniden eğitildiyse referansı yenile
```

Koşum videoları `cypress/videos/` altında oluşur.

---

## Bilinen sınırlar

- **Sokratik uç noktası hız sınırlı.** Art arda hızlı oturumlarda model cevap veremeyebilir; uygulama bu durumda yedek soruyu gösterir. Beklenen davranıştır, hata değil.
- **S6 (kararı nitelememe) en zayıf kural.** 20 oturumun ikisinde model kararı yüklü sıfatlarla çerçeveledi. Prompt bir kez sertleştirildi; ikinci bir tur sertleştirme mümkün.
- **Sohbetteki e-posta doğrulanmıyor.** Girilen adres bir kimlik değil etiket; kimse kendini doğrulamıyor ve herkes aynı sunucu kotasını kullanıyor. Farklı e-postalar farklı cevap üretiyorsa bunun nedeni farklı hesaplar değil, her e-postanın kendi sohbet geçmişi olması.
- **E-posta hatalarında kullanıcı iki farklı uyarı görebilir.** Alan `<input type="email">` olduğu için çoğu yazım hatasında tarayıcının kendi doğrulaması devreye giriyor ve kullanıcı **tarayıcının dilinde** bir balon görüyor; uygulamanın Türkçe uyarısı yalnızca HTML5'e göre geçerli ama uygulamanın kuralına uymayan adreslerde (örn. nokta içermeyen alan adı) çıkıyor. Testlerle doğrulandı, düzeltilmedi — tutarlı Türkçe uyarı için native doğrulamayı kapatmak gerekirdi ki bu da erişilebilirlik açısından bedelli.
- **Sohbetin Sokratik kuralları ölçülmedi.** `TUTOR-EVAL.md`'deki 20 oturumluk değerlendirme simülasyonun sonuç ekranını ölçüyor; sohbet v2'de eklendiği için o ölçümün dışında kaldı.
- **Tek tema.** Açık tema ve tema değiştirici kapsam dışı bırakıldı.

### v2 sınırları

- **Model gerçek veriyle eğitildi, ama azınlık sınıfı ağırlıkla sentetik.** 69 gerçek oturum / 207 gerçek satır + 60 sentetik satır. 39 "düşünerek" satırının yalnız 7'si gerçek olduğu için model bu sınıfı büyük ölçüde sentetik üreticiden öğrendi; sentetik veri gerçek davranışı değil onun hakkındaki varsayımlarımızı kodluyor. `model/config.json` → `veri.gercek_oturum` o anki gerçek sayıyı taşıyor.
- **11 MB'lık çalışma zamanı, 553 baytlık model.** `onnxruntime-web` ilk yüklemede ~11.4 MB indiriyor (ölçüldü). Aynı tahmin 10 satır JavaScript'le yazılabilirdi; ONNX yine de kullanıldı çünkü ödevin asıl kazanımı tek modelin birden çok tüketicide aynı sonucu verdiğini kanıtlamak. Gerekçe [`RELEASE.md`](./RELEASE.md) §2'de.
- **v2 sayfasında canlı Sokratik geri bildirim yok.** v1'in `/api/socratic` uç noktası CORS başlığı döndürmüyor; ayrı origin çağıramıyor. Sayfa yedek soruyu gösteriyor ve bu sınırı kullanıcıya söylüyor.
- **`okuma_orani` okumayı değil ekranda geçen süreyi ölçüyor.** Hızlı okuyan veya telefonu bırakıp dönen öğrenci yanlış sınıflanabilir.
- **1. karar noktasında model pratikte kör.** Geçmişe dayalı dört özellik 0 olduğu için tahmin taban orana yakın çıkıyor ve eşiği geçmiyor; duraklama ilk kararda hiç açılmıyor. Kabul edildi — ilk karardan önce müdahale için gerekçe de yok.
- **Çapraz doğrulama oturum bazında gruplanıyor, kişi bazında değil.** Kişi düzeyinde gruplama daha doğru olurdu ama 3 katılımcıda 5 katlı doğrulama kurulamaz.
- **Kendi sunucumuzda üçüncü tüketici (bonus) yapılmadı.** Parite iki bağımsız çalışma zamanıyla kanıtlanıyor; gerekçe [`RELEASE.md`](./RELEASE.md) §5'te.

---

## Araç beyanı

Bu ödevde yapay zekâ kodlama ajanı (**Claude Code**) kullanıldı. Hangi adımda ne yaptığı ve nereye elle müdahale edildiği:

1. **Spec, veri sözlüğü, model kartı ve `RELEASE.md` metinleri** ajanla yazıldı; kararların kendisi (model hedefi, çıkarımın nerede çalışacağı, hangi özelliklerin dışarıda kalacağı) tartışılarak verildi ve her birinin gerekçesi belgelere işlendi.
2. **İki tasarım hatası ajanla yapılan ölçüm sonucu düzeltildi, veri toplanmadan önce:** (a) `secim_degistirme` özelliği v1'in tek dokunuşlu akışında ölçülemiyordu, yerine `oturum_gecen_sure_sn` kondu; (b) etiket kuralı iki koşulluydu (`süre < 6 AND oran < 0.5`) ama 390×844 ekranda ikinci koşul bağımsız olarak bağlamıyordu, kural orana indirgendi. İkisinin gerekçesi `spec.md` §10.4 ve `data/SOZLUK.md`'de yazılı.
3. **`train.py`'nin ürettiği ONNX her koşumda farklı bayt veriyordu.** Sebep ajanla bulundu: `skl2onnx` graph adına rastgele UUID yazıyor, ağırlıklar aynı. Graph adı sabitlendi; artefakt artık bayt düzeyinde tekrarlanabilir.
4. **Cypress 16 `Cypress.env()`'i kaldırmış.** Hata alındıktan sonra doğru API (`expose`/`Cypress.expose`) tahminle değil kurulu paketin tip tanımları okunarak bulundu.
5. **Bir gerçek açık testler sayesinde kapandı:** seçenekler çıkarım bitmeden aktif olduğu için çok hızlı dokunan oyuncu duraklamayı atlayabiliyordu — ki modelin hedeflediği oyuncu tam olarak o. Seçenekler artık çıkarım bitene kadar pasif.

Ölçüm sonuçları (AUC, parite farkları, indirme boyutları, CORS başlıkları) ajana sorularak değil, komut çalıştırılarak elde edildi; bu dosyadaki her sayı bir koşumun çıktısıdır.
