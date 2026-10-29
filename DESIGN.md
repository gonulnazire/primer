# DESIGN.md — "Primer" Arayüz Tasarımı

**İlgili belge:** [`spec.md`](./spec.md)
**Hedef cihaz:** 390 × 844 px (iPhone 14), tek elle kullanım
**Araç:** Google Stitch → Google AI Studio
**Tarih:** 2026-10-29

---

## 1. Tasarım İlkeleri

Bu dört ilke spec'teki ürün kararlarından türetildi; her tasarım tercihi bunlardan birine dayanmak zorunda.

| # | İlke | Nereden geliyor |
|---|---|---|
| **İ1** | **Karar ekranda tek başına durur.** Bir seferde tek karar noktası görünür; ilerleme göstergesi dışında dikkat dağıtıcı öğe yok. | spec §3: "geri dönüş yok" — karar bağlayıcı olduğu için ekran da bağlayıcı hissettirmeli |
| **İ2** | **Uygulama hiçbir yerde doğru cevabı ima etmez.** Seçenekler görsel olarak eşittir (aynı boyut, renk, ağırlık; ikon/rozet/numara yok) **ve konumları sabit değildir** — sıra her karar noktasında karıştırılır. | spec §5: etiketler kullanıcıya gösterilmez. Yeşil tik veya uyarı ikonu koyarsak ürün kendi amacını çöker |

> **İ2 arkadaş testinden sonra genişletildi.** İlk hali yalnızca görsel eşitliği şart koşuyordu ve uygulama buna harfiyen uyuyordu — ama "sağlam" seçenek her zaman ilk sıradaydı. Gerçek bir öğrenci bunu üç kararda fark etti: *"hep birinci şık doğru oluyor."* **Konum, stil kadar güçlü bir sinyal.** İlkeye sıra kısıtı eklendi, `spec.md`'ye AC10 olarak kabul örneği yazıldı.
| **İ3** | **Sokratik blok bir cevap değil, bir soru gibi görünür.** Sonuç ekranında geri bildirim kutusu "başarı mesajı" estetiğinde değil, alıntı/not estetiğinde. | spec §6: tutor cevap vermez, sorgulatır |
| **İ4** | **Tek elle, tek başparmakla oynanır.** Tüm dokunma hedefleri ekranın alt %60'ında; üst alan sadece okuma. | spec §1: telefonda 3-5 dakikalık oturum |

---

## 2. Tasarım Dili

### 2.1 Renk

Koyu zemin seçildi: senaryolar baskı/gece anlarında geçiyor, koyu yüzey telefonda uzun metin okumayı kolaylaştırıyor ve "Primer" kitap metaforuna lamba ışığı hissi uyuyor.

| Token | Değer | Kullanım |
|---|---|---|
| `--ink-900` | `#0E1116` | Ekran zemini |
| `--ink-800` | `#161B22` | Kart ve panel yüzeyi |
| `--ink-700` | `#222A35` | Kenarlık, ayırıcı, pasif durum |
| `--text-high` | `#E6EAF0` | Başlık ve gövde metni |
| `--text-mid` | `#9AA6B8` | İkincil metin, yardım metni, ilerleme |
| `--amber-400` | `#E8A33D` | Birincil aksiyon, vurgu, aktif ilerleme noktası |
| `--amber-300` | `#F2C078` | Basılı/odaklı durum |
| `--good` | `#4FB286` | Yalnızca İYİ SON bandı |
| `--risk` | `#D96F63` | Yalnızca KÖTÜ SON bandı |
| `--focus` | `#7AA2F7` | Klavye odak halkası (2px) |

**Kurallar:**
- `--good` ve `--risk` **yalnızca sonuç ekranında** kullanılır. Karar ekranında asla — İ2'nin ihlali olur.
- Renk tek başına anlam taşımaz: iyi/kötü son renkle *ve* metinle *ve* ikonla belirtilir.
- Kehribar üzerindeki metin `--ink-900`'dir (koyu metin / açık buton), beyaz değil — kontrast oranı için.

### 2.2 Tipografi

