# Tutor Eval — Ham Koşum Sonuçları

**Ölçüm kaynağı:** `https://primer-1.ai.studio/api/socratic` · **Koşum tarihi:** 2026-10-29 · **Örnek sayısı:** 20

Protokol: `spec.md` §6.4. Kurallar: `spec.md` §6.1. Etiketler: `spec.md` §6.3.

**S1, S2, S5 otomatik denetlendi.** S3 (seçime atıf), S4 (varsayım avı) ve S6
(kararı nitelememe) regex'e yazılamadığı için elle etiketlenir — son sütunu siz
doldurun.

## Özet tablo

| # | Senaryo | Sınıf | Rol | Hedef | Son | S1 | S2a | S2b | S5 | Kelime | Süre | **Etiket** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E01 | donem-projesi | 3-4 | backend | staj | iyi | ✓ | ✓ | ✓ | ✓ | 43 | 1024 ms | |
| E02 | donem-projesi | 1-2 | frontend | proje | kotu | ✓ | ✓ | ✓ | ✓ | 39 | 846 ms | |
| E03 | donem-projesi | 1-2 | bilmiyorum | ogrenme | iyi | ✓ | ✓ | ✓ | ✓ | 41 | 1349 ms | |
| E04 | donem-projesi | 3-4 | frontend | staj | kotu | ✓ | ✓ | ✓ | ✓ | 52 | 1739 ms | |
| E05 | donem-projesi | 1-2 | backend | proje | iyi | ✓ | ✓ | ✓ | ✓ | 42 | 1031 ms | |
| E06 | donem-projesi | 3-4 | bilmiyorum | ogrenme | kotu | ✓ | ✓ | ✓ | ✓ | 42 | 1129 ms | |
| E07 | donem-projesi | 3-4 | backend | proje | iyi | ✓ | ✓ | ✓ | ✓ | 47 | 1346 ms | |
| E08 | staj-task | 3-4 | backend | staj | iyi | ✓ | ✓ | ✓ | ✓ | 43 | 1336 ms | |
| E09 | staj-task | 1-2 | frontend | ogrenme | kotu | ✓ | ✓ | ✓ | ✓ | 49 | 980 ms | |
| E10 | staj-task | 3-4 | bilmiyorum | proje | kotu | ✓ | ✓ | ✓ | ✓ | 49 | 1073 ms | |
| E11 | staj-task | 1-2 | backend | staj | iyi | ✓ | ✓ | ✓ | ✓ | 47 | 1650 ms | |
| E12 | staj-task | 3-4 | frontend | proje | iyi | ✓ | ✓ | ✓ | ✓ | 45 | 1418 ms | |
| E13 | staj-task | 1-2 | bilmiyorum | staj | kotu | ✓ | ✓ | ✓ | ✓ | 38 | 938 ms | |
| E14 | staj-task | 1-2 | frontend | ogrenme | iyi | ✓ | ✓ | ✓ | ✓ | 49 | 1524 ms | |
| E15 | vize-haftasi | 3-4 | bilmiyorum | ogrenme | iyi | ✓ | ✓ | ✓ | ✓ | 33 | 1341 ms | |
| E16 | vize-haftasi | 1-2 | backend | staj | kotu | ✓ | ✓ | ✓ | ✓ | 46 | 959 ms | |
| E17 | vize-haftasi | 1-2 | frontend | proje | iyi | ✓ | ✗ | ✗ | ✓ | 0 | 392 ms | |
| E18 | vize-haftasi | 3-4 | backend | ogrenme | kotu | ✓ | ✗ | ✗ | ✓ | 0 | 248 ms | |
| E19 | vize-haftasi | 3-4 | frontend | staj | iyi | ✓ | ✗ | ✗ | ✓ | 0 | 426 ms | |
| E20 | vize-haftasi | 1-2 | bilmiyorum | proje | kotu | ✓ | ✗ | ✗ | ✓ | 0 | 273 ms | |

## Cevaplar

### E01 — donem-projesi · 3-4 · backend · staj · iyi (3/3)

**Verilen kararlar:** saglam · saglam · saglam

> Son çalışan commit'e dönme ve eksik özellikleri sunumda açıklama kararını seçtin. Bir teknik mülakatta bu yaklaşımı "Risk Yönetimi" başlığı altında savunman gerekseydi, işveren adına bu stratejinin en zayıf halkası sence ne olurdu? Staj arayışında bu kararın, teknik kapasiteden ziyade hangi yetkinliğini öne çıkarır?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E02 — donem-projesi · 1-2 · frontend · proje · kotu (0/3)

**Verilen kararlar:** riskli · riskli · riskli

> Tüm özellikleri yarım bırakıp demoda hızlı geçmeyi seçtin ve gece boyu tek başına debug yaptın. Peki, bu yaklaşım sınırlı zamanda değer üretme önceliğinle nasıl örtüşüyor? Tüm ekibin yükünü sırtlandığında, projenin sürdürülebilirliği ve ekip dinamikleri açısından neyi gözden kaçırıyor olabilirsin?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E03 — donem-projesi · 1-2 · bilmiyorum · ogrenme · iyi (2/3)

