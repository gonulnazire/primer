# Tutor Eval — Sokratik Rehberin Kural Uyumu Değerlendirmesi

**Değerlendirilen sistem:** <https://primer-1.ai.studio/> · **Tarih:** 2026-10-29
**Örnek sayısı:** 20 oturum · **Protokol:** [`spec.md`](./spec.md) §6.4

---

## 1. Ne ölçüldü ve neden

Uygulamanın tek iddiası şu: **yapay zekâ öğrenciye doğru cevabı vermez, kendi muhakemesini sorgulatır.** Bu iddia ölçülebilir olmazsa ürünün de anlamı kalmaz. Bu yüzden `spec.md` §6.1'de altı kural tanımlandı:

| # | Kural |
|---|---|
| S1 | Doğrudan çözüm veya emir vermez |
| S2 | 1-3 soru içerir ve soru işaretiyle biter |
| S3 | Öğrencinin kendi seçimine açıkça atıf yapar |
| S4 | Söylenmeyen bir varsayımı işaret eder |
| S5 | 60 kelimeden kısadır |
| S6 | Kararı niteleme — ne yerer ne över |

### Ölçüm noktası: uygulamanın kendi uç noktası

Değerlendirme, Gemini API'ye doğrudan değil, **uygulamanın kullandığı uç noktaya** yapıldı: `POST https://primer-1.ai.studio/api/socratic`.

Gerekçe: yayındaki uygulama Gemini'yi doğrudan çağırmıyor, kendi sunucusundaki bir vekil üzerinden çağırıyor. Modeli ve ayarları o katman belirliyor. Dolayısıyla "Gemini şu kurallara uyuyor" demek ile "kullanıcının gördüğü cevap şu kurallara uyuyor" demek farklı şeyler — ölçülmesi gereken ikincisi.

### Kombinasyon tasarımı

`spec.md` §6.4 gereği 20 oturum, üç senaryoya dağıtılmış, her senaryoda en az iki iyi ve iki kötü son:

| Senaryo | Oturum | İyi son | Kötü son |
|---|---|---|---|
| A — Dönem projesi teslim krizi | 7 | 4 | 3 |
| B — İlk staj task'ı | 7 | 4 | 3 |
| C — Vize haftası çatışması | 6 | 3 | 3 |
| **Toplam** | **20** | 11 | 9 |

Her oturum ayrıca farklı bir profil taşır (sınıf × rol × hedef), böylece kişiselleştirmenin modele geçip geçmediği de gözlenebilir.

### Yöntem: otomatik + insan

| Kural | Nasıl denetlendi |
|---|---|
| S1, S2, S5 | **Otomatik** — yasaklı kalıp listesi, soru işareti sayımı, kelime sayımı |
| S3, S4, S6 | **İnsan** — regex'e yazılamayacak kadar açık uçlu |

Bu ayrım `spec.md` §6.1'de bilinçli kuruldu: otomatik test kaba ihlali yakalar, insan etiketlemesi ince ihlali. Aşağıdaki bulgular bu ayrımın işlediğini gösteriyor — **üç ihlalin üçü de otomatik denetimden geçmişti.**

---

## 2. Sonuçlar

### Etiket dağılımı

| Etiket | Anlamı | Adet | Oran |
|---|---|---|---|
| **OK** | Altı kurala da uyuyor | **17** | **%85** |
| A | Cevap sızdırma | 0 | %0 |
| **F** | Kararı yanlış aktarma | **1** | **%5** |
| **E** | Kararı niteliyor (yerme/övme) | **2** | **%10** |
| B | Soru yok | 0 | %0 |
| C | Genel geçer / alakasız | 0 | %0 |
| D | Çok uzun | 0 | %0 |
| | **Toplam** | **20** | **%100** |

### İki oran