Yazı tipi **Inter** (Stitch'te hazır mevcut, Türkçe karakter desteği tam).

| Rol | Boyut / satır yüks. | Ağırlık |
|---|---|---|
| Ekran başlığı | 28 / 34 | 600 |
| Senaryo/kriz gövdesi | 17 / 26 | 400 |
| Seçenek metni | 16 / 24 | 500 |
| İkincil / yardım metni | 14 / 20 | 400 |
| Etiket, ilerleme | 12 / 16 | 500, harf aralığı +0.04em |

Gövde metni 17px: 16'nın altına inmek 26 satır yüksekliğiyle birlikte telefonda yorucu oluyor, kriz metinleri 3-5 satır uzunluğunda.

### 2.3 Ölçü ve boşluk

- Boşluk ölçeği 4'ün katları: `4, 8, 12, 16, 20, 24, 32, 40`
- Ekran kenar boşluğu: **20px** (spec AC7: yatay kaydırma olmamalı)
- Köşe yarıçapı: kart `16px`, buton ve seçenek `12px`
- Dokunma hedefi: minimum `44px`, hedeflenen `48px` yükseklik (AC7)
- Seçenekler arası dikey boşluk: `12px` — yanlış dokunmayı önlemek için

---

## 3. Bileşen Envanteri

Dört ekran bu sekiz bileşenden kuruluyor. Her bileşen tek işe sahip; bu ayrım Stitch'te tekrar üretmeyi ve AI Studio'da yeniden kullanmayı kolaylaştırıyor.

| Bileşen | İşi | Durumları |
|---|---|---|
| `SegmentedChoice` | Profil sorusu — 2-3 seçenekli yatay grup | boş · seçili · odaklı |
| `PrimaryButton` | Tek birincil aksiyon (kehribar dolgu) | aktif · **pasif** (AC1) · basılı |
| `ScenarioCard` | Menüde bir senaryo (başlık + 1 satır özet + süre) | normal · basılı |
| `CrisisPanel` | Kriz kurulum metni (kart yüzeyi, sol kenarda kehribar şerit) | — |
| `ProgressDots` | 3 karar noktasının kaçıncısındayız | 1/3 · 2/3 · 3/3 |
| `DecisionOption` | Bir seçenek (tam genişlik, nötr, eşit ağırlık) | normal · basılı |
| `OutcomeBanner` | İYİ SON / KÖTÜ SON bandı + sağlam karar sayısı | iyi · kötü |
| `SocraticBlock` | Tutor geri bildirimi (alıntı estetiği) | **yükleniyor** · yüklendi · **hata** |

`SocraticBlock`'un üç durumu olması şart: canlı LLM çağrısı yavaş veya başarısız olabilir (spec §9 varsayım 2). Tasarımda bu durumlar yoksa AI Studio'da boş kutu görünür ve demo videoda bu yakalanır.

---

## 4. Ekranlar

### E1 — Profil

```
┌───────────────────────────────┐ 390
│ 20                            │
│  Primer                       │  28/600, kehribar nokta logo
│  Üç soru, sonra başlıyoruz.   │  14 --text-mid
│                               │
│  ── 24 ──                     │
│  Kaçıncı sınıftasın?          │  12 etiket --text-mid
│  ┌─────────┐ ┌─────────┐      │
│  │  1-2    │ │  3-4    │      │  SegmentedChoice, 48px
│  └─────────┘ └─────────┘      │
│                               │
│  Hangi role yakınsın?         │
│  ┌────────┐┌────────┐┌───────┐│
│  │Frontend││Backend ││ Henüz ││  3'lü, metin 14'e düşer
│  └────────┘└────────┘└───────┘│
│                               │
│  Şu an senin için önemli olan?│
│  ┌─────────────────────────┐  │
│  │ Staj bulmak             │  │  dikey liste, 48px
│  ├─────────────────────────┤  │
│  │ Projeyi bitirmek        │  │
│  ├─────────────────────────┤  │
│  │ Öğrenmek                │  │
│  └─────────────────────────┘  │
│                               │
│         ( esnek boşluk )      │
│  ┌─────────────────────────┐  │
│  │        Devam            │  │  PrimaryButton, PASİF
│  └─────────────────────────┘  │  3 alan dolana kadar
│  Simülasyon cevapların        │  12 --text-mid
│  kaydedilmiyor.               │
└───────────────────────────────┘
```

**Davranış:** "Devam" üç alan da seçilene kadar pasif (`--ink-700` zemin, `--text-mid` metin, dokunma yanıtı yok) → **AC1**.
**Neden üçüncü soru dikey:** "Staj bulmak" gibi ifadeler yatay segmentte kesilir; okunurluk sıkışıklığa yeniliyor.
**Neden bu not var:** Kullanıcıya veri toplandığını düşündürmemek hem dürüstlük hem de arkadaş testinde gereksiz soru engelliyor.

> **v2'de düzeltildi.** Not önce "Cevapların kaydedilmiyor" diyordu. Serbest sohbet eklenince bu cümle yanlış hale geldi — sohbet e-postayı ve geçmişi `localStorage`'a yazıyor. Simülasyon tarafı hâlâ hiçbir şey saklamadığı için cümle silinmedi, **kapsamı daraltıldı**: "Simülasyon cevapların kaydedilmiyor." Sohbet alanına ise ne saklandığını söyleyen ayrı bir not ve "Sohbeti sıfırla" denetimi kondu. Arayüzde yanlış bir şey söylememek, kapsam değişikliğinin ilk gereğiydi.

### E2 — Senaryo Menüsü

```
┌───────────────────────────────┐
│  ← Profil                     │  14 --text-mid, geri dönüş VAR
│                               │  (profil değiştirilebilir)
│  Hangi krizi yaşayalım?       │  28/600
│  Üçünü de oynayabilirsin.     │  14 --text-mid
│                               │
│  ┌─────────────────────────┐  │
│  │ Dönem projesi krizi     │  │  ScenarioCard
│  │ Teslime 48 saat, main   │  │  17 başlık / 14 özet
│  │ bozuk, biri kayıp.      │  │
│  │              ~3 dk  →   │  │  12 --text-mid
│  └─────────────────────────┘  │
│  ┌─────────────────────────┐  │
│  │ İlk staj task'ın        │  │
│  │ Mentor izinde, canlı    │  │
│  │ veriye dokunman gerek.  │  │
│  │              ~3 dk  →   │  │
│  └─────────────────────────┘  │
│  ┌─────────────────────────┐  │
│  │ Vize haftası            │  │
│  │ Üç sınav, bir grup ödevi│  │
│  │ ve kopya şüphesi.       │  │
│  │              ~3 dk  →   │  │
│  └─────────────────────────┘  │
└───────────────────────────────┘
```

**Neden "~3 dk" yazıyor:** arkadaş testinde en büyük terk sebebi süre belirsizliği. Beklenti vermek oturum tamamlama oranını artırır (spec §1 başarı ölçütü 1).
**Kartlar eşit ağırlıkta:** hiçbiri "önerilen" veya "kolay" diye işaretlenmez — İ2.

### E3 — Kriz ve Karar

```
┌───────────────────────────────┐
│  ← Menü              ● ● ○    │  ProgressDots 2/3
│                               │  aktif: kehribar, geçmiş: dolu
│  ┃ Teslime 48 saat kaldı.     │  CrisisPanel
│  ┃ Son migration veritabanını │  sol şerit 3px kehribar
│  ┃ kilitledi, kimse projeyi   │  17/26 --text-high
│  ┃ local'de açamıyor.         │  ← rol=backend uyarlaması
│  ┃ Hoca canlı demo bekliyor.  │
│                               │
│  ── 24 ──                     │
│  Ne yapıyorsun?               │  20/600
│                               │
│  ┌─────────────────────────┐  │
│  │ Son çalışan commit'e    │  │  DecisionOption
│  │ dön, kaybolan işi sonra │  │  tam genişlik, --ink-800
│  │ ekle                    │  │  kenarlık --ink-700
│  └─────────────────────────┘  │
│  ┌─────────────────────────┐  │
│  │ Gece boyu hatayı debug  │  │  ← görsel olarak TAMAMEN
│  │ et, çözene kadar uğraş  │  │     aynı (İ2)
│  └─────────────────────────┘  │
│  ┌─────────────────────────┐  │
│  │ Kendi branch'inde       │  │
│  │ minimal çalışan bir     │  │
│  │ sürüm kur               │  │
│  └─────────────────────────┘  │
│                               │
│  Seçtikten sonra geri         │  12 --text-mid
│  dönemezsin.                  │
└───────────────────────────────┘
```

**Kriz metni rol'e göre değişir** → **AC2**. Metin üç varyantta da aynı uzunlukta tutulmalı (3-4 satır), yoksa düzen zıplar.
**"Geri dönemezsin" uyarısı metin olarak var, modal olarak yok.** Onay modalı eklemek akışı üç kat uzatır ve spec §3'teki "karar bağlayıcıdır" kararını yumuşatır — kasıtlı olarak eklenmedi.
**ProgressDots geri dönüşü değil ilerlemeyi gösterir;** tıklanabilir değil → **AC3**.

### E4 — Sonuç ve Sokratik Geri Bildirim

```
┌───────────────────────────────┐
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━┓  │  OutcomeBanner
│  ┃ ✓  İYİ SON              ┃  │  --good zemin %12 opak
│  ┃    2/3 sağlam karar     ┃  │  sol kenar 4px --good
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━┛  │  ikon + metin + renk
│                               │
│  Proje teslim edildi. Hoca    │  17/26
│  eksikleri biliyordu, demo    │  son metni
│  canlıda çalıştı.             │
│                               │
│  ── 24 ──                     │
│  ╭─────────────────────────╮  │  SocraticBlock
│  │ ,,                      │  │  alıntı tırnağı, kehribar
│  │ Son çalışan commit'e    │  │  17/26, kart --ink-800
│  │ dönmeyi seçtin. O       │  │  üstte "düşün" etiketi YOK
│  │ commit'in gerçekten     │  │  — başarı mesajı gibi
│  │ çalıştığını nereden     │  │     görünmemeli (İ3)
│  │ biliyordun? Kaybolan iş │  │
│  │ kimin işiydi?           │  │
│  ╰─────────────────────────╯  │
│                               │
│  ┌─────────────────────────┐  │
│  │   Başka bir kriz dene   │  │  PrimaryButton → E2
│  └─────────────────────────┘  │
│  Aynı krizi tekrar oyna       │  14, metin bağlantı → E3
└───────────────────────────────┘
```

**`SocraticBlock` yükleniyor durumu:** üç satır iskelet (skeleton) çubuğu, `--ink-700`, nefes alan opaklık animasyonu. Spinner değil — spinner "bekle" der, iskelet "metin geliyor" der.
**`SocraticBlock` hata durumu:** kutu yerinde kalır, içinde `--text-mid` ile: *"Rehber şu an cevap veremedi. Kendine sor: bu kararı verirken neyi varsaydın?"* — sabit bir yedek soru. Bu, LLM çökse bile ekranın Sokratik kalmasını ve **AC6**'nın geçmesini sağlıyor.
**"Başka bir kriz dene" → E2, kararlar sıfırlanır, profil korunur** → **AC8**.

---

## 5. Erişilebilirlik ve Doğrulama

| Konu | Karar |
|---|---|
| Kontrast | Gövde metni `--text-high` / `--ink-900` ≈ 14:1; ikincil `--text-mid` / `--ink-900` ≈ 7:1. İkisi de WCAG AA'yı aşıyor. |
| Dokunma hedefi | Tüm etkileşimli öğeler ≥ 44px yükseklik, hedef 48px → **AC7** |
| Renk bağımsızlığı | İYİ/KÖTÜ SON renk + ikon + metinle belirtilir; renk körlüğünde anlam kaybolmaz |
| Odak | 2px `--focus` halkası, `outline-offset: 2px`; klavye ile tüm akış gezilebilir |
| Yatay kaydırma | 390px genişlikte hiçbir öğe taşmaz; 20px kenar boşluğu sabit → **AC7** |
| Metin ölçeği | Kullanıcı yazı tipini %130 büyütürse düzen bozulmaz (sabit yükseklik yok, içerik akar) |

---

## 6. Stitch Prompt'ları

Aşağıdakiler **gerçekten ekran üreten, doğrulanmış** prompt'lardır (bkz. §9).

**Prompt yapısı ve nedeni.** İlk denemede prompt'lar renk token listesiyle başlıyordu; Stitch bunu "bana bir tema tanımla" talebi olarak okudu ve ekran yerine bir palet/tema sayfası üretti. Çalışan yapı üç kuralla düzeltildi:

1. Prompt **"Design ONE finished mobile app screen"** ile başlar — ne istendiği ilk cümlede söylenir
2. İçerik yukarıdan aşağıya tek tek sayılır, metinler tırnak içinde verilir
3. Stil **sona** iner ve en altta şu cümle yer alır: *"Do not design a style guide, palette page or component sheet."*

Üçüncü madde asıl düzeltmedir; onsuz Stitch tema sayfasına dönme eğiliminde.

### E1 Profil
```
Design ONE finished mobile app screen (portrait phone, 390x844) for an
interactive learning app called "Primer". This is the onboarding screen
where a software engineering student answers three short questions before
starting.

Screen content, top to bottom:
- A small amber dot next to the app name "Primer" in large semibold text
- One muted subtitle line: "Üç soru, sonra başlıyoruz."
- Question 1: small uppercase label "KAÇINCI SINIFTASIN?" with two
  equal-width pill buttons side by side: "1-2" and "3-4"
- Question 2: label "HANGİ ROLE YAKINSIN?" with three equal-width pill
  buttons side by side: "Frontend", "Backend", "Henüz bilmiyorum"
- Question 3: label "ŞU AN SENİN İÇİN ÖNEMLİ OLAN?" with three full-width
  stacked option buttons: "Staj bulmak", "Projeyi bitirmek", "Öğrenmek"
- At the bottom, a full-width button labeled "Devam" drawn in a DISABLED,
  greyed-out state (grey background, grey text, no amber)
- Under the button, tiny muted text: "Simülasyon cevapların kaydedilmiyor."

Style: dark UI. Page background #0E1116, cards and buttons #161B22,
borders #222A35, primary text #E6EAF0, muted text #9AA6B8, accent amber
#E8A33D. Inter font. 20px side padding, 16px card corners, 12px button
corners, every tap target at least 48px tall, no horizontal scrolling.

Do not design a style guide, palette page or component sheet.
Output one finished phone screen with exactly this content.
```

### E2 Senaryo Menüsü
```
Design ONE finished mobile app screen (portrait phone, 390x844) — the
scenario menu of a learning app called "Primer", where the student picks
which crisis to play.

Screen content, top to bottom:
- A small muted back link: "← Profil"
- Large semibold heading: "Hangi krizi yaşayalım?"
- Muted subtitle: "Üçünü de oynayabilirsin."
- Three stacked cards, identical in every respect. Each card contains a
  semibold title, two lines of muted description, and a bottom row with
  muted "~3 dk" on the left and a small amber arrow on the right:
  Card 1 — "Dönem projesi krizi" / "Teslime 48 saat, main bozuk, biri
  kayıp."
  Card 2 — "İlk staj task'ın" / "Mentor izinde, canlı veriye dokunman
  gerek."
  Card 3 — "Vize haftası" / "Üç sınav, bir grup ödevi ve kopya şüphesi."

Style: dark UI. Page background #0E1116, cards #161B22, borders #222A35,
primary text #E6EAF0, muted text #9AA6B8, accent amber #E8A33D. Inter
font. 20px side padding, 16px card corners, 12px gap between cards.

CONSTRAINT: the three cards must be visually identical — same size, same
background, same border. None of them is featured, recommended,
highlighted, or carries a badge or label.

Do not design a style guide, palette page or component sheet.
Output one finished phone screen with exactly this content.
```

### E3 Kriz ve Karar
```
Design ONE finished mobile app screen (portrait phone, 390x844) — the
decision screen of a learning app called "Primer", where the student reads
a crisis situation and chooses what to do.

Screen content, top to bottom:
- Top row: muted back link "← Menü" on the left; on the right three small
  progress dots — the first two filled amber, the third hollow grey
- A panel on a dark card background with a 3px solid amber stripe down its
  left edge, containing this paragraph: "Teslime 48 saat kaldı. Son
  migration veritabanını kilitledi, kimse projeyi local'de açamıyor. Hoca
  canlı demo bekliyor."
- Semibold heading: "Ne yapıyorsun?"
- Three full-width option buttons, stacked with equal gaps, left-aligned
  text that wraps to multiple lines:
  "Son çalışan commit'e dön, kaybolan işi sonra ekle"
  "Gece boyu hatayı debug et, çözene kadar uğraş"
  "Kendi branch'inde minimal çalışan bir sürüm kur"
- Tiny muted note at the bottom: "Seçtikten sonra geri dönemezsin."

Style: dark UI. Page background #0E1116, panels and buttons #161B22,
borders #222A35, primary text #E6EAF0, muted text #9AA6B8, accent amber
#E8A33D. Inter font. 20px side padding, 16px panel corners, 12px button
corners, each option at least 48px tall, 12px gap between options.

CRITICAL CONSTRAINT: the three option buttons must be identical in style —
same background, same border, same text size and weight. No icons, no
checkmarks, no numbers, no color differences, no badges, no "recommended"
marker, no highlight on any one of them. Nothing in the design may hint
which option is the better choice.
Do not add any eyebrow label, alert header or extra caption.

Do not design a style guide, palette page or component sheet.
Output one finished phone screen with exactly this content.
```

### E4 Sonuç ve Sokratik Geri Bildirim
```
Design ONE finished mobile app screen (portrait phone, 390x844) — the
result screen of a learning app called "Primer", shown after the student
has made three decisions.

Screen content, top to bottom:
- A full-width outcome banner with a soft green tinted background and a
  4px solid green left edge, containing a check icon, "İYİ SON" in
  semibold, and muted smaller text underneath: "2/3 sağlam karar"
- A paragraph: "Proje teslim edildi. Hoca eksikleri biliyordu, demo
  canlıda çalıştı."
- A quote block on a dark card with a large amber quotation mark in its
  top-left corner, containing this text: "Son çalışan commit'e dönmeyi
  seçtin. O commit'in gerçekten çalıştığını nereden biliyordun? Kaybolan
  iş kimin işiydi?"
- A full-width amber button with dark text: "Başka bir kriz dene"
- Below it, a small amber text link: "Aynı krizi tekrar oyna"

Style: dark UI. Page background #0E1116, cards #161B22, borders #222A35,
primary text #E6EAF0, muted text #9AA6B8, accent amber #E8A33D, success
green #4FB286. Inter font. 20px side padding, 16px card corners, 12px
button corners.

CONSTRAINTS:
- The quote block must read as a quiet note or question, NOT as a success
  message. Inside it: no green, no checkmark, no celebration icon, no
  congratulation, and no label above or below the question text.
- Do not add any revision badge, version number, eyebrow label or caption
  that is not listed above.

Do not design a style guide, palette page or component sheet.
Output one finished phone screen with exactly this content.
```

### E4-kötü Sonuç (kötü son)

```
Design ONE finished mobile app screen (portrait phone, 390x844) — the
result screen of a learning app called "Primer", this time showing a BAD
outcome.

Screen content, top to bottom:
- A full-width outcome banner with a soft red tinted background and a 4px
  solid red (#D96F63) left edge, containing "KÖTÜ SON" in semibold and
  muted smaller text underneath: "1/3 sağlam karar"
- A paragraph: "Demo sunumda çöktü. Hoca projeyi değil, hazırlıksızlığı
  gördü. Takım arkadaşın hiç ortaya çıkmadı."
- A quote block on a dark card with a large amber quotation mark in its
  top-left corner, containing this text: "Gece boyu debug etmeyi seçtin.
  O saatlerin sonunda elinde ne vardı? Teslime kalan süreyi kim takip
  ediyordu?"
- A full-width amber button with dark text: "Başka bir kriz dene"
- Below it, a small amber text link: "Aynı krizi tekrar oyna"

Style: dark UI. Page background #0E1116, cards #161B22, borders #222A35,
primary text #E6EAF0, muted text #9AA6B8, accent amber #E8A33D, risk red
#D96F63. Inter font. 20px side padding, 16px card corners.

CONSTRAINTS:
- The quote block must read as a quiet question, NOT as a verdict. No red
  inside it, no warning icon, no "you failed" tone, no label above or
  below it.
- Do not add any extra badge, revision number, eyebrow label or caption.

Do not design a style guide, palette page or component sheet.
Output one finished phone screen with exactly this content.
```

### E3-c Kriz ve Karar — frontend rolü (AC2 kanıtı)

E3 ile aynıdır, yalnızca kriz paragrafı değişir. İki ekranı yan yana koymak §4'teki kişiselleştirme kuralının görsel kanıtını oluşturur.

```
Design ONE finished mobile app screen (portrait phone, 390x844) — the same
decision screen as before, but for a student whose target role is FRONTEND.
Only the crisis paragraph changes; everything else stays identical.

Screen content, top to bottom:
- Top row: muted back link "← Menü" on the left; three small progress dots
  on the right — first two filled amber, third hollow grey
- A panel on a dark card with a 3px amber stripe down its left edge:
  "Teslime 48 saat kaldı. Build pipeline kırıldı, npm run build hata
  veriyor, kimse projeyi derleyemiyor. Hoca canlı demo bekliyor."
- Semibold heading: "Ne yapıyorsun?"
- Three full-width option buttons, equal gaps, left-aligned wrapping text:
  "Son çalışan commit'e dön, kaybolan işi sonra ekle"
  "Gece boyu hatayı debug et, çözene kadar uğraş"
  "Kendi branch'inde minimal çalışan bir sürüm kur"
- Tiny muted note at the bottom: "Seçtikten sonra geri dönemezsin."

Style: dark UI. Page background #0E1116, panels and buttons #161B22,
borders #222A35, primary text #E6EAF0, muted text #9AA6B8, accent amber
#E8A33D. Inter font. 20px side padding, 16px panel corners, 12px button
corners, 12px gap between options.

CRITICAL CONSTRAINT: the three option buttons must be identical in style.
No icons, chevrons, checkmarks, numbers, color differences or badges.
Nothing may hint which option is better.
Do not add any eyebrow label, alert header or extra caption.

Do not design a style guide, palette page or component sheet.
Output one finished phone screen with exactly this content.
```

---

## 7. Spec Eşlemesi

Her kabul örneğinin hangi ekranda ve hangi tasarım kararıyla karşılandığı:

| Kabul örneği | Ekran | Tasarım kararı |
|---|---|---|
| **AC1** profil zorunlu | E1 | `PrimaryButton` pasif durumu (`--ink-700` zemin) |
| **AC2** rol bazlı içerik | E3 | `CrisisPanel` metni üç varyantta, eşit uzunlukta |
| **AC3** geri dönüş yok | E3 | `ProgressDots` tıklanamaz; metinsel uyarı |
| **AC4** iyi son | E4 | `OutcomeBanner` iyi durumu (`--good`, ✓ ikon) |
| **AC5** kötü son | E4 | `OutcomeBanner` kötü durumu (`--risk`, uyarı ikon) |
| **AC6** Sokratik kural | E4 | `SocraticBlock` + hata durumundaki sabit yedek soru |
| **AC7** mobil düzen | hepsi | 20px kenar boşluğu, 48px hedefler, sabit yükseklik yok |
| **AC8** baştan başla | E4 | "Başka bir kriz dene" → E2, profil korunur |
| **AC9** Türkçe büyük harf | hepsi | `<html lang="tr">` — bkz. §9.5; Stitch çıktıları `lang="en"` taşıyor |

---

## 8. Tasarım Tarafında Kapsam Dışı

| Yapılmayan | Gerekçe |
|---|---|
| Açık tema / tema değiştirici | Tek tema dört ekranı tutarlı tutuyor; iki tema hem Stitch'te hem Cypress'te iş yükünü ikiye katlar. |
| Geçiş animasyonları | 60 saniyelik demoda ölçülen akışın çalışması; animasyon AI Studio'da ek kırılganlık getirir. |
| İllüstrasyon / karakter görseli | Metin tabanlı simülasyonda görsel, krizin tonunu yanlış yere çeker (oyunlaştırma hissi, Sokratik ciddiyet değil). |
| Onay modalı ("emin misin?") | spec §3'teki "karar bağlayıcıdır" kararını yumuşatır ve akışı uzatır. |
| Kendi tasarım sistemi dokümantasyonu | Dört ekran ve sekiz bileşen için ayrı bir sistem belgesi aşırı; §2 ve §3 yeterli. |

---

## 9. Üretim Notları (Stitch)

**Üretim tarihi:** 2026-10-29 · **Araç:** Google Stitch · **Üretilen ekran:** 7

Bu bölüm, tasarımın gerçekten üretildiğini ve bu belgeden sapan her noktanın bilinçli bir karar olduğunu kayda geçirmek için yazıldı.

### 9.1 Ekran envanteri

| # | Ekran | Klasör | Durum |
|---|---|---|---|
| E1 | Profil | `stitch_primer_onboarding_screen/primer_onboarding_screen/` | ✅ kullanılacak |
| E2 | Senaryo menüsü | `stitch_primer_onboarding_screen/primer_senaryo_se_imi/` | ✅ kullanılacak |
| E3-a | Kriz & karar, varyant 1 | `stitch_primer_onboarding_screen/primer_kriz_ve_karar_1/` | ⊘ değerlendirildi, seçilmedi |
| E3-b | Kriz & karar, varyant 2 | `stitch_primer_onboarding_screen/primer_kriz_ve_karar_2/` | ✅ **referans** |
| E3-c | Kriz & karar, frontend rolü | `…(1)/stitch_primer_onboarding_screen/primer_kriz_ve_karar_frontend/` | ✅ AC2 kanıtı |
| E4-iyi | Sonuç, iyi son | `…(1)/stitch_primer_onboarding_screen/primer_sonu/` | ✅ kullanılacak |
| E4-kötü | Sonuç, kötü son | `…(1)/stitch_primer_onboarding_screen/primer_k_t_son/` | ✅ kullanılacak |

> **Bilinen tutarsızlık:** E4-iyi'nin dışa aktarımındaki `screen.png`, düzeltme öncesi sürümden kalmıştır (önceki dosyayla byte düzeyinde aynıdır). Aynı klasördeki `code.html` düzeltilmiş sürümdür. Değerlendirmede `code.html` esas alınmalıdır.

### 9.2 İlke doğrulaması

Üretilen ekranlar §1'deki dört ilkeye göre denetlendi:

| İlke | Sonuç |
|---|---|
| **İ1** karar ekranda tek başına durur | E3-b ve E3-c'de tutuyor. E3-a'da üç ek katman var (üst etiket, uyarı başlığı, seçeneklerde `>` oku) — bu yüzden seçilmedi |
| **İ2** seçenekler görsel olarak eşit | **Üç E3 varyantının hepsinde tutuyor.** Hiçbir seçenekte tik, renk farkı, rozet veya boyut farkı yok. E2'deki üç senaryo kartı da birbirinin aynısı |
| **İ3** Sokratik blok cevap gibi görünmez | E4-kötü'de tutuyor. E4-iyi'nin ilk üretiminde `Post-Mortem Çıkarımı` etiketi vardı — soruları "çıkarım" diye adlandırmak varılmış bir sonuç ima ettiği için ihlal sayıldı ve kaldırıldı |
| **İ4** tek elle oynanır | Tüm dokunma hedefleri ekranın alt bölümünde, 48px üzerinde |

### 9.3 E3 varyant kararı

İki varyant üretildi, **E3-b seçildi.** Gerekçe iki katlı:

1. **İlke uyumu:** E3-a ekrana `SENARYO • KRİZ #02` üst etiketi, `⚠ Acil Durum Bildirimi` başlığı ve her seçeneğe `>` oku ekliyor. Bunların hiçbiri İ2'yi ihlal etmiyor (üçüne de eşit uygulanmış), ama İ1'e ters: karar ekranı sadeleştikçe kararın ağırlığı artıyor.
2. **Token uyumu:** E3-b bu belgedeki renk token'larını kullanıyor (`#161B22`, `#222A35`, `#E6EAF0`, `#9AA6B8`); E3-a bunların yerine Stitch'in Material karşılıklarını kullanıyor.

E3-a silinmedi; değerlendirilmiş bir alternatif olarak repoda tutuluyor.

### 9.4 Kabul edilen sapmalar

Aşağıdakiler ölçüldü, değerlendirildi ve **düzeltilmemesine karar verildi.** Ortak gerekçe: Stitch çıktıları nihai ürün değil tasarım referansıdır; nihai renkler ve işaretleme AI Studio aşamasında uygulanacaktır. Stitch'te hex kovalamak, gözle görünmeyen bir kazanç için saatler harcamak olurdu.

| Sapma | Ölçüm | Etkilenen ekran |
|---|---|---|
| Zemin rengi | `#111319` kullanıldı, bu belgede `#0E1116` | 7/7 |
| Nötr renkler | Stitch'in Material paleti (`#1d2025`, `#e1e2e9`, `#bbc7da`) | E1, E3-a, E4-iyi |
| Kötü son kırmızısı | Material error paleti (`#ffb4ab` / `#93000a`), bu belgede `#D96F63` | E4-kötü |
| `<html lang="en">` | 7/7 ekranda | **AI Studio'ya taşınacak gereksinim, bkz. §9.5** |

### 9.5 AI Studio'ya taşınacak iki gereksinim

Stitch aşamasında ortaya çıkan ama orada çözülmeyecek olan iki şey:

**1. `<html lang="tr">` zorunlu.** Stitch tüm dosyalara `lang="en"` yazdı. CSS'in `text-transform: uppercase` dönüşümü dile duyarlıdır: `lang="en"` altında `i` harfi `I` olur, `lang="tr"` altında doğru şekilde `İ` olur. E4-iyi'nin ilk üretiminde `Simülasyon Özeti` etiketi ekranda `SIMÜLASYON ÖZETI` diye göründü — kök neden buydu. Bu bulgu `spec.md`'ye **AC9** olarak eklendi.

**2. `data-testid` nitelikleri zorunlu.** Bu belgedeki sekiz bileşenin her etkileşimli örneği sabit bir test kimliği taşımalı. Cypress testleri elementleri görünen metne göre bulursa, metnin tek kelimesi değiştiğinde testler kırılır. Sonradan eklemek uygulamayı yeniden ürettirmek demektir; üretim sırasında eklemek maliyetsizdir.

| Bileşen | Beklenen `data-testid` |
|---|---|
| `SegmentedChoice` | `profil-sinif`, `profil-rol`, `profil-hedef` |
| `PrimaryButton` (E1) | `profil-devam` |
| `ScenarioCard` | `senaryo-donem-projesi`, `senaryo-staj-task`, `senaryo-vize-haftasi` |
| `CrisisPanel` | `kriz-metni` |
| `ProgressDots` | `ilerleme` |
| `DecisionOption` | `secenek-0`, `secenek-1`, `secenek-2` |
| `OutcomeBanner` | `sonuc-bandi` |
| `SocraticBlock` | `sokratik-blok` |
| "Baştan başla" | `bastan-basla` |