**Verilen kararlar:** saglam · saglam · orta

> Son çalışan commit'e dönüp eksikleri sonra ekleme kararını seçtin ve videolu demo yolunu izledin. Burada "zamanı geri alarak" riski sıfırladığını varsaydın. Peki, canlı demo yapmamak hocaya sunum anında neyi kanıtlamaz? Bu durum, gerçek bir yazılım krizinde müşteriye karşı ellerini nasıl bağlayabilir?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E04 — donem-projesi · 3-4 · frontend · staj · kotu (0/3)

**Verilen kararlar:** orta · riskli · orta

> Kendi branch'inde minimal bir sürüm kurup takımdan gizlice arkadaşının işini üstlenmeyi ve riski önlemek için demoyu video ile yapmayı seçtin. 
> 
> Bir yazılım müfettişi veya staj mülakatçısı bu "tek kişilik ordu" yaklaşımını ve iletişimsizliği teknik bir başarı olarak mı, yoksa takım çalışması açısından nasıl değerlendirirdi? 
> 
> Bu süreç, gelecekteki iş yerlerinde seni nasıl konumlandırır?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E05 — donem-projesi · 1-2 · backend · proje · iyi (2/3)

**Verilen kararlar:** saglam · riskli · saglam

> Son çalışan commit’e dönmeyi, eksik özellikleri açıkça söylemeyi ve durumu hocaya bildirmeyi seçtin. "Eksikleri açıkça söylemek" stratejisinin, hocanın ve jürinin gözündeki "tamamlanmış ürün" algısını nasıl etkileyeceğini düşündün mü? Sence bir yazılım projesinde dürüstlük ile beklenti yönetimi her zaman aynı anlama mı gelir?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E06 — donem-projesi · 3-4 · bilmiyorum · ogrenme · kotu (1/3)

**Verilen kararlar:** riskli · saglam · riskli

> Gece boyu hata ayıklayıp sabahında tüm özellikleri yarım bırakarak demoya girme kararını uyguladın. 
> 
> Tüm özellikleri yarım bırakmanın, bu projenin temel öğrenme hedefleriyle nasıl bir bağı var? 
> 
> Kodun çalışır bir parçasını sunmak yerine hepsini yarıda bırakmak, teknik önceliklendirme becerin hakkında ne söylüyor olabilir?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E07 — donem-projesi · 3-4 · backend · proje · iyi (2/3)

**Verilen kararlar:** saglam · saglam · riskli

> Son çalışan commit'e dönüp eksikleri sonradan ekleme kararını seçtin, değil mi? "Her şeyi yarım bırakıp demoda hızlı geçerim" stratejisiyle bu yaklaşım birleştiğinde, hocanın gözündeki teknik tutarlılık ile eksik özelliklerin algısı nasıl bir denge oluşturur? Ekip arkadaşının sessizliği sürerken bu riski üstlenmek projeye ne kazandırır veya neyi kaybettirir?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E08 — staj-task · 3-4 · backend · staj · iyi (3/3)

**Verilen kararlar:** saglam · saglam · saglam

> Takım kanalına yazıp ardından mentorun vekiline doğrudan gitmeyi ve küçük bir test yazıp PR açmayı seçtin. Bu süreçte, ekibin iletişim dinamikleri ve kod kalitesi hakkında nasıl bir varsayımda bulundun? Stajyer değerlendirmelerinde bu adımların teknik yeterliliğin yanı sıra hangi sinyalleri verdiğini hiç düşündün mü?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E09 — staj-task · 1-2 · frontend · ogrenme · kotu (0/3)

**Verilen kararlar:** riskli · riskli · riskli

> "Hemen düzelt, kimse fark etmez" diyerek canlıda doğrudan yedekle deneme yapmayı ve "test yazmak stajyer işi değil" düşüncesiyle PR açmayı seçtin. 
> 
> Küçük bir değişikliğin canlı ortamda beklenmeyen bir etki yaratma olasılığı hakkında ne düşünüyorsun? Bir stajyerin sorumluluk alanı sence neleri kapsar? Bu süreç, kod kalitesini öğrenme hedefinle nasıl bağdaşır?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E10 — staj-task · 3-4 · bilmiyorum · proje · kotu (0/3)

**Verilen kararlar:** orta · orta · orta

> İlk staj görevinde hatayı kendi kopyanda çoğaltıp kanıtlamayı, task'ı bekletip yazılı not düşmeyi ve "test eklenmeli" notuyla PR açmayı seçtin. 
> 
> Tüm bu adımlardan sonra projenin ulaştığı durum sence mevcut zaman kısıtlarıyla nasıl bir çelişki barındırıyor olabilir? Bekleyen bir task ve eksik testlerle açılan PR, takımın teslimat takvimini nasıl etkiler?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E11 — staj-task · 1-2 · backend · staj · iyi (2/3)

