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

### v2 kabul örnekleri (model katmanı)

Aşağıdaki üçü **veri toplanmadan ve model eğitilmeden önce** yazıldı. Ayrıntılı gerekçe: §10.

| # | Given | When | Then |
|---|---|---|---|
| **AC11** | `data/oturumlar.csv` hazır, kabul eşiği §10.5'te yazılı | `python train.py` koşar | 5 katlı çapraz doğrulama ROC-AUC eşiğin altındaysa betik sıfırdan farklı çıkış koduyla durur ve `model/` altındaki artefaktlar **güncellenmez**; eşiği geçerse `model.onnx` + `config.json` yeniden yazılır |
| **AC12** | `tests/parite.json`'daki beş referans girdi ve Python kahininin olasılıkları | Aynı beş girdi uygulamanın içindeki ONNX çıkarımıyla hesaplanır | Her girdide `\|p_uygulama − p_kahin\| < 1e-4` |
| **AC13** | Geçmişi `p(refleks) ≥ karar_esigi` üreten bir oturum | Karar noktasına girilir | Yansıma duraklaması görünür ve seçenekler 3 saniye pasif kalır; duraklama **hiçbir seçeneği işaret etmez**. Eşiğin altındaki bir oturumda duraklama hiç görünmez ve seçenekler anında aktiftir |

**AC13'ün ikinci yönü neden şart:** yalnızca "duraklama görünüyor" test edilirse, her zaman duraklatan bir uygulama da testi geçer — model hiç çalışmasa bile. İki yönlü test, davranış değişikliğinin gerçekten modelden geldiğini doğrular.

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

### Sohbet testleri (v2)

Serbest sohbet, ilk spec'te *"deterministik test edilemez"* gerekçesiyle kapsam dışıydı. Gerekçe hatalıydı: test edilmesi gereken şey modelin metni değil, uygulamanın sözleşmesi — Sokratik blok için zaten bu ayrımı yapmıştık. [`cypress/e2e/sohbet.cy.js`](./cypress/e2e/sohbet.cy.js) yedi testle şunları doğruluyor:

| Test | Doğruladığı |
|---|---|
| HTML5 doğrulaması | `@` içermeyen adres gönderilemiyor, hiçbir şey saklanmıyor |
| Uygulama doğrulaması | Nokta içermeyen adres Türkçe uyarı veriyor |
| E-posta normalizasyonu | Boşluklar kırpılıp küçük harfe çevriliyor |
| İstek sözleşmesi | `POST /api/chat` gövdesinde `email`, `message`, `history` |
| Saklama | Geçmiş `primer_chat_<eposta>` anahtarıyla ayrışıyor |
| Boş mesaj | Gönder butonu pasif |
| Sıfırlama | "Sohbeti sıfırla" saklanan e-postayı siliyor |

**İki doğrulama katmanı bulundu.** Alan `<input type="email">` olduğu için tarayıcının HTML5 doğrulaması uygulamanınkinden önce çalışıyor; çoğu yazım hatasında kullanıcı tarayıcının kendi dilindeki balonunu görüyor, uygulamanın Türkçe uyarısını değil. İkisi ayrı ayrı test edildi, davranış belgelendi ama düzeltilmedi — tutarlı Türkçe uyarı için native doğrulamayı kapatmak gerekirdi ki bunun erişilebilirlik bedeli var.

### Model katmanı testleri (v2)

| Test | Nerede | Doğruladığı |
|---|---|---|
| Eval kapısı — eşik altı sürüm durur | `train.py` (komut satırı) | AC11 |
| ONNX ↔ sklearn farkı `< 1e-4` | `train.py` dışa aktarım denetimi | §10.7 artefakt bütünlüğü |
| Diferansiyel (parite) testi — uygulama vs Python kahini | `cypress/e2e/parite.cy.js` + `tests/parite.py` | AC12 |
| Yansıma duraklaması iki yönlü | `cypress/e2e/v2-akis.cy.js` | AC13 |
| Akış bütünlüğü (profil, karıştırma, iki son) v2 sayfasında | `cypress/e2e/v2-akis.cy.js` | AC1, AC3–AC5, AC10 |

**Regresyon kuralı: v1 test dosyaları değiştirilmez.** `cypress/e2e/primer.cy.js` ve `cypress/e2e/sohbet.cy.js` v2 çalışması boyunca tek karakter bile değişmeyecek ve her koşumda yeşil kalacak. Regresyon kanıtının değeri dosyaların aynı kalmasından geliyor; v2 spec'leri bu yüzden kendi yardımcı fonksiyonlarını taşır (≈30 satır tekrar, bilinçli bedel — ortak bir yardımcı dosyaya çekmek v1 dosyalarına dokunmak demekti).

