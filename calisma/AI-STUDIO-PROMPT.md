# AI Studio İnşa Prompt'u — Adım 3

> **Teslim belgesi değil, çalışma dosyası.** Google AI Studio'ya verilecek prompt burada hazır duruyor.
>
> **Ekli dosya:** [`ekran-markup.html`](./ekran-markup.html) — altı ekranın Stitch'ten çıkarılmış, token bloğundan arındırılmış markup'ı. AI Studio'ya prompt ile birlikte verin.

---

## ⚠ Probe sonucuna bağlı tek bölüm

Aşağıdaki prompt, `spec.md` §3'teki **hibrit mimarinin çalıştığı** varsayımıyla yazıldı: dallanma önceden yazılmış, Sokratik geri bildirim canlı LLM'den geliyor.

Gemini probe'u başarısız olursa (kota, erişim veya Türkçe kural uyumsuzluğu) değişecek **tek bölüm §5'tir** — Sokratik katman canlı çağrı yerine önceden yazılmış soru havuzuna döner. Prompt'un geri kalanı aynı kalır.

---

## Prompt (buradan aşağısını kopyalayın)

```
Build a single-page interactive mobile web app called "Primer".
It is a Socratic learning simulation for software engineering students.
Attached is `ekran-markup.html` containing the finished design for six
screens. Follow it closely.

═══════════════════════════════════════════════════════════════
1. WHAT THE APP DOES
═══════════════════════════════════════════════════════════════

A student answers three profile questions, picks one of three crisis
scenarios, makes three decisions inside it, and reaches one of two
endings. On the result screen a Socratic tutor asks questions about the
decisions instead of telling the student what was right.

Four screens, all in ONE page with client-side state (no routing library,
no backend, no database, no login):

  E1 Profile  →  E2 Scenario menu  →  E3 Crisis & decisions (x3)
              →  E4 Result + Socratic feedback  →  back to E2

═══════════════════════════════════════════════════════════════
2. STATE
═══════════════════════════════════════════════════════════════

profile = { sinif: "1-2" | "3-4",
            rol:   "frontend" | "backend" | "bilmiyorum",
            hedef: "staj" | "proje" | "ogrenme" }

run     = { senaryoId: "donem-projesi" | "staj-task" | "vize-haftasi",
            kararlar: []  // three entries: "saglam" | "orta" | "riskli"
          }

- Nothing is persisted. No localStorage, no server.
- "Başka bir kriz dene" resets `run` and keeps `profile`.
- E1's "Devam" button stays DISABLED until all three profile fields are
  set.

ENDING RULE (exact): if at least 2 of the 3 decisions are labelled
"saglam" → GOOD ENDING. Otherwise → BAD ENDING.
Show the count as "<n>/3 sağlam karar" on the result banner.
The labels saglam/orta/riskli are NEVER shown to the user and must not
be inferable from the markup, class names or ordering.

═══════════════════════════════════════════════════════════════
3. PERSONALISATION
═══════════════════════════════════════════════════════════════

The menu choice decides WHICH scenario runs. The profile decides the
CONTENT inside it:

- `rol` changes the technical detail of the crisis text.
  In "donem-projesi":
    backend     → "Son migration veritabanını kilitledi, kimse projeyi
                   local'de açamıyor."
    frontend    → "Build pipeline kırıldı, npm run build hata veriyor,
                   kimse projeyi derleyemiyor."
    bilmiyorum  → "Proje artık açılmıyor, hata mesajı anlaşılmaz."
  Keep all three variants the same length (3-4 lines) so the layout
  does not jump.

- `sinif` changes how the Socratic questions are framed:
    "1-2" → more guiding    "3-4" → more open-ended

- `hedef` changes the framing on the result screen:
    staj → interview framing · proje → delivery impact ·
    ogrenme → concept connection

═══════════════════════════════════════════════════════════════
4. SCENARIOS (exact content — do not invent or rewrite)
═══════════════════════════════════════════════════════════════

Each scenario: a setup paragraph, then three decision points, each with
three options. The label in [brackets] is internal only.

--- SCENARIO A: "donem-projesi" — Dönem projesi teslim krizi ---
Setup: "Teslime 48 saat kaldı. Üç kişilik takımdasınız. [rol variant].
Takım arkadaşlarınızdan biri iki gündür mesajlara cevap vermiyor. Hoca
sunumda canlı demo bekliyor."

A1 "Ne yapıyorsun?"
  - "Son çalışan commit'e dön, kaybolan işi sonra ekle"        [saglam]
  - "Gece boyu hatayı debug et, çözene kadar uğraş"            [riskli]
  - "Kendi branch'inde minimal çalışan bir sürüm kur"          [orta]
A2 "Kayıp takım arkadaşın hâlâ sessiz. Ne yapıyorsun?"
  - "Net bir süre veren son bir mesaj at, cevap gelmezse hocaya bildir"
                                                                [saglam]
  - "Hiçbir şey söyleme, onun işini de sen yap"                [riskli]
  - "Teslimden sonra durumu hocaya şikayet et"                 [riskli]
A3 "Teslime 6 saat kaldı. Kapsamı nasıl bitiriyorsun?"
  - "Çalışan 3 özelliği cilala, eksikleri sunumda açıkça söyle" [saglam]
  - "8 özelliğin hepsini yarım bırak, demoda hızlı geç"        [riskli]
  - "Demoyu video olarak çek, canlı gösterim riskinden kaç"    [orta]

--- SCENARIO B: "staj-task" — İlk staj task'ın ---
Setup: "Stajınızın ikinci haftası. Mentorunuz izinde. Size 'basit'
denilen bir hata verildi: bir müşteri raporu yanlış toplam gösteriyor.
Düzeltmek için [rol variant] gerekiyor gibi görünüyor. Kimse size bu
yetkiyi vermedi ama teknik erişiminiz var."
  rol variant: backend → "canlı veritabanında bir kaydı UPDATE etmek"
               frontend → "prod'a doğrudan bir hotfix göndermek"
               bilmiyorum → "yetkilendirilmemiş bir sisteme dokunmak"

B1 "Ne yapıyorsun?"
  - "Durumu takım kanalına yazılı olarak sor, bekle"            [saglam]
  - "Hemen düzelt, küçük bir değişiklik, kimse fark etmez"     [riskli]
  - "Hatayı kendi kopyanda çoğalt, kanıtla, sonra öneri getir"  [orta]
B2 "İki saat geçti, kimse cevap vermedi. Ne yapıyorsun?"
  - "Mentorun yerine bakan kişiyi bul ve doğrudan sor"          [saglam]
  - "Canlıda dene, önce yedek al"                              [riskli]
  - "Task'ı beklet, başka işe geç, durumu yazılı not düş"       [orta]
B3 "Çözümü buldun ama test yok. Ne yapıyorsun?"
  - "Küçük bir test yaz, sonra PR aç"                           [saglam]
  - "Test yazmak stajyer işi değil, doğrudan PR aç"            [riskli]
  - "PR'ı aç ama 'test eklenmeli' notunu düş"                   [orta]

--- SCENARIO C: "vize-haftasi" — Vize haftası çatışması ---
Setup: "Üç gün içinde üç vizeniz var. Aynı hafta grup ödevi teslimi.
Grup arkadaşınızın gönderdiği kod çalışıyor, ama internette neredeyse
birebir aynısını buldunuz."

C1 "Ne yapıyorsun?"
  - "Arkadaşına doğrudan ve yargılamadan sor"                   [saglam]
  - "Hiçbir şey deme, olduğu gibi teslim et"                   [riskli]
  - "Sessizce kendi kısmını ayır, onun kodunu kullanma"         [orta]
C2 "İki gün kaldı. Zamanı nasıl bölüyorsun?"
  - "En ağır vizeye odaklan, ödevi geçer seviyede bitir"        [saglam]
  - "Ödevi mükemmel yap, vizelere gece çalış"                  [riskli]
  - "Gruptan birlikte süre uzatımı talebi yazmayı öner"         [orta]
C3 "Teslim anı geldi. Ne yapıyorsun?"
  - "Kendi katkını açıkça işaretleyip teslim et"                [saglam]
  - "Olduğu gibi, hiçbir not düşmeden teslim et"               [riskli]
  - "Teslimi geciktir, önce durumu netleştir"                   [orta]

ENDING TEXTS (exact — do not rewrite or add a moral)

  A good: "Proje teslim edildi. Hoca eksikleri biliyordu, demo canlıda
           çalıştı."
  A bad:  "Demo sunumda çöktü. Hoca projeyi değil, hazırlıksızlığı
           gördü. Takım arkadaşın hiç ortaya çıkmadı."

  B good: "Mentorun döndüğünde sorunu yazılı bir özetle karşıladı.
           Düzeltme ertesi gün test edilip yayına alındı. Takım sana bir
           iş daha emanet etti."
  B bad:  "Canlı veriyi değiştirdin, rapor düzeldi. İki hafta sonra
           muhasebe tutmayan bir kayıt buldu; kimin ne zaman değiştirdiği
           belli değildi. Stajın kalanında sana erişim verilmedi."

  C good: "Ödev geçer notu aldı, üç vizeden ikisini iyi verdin. Grup
           arkadaşın kodun kaynağını hocaya kendisi söyledi."
  C bad:  "Ödev intihal taramasına takıldı. Hoca grubun tamamını çağırdı;
           kodu kimin yazdığını kimse açıklayamadı. Vizelerden birine
           hazırlıksız girdin."

═══════════════════════════════════════════════════════════════
5. THE SOCRATIC TUTOR  (live model call)
═══════════════════════════════════════════════════════════════

On the result screen, call the Gemini API once and render the answer in
the quote block.

MODEL: use `gemini-3.5-flash-lite`.
This was chosen by measurement, not preference: `gemini-3.8-flash`
spends ~821 thinking tokens on a 90-token answer and takes 75-142
seconds, while `gemini-3.5-flash-lite` answers in ~5.6 seconds with zero
thinking tokens and the same rule compliance. Do not substitute another
model. `gemini-2.5-flash` returns 404 for new keys.

Use this prompt, filling the placeholders from state:

  Sen bir Sokratik öğrenme rehberisin. Bir yazılım mühendisliği öğrencisi
  bir kriz senaryosunda kararlar verdi. Görevin ona DOĞRU CEVABI
  VERMEMEK, kendi muhakemesini sorgulatmaktır.

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

  Cevabını Türkçe yaz.

THREE STATES — all three must be implemented:
  loading → three skeleton bars in #222A35 with a soft pulsing opacity.
            NOT a spinner.
  loaded  → the model's text in the quote block.
  error   → the block stays in place and shows this fixed fallback in
            muted text:
            "Rehber şu an cevap veremedi. Kendine sor: bu kararı verirken
             neyi varsaydın?"
            This fallback is required: the screen must stay Socratic even
            when the API fails.

═══════════════════════════════════════════════════════════════
6. HARD REQUIREMENTS
═══════════════════════════════════════════════════════════════

6.1  <html lang="tr">  — REQUIRED.
     CSS text-transform:uppercase is locale aware. Under lang="en" the
     letter "i" becomes "I"; under lang="tr" it correctly becomes "İ".
     Without this, "Simülasyon Özeti" renders as "SIMÜLASYON ÖZETI".

6.2  data-testid on every interactive element — REQUIRED.
     End-to-end tests must not depend on visible text.
       profil-sinif · profil-rol · profil-hedef · profil-devam
       senaryo-donem-projesi · senaryo-staj-task · senaryo-vize-haftasi
       kriz-metni · ilerleme
       secenek-0 · secenek-1 · secenek-2
       sonuc-bandi · sokratik-blok · bastan-basla

6.3  The three decision options must be visually IDENTICAL *and* their
     order must be SHUFFLED.
     Same background, border, text size, weight and height. No icons,
     checkmarks, numbers, colour differences, badges or "recommended"
     markers. Nothing in the markup or class names may hint which option
     is better.
     On top of that, shuffle the three options every time a decision
     point is entered — shuffle ONCE on entry, not on every re-render,
     so options never move while the student is reading them.
     Reason, found by user testing: with a fixed order the "saglam"
     option was always first and a real student worked that out in three
     decisions ("the first choice is always right"). Identical styling is
     not enough — position leaks the answer just as loudly. This is the
     product's core constraint: if the student can read the answer off
     the screen, the app has no purpose.

6.4  The Socratic quote block must read as a quiet question, never as a
     verdict or a success message. No green, no checkmark, no
     celebration, no label above or below it.

6.5  Mobile: 390x844 target, 20px side padding, every tap target at
     least 48px tall, no horizontal scrolling at 390px width.

6.6  The viewport meta tag must NOT contain user-scalable=no or
     maximum-scale. Pinch zoom stays available — blocking it breaks text
     scaling for users who need it and gains nothing here.
     Use exactly:
     <meta name="viewport"
           content="width=device-width, initial-scale=1.0,
                    viewport-fit=cover">

6.7  NEVER read the API key from a URL query parameter.
     URLs end up in browser history, server logs and referrer headers,
     and a shared link or QR code carries the key with it. Ask for the
     key in an in-page dialog and keep it in memory only. Do not write
     it to localStorage, sessionStorage or a cookie.

═══════════════════════════════════════════════════════════════
7. STYLING
═══════════════════════════════════════════════════════════════

The attached markup carries some Tailwind class names from a theme
config that is NOT included. Replace every one of them with the explicit
value below. Keep the literal #hex classes that are already there.

  bg-surface, bg-background                     → #0E1116
  bg-surface-container, -low, -lowest           → #161B22
  bg-surface-container-highest                  → #222A35
  text-on-surface, text-on-background           → #E6EAF0
  text-secondary, text-on-surface-variant,
    text-on-secondary-container                 → #9AA6B8
  text-primary, text-primary-container,
    bg-primary, bg-primary-container,
    border-primary-container                    → #E8A33D
  text-on-primary, text-on-primary-container    → #0E1116
  text-error, bg-error, bg-error-container      → #D96F63
  outline, border-outline                       → #222A35

  font/text-display-lg, -headline-lg   → 28px / 34px / 600
  font/text-headline-md                → 20px / 28px / 600
  font/text-headline-sm                → 18px / 24px / 600
  font/text-body-lg                    → 17px / 26px / 400
  font/text-body-md                    → 14px / 20px / 400
  font/text-body-sm                    → 12px / 16px / 400
  font/text-label-lg                   → 16px / 24px / 500
  font/text-label-md                   → 12px / 16px / 500
  font/text-label-caps                 → 12px / 16px / 500, uppercase,
                                          letter-spacing 0.04em

Font: Inter. Corners: 16px cards, 12px buttons.
Keep the Turkish aria-labels and role attributes already in the markup.

═══════════════════════════════════════════════════════════════
8. DO NOT BUILD
═══════════════════════════════════════════════════════════════

No login or accounts · no database or persistence · no progress saving ·
no score comparison between users · no sound or animation beyond the
loading skeleton · no scenario editor · no free-form chat with the tutor
· no confirmation modal before a decision (decisions are binding by
design) · no light theme or theme switcher.
```

