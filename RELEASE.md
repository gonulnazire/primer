# RELEASE.md — Primer v2.0 yayın, devreye alma ve geri alma

**Sürüm:** 2.0.0 · **Tarih:** 2026-11-01 · **Artefakt:** `model/model.onnx` (553 bayt, ONNX opset 18)
**İlgili belgeler:** [`spec.md`](./spec.md) §10 · [`model/README.md`](./model/README.md) (model kartı) · [`data/SOZLUK.md`](./data/SOZLUK.md)

---

## 1. v2.0'da ne değişti

v1 sabit kurallarla kişiselleşiyordu: profil cevapları metni ve Sokratik soruların derinliğini değiştiriyordu (`spec.md` §4). Hiçbir şey oyuncunun **davranışından** öğrenmiyordu.

v2 üçüncü bir katman ekliyor:

| | v1 | v2 |
|---|---|---|
| Dallanma | Deterministik karar ağacı | *değişmedi* |
| Sokratik geri bildirim | Canlı LLM (vekil üzerinden) | *değişmedi* |
| **Uyum** | yok | **`primer-refleks` — kendi eğittiğimiz lojistik regresyon, ONNX olarak tarayıcıda** |

Modelin tek yetkisi **yansıma duraklamasını** açmak: eşik geçilirse karar noktasına girişte tek bir Sokratik soru gösterilir ve seçenekler 3 saniye pasif kalır. Model hangi seçeneğin seçileceğine dair hiçbir şey yapamaz (`spec.md` §10.2).

**v1'in hiçbir teslimi bozulmadı.** v1 Cypress takımı (`primer.cy.js`, `sohbet.cy.js`) tek karakter değişmeden **20/20 geçiyor**; v2 testleri 14 testle ayrı dosyalarda.

---

## 2. Mimari dağıtım kararı ve ödünleşim matrisi

Model üç yerde çalışabilirdi. Dersin üç sorusuna göre değerlendirme:

| | **Tarayıcı** (`onnxruntime-web`, GitHub Pages) ✅ **seçildi** | **Cihaz içi mobil** (Expo + `onnxruntime-react-native`) | **Kendi sunucumuz** (Render.com, FastAPI / Rails `onnxruntime`) |
|---|---|---|---|
| **1. İnternet zorunlu mu, gecikme nasıl?** | İlk yüklemede ağ şart: `ort.min.js` **436 KB** + WASM çalışma zamanı **~11 MB** (ölçüldü). Sonrası tarayıcı önbelleğinden. Çıkarımın kendisi ~1 ms, ağ yok | Kurulumdan sonra **internetsiz çalışır**, çalışma zamanı APK içinde gömülü. Ama APK kurulumu gerekiyor | Her istekte ağ gecikmesi. Render ücretsiz katmanı uykuya geçiyor → ilk istek 20-50 sn |
| **2. Veri cihazdan çıkar mı?** | **Çıkmıyor.** Özellikler tarayıcıda hesaplanır, çıkarım tarayıcıda olur, hiçbir şey gönderilmez | Çıkmıyor | **Çıkıyor.** Her karar noktasının davranış verisi sunucuya gider |
| **3. Model gizli kalır mı?** | **Kalmıyor** — `model.onnx` istemciye iniyor ve indirilebilir | Kalmıyor (APK'dan çıkarılabilir) | Kalıyor; ama istek-yanıt üzerinden tersine mühendislik (REA) hâlâ mümkün |

### Neden tarayıcı

1. **Veri toplama kritik yolda.** Ödev en az 15 gerçek oturum istiyor. Pages linki bir mesajda paylaşılıyor; arkadaş telefonunda tek dokunuşla açıyor. APK kurulumu veya sunucu uyanma süresi bu adımı günlere yayardı.
2. **Gizlilik tarafı bedava geliyor.** `data/SOZLUK.md`'deki "hiçbir şey sunucuya gönderilmez" taahhüdü, sunucu tüketicisiyle doğrudan çelişirdi. Tarayıcıda çıkarım bu taahhüdü mimari olarak garanti ediyor, söz vererek değil.
3. **"Model gizli kalmıyor" bir bedel değil, zaten verilmiş bir karar.** Model Hugging Face'te **public** bir repoda yayınlanıyor (ödev gereği). Gizliliği korumaya çalışmak, aynı dosyayı herkese açık yayınlarken anlamsız olurdu.
4. **Ölçülmüş bir kısıt:** v1'in Sokratik uç noktası (`https://primer-1.ai.studio/api/socratic`) CORS başlığı döndürmüyor — `OPTIONS` yanıtında `Access-Control-Allow-Origin` yok. Yani ayrı origin'deki bir sayfa o uç noktayı çağıramaz. Bu, v2 sayfasının canlı Sokratik katmanı taşımamasının nedeni ve sayfada kullanıcıya açıkça yazılı.

### Kabul edilen bedeller

| Bedel | Büyüklük | Neden kabul edildi |
|---|---|---|
| İlk yükleme ~11.4 MB | ort.min.js 436 KB + WASM ~11 MB | **Modelin kendisi 553 bayt.** Yani maliyetin %99.99'u taşıyıcıda, modelde değil. Bir kez iniyor ve önbelleğe giriyor; çıkarım sonrasında ücretsiz |
| Model açıkta | 553 bayt | Zaten public HF reposunda yayınlanıyor |
| İnternetsiz çalışmıyor | — | Oturum 3-5 dakika ve zaten çevrimiçi paylaşılan bir linkten açılıyor |
| v2 sayfasında canlı Sokratik yok | — | CORS ölçümü (yukarıda); v1 uygulaması o katmanı taşımaya devam ediyor |

**Dürüst not:** 6 özellikli bir lojistik regresyon için 11 MB'lık bir çalışma zamanı taşımak, mühendislik olarak bakıldığında orantısız — aynı tahmin 10 satır JavaScript'le bir iç çarpım olarak yazılabilirdi. ONNX yine de kullanıldı, çünkü ödevin asıl kazanımı tek bir modelin **birden çok tüketicide aynı sonucu verdiğini kanıtlamak** (parite testi); elle yazılmış bir iç çarpım bu kanıtı veremez, çünkü iki uygulama arasındaki farkı değil, iki ayrı elle yazımı karşılaştırırdı.

---

## 3. Sürümleme: commit'e sabitlenmiş URL

Tüketiciler modeli **`main` dalından indirmez**. İndirme adresi `web/site.json`'da tutulur:

```
https://huggingface.co/<kullanici>/<repo>/resolve/<commit>/model.onnx
```

`main`'den indirmek, modelin herhangi bir anda haber vermeden değişmesi demek olurdu: aynı uygulama sürümü farklı kullanıcılarda farklı model çalıştırır ve parite testi hangi modeli ölçtüğünü bilemez.

**Artefakt bayt düzeyinde tekrarlanabilir.** Aynı CSV + aynı tohum (42) aynı `model.onnx` baytlarını üretir. (`skl2onnx` ONNX graph adına rastgele bir UUID yazıyordu; `train.py` bu adı sabitliyor. Bu düzeltme olmadan her eğitim farklı bayt üretir ve commit pin'i "hangi model" sorusunu cevaplamazdı.)

**Sürüm bilgisi toplanan veriye de yazılıyor:** `site.json` → `surum` alanı her CSV satırının `surum` sütununa geçiyor. Yani ileride elimizdeki her davranış satırı, hangi model sürümü devredeyken üretildiğini söylüyor. 3V'nin *Versioning* ayağı burada kapanıyor.

### Yayın adımları

```bash
# 1. Hugging Face hesabı + write token (hesap henüz açılmadı — aşağıdaki "Bekleyen" bölümüne bakın)
pip install -r requirements.txt
hf auth login

# 2. Public model reposu açıp artefaktları yükle
hf repo create primer-refleks-onnx --type model
hf upload <kullanici>/primer-refleks-onnx model/ . --repo-type model

# 3. Dönen commit hash'ini web/site.json'a yaz
#    "model_url": "https://huggingface.co/<kullanici>/primer-refleks-onnx/resolve/<commit>/model.onnx"
#    "model_pin": "<commit>"
```

---

## 4. Yeni sürümü güvenle devreye alma

Devreye alma durumu tek bir dosyada, `web/site.json`'da:

```json
{ "golge": true, "devreye_alma_orani": 0.0, "karar_esigi": 0.6, "model_pin": null }
```

Her adım **tek bir sayının değişmesi**, yani tek bir commit — dolayısıyla her adım geri alınabilir.

### Adım 1 — Gölge dağıtım (`golge: true`)

Model **çalışır**, tahmini `golge_tahmin` sütununa yazılır, **hiçbir müdahale yapılmaz**. Kullanıcı deneyimi v1 ile birebir aynıdır.

Bunun değeri şu: aynı CSV satırında hem modelin tahmini (`golge_tahmin`) hem de gerçekleşen sonuç (`refleks`) bulunuyor. Yani **karşılaştırma verisini gölge modun kendisi üretiyor** — çevrimdışı ölçtüğümüz 0.74 AUC'nin gerçek oturumlarda da tutup tutmadığı, hiç kimseyi etkilemeden ölçülebiliyor.

Bu davranış test edilmiş durumda: `cypress/e2e/v2-akis.cy.js` → *"gölge modunda model çalışır ama MÜDAHALE ETMEZ"*.

**Kanaryaya terfi koşulu (önceden yazılmış):** en az 15 gerçek oturumun gölge verisinde, eylem eşiğinde (0.60) **kesinlik ≥ 0.70**. Kesinlik seçildi çünkü buradaki asıl risk yanlış pozitif: metni okuyan öğrenciyi boşuna durdurmak.

### Adım 2 — Kanarya (`golge: false`, `devreye_alma_orani: 0.05`)

Oturumların **%5'inde** müdahale açılır. Kova, `oturum_id`'nin FNV-1a karmasından hesaplanır: aynı oturum sayfa yenilense bile aynı kovada kalır, yani kullanıcı oturum ortasında farklı bir deneyime düşmez.

İzlenecek: duraklama gösterilen oturumlarda terk oranı (3 kararın tamamlanmaması) artıyor mu.

### Adım 3 — Aşamalı geçiş (`0.25` → `0.50` → `1.0`)

Her basamakta aynı ölçüme bakılır. Basamaklar arasında en az 10 oturum beklenir.

### Geri alma (rollback)

Hafiften ağıra, hepsi tek commit:

| # | Yapılan | Etkisi |
|---|---|---|
| 1 | `devreye_alma_orani: 0` | Müdahale durur, model ölçmeye devam eder |
| 2 | `golge: true` | Tamamen gölgeye düşer |
| 3 | `model_pin` ve `model_url` önceki commit'e çevrilir | Önceki model sürümüne dönülür |
| 4 | `model_url: null`, `yerel_yedek: null` | Model hiç yüklenmez; uygulama **v1 davranışına** düşer |

4. seçenek kodda sessiz bir dal değil, **sınanmış bir yol**: `tahminEt()` null döndüğünde seçenekler açılır ve hiçbir müdahale yapılmaz (`web/index.html` → `uyumKatmani`). Yapılandırma dosyası hiç okunamazsa da aynı güvenli hale düşülür.

---

## 5. Bekleyen adımlar

| Ne | Durum | Kim |
|---|---|---|
| Hugging Face hesabı + write token | **bekliyor** — hesap açılacak | kullanıcı |
| `model_url` / `model_pin` doldurulması | HF yayınından sonra | yayın betiği |
| GitHub Pages'in açılması (`main` / kök) | bekliyor | kullanıcı |
| En az 15 gerçek oturum (3 kişi × 5) | bekliyor — veri toplama modu hazır | kullanıcı |
| Gerçek veriyle yeniden eğitim ve model kartının 3. bölümü | veri geldikten sonra | `veri_derle.py` + `train.py` |
| 60–90 sn demo video | bekliyor | kullanıcı |

HF yayını yapılana kadar `site.json` → `model_url: null` ve uygulama `yerel_yedek` (`../model/model.onnx`) ile çalışır. Parite testi bu haliyle de geçerlidir; yalnızca "commit'e sabitlenmiş URL" kalemi HF yayınını bekliyor.

### Yapılmadı: kendi sunucumuzda üçüncü tüketici (bonus)

Bir Render.com/FastAPI tüketicisi eklenmedi. Gerekçe: parite iddiası iki bağımsız çalışma zamanıyla (tarayıcı `onnxruntime-web` ve Python `onnxruntime`) zaten kanıtlanıyor; üçüncü bir tüketici aynı iddiayı güçlendirmez, yalnız tekrarlar. Ayrıca ücretsiz katmanın uyku davranışı, testleri zaman aşımına duyarlı hale getirirdi.

---

## 6. Kaynaklar

Bu belgedeki mimari tartışma şu kaynaklara dayanıyor:

- **Amershi vd. (2019),** *Software Engineering for Machine Learning: A Case Study* (Microsoft) — yaşayan ML yaşam döngüsü; veri toplamadan gözleme dönen döngü. Gölge dağıtımın "karşılaştırma verisini kendi üretmesi" fikri buradaki geri besleme halkasının somut hâli.
- **Shankar vd. (2022),** *Operationalizing Machine Learning: An Interview Study* — üretimde ML'in 3V problemi (Velocity, Validation, Versioning). Bu belgenin 3. ve 4. bölümleri sırasıyla Versioning ve Validation ayaklarına karşılık geliyor.
- **Breck vd. (2017),** *The ML Test Score* — üretime hazırlık rubriği. Buradan alınan iki madde: eğitim verisinin şema doğrulaması (`veri_derle.py` → `dogrula`) ve modelin basit bir taban çizgisiyle karşılaştırılması (tek özellikli taban, `model/README.md` §4).
- **Mitchell vd. (2019),** *Model Cards for Model Reporting* — `model/README.md` bu yapıyı izliyor.
- **Sommerville,** *Software Engineering* (10. baskı), Bl. 8 (Doğrulama ve Geçerleme) ve Bl. 25 (Konfigürasyon Yönetimi) — commit'e sabitleme ve geri alma planı konfigürasyon yönetimi başlığının doğrudan uygulaması.
- **Stanford HAI (2025),** *AI Index Report* — çıkarım maliyetlerinde 300 kat düşüş; **Gartner (2025)** — 2027'ye kadar göreve özel küçük modellerin genel amaçlı LLM'lerden 3 kat fazla kullanılacağı öngörüsü. Bu ödevin 553 baytlık modeli, aynı işi bir LLM çağrısıyla yapmanın alternatifi.
- **Hugging Face Hub** belgeleri (`revision`, `resolve` URL biçimi) · **ONNX Runtime** (`onnxruntime-web`) · **skl2onnx** (`zipmap` seçeneği) · **Cypress** (`cy.intercept` ile devreye alma yapılandırmasının sabitlenmesi).
