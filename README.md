# Primer

**Yazılım mühendisliği öğrencileri için Sokratik kriz simülasyonu.**

## Teslim linkleri

| # | Ne | Link |
|---|---|---|
| 1 | **Repo** | <https://github.com/gonulnazire/primer> |
| 2 | **Çalışan uygulama** | <https://primer-1.ai.studio/> |
| 3 | **60 sn demo video** | *(yükleme sonrası eklenecek)* |

## Puanlama kalemleri nerede

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
| Uçtan uca test | **20/20 geçiyor** (13 simülasyon + 7 sohbet), 10 kabul örneğini karşılıyor |

Ayrıntı: [`TUTOR-EVAL.md`](./TUTOR-EVAL.md)

---

## Depo haritası

| Dosya | İçerik |
|---|---|
| [`spec.md`](./spec.md) | Problem tanımı, kapsam, mimari, üç senaryonun tam içeriği, 9 kabul örneği, Sokratik kurallar |
| [`DESIGN.md`](./DESIGN.md) | Tasarım ilkeleri, renk/tipografi token'ları, dört ekran, Stitch prompt'ları, üretim notları |
| [`TUTOR-EVAL.md`](./TUTOR-EVAL.md) | 20 oturumluk değerlendirme: etiket dağılımı, hata türleri, alıntılı örnekler |
| [`cypress/e2e/primer.cy.js`](./cypress/e2e/primer.cy.js) | 12 uçtan uca test |
| `uygulama/` | AI Studio'dan indirilen tek dosyalık sürüm |
| `stitch_.../` | Stitch ekran çıktıları (7 ekran) |
| `calisma/` | Teslim edilmeyen çalışma dosyaları: AI Studio prompt'u, ham eval koşumları |

---

## Testleri çalıştırma

```bash
npm install
npx cypress run
```

Testler yayındaki uygulamaya koşar (`baseUrl: https://primer-1.ai.studio`). Sokratik API çağrısı `cy.intercept` ile sabitlenir — testler modelin o anki metnine değil uygulamanın sözleşmesine bakar.

Koşum videoları `cypress/videos/` altında oluşur.

---

## Bilinen sınırlar

- **Sokratik uç noktası hız sınırlı.** Art arda hızlı oturumlarda model cevap veremeyebilir; uygulama bu durumda yedek soruyu gösterir. Beklenen davranıştır, hata değil.
- **S6 (kararı nitelememe) en zayıf kural.** 20 oturumun ikisinde model kararı yüklü sıfatlarla çerçeveledi. Prompt bir kez sertleştirildi; ikinci bir tur sertleştirme mümkün.
- **Sohbetteki e-posta doğrulanmıyor.** Girilen adres bir kimlik değil etiket; kimse kendini doğrulamıyor ve herkes aynı sunucu kotasını kullanıyor. Farklı e-postalar farklı cevap üretiyorsa bunun nedeni farklı hesaplar değil, her e-postanın kendi sohbet geçmişi olması.
- **E-posta hatalarında kullanıcı iki farklı uyarı görebilir.** Alan `<input type="email">` olduğu için çoğu yazım hatasında tarayıcının kendi doğrulaması devreye giriyor ve kullanıcı **tarayıcının dilinde** bir balon görüyor; uygulamanın Türkçe uyarısı yalnızca HTML5'e göre geçerli ama uygulamanın kuralına uymayan adreslerde (örn. nokta içermeyen alan adı) çıkıyor. Testlerle doğrulandı, düzeltilmedi — tutarlı Türkçe uyarı için native doğrulamayı kapatmak gerekirdi ki bu da erişilebilirlik açısından bedelli.
- **Sohbetin Sokratik kuralları ölçülmedi.** `TUTOR-EVAL.md`'deki 20 oturumluk değerlendirme simülasyonun sonuç ekranını ölçüyor; sohbet v2'de eklendiği için o ölçümün dışında kaldı.
- **Tek tema.** Açık tema ve tema değiştirici kapsam dışı bırakıldı.