---

## Prompt'tan sonra yapılacak kontrol

Uygulama üretildikten sonra, AI Studio önizlemesinde şunları sırayla doğrulayın:

- [ ] Profilde bir alan boşken "Devam" pasif mi? (AC1)
- [ ] `rol` = backend ve frontend ile aynı senaryoda kriz metni değişiyor mu? (AC2)
- [ ] Karar verdikten sonra geri dönüş yolu var mı? Olmamalı (AC3)
- [ ] 2 sağlam karar → İYİ SON, 1 sağlam karar → KÖTÜ SON (AC4, AC5)
- [ ] Sokratik blokta soru işareti var mı, yasaklı emir kalıbı yok mu? (AC6)
- [ ] 390px genişlikte yatay kaydırma var mı? Olmamalı (AC7)
- [ ] "Başka bir kriz dene" kararları sıfırlayıp profili koruyor mu? (AC8)
- [ ] Büyük harfli bir etiketteki `i` harfi `İ` olarak çıkıyor mu? (AC9)
- [ ] Üç seçenek birbirinden ayırt edilebiliyor mu? **Edilmemeli** (İ2)
- [ ] Sayfa kaynağında `data-testid` nitelikleri var mı? (Cypress için şart)

Bir madde tutmuyorsa AI Studio'ya sadece o maddeyi düzelttiren kısa bir talimat verin; tüm prompt'u yeniden göndermeyin.
