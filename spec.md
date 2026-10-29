# spec.md — "Primer" Kişiselleştirilmiş Öğrenme Simülasyonu

**Proje:** Mobil Uygulama Geliştirme dersi ödevi
**Sürüm:** 1.0
**Tarih:** 2026-10-29

---

## 1. Problem Tanımı

### Kim için
Yazılım mühendisliği öğrencisi (1-4. sınıf), mobil telefonda, tek oturumda 3-5 dakika.

### Çözülen problem
Öğrenci "kriz anında ne yapılır" **bilgisini** ediniyor; dersten, videolardan, arkadaşından. Ama o bilgiyi kullanacak **muhakemeyi** hiç çalıştırmıyor.

Klasik anlatım ve sınav bu boşluğu kapatmıyor, çünkü yanlış şeyi ölçüyor:

| Sınavda sorulan | Gerçekte gereken |
|---|---|
| "Rollback nedir?" | "Teslime 6 saat var, main bozuk, takım arkadaşın kayıp — rollback mi yaparsın, kapsamı mı kısarsın? Neyi varsayıyorsun?" |
| "Kod etiği nedir?" | "Grup arkadaşının kodunu internette buldun. Ne yapacaksın, kime karşı sorumlusun?" |

Sonuç: öğrenci ilk gerçek krizde donup kalıyor veya refleksle en kötü seçeneği alıyor.

### Çözüm
Öğrencinin kendi hayatından üç krizi oynatan, karar verdiren bir mobil simülasyon. Uygulama **doğru cevabı vermez**. Seçim yaptırır, seçimin sonucunu gösterir, ardından Sokratik sorularla öğrenciyi kendi kararını sorgulamaya yönlendirir.

İlham: Neal Stephenson, *The Diamond Age* — "The Primer", okuyucusuna uyum sağlayan ve cevap vermek yerine düşündüren kitap.

### Başarı ölçütü
1. Bir oturum telefonda baştan sona, hatasız, 3-5 dakikada tamamlanabiliyor.
2. Kullanıcı sonuç ekranında en az bir kez kendi varsayımını fark ediyor. *Doğrulama yöntemi: arkadaş testinde sözlü geri bildirim ("şunu hiç düşünmemiştim" cümlesi veya eşdeğeri).*
3. Sokratik geri bildirim, 20 örneklik değerlendirmede en az **%80 oranında** kurallara uyuyor (bkz. Bölüm 6).

---

## 2. Kapsam