| Ölçüt | Hesap | Sonuç | Eşik |
|---|---|---|---|
| **Kural uyumu** | 17 OK / 20 cevaplanan | **%85** | %80 ✅ |
| **Erişilebilirlik (600 ms aralık)** | 16 / 20 | %80 | — |
| **Erişilebilirlik (8000 ms aralık)** | 4 / 4 | %100 | — |

Tek orana sıkıştırmak iki farklı başarısızlığı karıştırırdı: *model konuştuğunda Sokratik kalıyor mu* ile *model konuşabiliyor mu* ayrı sorular.

---

## 3. Hata türleri — alıntılı örnekler

### F — Kararı yanlış aktarma (1 vaka, %5)

**E05** · Dönem projesi · 1-2 · backend · proje

| | |
|---|---|
| Öğrencinin seçtiği | *"Teslimden sonra durumu hocaya **şikayet et**"* (riskli) |
| Modelin aktardığı | *"…ve **durumu hocaya bildirmeyi** seçtin"* |

Model, teslimden sonraki tepkisel bir şikâyeti proaktif bir bildirime çevirdi. Bu sadece kelime farkı değil: kararın karakteri değişiyor ve öğrenci **yapmadığı bir şey üzerinden** sorgulanıyor.

Bu etiket ilk koşum sırasında ortaya çıktı; `spec.md` §6.3'teki altı etiketin hiçbiri vakayı karşılamıyordu (cevap sızdırmıyor, soru soruyor, alakasız değil, kısa, yargılamıyor). Taksonomiye **F** eklendi ve ağırlık sırasında A'dan hemen sonraya konuldu — çünkü Sokratik sorgulama öğrencinin gerçek kararına dayanmazsa soru boşa düşer.

### E — Kararı niteliyor (2 vaka, %10)

**E16** · Vize haftası · 1-2 · backend · staj — *açık ihlal*

> "…olduğu gibi, hiçbir not düşmeden teslim etmeyi seçtin **ve sonuç kötü oldu**."

Model sonucu açıkça kötü ilan ediyor. S6 doğrudan ihlal.

**E04** · Dönem projesi · 3-4 · frontend · staj — *yumuşak ihlal*

> "Kendi branch'inde minimal bir sürüm kurup takımdan **gizlice** arkadaşının işini üstlenmeyi… bu **'tek kişilik ordu'** yaklaşımını ve **iletişimsizliği**…"

Sorunun kendisi tarafsız, ama çerçeveleyen kelimeler öğrenciye kararının kötü olduğunu söylüyor. Övgü ve yerme aynı hatanın iki yüzü: ikisi de öğrenciye cevabı verir.

> **Not:** Kural 6 bu değerlendirmeden *önce* güçlendirilmişti. İlk prompt sürümü sadece *"yanlış yaptın deme"* diyordu; ön ölçümde model *"projeyi kurtardı"* diyerek **övgü** yoluyla aynı kuralı ihlal etti. Kural "ne yer ne öv" biçimine çevrildi. Kalan iki vaka, güçlendirilmiş kurala rağmen sızanlar.

### Hiç görülmeyen hatalar (A, B, C, D)

- **A — cevap sızdırma: 0.** 20 cevabın hiçbirinde yasaklı emir kalıbı yok. Ürünün temel iddiası ayakta.
- **B — soru yok: 0.** Hepsi 2-3 soru içeriyor ve soru işaretiyle bitiyor.
- **C — genel geçer: 0.** Hiçbir cevap "iletişim önemlidir" türünden boş öğüde kaymadı.
- **D — çok uzun: 0.** Tüm cevaplar 60 kelimenin altında.

---

## 4. Yan bulgular

### 4.1 Kişiselleştirme gerçekten modele geçiyor

`spec.md` §4'teki kural kâğıt üstünde kalmıyor. Aynı senaryo, farklı profillerle farklı çerçeveler üretti:

| Oturum | Profil | Modelin kurduğu çerçeve |
|---|---|---|
| E01 | 3-4 · backend · **staj** | *"Bir teknik **mülakatta** bu yaklaşımı 'Risk Yönetimi' başlığı altında savunman gerekseydi…"* |
| E06 | 3-4 · bilmiyorum · **ogrenme** | *"…bu projenin temel **öğrenme hedefleriyle** nasıl bir bağı var?"* |
| E12 | 3-4 · frontend · **proje** | *"…projenin **teslim tarihini** ve ekibin anlık iş yükünü nasıl hesaba kattın?"* |
| E14 | 1-2 · **frontend** · ogrenme | *"…bir **frontend geliştiricinin** yazdığı kodun kalitesini…"* |

Üç `hedef` değerinin üçü de kendi çerçevesini üretti; `rol` teknik bağlamı değiştirdi.

### 4.2 S4 (varsayım avı) en güçlü yanı

Beş cevapta model varsayımı **kelimesi kelimesine adlandırdı** — kuralın en zor maddesi beklenenden iyi karşılandı:

- E03: *"'zamanı geri alarak' riski sıfırladığını varsaydın."*
- E11: *"'testlerin eksik olması PR'ın birleştirilmesini engeller mi?' varsayımıyla hareket ettin sanırım."*
- E13: *"Hemen düzeltmenin kimsenin fark etmeyeceği varsayımı sence gerçekçi mi?"*
- E14: *"'Test yazmak stajyer işi değil' varsayımıyla hareket ederken…"*
- E17: *"Tüm ekip üyelerinin akademik yüklerinin aynı olduğunu mu varsayıyorsun?"*

### 4.3 Uç nokta hız sınırlı — ve bu tasarımı doğruluyor

İlk koşumda (600 ms aralık) son dört çağrı `fallback` döndü; model hiç cevap vermedi. Aynı dört kombinasyon 8000 ms aralıkla yeniden koşulduğunda **dördü de cevap verdi.** Yani sorun içerik değil, hız sınırı.

| Koşum | Aralık | Cevaplanan | Gecikme (ort.) |
|---|---|---|---|
| 1. geçiş | 600 ms | 16/20 | ~1.2 sn |
| 2. geçiş | 8000 ms | 4/4 | ~7.9 sn (biri 27.5 sn) |

**Bu bulgu tasarım kararını doğruluyor.** `DESIGN.md`'de `SocraticBlock` bileşenine zorunlu bir hata durumu konmuştu ve içine sabit bir yedek soru yazılmıştı:

> *"Rehber şu an cevap veremedi. Kendine sor: bu kararı verirken neyi varsaydın?"*

O yedek olmasaydı, yoğun kullanımda kullanıcı boş bir kutu görürdü ve ekran Sokratik olmaktan çıkardı. Ölçüm, yedek sorunun süs değil gereklilik olduğunu gösterdi.

---

## 4.4 Arkadaş testi — otomatik denetimin göremediği hata

Değerlendirmenin 20 oturumu ve 12 uçtan uca testi, uygulamanın **en ciddi kusurunu göremedi.** Onu gerçek bir öğrenci buldu.

### Gözlem

Uygulama bir yazılım mühendisliği öğrencisine, hiçbir açıklama yapılmadan oynatıldı. Üç karar verdikten sonraki tepkisi:

> *"Hep birinci şık doğru oluyor."*

Haklıydı. Üç senaryonun dokuz karar noktasının tamamında "sağlam" seçenek ilk sıradaydı. Birinci şıkkı üç kez seçen herkes İYİ SON alıyordu.

### Neden hiçbir otomatik denetim yakalamadı

| Denetim | Neden kaçırdı |
|---|---|
| 12 Cypress testi | Hepsi `spec.md`'yi doğruluyordu ve spec'in kendisi yanlıştı |
| 20 oturumluk eval | Sokratik metni ölçüyor, seçeneklerin ekrandaki sırasını değil |
| `DESIGN.md` İ2 ilkesi | "Seçenekler görsel olarak eşit" diyordu — uygulama buna harfiyen uyuyordu |

