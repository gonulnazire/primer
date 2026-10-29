# Stitch Adımları — Çalışma Notu

> Bu dosya **teslim edilecek bir belge değil**, Stitch'te ekranları üretirken yanınızda açık tutmanız için bir çalışma notu. Teslim belgeleri: [`spec.md`](./spec.md), [`DESIGN.md`](./DESIGN.md).

**Doğrulanmamış bilgi uyarısı:** Stitch'in güncel arayüzü doğrulanmadı. Buton adları ve menü yerleşimi burada tarif edilenden farklı olabilir; bazı bölgelerde bekleme listesi uygulanıyor olabilir. Bu yüzden adımlar buton adlarına değil *yapılacak işe* göre yazıldı.

---

## 1. Hazırlık

**1.1** [`DESIGN.md`](./DESIGN.md)'yi bir editörde açın ve açık tutun. Prompt'lar orada; bu dosyaya kopyalanmadı ki iki yerde birbirinden kaymasın.

| Ekran | `DESIGN.md` satırı |
|---|---|
| E1 Profil | **259** |
| E2 Senaryo Menüsü | **279** |
| E3 Kriz ve Karar | **299** |
| E4 Sonuç ve Sokratik | **322** |

Her biri bir kod bloğu içinde. **Bloğun tamamını** kopyalayın, başlığı değil.