### Kapsam içi (MVP)
- 4 ekranlı interaktif akış (minimum gereksinim 3 ekran).
- Açılışta 3 soruluk profil alımı ve profilin akış içeriğine etkisi.
- 3 senaryo, her birinde 3 karar noktası, her kararda 3 seçenek.
- İki farklı son: iyi son / kötü son.
- Canlı LLM'den gelen Sokratik geri bildirim.
- Cypress ile uçtan uca test, 60 saniyelik demo video.
- **Serbest sohbet (v2'de eklendi)** — simülasyon bittikten sonra kullanıcının
  rehberle konuşmaya devam edebildiği, e-posta ile ayrışan bir sohbet.

### Kapsam genişlemesi: serbest sohbet (v2, 2026-10-29)

Spec'in ilk sürümü serbest sohbeti açıkça **kapsam dışı** bırakmıştı. Gerekçe şuydu: *"deterministik test edilemez ve Cypress kalemini riske atar."* Geliştirme sırasında bu karar değiştirildi ve sohbet eklendi.

**Gerekçenin yanlış olan kısmı:** Sohbetin *içeriği* gerçekten deterministik değil — ama test edilmesi gereken şey içerik değil, sözleşme. Sokratik blok için zaten bu ayrımı yapmıştık (§8: "testler modelin o anki çıktısına değil uygulamanın sözleşmesine bakar"); aynı yaklaşım sohbete de uygulanabilir. İlk gerekçe, kendi mimarimizde çözdüğümüz bir problemi çözülemez saymıştı.

**Kabul edilen bedel:** Sohbet, simülasyonun aksine kalıcı veri tutuyor. Bu, aşağıdaki iki kapsam dışı maddesini kısmen geçersiz kılıyor ve dürüstçe belirtilmesi gerekiyor:

| Veri | Nerede | Simülasyon | Sohbet |
|---|---|---|---|
| Profil cevapları (sınıf, rol, hedef) | bellek | saklanmıyor | — |
| Kararlar | bellek | saklanmıyor | — |
| E-posta | `localStorage` → `primer_user_email` | — | **saklanıyor** |
| Sohbet geçmişi | `localStorage` → `primer_chat_<eposta>` | — | **saklanıyor** |
| Mesajlar | sunucuya gönderiliyor (`POST /api/chat`) | — | **gönderiliyor** |

Bu yüzden profil ekranındaki bilgilendirme "Cevapların kaydedilmiyor" yerine **"Simülasyon cevapların kaydedilmiyor"** olarak düzeltildi, ve sohbet alanına ne saklandığını söyleyen ayrı bir not ile "Sohbeti sıfırla" denetimi eklendi. Kullanıcıya yanlış bir şey söylememek, kapsam değişikliğinin en önemli parçasıydı.

### Kapsam dışı (gerekçeleriyle)
Her madde bilinçli bir üründen feragat; README'deki "yapmadığım özellikler" bölümü bu listeyle birebir tutarlı olacak.

| Yapılmayan | Tek cümlelik gerekçe |
|---|---|
| Hesap / giriş sistemi | Parola, oturum ve kimlik doğrulama yok; sohbetteki e-posta bir **kimlik değil etiket**tir (bkz. §9). |
| Simülasyonun kaydedilmesi | Profil ve kararlar kalıcı tutulmuyor; her oturum sıfırdan başlıyor. Yalnızca sohbet veri saklıyor. |
| Sınıf arkadaşıyla skor karşılaştırma | Yarışma, Sokratik sorgulamanın yerini "doğru cevabı bulma" refleksine bıraktırır; ürünün amacına ters. |
| Ses efekti ve animasyon | 60 saniyelik demoda ölçülen şey akışın çalışması, cilası değil. |
| Senaryo editörü | Üç sabit senaryo kabul örneklerini karşılıyor; editör, kullanıcısı olmayan bir özellik olur. |
| ~~Tutor ile serbest sohbet~~ | **v2'de kapsama alındı** — ilk gerekçe hatalıydı, bkz. yukarıdaki kapsam genişlemesi. |
| Native mağaza paketleme | Web tabanlı mobil görünüm ödev gereksinimini karşılıyor. |

---

## 3. Mimari ve Akış

### Ekran akışı

```
┌──────────────┐
│ E1 Profil    │  sınıf · hedef rol · hedef
└──────┬───────┘
       │ (3 alan da dolu)
       ▼
┌──────────────┐
│ E2 Menü      │  3 senaryo kartı
└──────┬───────┘
       │ senaryo seçimi
       ▼
┌──────────────────────────────────┐
│ E3 Kriz & Karar                  │
│  karar 1 → karar 2 → karar 3     │  geri dönüş yok
└──────┬───────────────────────────┘
       │ kararlar[3]
       ▼
┌──────────────────────────────────┐
│ E4 Sonuç & Sokratik              │
│  iyi son / kötü son              │
│  + canlı Sokratik geri bildirim  │
└──────┬───────────────────────────┘
       │ "baştan başla" (profil korunur)
       └──────────────▶ E2
```

### Hibrit tutor mimarisi

Uygulama iki ayrı katmandan oluşur. Bu ayrım kasıtlı ve ödevin iki gereksinimi arasındaki gerilimi çözmek için var:

| Katman | Nasıl çalışır | Neden böyle |
|---|---|---|
| **Dallanma katmanı** (senaryo metni, seçenekler, sonlar) | Önceden yazılmış, deterministik karar ağacı | Cypress her çalıştırmada aynı sonucu görmeli; "iyi son / kötü son" testi kesin olmalı |
| **Geri bildirim katmanı** (Sokratik sorular) | Canlı LLM çağrısı, Bölüm 6.2'deki prompt ile | Tutor Eval'de ölçülecek bir şey olması için modelin gerçekten cevap üretmesi gerekiyor |

**Sonuç:** Cypress, geri bildirim metnini *içerik olarak* değil *kural olarak* test eder (boş değil, soru içeriyor, yasaklı emir kalıbı yok). Testlerde LLM çağrısı `cy.intercept` ile sabit bir cevaba bağlanır.

### Durum (state)

```
profile = { sinif: "1-2" | "3-4",
            rol:   "frontend" | "backend" | "bilmiyorum",
            hedef: "staj" | "proje" | "ogrenme" }

run = { senaryoId: "donem-projesi" | "staj-task" | "vize-haftasi",
        kararlar: [ "saglam" | "orta" | "riskli", ... ] }   // 3 eleman
```

Kalıcı depolama yok; `run` "baştan başla" ile sıfırlanır, `profile` korunur.

### Sonuç hesabı

Her seçenek üç etiketten birini taşır: **sağlam**, **orta**, **riskli**. Etiketler kullanıcıya gösterilmez.

**Son belirleme kuralı:** 3 kararın **en az 2'si "sağlam" ise İYİ SON**, aksi halde **KÖTÜ SON**.

Sonuç ekranında kullanıcıya yalnızca `sağlam karar sayısı / 3` gösterilir (ör. "2/3 sağlam karar") — yani dallanmayı belirleyen sayının ta kendisi. Ağırlıklı puanlama (sağlam +1, riskli −1 gibi) bilinçli olarak **kullanılmadı**: hiçbir kararı etkilemediği için ölü bir kavram olurdu ve negatif toplamların ekranda nasıl gösterileceği ayrı bir belirsizlik yaratırdı. Sayıma dayanmak deterministik, tek cümleyle ifade edilebilir ve Cypress'te tek koşulla doğrulanabilir. Üçüncü bir "orta son" MVP kapsamı dışında bırakıldı.

---

## 4. Kişiselleştirme

Menü seçimi **hangi** senaryonun oynandığını belirler. Profil cevapları **o senaryonun içeriğini** belirler. Profil hiçbir yerde yalnızca hitap/süs olarak kullanılmaz.

| Profil alanı | Akışta ne değişir |
|---|---|
| **hedef rol** | Krizin teknik detayı. Dönem projesi senaryosunda: `backend` → son migration veritabanını kilitledi; `frontend` → build pipeline kırıldı, `npm run build` hata veriyor; `bilmiyorum` → nötr anlatım ("proje artık açılmıyor, hata mesajı anlaşılmaz") |
| **sınıf** | Sokratik soruların derinliği. `1-2` → yönlendirici ("Bu kararı vermek için hangi bilgi sende yoktu?"); `3-4` → açık uçlu ("Bu kararın bedelini kim ödüyor?") |
| **hedef** | Sonuç ekranının çerçevesi. `staj` → "Bunu bir mülakatta nasıl anlatırdın?"; `proje` → teslim üzerindeki somut etki; `ogrenme` → kararın bağlı olduğu kavram |

---

## 5. Senaryolar

Üç senaryo da aynı iskelete sahiptir: kurulum metni → 3 karar noktası → son. Etiketler (sağlam/orta/riskli) kullanıcıya **gösterilmez**.

**Seçenek sırası her karar noktasında karıştırılır.** Aşağıdaki tablolardaki sıra veri sırasıdır, ekran sırası değildir.

> **Bu kural bir arkadaş testi sonucunda eklendi.** Spec'in ilk sürümü "seçenek sıralaması karıştırılmaz" diyordu. Gerçek bir öğrenciye oynatıldığında ilk tepkisi şu oldu: *"hep birinci şık doğru oluyor."* Üç karar noktası, cevabı ekrandan okumayı öğrenmesine yetti.
>
> Gözden kaçan varsayım şuydu: §6'daki görsel eşitlik kısıtını (aynı renk, aynı boyut, ikon yok) yeterli sandık. Oysa **konum da bir sinyal.** Stil eşit olsa bile sıra sabitse cevap yine sızar ve öğrenci düşünmeyi bırakıp kalıbı oynar — ki bu, ürünün çözmeye çalıştığı problemin ta kendisi. Kural **AC10** olarak kabul örneklerine eklendi.
>
> Karıştırma, karar noktasına **girişte bir kez** yapılır; her yeniden çizimde değil. Aksi halde seçenekler kullanıcının gözü önünde yer değiştirir.

### 5.1 Senaryo A — Dönem projesi teslim krizi (`donem-projesi`)

**Kurulum:** Teslime 48 saat kaldı. Üç kişilik takımdasınız. `main` branch çalışmıyor. Takım arkadaşlarınızdan biri iki gündür mesajlara cevap vermiyor. Hoca sunumda canlı demo bekliyor.
*Rol uyarlaması:* bkz. Bölüm 4.

| Karar | Seçenekler | Etiket |
|---|---|---|
| **A1** — Bozuk `main` ile ne yapacaksınız? | Son çalışan commit'e dön, kaybolan işi sonra ekle | sağlam |
| | Gece boyu hatayı debug et, çözene kadar uğraş | riskli |
| | Kendi branch'inde minimal çalışan bir sürüm kur | orta |
| **A2** — Kayıp takım arkadaşı | Arkadaşına net bir süre veren son bir mesaj at, cevap gelmezse hocaya bildir | sağlam |
| | Hiçbir şey söylemeyip onun işini de sen yap | riskli |
| | Teslimden sonra durumu hocaya şikayet et | riskli |
| **A3** — Teslim kapsamı | Çalışan 3 özelliği cilala, eksikleri sunumda açıkça söyle | sağlam |
| | 8 özelliğin hepsini yarım bırak, demoda hızlı geç | riskli |
| | Demoyu video olarak çek, canlı gösterim riskinden kaç | orta |

**Sonlar:**

| Son | Metin |
|---|---|
| İyi | "Proje teslim edildi. Hoca eksikleri biliyordu, demo canlıda çalıştı." |
| Kötü | "Demo sunumda çöktü. Hoca projeyi değil, hazırlıksızlığı gördü. Takım arkadaşın hiç ortaya çıkmadı." |

### 5.2 Senaryo B — İlk staj task'ı (`staj-task`)

**Kurulum:** Stajınızın ikinci haftası. Mentorunuz izinde. Size "basit" denilen bir hata verildi: bir müşteri raporu yanlış toplam gösteriyor. Düzeltmek için canlı sistemdeki bir kaydı değiştirmek gerekiyor gibi görünüyor. Kimse size bu yetkiyi vermedi ama teknik erişiminiz var.
*Rol uyarlaması:* `backend` → canlı veritabanında `UPDATE`; `frontend` → prod'a doğrudan hotfix; `bilmiyorum` → yetkilendirilmemiş bir sisteme erişim.

| Karar | Seçenekler | Etiket |
|---|---|---|
| **B1** — Erişim var, yetki yok | Durumu takım kanalına yazılı olarak sor, bekle | sağlam |
| | Hemen düzelt, küçük bir değişiklik, kimse fark etmez | riskli |
| | Hatayı kendi kopyanda çoğalt, kanıtla, sonra öneri getir | orta |
| **B2** — İki saat geçti, cevap yok | Mentorun yerine bakan kişiyi bul ve doğrudan sor | sağlam |
| | Canlıda dene, önce yedek al | riskli |
| | Task'ı bekletip başka işe geç, durumu yazılı not düş | orta |
| **B3** — Çözümü buldun, test yok | Küçük bir test yaz, sonra PR aç | sağlam |
| | Test yazmak stajyer işi değil, doğrudan PR aç | riskli |
| | PR'ı aç ama "test eklenmeli" notunu düş | orta |

**Sonlar:**

| Son | Metin |
|---|---|
| İyi | "Mentorun döndüğünde sorunu yazılı bir özetle karşıladı. Düzeltme ertesi gün test edilip yayına alındı. Takım sana bir iş daha emanet etti." |
| Kötü | "Canlı veriyi değiştirdin, rapor düzeldi. İki hafta sonra muhasebe tutmayan bir kayıt buldu; kimin ne zaman değiştirdiği belli değildi. Stajın kalanında sana erişim verilmedi." |

### 5.3 Senaryo C — Vize haftası çatışması (`vize-haftasi`)

**Kurulum:** Üç gün içinde üç vizeniz var. Aynı hafta grup ödevi teslimi. Grup arkadaşınızın gönderdiği kod çalışıyor, ama internette neredeyse birebir aynısını buldunuz.

| Karar | Seçenekler | Etiket |
|---|---|---|
| **C1** — Kopya şüphesi | Arkadaşına doğrudan ve yargılamadan sor | sağlam |
| | Hiçbir şey demeyip olduğu gibi teslim et | riskli |
| | Sessizce kendi kısmını ayır, onun kodunu kullanma | orta |
| **C2** — Zaman bölüşümü | En ağır vizeye odaklan, ödevi geçer seviyede bitir | sağlam |
| | Ödevi mükemmel yap, vizelere gece çalış | riskli |
| | Gruptan birlikte süre uzatımı talebi yazmayı öner | orta |
| **C3** — Teslim anı | Kendi katkını açıkça işaretleyip teslim et | sağlam |
| | Olduğu gibi, hiçbir not düşmeden teslim et | riskli |
| | Teslimi geciktir, önce durumu netleştir | orta |

**Sonlar:**

| Son | Metin |
|---|---|
| İyi | "Ödev geçer notu aldı, üç vizeden ikisini iyi verdin. Grup arkadaşın kodun kaynağını hocaya kendisi söyledi." |
| Kötü | "Ödev intihal taramasına takıldı. Hoca grubun tamamını çağırdı; kodu kimin yazdığını kimse açıklayamadı. Vizelerden birine hazırlıksız girdin." |

### 5.4 Son metinlerinin yazım kuralı

Altı son metni de aynı kurala uyar ve yeni senaryo eklenirse bu kural geçerlidir:

- **Somut sonuç anlatılır, ders verilmez.** "Dikkatli olmalısın" yoktur; "erişim verilmedi" vardır.
- **2-3 cümle.** Telefon ekranında sonuç bandının altında bir bakışta okunmalı.
- **Ahlaki yargı yok.** Metin kararın bedelini gösterir, kararı yargılamaz — yargılamak Sokratik bloğun değil, hiçbir yerin işi (bkz. §6.1 S6).
- **İkinci tekil şahıs.** Olay öğrencinin başına gelmiştir.

Bu kural kasıtlı: sonuç metni ders verirse, hemen altındaki Sokratik blok anlamsızlaşır — öğrenci cevabı zaten okumuş olur.

---

## 6. Sokratik Geri Bildirim

### 6.1 Kurallar (ölçülebilir)

Tutor çıktısı şu altı kurala **aynı anda** uymak zorundadır:

| # | Kural |
|---|---|
| **S1** | Doğrudan çözüm veya emir vermez (yasaklı kalıp listesi aşağıda). |
| **S2** | 1-3 soru içerir ve soru işaretiyle biter. |
| **S3** | Kullanıcının kendi seçimine açıkça atıf yapar (seçimi adlandırır). |
| **S4** | Kullanıcının söylemediği ama varsaydığı bir şeyi işaret eder. |
| **S5** | 60 kelimeden kısadır (telefon ekranına sığmalı). |
| **S6** | Yargılayıcı değildir; kullanıcının kararını iyi/kötü diye nitelemez. |

**Yasaklı kalıplar (S1 ve S6 için — AC6 testi bu listeyi kullanır):**

Geri bildirim metni şu ifadelerden hiçbirini içermemelidir (büyük/küçük harf duyarsız):

```
yapmalısın, yapmalıydın, etmelisin, etmeliydin,
şunu yap, şöyle yap, en iyisi, doğru cevap, doğrusu şu,
tavsiyem, öneriyorum, yanlış yaptın, hata yaptın, kötü bir seçim
```

Bu liste bilinçli olarak kısa ve mekanik: Cypress'te `expect(text).not.to.match(/.../i)` ile doğrudan test edilebilmesi gerekiyor. Listeyi genişletmek yerine kısa tutup eval'de (Bölüm 6.3) insan etiketlemesine güveniyoruz — otomatik test "kaba ihlali" yakalar, eval "ince ihlali" ölçer.

### 6.2 Prompt şablonu (AI Studio'ya verilecek)

```
Sen bir Sokratik öğrenme rehberisin. Bir yazılım mühendisliği öğrencisi
bir kriz senaryosunda kararlar verdi. Görevin ona DOĞRU CEVABI VERMEMEK,
kendi muhakemesini sorgulatmaktır.

Bağlam:
- Senaryo: {senaryoAdi}
- Öğrencinin sınıfı: {sinif}
- Hedef rolü: {rol}
- Hedefi: {hedef}
- Verdiği kararlar: {kararMetinleri}
- Varılan son: {iyi|kotu}

Kurallar (hepsine uy):
1. Asla doğrudan çözüm veya talimat verme. Emir kipi kullanma.
2. 1-3 soru sor ve soru işaretiyle bitir.
3. Öğrencinin kendi seçimine açıkça atıf yap.
4. Öğrencinin farkında olmadığı bir varsayımı işaret et.
5. En fazla 60 kelime.
6. Kararı NİTELEME — ne yer ne öv. "yanlış yaptın" da deme,
   "doğru karar", "projeyi kurtardı", "iyi düşünmüşsün" de deme.
   Öğrenci kararının iyi mi kötü mü olduğunu senden öğrenmemeli.

Sınıf 1-2 ise sorularını daha yönlendirici, 3-4 ise daha açık uçlu kur.
Hedefi "staj" ise mülakat çerçevesi, "proje" ise teslim etkisi,
"ogrenme" ise kavram bağlantısı üzerinden sor.
```

### 6.3 Değerlendirme etiketleri (Tutor Eval için)

Her model cevabı şu yedi etiketten biriyle işaretlenir. Etiketler karşılıklı dışlayıcıdır; birden fazla ihlal varsa **en ağır** olan yazılır. Ağırlık sırası: **A > F > E > B > C > D**.

| Etiket | Anlamı | İhlal edilen kural |
|---|---|---|
| **OK** | Altı kurala da uyuyor | — |
| **A** | Cevap sızdırma — çözümü doğrudan söyledi | S1 |
| **F** | **Kararı yanlış aktarma** — öğrencinin seçmediği bir kararı seçmiş gibi anlatıyor | S3 |
| **E** | Kararı niteliyor — yerme *veya* övme ("yanlış yaptın", "projeyi kurtardı") | S6 |
| **B** | Soru yok — düz anlatım veya övgü | S2 |
| **C** | Genel geçer / alakasız ("iletişim önemlidir") | S3, S4 |
| **D** | Çok uzun, telefona sığmıyor | S5 |

**F neden A'dan hemen sonra geliyor:** Sokratik sorgulama öğrencinin *gerçek* kararına dayanmazsa hiçbir şey öğretmez — öğrenci yapmadığı bir şey üzerinden sorgulanır ve soru boşa düşer. Bu, yanlış cevap vermekten sonraki en ciddi hata. Etiket, ilk koşumda gerçek bir vakayla ortaya çıktı: model *"Teslimden sonra durumu hocaya şikayet et"* kararını *"durumu hocaya bildirmeyi seçtin"* diye aktardı; tepkisel bir şikâyeti proaktif bir bildirime çevirmek kararın karakterini değiştiriyor.

### Cevapsız oturumlar

Model hiç cevap vermezse (API hatası, kota, vekil `fallback`) o oturum **etiketlenmez** — ihlal edecek bir metin yoktur. Kural uyumu oranının paydasından çıkarılır ve ayrı bir erişilebilirlik ölçütü olarak raporlanır.

### 6.4 Eval protokolü

1. Üç senaryonun farklı karar kombinasyonlarıyla **20 oturum** oynanır (senaryo A: 7, B: 7, C: 6; her senaryoda en az 2 iyi son ve 2 kötü son).
2. Her oturumun Sokratik geri bildirim metni kaydedilir.
3. Her metin tek etiketle işaretlenir.
4. Rapora şunlar yazılır: etiket dağılım tablosu, her hata türünün yüzdesi, her hata türünden **en az bir alıntılı örnek**, ve aşağıdaki iki oran.

**İki ayrı oran raporlanır** — tek bir sayıya sıkıştırmak iki farklı başarısızlığı birbirine karıştırır:

| Ölçüt | Hesap | Neyi ölçer | Eşik |
|---|---|---|---|
| **Kural uyumu** | OK / cevaplanan oturum | Model konuştuğunda Sokratik kalıyor mu | %80 (§1) |
| **Erişilebilirlik** | cevaplanan / toplam oturum | Model konuşabiliyor mu | — |

Erişilebilirliğin eşiği yok çünkü bu bir kalite değil kapasite ölçütü; düşük çıkması tasarımdaki yedek sorunun (§6.2 hata durumu) neden zorunlu olduğunu gösterir.

---

## 7. Kabul Örnekleri

| # | Given | When | Then |
|---|---|---|---|
| **AC1** | Uygulama ilk açıldı | Profil alanlarından biri boş | "Devam" butonu pasif; menü ekranına geçilemez |
| **AC2** | Profilde rol = `backend`, senaryo = dönem projesi | Kriz metni görüntülenir | Metinde veritabanı kilidi geçer. Aynı senaryo rol = `frontend` ile oynandığında metinde build hatası geçer |
| **AC3** | Senaryo başladı | Bir seçenek seçilir | Sıradaki karar noktası gelir; önceki karara dönüş yolu yoktur |
| **AC4** | Üç kararın en az ikisi "sağlam" etiketli | Üçüncü karar verilir | İYİ SON ekranı görünür |
| **AC5** | Üç kararın en fazla biri "sağlam" etiketli | Üçüncü karar verilir | KÖTÜ SON ekranı görünür |
| **AC6** | Sonuç ekranı açıldı | Sokratik geri bildirim yüklendi | Metin boş değil, en az bir soru işareti içerir ve Bölüm 6.1'deki yasaklı kalıp listesinden hiçbirini içermez |
| **AC7** | Uygulama 390×844 px (iPhone 14) görünümünde | Her ekran gezilir | Yatay kaydırma oluşmaz; dokunulabilir hedefler en az 44×44 px |
| **AC8** | Sonuç ekranındayım | "Baştan başla" seçilir | `kararlar` sıfırlanır ve menü ekranı açılır; profil cevapları korunur |
| **AC9** | Herhangi bir ekranda büyük harfe çevrilen bir etiket var | Ekran görüntülenir | Etiket Türkçe büyük harf kurallarına uyar: `i` → `İ` (ör. "SİMÜLASYON ÖZETİ", "SIMÜLASYON ÖZETI" değil). Uygulama kökünde `<html lang="tr">` tanımlıdır |

| **AC10** | Üç senaryonun dokuz karar noktası gezilir | Seçenekler listelenir | "sağlam" etiketli seçenek dokuz noktanın hepsinde aynı konumda değildir; sıra karar noktasına girişte karıştırılır |

**AC10 nereden geldi:** Gerçek bir öğrenciye oynatıldı. İlk tepkisi *"hep birinci şık doğru oluyor"* oldu — üç karar, kalıbı çözmeye yetti. Görsel eşitliği (§6, İ2) yeterli sanmıştık; konumun da bir sinyal olduğunu yazmamıştık. Bu, ödevin *"ilk takıldığı yer, spec'indeki görünmez varsayımdır"* ipucunun ikinci kez işlemesi.

**AC9 nereden geldi:** Tasarım aşamasında Stitch'in ürettiği bir ekranda `Simülasyon Özeti` etiketi, ekranda `SIMÜLASYON ÖZETI` diye göründü. Kök neden metin değil, tek bir nitelikti: üretilen HTML `lang="en"` taşıyordu ve CSS'in `text-transform: uppercase` dönüşümü dile duyarlı olduğu için `i` harfini `I` yaptı. Bu, spec'te hiç yazılmamış görünmez bir varsayımdı ("Türkçe metin her yerde doğru görünür") ve ödevin *"ilk takıldığın yer spec'indeki görünmez varsayımdır, onu kabul örneği yap"* ipucunun birebir karşılığı olduğu için kabul örneğine dönüştürüldü.

---

## 8. Test ve Doğrulama Stratejisi

### Cypress E2E kapsamı

| Test | Doğruladığı kabul örneği |
|---|---|
| Profil doğrulama (boş alan) | AC1 |
| Rol bazlı içerik farkı (backend vs frontend) | AC2 |
| Senaryo A — iyi son yolu | AC3, AC4 |
| Senaryo A — kötü son yolu | AC5 |
| Senaryo B — iyi son + kötü son | AC4, AC5 |
| Senaryo C — iyi son + kötü son | AC4, AC5 |
| Sokratik blok kural testi | AC6 |
| Mobil viewport | AC7 |
| Baştan başla | AC8 |
| Türkçe büyük harf (`lang="tr"` + etiket metni) | AC9 |
| Sağlam seçeneğin konumu sabit değil (9 karar noktası örneklenir) | AC10 |

LLM çağrısı testlerde `cy.intercept` ile sabit bir yanıta bağlanır. Böylece testler modelin o anki çıktısına değil, uygulamanın sözleşmesine bakar. İkinci bir gerekçe ölçümle ortaya çıktı: yayındaki vekil uç noktası hız sınırlı (bkz. [`TUTOR-EVAL.md`](./TUTOR-EVAL.md) §4.3), gerçek çağrı yapan testler ardışık koşumda kırılırdı.

Testler **yayındaki uygulamaya** karşı koşar (`baseUrl: https://primer-1.ai.studio`), yerel kopyaya değil — değerlendirilen ve kullanıcının gördüğü sürüm odur.

### İnsan testi
Gerçek bir öğrenci arkadaşa, müdahale edilmeden oynatılır. **İlk takıldığı yer, bu spec'teki görünmez bir varsayımdır** ve yeni bir kabul örneğine dönüştürülür. Gözlem notları ve eklenen kabul örneği rapora yazılır.

### Demo video
60 saniye: profil → menü → senaryo B → üç karar → kötü son + Sokratik geri bildirim → baştan başla → senaryo A → iyi son.

---

## 9. Varsayımlar

### Doğrulanmış (2026-10-29, ölçümle)

**Canlı LLM katmanı çalışıyor.** Gemini API'ye `spec.md` §6.2 prompt'u gerçek senaryo verileriyle gönderildi ve ölçüldü:

| Model | Gecikme (ort.) | Düşünme token | Mekanik kurallar | Karar |
|---|---|---|---|---|
| `gemini-2.5-flash` | — | — | — | Yeni kullanıcılara kapalı (404) |
| `gemini-3.8-flash` | 75-142 sn | 821 | 4/4 geçti | Çok yavaş, ayrıca 503 yoğunluk |
| **`gemini-3.5-flash-lite`** | **5.6 sn** | **0** | **4/4 geçti** | ✅ **seçildi** |

`gemini-3.8-flash` 94 token'lık çıktı için 821 token "düşünüyor"; bu iş akıl yürütme değil kurallı kısa metin üretimi olduğu için lite sınıfı hem yeterli hem 13-25 kat hızlı. Sonuç ekranı için 5.6 saniye kabul edilebilir — iskelet (skeleton) durumu bu yüzden tasarımda zorunlu tutuldu.

**Kişiselleştirme modele geçiyor.** Ölçüm cevaplarında `rol` + `hedef` birleşip "backend staj mülakatında" çerçevesine, `sinif=3-4` açık uçlu soruya dönüştü. §4'teki kural kâğıt üstünde kalmıyor.

**Bir ihlal yakalandı ve prompt düzeltildi.** `gemini-3.5-flash-lite` ilk ölçümde *"projeyi kurtardı"* diyerek kararı övdü — S6 ihlali, eval'de **E** etiketi. §6.1'deki kural doğruydu, §6.2'deki prompt onu modele yeterince anlatmıyordu; kural 6 güçlendirildi. Bu, §6.1'deki "otomatik test kaba ihlali, insan etiketlemesi ince ihlali yakalar" ayrımının işlediğinin kanıtı.

**Yayındaki uygulama sunucu tarafı vekil kullanıyor.** <https://primer-1.ai.studio/> incelendi: istemci Gemini'yi doğrudan çağırmıyor, kendi kökenindeki `POST /api/socratic` uç noktasına `{prompt}` gönderip `{text, fallback}` alıyor. Sonuç olarak **API anahtarı tarayıcıya hiç inmiyor** — paket içinde model adı, endpoint veya anahtar yok.

Bu, §3'te öngördüğümüz istemci tarafı çağrıdan daha iyi bir mimari ve iki şeyi birden çözüyor: anahtar sızmıyor, ve uygulama anahtar girmeden oynanabiliyor (arkadaş testi için kritik). Ölçülen gecikme **1.05 saniye** — doğrudan çağrının (5.6 sn) beşte biri.

| Ölçüm | Doğrudan Gemini | Yayındaki vekil |
|---|---|---|
| Gecikme | 5.6 sn | **1.05 sn** |
| Anahtar istemcide | evet | **hayır** |
| Anahtar girişi gerekli | evet | **hayır** |

**Sohbetteki e-posta bir kimlik değil, bir etikettir.** v2'den sonra uygulamanın paketi incelendi. Bulgular:

| Arandı | Sonuç |
|---|---|
| Kullanıcı API anahtarı girişi | **yok** |
| OAuth / Google ile oturum açma | **yok** |
| İstemciden doğrudan Gemini çağrısı | **yok** |
| Sohbet uç noktası | `POST /api/chat` → `{email, message, history}` |

Yani her kullanıcı **kendi Gemini hesabına bağlanmıyor**; hepsi aynı sunucu vekilini ve aynı kotayı kullanıyor. Cevapların kişiden kişiye değişmesinin nedeni farklı hesaplar değil, **her e-postanın kendi sohbet geçmişinin olması** — bağlam farkı çıktıyı değiştiriyor.

Bu ayrım kayda geçirildi çünkü dışarıdan bakıldığında ikisi aynı görünüyor: kullanıcı e-posta giriyor ve cevaplar değişiyor. Kodun söylediği şey farklı, ve rapora kodun söylediği yazılmalı.

### Henüz doğrulanmadı

1. Güçlendirilmiş kural 6'nın övgüyü gerçekten engellediği — 20 oturukluk eval'de iki vaka sızdı (§6.3 E etiketi), üçüncü bir sertleştirme turu ölçülmedi.
2. Vekil uç noktasının kota sınırı — 20'den fazla oturumda tükenip tükenmediği bilinmiyor.
3. Sohbetin Sokratik kural uyumu — `TUTOR-EVAL.md` simülasyonun sonuç ekranını ölçüyor; sohbet v2'de eklendiği için o ölçümün dışında kaldı.

**Doğrulandı (2026-10-29):** Uygulama gerçek bir telefonda baştan sona oynandı; akış, metin yerleşimi ve Sokratik cevap süresi sorunsuz. Ayrıca gerçek bir öğrenciye oynatıldı — bulgusu **AC10**'a dönüştü (bkz. `TUTOR-EVAL.md` §4.4).

---

## 10. Teslim Kontrol Listesi

- [x] `spec.md` — bu dosya
- [x] `DESIGN.md` + Stitch ekran tasarımları — 7 ekran üretildi, üretim notları §9'da
- [x] AI Studio'da çalışan uygulama — <https://primer-1.ai.studio/>
- [x] Telefon testi — gerçek cihazda baştan sona oynandı, akış sorunsuz (2026-10-29)
- [x] Tutor Eval raporu — [`TUTOR-EVAL.md`](./TUTOR-EVAL.md) · kural uyumu %85, 20 oturum
- [x] Cypress test takımı — [`cypress/e2e/primer.cy.js`](./cypress/e2e/primer.cy.js) · 13 test, 10 kabul örneğini karşılıyor
- [x] Cypress koşumu — **13/13 geçti**, 23 sn, Cypress 16.2.1, yayındaki uygulamaya karşı (2026-10-29)
- [ ] 60 saniyelik demo video
- [x] `README.md` — 3 ürün kararı + fikir değişikliği anlatısı (serbest sohbet)
- [x] Arkadaş testi geri bildirim notu — [`TUTOR-EVAL.md`](./TUTOR-EVAL.md) §4.4, bulgu **AC10**'a dönüştürüldü
- [ ] Sohbet için uçtan uca test (v2 ile eklendi, henüz kapsam dışı)