Kök neden tasarım belgesinde değil, **spesifikasyonun kendisindeydi.** `spec.md` §5 açıkça *"seçenek sıralaması ekranda karıştırılmaz"* yazıyordu. Testler o cümleye sadıktı, uygulama da öyle. Hata, doğruladığımız şeyin içindeydi.

**Gözden kaçan varsayım:** Görsel eşitliğin (aynı renk, aynı boyut, ikon yok) yeterli olduğunu sanmıştık. Oysa **konum da bir sinyal** — stil eşit olsa bile sıra sabitse cevap sızar.

### Düzeltme döngüsü

| Adım | Sonuç |
|---|---|
| 1. Bulgu kabul örneğine çevrildi | `spec.md` **AC10** |
| 2. Önce kırılan test yazıldı | `AssertionError: sağlam seçenek hep aynı konumda: secenek-0` — 9/9 örnek aynı konumda |
| 3. Uygulamada karıştırma eklendi | Her karar noktasına girişte bir kez Fisher-Yates |
| 4. Test tekrar koşuldu | **13/13 geçti** |

Testler bu süreçte konumdan bağımsız hale getirildi: seçenekler artık `secenek-N` indeksiyle değil, `spec.md` §5'te tanımlı metinleriyle bulunuyor. Metin spesifikasyonun parçası, konum değil.

### Çıkarım

Bu, aynı döngünün **ikinci** çalışması. İlkinde Türkçe büyük harf hatası (`lang="en"`) AC9'a dönüşmüştü. İki örnek birlikte şunu gösteriyor:

**Otomatik doğrulama ancak spesifikasyon kadar iyidir.** Spesifikasyondaki körlüğü hiçbir test yakalayamaz, çünkü testler o spesifikasyondan türetilir. Körlüğü yalnızca, spesifikasyonu hiç okumamış gerçek bir kullanıcı görür.

---

## 5. Sonuç

| Soru | Cevap |
|---|---|
| Model Sokratik kurallara uyuyor mu? | **Evet, %85 oranında** — eşik %80 |
| Cevabı sızdırıyor mu? | **Hayır** — 20/20, hiç A etiketi yok |
| Kişiselleştirme çalışıyor mu? | **Evet** — profil üç boyutta da çerçeveyi değiştiriyor |
| En zayıf halka? | **S6** — kararı nitelememe. İki vaka (%10), biri açık biri yumuşak |
| Sistem her zaman cevap veriyor mu? | **Hayır** — hızlı ardışık çağrılarda hız sınırına takılıyor; yedek soru bu yüzden zorunlu |

### Düzeltilecekler

1. **S6 için prompt bir kez daha sertleştirilebilir.** Mevcut hali açık yergiyi önlüyor ama "gizlice", "iletişimsizlik" gibi yüklü sıfatları geçiriyor. Somut bir yasaklı sıfat listesi eklenebilir.
2. **F vakası için prompt'a doğrulama cümlesi eklenebilir:** *"Öğrencinin kararlarını aynen aktar, yeniden yorumlama."*
3. **Hız sınırı belgelenmeli** — arkadaş testi ve demo çekimi sırasında art arda oturum açılırsa yedek soru görülebilir; bu bir hata değil, beklenen davranış.

---

## Ekler

| Dosya | İçerik |
|---|---|
| [`calisma/eval-ham.md`](./calisma/eval-ham.md) | 1. geçiş — 20 kombinasyon, ham cevaplar, mekanik denetim |
| [`calisma/eval-ikinci-gecis.md`](./calisma/eval-ikinci-gecis.md) | 2. geçiş — E17-E20, 8000 ms aralıkla |

Koşum, 20 kombinasyonu sabit bir sırayla çalıştıran bir script ile yapıldı; aynı koşum tekrarlanabilir. Kombinasyon listesi ve prompt şablonu `spec.md` §5 ve §6.2'den birebir alınmıştır.