**1.2** [stitch.withgoogle.com](https://stitch.withgoogle.com) → Google hesabıyla giriş.

**1.3** Yeni proje açın ve **mobil (mobile) modu** seçin.

> Bu adımı atlamayın. Stitch hem web hem mobil çıktı üretiyor; web modunda 390px telefon düzeni yerine masaüstü düzeni gelir ve `DESIGN.md`'deki her ölçü anlamsızlaşır.

---

## 2. Üretim sırası

Dört ekranı **E1 → E2 → E3 → E4** sırasıyla ve **aynı Stitch projesinde** üretin.

> **Neden aynı proje:** Stitch aynı oturumda önceki ekranların görsel dilini taşıma eğiliminde. Dört ayrı projede üretirseniz renkler ve boşluklar birbirinden kayar; rubrikteki "Stitch ekranları ve `DESIGN.md` uyumu" kalemi zarar görür.

---

## 3. Ekran ekran: neye bakacaksınız

Her ekranda tek bir şeye bakıyorsunuz. Tutmuyorsa aşağıdaki düzeltme cümlesini prompt'un **sonuna** ekleyip yeniden üretin.

### E1 — Profil

**Bakılacak:** "Devam" butonu pasif (soluk) görünüyor mu?

Prompt'ta `DISABLED state` yazılı ama Stitch bunu sıkça yoksayıp canlı kehribar buton üretiyor. Pasif görünmüyorsa:

```
IMPORTANT: The "Devam" button must look clearly disabled and unclickable -
grey #222A35 background, grey #9AA6B8 text, no amber color at all.
```

*Niçin önemli:* `spec.md` AC1 — profil dolmadan menüye geçilemez. Pasif durum ekranda görünmüyorsa kabul örneğinin tasarım karşılığı yok.

### E2 — Senaryo Menüsü

**Bakılacak:** Üç kart birbirinin tıpatıp aynısı mı?

Stitch ilk kartı öne çıkarmayı sever (daha büyük, kehribar kenarlık, "Popular" etiketi). Öne çıkarmışsa:

```
IMPORTANT: All three cards must be visually identical - same size, same
background, same border. No card is featured, recommended or highlighted.
No badges or labels on any card.
```

### E3 — Kriz ve Karar ← en kritik ekran

**Bakılacak:** Üç seçenekten herhangi biri diğerlerinden farklı görünüyor mu?

Olmaması gerekenler: tik, onay ikonu, yeşil/kırmızı renk, kalın kenarlık, farklı boyut, numara, "önerilen" yazısı.

Stitch bu ekranda yanılmaya en yatkın, çünkü "seçenek listesi" gördüğünde alışkanlıkla birini vurguluyor. Herhangi bir fark varsa:

```
CRITICAL CONSTRAINT: The three option buttons must be pixel-identical in
style - same background #161B22, same border #222A35, same text size and
weight. No icons, no checkmarks, no numbers, no color differences, no
badges, no "recommended" markers, no hover highlight on any specific one.
The user must not be able to guess which option is better from the design.
```

*Niçin ısrarla:* `DESIGN.md` İ2'nin ihlali ürünü işlevsiz bırakır. Kullanıcı doğru cevabı ekrandan okursa Sokratik sorgulama diye bir şey kalmaz ve 25 puanlık Tutor Eval'in dayanağı çöker.

### E4 — Sonuç ve Sokratik

**Bakılacak:** Sokratik alıntı bloğu bir "başarı mesajı" gibi mi duruyor?

Yeşil zemin, kutlama ikonu, 🎉, "Tebrikler" tonu varsa İ3 ihlali:

```
IMPORTANT: The quote block with the questions must NOT look like a success
message. No green background, no checkmark, no celebration icon, no
congratulation. It is a quiet note on a dark #161B22 card with only an
amber quotation mark.
```

---

## 4. Türkçe karakter sorunu

Stitch Türkçe metinleri bozabilir (`ı`, `ğ`, `ş`, `İ`) veya metinleri İngilizceye çevirebilir.

**Böyle olursa düzeltmeye çalışmayın, ilerleyin.**

> *Neden:* Bu ekranlar nihai ürün değil, tasarım referansı. Çalışan uygulamanın gerçek metni AI Studio aşamasında `spec.md` §5'ten gelecek. Stitch'te metin düzeltmek için tur atmak, hiçbir puana karşılık gelmeyen zaman kaybı.

Sadece not alın: *"E3'te Türkçe karakterler bozuldu"* gibi. Bu, `DESIGN.md`'ye bilinen sapma olarak eklenecek — sapmayı gizlemek yerine belgelemek lehinize, çünkü rubrik `DESIGN.md` uyumunu arıyor.

---

## 5. Ekran görüntüsü alma

Dört ekranın her biri için:

- **Windows 11:** `Win + Shift + S` → alan seçin → panoya kopyalanır
- Stitch'te indirme/export varsa o da olur, PNG yeterli

İsimlendirme (işi kolaylaştırır): `e1-profil.png`, `e2-menu.png`, `e3-karar.png`, `e4-sonuc.png`

---

## 6. Göndermeden önce kendi kontrol listeniz

- [ ] **E1:** "Devam" butonu soluk/pasif görünüyor
- [ ] **E2:** Üç kart tıpatıp aynı, hiçbiri öne çıkarılmamış
- [ ] **E3:** Üç seçenek tıpatıp aynı — tik/renk/ikon/boyut farkı yok
- [ ] **E4:** Soru bloğu kutlama değil, sessiz bir not gibi duruyor

Dördü tutuyorsa gönderin. Tutmuyorsa ilgili düzeltme cümlesiyle yeniden üretin.

---

## 7. Sonra ne olacak

**Siz gönderirsiniz:** 4 ekran görüntüsü + varsa notlar (*"E2'yi 3 kez ürettim, kartları hep farklı yapıyor"* gibi).

**Yapılacak denetim:** Her ekran `DESIGN.md` §2.1 renk token'ları, §4 wireframe'leri ve İ1-İ4 ilkelerine göre denetlenip sapma tablosu çıkarılacak.

**Ardından:** `DESIGN.md`'ye **§9 Üretim Notları** bölümü eklenecek — hangi ekran kaç denemede çıktı, Stitch neyi yoksaydı, hangi sapma kabul edildi. Bu bölüm rubrikteki "Stitch ekranları ve `DESIGN.md` uyumu" kalemine doğrudan hizmet ediyor: değerlendiren kişi tasarımın gerçekten üretildiğini ve sapmaların bilinçli olduğunu görür.

---

## 8. Tıkanırsanız

| Sorun | Ne yapın |
|---|---|
| Stitch bekleme listesi istiyor / bölgenizde yok | Haber verin. Alternatif: Figma veya AI Studio'nun kendi UI üretimi — `DESIGN.md` prompt'ları ikisinde de çalışır |
| Üretim sürekli masaüstü düzeni veriyor | Prompt'un başına ekleyin: `Mobile phone screen only, 390x844 viewport, portrait orientation.` |
| 3 denemede istediğiniz çıkmıyor | **Durun**, o haliyle gönderin. Mükemmel ekran 15 puanlık kalemin tamamı değil; `DESIGN.md` uyumu ve sapmanın belgelenmesi de puan taşıyor |
| Stitch girişte hata veriyor | Ekran görüntüsü alıp gönderin, oradan devam edilir |

---

## 9. Bu adımdan sonraki sıra

`mobil_uygulama_dev_detaylar.md`'deki yol haritasına göre:

| Adım | Durum |
|---|---|
| 1. `spec.md` | ✅ yazıldı — AC9 dahil 9 kabul örneği |
| 2. Stitch + `DESIGN.md` | ✅ **bitti** — 7 ekran üretildi, `DESIGN.md` §9 Üretim Notları yazıldı |
| 3. AI Studio'da çalışan uygulama | 🔄 **sıradaki** — Gemini doğrulaması bloke ediyor |
| 4. Tutor Eval (20 cevap) | ⏳ Adım 3'e bağlı |
| 5. Cypress + 60 sn demo | ⏳ Adım 3'e bağlı |
| 6. `README.md` (ürün kararı) | ⏳ en sona bırakılabilir, ~10 dk |

**Adım 2'den kalan tek iş:** E4-iyi ekranının güncel ekran görüntüsü. Dışa aktarımdaki `screen.png` düzeltme öncesi sürümden kalmış; `code.html` doğru. Stitch'te o ekranı açıp yeni görüntüyü almak yeterli.

**Bloke edici iş:** `spec.md` §9 varsayım 2 — Gemini API erişimi ve Türkçe Sokratik kural uyumu. Adım 3'ün mimarisi buna bağlı:
- Çalışıyorsa → hibrit mimari onaylanır, AI Studio'ya geçilir
- Çalışmıyorsa → `spec.md` §3 revize edilir, Sokratik katman önceden yazılmış soru havuzuna döner

Doğrulayan atılabilir probe script'i oturum scratchpad'inde; kaybolursa 1 dakikada yeniden üretilir.

**Adım 3'e taşınacak iki gereksinim** (bkz. `DESIGN.md` §9.5): `<html lang="tr">` ve her etkileşimli öğeye `data-testid`. İkincisi sonradan eklenemez — uygulama üretilirken konulmalı, yoksa Cypress testleri görünen metne bağımlı kalır ve kırılgan olur.
