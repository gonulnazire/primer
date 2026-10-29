# Tutor Eval — Ham Koşum Sonuçları

**Ölçüm kaynağı:** `https://primer-1.ai.studio/api/socratic` · **Koşum tarihi:** 2026-10-29 · **Örnek sayısı:** 4

Protokol: `spec.md` §6.4. Kurallar: `spec.md` §6.1. Etiketler: `spec.md` §6.3.

**S1, S2, S5 otomatik denetlendi.** S3 (seçime atıf), S4 (varsayım avı) ve S6
(kararı nitelememe) regex'e yazılamadığı için elle etiketlenir — son sütunu siz
doldurun.

## Özet tablo

| # | Senaryo | Sınıf | Rol | Hedef | Son | S1 | S2a | S2b | S5 | Kelime | Süre | **Etiket** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E17 | vize-haftasi | 1-2 | frontend | proje | iyi | ✓ | ✓ | ✓ | ✓ | 34 | 1249 ms | |
| E18 | vize-haftasi | 3-4 | backend | ogrenme | kotu | ✓ | ✓ | ✓ | ✓ | 39 | 1537 ms | |
| E19 | vize-haftasi | 3-4 | frontend | staj | iyi | ✓ | ✓ | ✓ | ✓ | 45 | 1379 ms | |
| E20 | vize-haftasi | 1-2 | bilmiyorum | proje | kotu | ✓ | ✓ | ✓ | ✓ | 41 | 27531 ms | |

## Cevaplar

### E17 — vize-haftasi · 1-2 · frontend · proje · iyi (2/3)

**Verilen kararlar:** saglam · orta · saglam

> Arkadaşına doğrudan sorup gruptan süre istemeyi ve kendi katkını işaretleyerek teslim etmeyi seçtin. Tüm ekip üyelerinin akademik yüklerinin aynı olduğunu mu varsayıyorsun? Kendi katkını ayırmanın, kalan ortak sorumlulukların geleceği üzerinde nasıl bir etkisi olabilir?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E18 — vize-haftasi · 3-4 · backend · ogrenme · kotu (0/3)

**Verilen kararlar:** orta · riskli · orta

> Sessizce kendi kodunu ayırıp gece çalışarak ödevi mükemmel yapmayı ve teslimi geciktirmeyi seçtin. 
> 
> Ekip çalışmasında bireysel mükemmeliyetçiliği önde tutarken, backend sistemlerindeki bağımlılık yönetimini ve zaman maliyetini nasıl hesaba kattın? Bu yaklaşım, gerçek bir projede ekip içi iletişimi nasıl etkiler?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E19 — vize-haftasi · 3-4 · frontend · staj · iyi (2/3)

**Verilen kararlar:** saglam · saglam · riskli

> Arkadaşına doğrudan sormayı ve ödevi geçer seviyede bırakıp en ağır vizeye odaklanmayı seçtin. Projeyi bu şekilde, hiçbir not eklemeden teslim ettin. 
> 
> Sektörde kıdemli bir frontend geliştiriciyle kod incelemesinde (code review) karşılaştığında, bu eksik teslimatı nasıl savunursun? Gelecekteki mülakatlarda bu yaklaşımın teknik sahiplenme algısını nasıl etkiler?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E20 — vize-haftasi · 1-2 · bilmiyorum · proje · kotu (0/3)

**Verilen kararlar:** riskli · orta · riskli

> "Hiçbir şey deme, olduğu gibi teslim et" ve "olduğu gibi, hiçbir not düşmeden teslim et" kararlarını seçtin. Bu tercihlerle, eksik işin ekip arkadaşlarına ve hocaya nasıl görüneceğini varsayıyorsun? Acaba bu sessizlik, projede senin sorumluluğunda olan kısımlar hakkında nasıl bir izlenim bırakır?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

## Etiketleme sonrası doldurulacak

| Etiket | Adet | Oran |
|---|---|---|
| OK | | |
| A — cevap sızdırma | | |
| B — soru yok | | |
| C — genel geçer | | |
| D — çok uzun | | |
| E — kararı niteliyor | | |
| **Toplam** | 4 | %100 |

**Başarı eşiği:** `spec.md` §1 — OK oranı en az %80 olmalı.