İki test hedefi var: v1 spec'leri `cypress.config.js`'teki `baseUrl` ile **yayındaki AI Studio uygulamasına**, v2 spec'leri `Cypress.env('v2Url')` ile **GitHub Pages sayfasına** (veya yerel sunucuya) koşar.

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

## 10. Model Gereksinimi (v2)

v1'de kişiselleştirme **sabit kurallara** dayanıyordu: profil cevapları §4'teki tabloya göre metni ve soru derinliğini değiştiriyordu. Hiçbir şey oyuncunun *davranışından* öğrenmiyordu. v2, uyumun bir kısmını kendi eğittiğimiz küçük bir modele devrediyor.

Bu bölüm **eğitimden önce** yazıldı. Eşik burada sabitlendi; ölçüm sonucuna göre gevşetilmesi kural ihlalidir.

### 10.1 Mimari: üçüncü katman

| Katman | Nasıl çalışır | Neden böyle |
|---|---|---|
| **Dallanma** (senaryo, seçenekler, sonlar) | Deterministik karar ağacı | Cypress her koşumda aynı sonucu görmeli |
| **Sokratik geri bildirim** | Canlı LLM çağrısı, vekil üzerinden | Eval'de ölçülecek gerçek model davranışı gerekiyor |
| **Uyum (v2'de eklendi)** | **Kendi eğittiğimiz lojistik regresyon, ONNX olarak uygulamada** | Davranıştan öğrenen kısım ölçülebilir, sürümlenebilir ve geri alınabilir bir artefakt olmalı |

### 10.2 Hedef: `refleks`

Model şunu tahmin eder: **öğrenci girdiği karar noktasında refleksle mi karar verecek?**

Eşik geçilirse uygulama, karar noktasına girişte **yansıma duraklaması** gösterir: tek bir Sokratik mikro-soru ("Bu kararı vermeden önce: neyi varsayıyorsun?") ve seçenekler 3 saniye pasif kalır.

**Müdahale cevap-nötr olmak zorundadır.** Bu, §5'teki karıştırma kuralının ve §1'deki ürün iddiasının doğrudan sonucu: duraklama hiçbir seçeneği işaret etmez, hiçbir seçeneği öne çıkarmaz, metni değiştirmez. Yalnızca kararı geciktirir ve soruyu sorar. Model "şu seçeneği seç" diyebilseydi ürünün amacı çökerdi — modelin yetkisi *ne zaman durdurulacağı* ile sınırlıdır, *ne seçileceği* ile değil.

Başlangıç reposundaki *"bu oyuncunun ipucuna ihtiyacı var mı"* örneği bilinçli olarak kullanılmadı: ipucu vermek, bu üründe doğrudan cevabı sızdırmak demektir (§6.1 S1).

### 10.3 Özellik sözleşmesi

Çıkarım anı: öğrenci **karar noktası k'ya girdiğinde**. Özellikler yalnızca k'dan *önce* bilinen şeylerden türer; k=1'de geçmişe dayalı alanlar 0'dır. Bu kısıt etiket sızıntısını engellemek için var — modelin tahmin ettiği şey henüz gerçekleşmemiş olmalı.

| # | Özellik | Birim / aralık |
|---|---|---|
| 1 | `sahne_no` | 1–3 |
| 2 | `sinif_kodu` | 0 = `1-2`, 1 = `3-4` |
| 3 | `onceki_karar_suresi_sn` | saniye (k=1'de 0) |
| 4 | `onceki_okuma_orani` | 0–1 (k=1'de 0) |
| 5 | `onceki_refleks_sayisi` | 0–2 |
| 6 | `oturum_gecen_sure_sn` | saniye, oturum başından bu karar noktasına kadar |

**Sıra sözleşmenin parçasıdır** ve `model/config.json`'da yazılıdır; tensör `float32[1,6]`. Tüketiciler (uygulama ve Python kahini) aynı sırayı kullanmak zorundadır.

`rol` ve `hedef` **bilinçli olarak özellik değildir.** Gerekçe: ~45 gerçek satırda altı kategorik seviyeyi one-hot etmek modeli gürültüye oturtur. `sinif` kalıyor, çünkü §4 zaten derinliği sınıfa bağlıyor — yani zaten sistemde olan bir sinyal. Bu kısıt model kartında "kullanılmayan sinyaller" olarak yazılacak.

### 10.4 Etiket kuralı

```
refleks = 1   eğer   okuma_orani < 0.4

okuma_orani = min(1, metin_gorunur_sure_sn / tahmini_okuma_suresi_sn)
tahmini_okuma_suresi_sn = o karar noktasında YENİ gösterilen kelime / 200 * 60
```

Yani: öğrenci, ekranda yeni çıkan metni okumak için gereken sürenin **%40'ından azını** harcadıysa o karar refleks karardır. 200 kelime/dakika Türkçe ortalama okuma hızı varsayımı; %40 eşiği nominal hızın 2,5 katına denk gelir — bu, göz gezdirmenin bile üstünde bir hız, dolayısıyla "okumadı" demek güvenli.

**Bu kural bir ara sürümden sonra düzeltildi, veri toplanmadan önce.** İlk hali iki koşulluydu: `karar_suresi_sn < 6 AND okuma_orani < 0.5`. Uygulama yazılırken iki sorun görüldü:

| Sorun | Neden |
|---|---|
| İki koşul aslında tek koşul | 390×844 ekranda kriz paneli, soru ve üç seçenek birlikte sığıyor; metin hiç görünürlükten çıkmıyor, dolayısıyla `metin_gorunur_sure ≈ karar_suresi` ve ikinci koşul bağımsız olarak bağlamıyor |
| Sabit 6 saniye sahneleri eşit sayıyor | 1. karar noktasında yeni metin ~86 kelime (kriz kurulumu + soru + üç seçenek), 2. ve 3.'de ~36 kelime. Aynı 6 saniye, birinde "okumadı" diğerinde "okudu" demek anlamına geliyor |

Orana indirgemek ikisini birden çözüyor: oran sahnenin kendi okuma yüküne göre normalize oluyor. Eşik veri görülmeden sabitlendi ve veriden sonra değiştirilmeyecek — değiştirilirse etiketi modele uydurmak olur.

### 10.5 Eval metriği ve kabul eşiği

| Ölçüt | Hesap | Eşik | Rolü |
|---|---|---|---|
| **ROC-AUC** | 5 katlı tabakalı çapraz doğrulama ortalaması | **≥ 0.70** | **Eval kapısı** — altındaysa `train.py` hata verir, artefakt yayınlanmaz |
| Dengeli doğruluk | aynı CV | — | raporlanır |
| Çoğunluk-sınıfı taban çizgisi | aynı CV | — | raporlanır, modelin tabanı geçtiği gösterilir |
| **`karar_esigi`** | olasılık kesme noktası | **0.60** | **Eylem eşiği** — duraklamanın açılma noktası |

**İki eşik birbirine karıştırılmamalı.** `0.70` modelin *yayınlanabilir* olup olmadığını söyler; `0.60` uygulamanın *müdahale edip etmeyeceğini*. 0.60 bilinçli olarak 0.50'nin üstünde: yanlış pozitif, metni gerçekten okuyan bir öğrenciyi boşuna durdurmak demektir ve bu, ürünün akışına zarar verir. Kesinlik (precision) duyarlılıktan (recall) önce gelir.

Doğruluğun kendisi bir hedef değil: düşük ama dürüstçe ölçülmüş ve sınırları model kartında yazılı bir model, ölçülmemiş iyi bir modelden daha değerlidir.

### 10.6 Veri

`data/oturumlar.csv` — her karar noktası bir satır. En az **15 gerçek oturum** (3 kişi × 5 oturum). `kaynak` sütunu zorunlu: `gercek` | `sentetik`. Sentetik veri yalnızca dengeleme için; üretici kural ve tohum `README.md`'de yazılı. Sütun tanımları `data/SOZLUK.md`'de.

**KVKK.** Ad, e-posta, cihaz kimliği, konum veya başka hassas alt detay **toplanmaz**. `oturum_id` rastgele üretilir; `kisi_kodu` yalnızca `k1`/`k2`/`k3` gibi anonim bir ayrıştırıcıdır ve kimseye geri bağlanamaz. Bu, v1'deki sohbet e-postasından farklı bir karardır: orada e-posta bir etiketti ama yine de saklanıyordu (§2); burada hiçbir kişisel alan hiç toplanmıyor.

### 10.7 Sürümleme

Tüketiciler modeli `main` dalından değil, **commit'e sabitlenmiş URL'den** indirir:

```
https://huggingface.co/<kullanici>/<repo>/resolve/<commit>/model.onnx
```

Sabitlenen commit, eylem eşiği ve devreye alma oranı `web/site.json`'da tutulur; geri alma (rollback) bu dosyadaki pin'i önceki commit'e çevirmekten ibarettir. Ayrıntı: `RELEASE.md`.

### 10.8 Kapsam dışı (v2)

| Yapılmayan | Gerekçe |
|---|---|
| LLM ince ayarı | Ödev kapsamı dışı; Sokratik katman prompt ile yönetiliyor (§6.2) |
| Ücretli barındırma | Tüm zincir ücretsiz katmanda: HF Hub, GitHub Pages |
| Gerçek kişisel veri | §10.6 — hiç toplanmıyor |
| Kullanıcı hesabı / giriş | v1'deki kararla aynı (§2) |
| Kendi sunucusunda üçüncü tüketici (bonus) | Dört tüketici doğrulamak bir haftaya sığmıyor; parite iki tüketiciyle (uygulama + Python kahini) kanıtlanıyor |
| Cihaz içi mobil (Expo / APK) | Tarayıcı tüketicisi ödev gereksinimini karşılıyor; ödünleşim matrisinde yine de değerlendirildi (`RELEASE.md`) |

---

## 11. Teslim Kontrol Listesi

- [x] `spec.md` — bu dosya
- [x] `DESIGN.md` + Stitch ekran tasarımları — 7 ekran üretildi, üretim notları §9'da
- [x] AI Studio'da çalışan uygulama — <https://primer-1.ai.studio/>
- [x] Telefon testi — gerçek cihazda baştan sona oynandı, akış sorunsuz (2026-10-29)
- [x] Tutor Eval raporu — [`TUTOR-EVAL.md`](./TUTOR-EVAL.md) · kural uyumu %85, 20 oturum
- [x] Cypress test takımı — [`cypress/e2e/primer.cy.js`](./cypress/e2e/primer.cy.js) · 20 test: 13'ü 10 kabul örneğini, 7'si sohbet sözleşmesini doğruluyor
- [x] Cypress koşumu — **20/20 geçti** (13 simülasyon + 7 sohbet), 22 sn, Cypress 16.2.1, yayındaki uygulamaya karşı (2026-10-29)
- [x] 60 saniyelik demo video — <https://youtube.com/shorts/akFFeEdus34>
- [x] `README.md` — 3 ürün kararı + fikir değişikliği anlatısı (serbest sohbet)
- [x] Arkadaş testi geri bildirim notu — [`TUTOR-EVAL.md`](./TUTOR-EVAL.md) §4.4, bulgu **AC10**'a dönüştürüldü
- [x] Sohbet için uçtan uca test — [`cypress/e2e/sohbet.cy.js`](./cypress/e2e/sohbet.cy.js) · 7 test

### v2 kalemleri

- [x] Model gereksinimi, eval metriği ve kabul eşiği — §10, eğitimden önce yazıldı
- [x] Üç yeni kabul örneği — **AC11, AC12, AC13** (§7)
- [x] Veri sözlüğü — [`data/SOZLUK.md`](./data/SOZLUK.md) · 23 sütun, etiket kuralı, KVKK notu
- [x] **En az 15 gerçek oturum** — `data/oturumlar.csv` · **69 gerçek oturum / 207 gerçek satır** (+60 sentetik). İlk toplama turu tek etiketli çıktığı için kullanılamadı ve yeniden toplandı; azınlık sınıfının hâlâ ağırlıkla sentetik olduğu `model/README.md` §5'te raporlanıyor
- [x] Tekrarlanabilir eğitim ve eval kapısı — [`train.py`](./train.py) · tek komut, tohum 42, `--esik 0.99` ile kapının kapattığı doğrulandı (çıkış kodu 2, `model/` değişmedi)
- [x] Artefakt ve sözleşme — `model/model.onnx` (553 bayt, opset 18) + `model/config.json` · ONNX/sklearn farkı 9.1e-08
- [x] Model kartı — [`model/README.md`](./model/README.md) · Mitchell vd. (2019) yapısında
- [ ] **Hugging Face yayını, commit'e sabit URL** — adımlar [`RELEASE.md`](./RELEASE.md) §3'te; hesap açılmayı bekliyor
- [x] Devreye alma ve geri alma planı + ödünleşim matrisi — [`RELEASE.md`](./RELEASE.md) §2 ve §4
- [x] Uygulamada çıkarım — [`web/index.html`](./web/index.html) · onnxruntime-web 1.20.1, model kararı yansıma duraklamasını açıyor
- [x] Diferansiyel test ve test kahini — [`cypress/e2e/parite.cy.js`](./cypress/e2e/parite.cy.js) + [`tests/parite.py`](./tests/parite.py) · 5 girdi, en büyük fark < 1e-4
- [x] Davranış testi (AC13) ve regresyon koşumu — [`cypress/e2e/v2-akis.cy.js`](./cypress/e2e/v2-akis.cy.js) · **v2 14/14**, v1 takımı dokunulmadan **20/20** (2026-11-01)
- [ ] **60–90 sn demo video** — aynı sahnede iki oyuncu, modelin iki farklı kararı
- [x] Vize sınav tasarımı düşünce egzersizi — [`SINAV_TASARIMI.md`](./SINAV_TASARIMI.md)
- [x] GitHub Pages yayını — <https://gonulnazire.github.io/primer/web/> · v2'nin 14 testi **canlı adrese karşı** 14/14 geçti (2026-11-01)