**Verilen kararlar:** saglam · saglam · orta

> Takım kanalına yazıp beklemeyi, ardından yedek mentora sormayı ve PR'a "test eklenmeli" notu düşerek açmayı seçtin. 
> 
> Burada, "testlerin eksik olması PR'ın birleştirilmesini engeller mi?" varsayımıyla hareket ettin sanırım. Ekip, testleri yazmadan kodu incelemek istemezse, bu not onların inceleme sürecini nasıl etkiler? Bir mülakatta bu kararı nasıl savunurdun?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E12 — staj-task · 3-4 · frontend · proje · iyi (2/3)

**Verilen kararlar:** saglam · orta · saglam

> Takım kanalına yazıp beklemeyi, task'ı bekletip başka işe geçmeyi ve test yazıp PR açmayı seçtin. 
> 
> Tüm bu adımları atarken, projenin teslim tarihini ve ekibin anlık iş yükünü nasıl hesaba kattın? İletişim kurduğun an ile kod yazdığın an arasındaki sürede, projenin ilerleyişini hangi dinamikler etkiliyor olabilir?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E13 — staj-task · 1-2 · bilmiyorum · staj · kotu (1/3)

**Verilen kararlar:** riskli · saglam · orta

> İlk stajında küçük bir değişikliği hemen yapıp kimsenin fark etmeyeceğini ummayı, vekâleten mentoruna sormayı ve "test eklenmeli" notuyla PR açmayı seçtin. 
> 
> Hemen düzeltmenin kimsenin fark etmeyeceği varsayımı sence gerçekçi mi? Stajyer gözüyle ekip içi şeffaflık mülakatlarda nasıl değerlendirilir?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E14 — staj-task · 1-2 · frontend · ogrenme · iyi (2/3)

**Verilen kararlar:** saglam · saglam · riskli

> İlk staj görevinde durum kanalına yazmayı, mentor yerine bakan kişiye sormayı ve test yazmadan PR açmayı seçtin. 
> 
> "Test yazmak stajyer işi değil" varsayımıyla hareket ederken, bir frontend geliştiricinin yazdığı kodun kalitesini ekip arkadaşlarına nasıl kanıtlayacağını hiç düşündün mü? PR sürecinde test eksikliği sence kodu inceleyen kıdemlilerin dikkatini nasıl etkiler?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E15 — vize-haftasi · 3-4 · bilmiyorum · ogrenme · iyi (3/3)

**Verilen kararlar:** saglam · saglam · saglam

> Arkadaşına doğrudan sorup en ağır vizeye odaklandın ve katkını işaretleyerek teslim ettin. Bu süreç, bireysel öğrenmen ile ortak sorumluluk arasında nasıl bir denge kurdu? Sence bu yaklaşım, kod tabanının bütününe hakimiyetini nasıl etkiledi?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E16 — vize-haftasi · 1-2 · backend · staj · kotu (0/3)

**Verilen kararlar:** riskli · riskli · riskli

> Vizelerle çakışan bu görevde "olduğu gibi, hiçbir not düşmeden teslim etmeyi" seçtin ve sonuç kötü oldu. 
> 
> Burada ekibe durumu hiç bildirmemenin, bir stajyerin mülakatlarında değerlendirilen şeffaflık ve iletişim becerilerini nasıl etkileyeceğini düşünüyorsun? Kod kalitesinden ziyade, bu belirsizlik yönetimi bir yazılım ekibinde sence nasıl bir iz bırakır?

Mekanik: hepsi geçti

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E17 — vize-haftasi · 1-2 · frontend · proje · iyi (2/3)

**Verilen kararlar:** saglam · orta · saglam

> **HATA:** vekil fallback dondu (model cevap vermedi)

Mekanik: **KALDI** — S2a (0 soru) · S2b (soru işaretiyle bitmiyor)

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E18 — vize-haftasi · 3-4 · backend · ogrenme · kotu (0/3)

**Verilen kararlar:** orta · riskli · orta

> **HATA:** vekil fallback dondu (model cevap vermedi)

Mekanik: **KALDI** — S2a (0 soru) · S2b (soru işaretiyle bitmiyor)

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E19 — vize-haftasi · 3-4 · frontend · staj · iyi (2/3)

**Verilen kararlar:** saglam · saglam · riskli

> **HATA:** vekil fallback dondu (model cevap vermedi)

Mekanik: **KALDI** — S2a (0 soru) · S2b (soru işaretiyle bitmiyor)

**Etiket:** `____`  (OK / A / B / C / D / E — bkz. spec §6.3)

### E20 — vize-haftasi · 1-2 · bilmiyorum · proje · kotu (0/3)

**Verilen kararlar:** riskli · orta · riskli

> **HATA:** vekil fallback dondu (model cevap vermedi)

Mekanik: **KALDI** — S2a (0 soru) · S2b (soru işaretiyle bitmiyor)

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
| **Toplam** | 20 | %100 |

**Başarı eşiği:** `spec.md` §1 — OK oranı en az %80 olmalı.
