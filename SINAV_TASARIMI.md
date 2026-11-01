# SINAV_TASARIMI.md — "Sizinle uyumlanan sınav"

**Soru:** Primer kullanıcıyla uyumlanan bir sistemdi. Peki *sizinle* uyumlanan, ezberi değil kavramın gerekçesini ölçen 1 sayfalık klasik vize sorusu nasıl olurdu?

## Tasarım ilkesi

Primer'ın kuralı şuydu: **doğru cevabı verme, muhakemeyi sorgulat.** Sınavın da aynı kurala uyması gerekiyor — yani "diferansiyel test nedir?" diye sormamalı. O soru tanımı ezberleyeni ödüllendirir; oysa ölçmek istediğimiz şey, öğrencinin kavramı *tanımadığı bir durumda* kullanıp kullanamadığı.

Bu yüzden tek bir somut arıza anlatılıyor ve bütün sorular onun içinden soruluyor. Sınav "sizinle uyumlanıyor", çünkü cevaplar tek doğruya değil **savunulabilir gerekçeye** puan veriyor; farklı kararlar tam puan alabiliyor, gerekçesiz karar alamıyor.

---

## Senaryo (sınav kâğıdındaki metin)

> Bir ekip, küçük bir tabular modeli ONNX'e aktarıp mobil uygulamaya gömdü. Python referans betiği ile uygulama, beş referans girdide aynı sonucu veriyordu. Bir performans iyileştirmesinden sonra iki taraf **beşinci ondalık basamakta** ayrışmaya başladı. Eski skorlama fonksiyonunun yazılı bir şartnamesi yok; yalnız iki yıllık kod var. Ürün ekibi bugün tüm kullanıcılara açmak istiyor; elinizde iki saat var.

**S1 (6 p).** Bu bir hata mı? Cevaplamak için hangi *tek* bilgiye ihtiyacınız var ve neden?

**S2 (6 p).** Gerçek bir bozulmayı yakalayacak ama bu ayrışmayı yakalamayacak bir test tasarlayın. Testin iki tarafı nedir, karar ölçütü nedir?

**S3 (6 p).** Şartname yok, yalnız eski kod var. İlk hangi testi yazarsınız ve bu test neyi *doğrulamaz*?

**S4 (6 p).** İki saatte tüm kullanıcılara açmak mı, yoksa açmamak mı? Kararınızı, açmamanın maliyetini de sayarak savunun.

**S5 (6 p).** Ekip diyor ki: "Yeniden eğittik, doğruluk 0.81'den 0.86'ya çıktı, yayınlayalım." Bu cümle tek başına yayın kararı için yeterli mi?

---

## Beklenen kavramlar ve çeldiriciler

| # | Ölçtüğü | Beklenen öz | Çeldirici (yaygın ama eksik cevap) |
|---|---|---|---|
| S1 | **Hata toleransı** | Önce *tolerans* bilinmeli: 1e-4 toleransı olan bir sözleşmede 5. ondalık fark **hata değildir**. "Fark var" ile "sözleşme ihlali var" ayrı şeyler | "Evet, hata — iki sistem aynı sonucu vermeli." Kayan nokta aritmetiğinin iki çalışma zamanında birebir aynı olmasını beklemek |
| S2 | **Diferansiyel test + kahin** | İki *bağımsız* uygulama (test kahini vs hedef), aynı referans girdiler, karar ölçütü mutlak fark < tolerans. Tolerans, ayrışmanın üstünde ama anlamlı bozulmanın altında seçilir | "Birim test yazarım." Birim test tek uygulamayı kendi beklentisine göre ölçer; iki uygulamanın *ayrışmasını* göremez |
| S3 | **Karakterizasyon testi** · **doğrulama ≠ geçerleme** | Mevcut davranışı olduğu gibi dondurmak. Bu test kodun **doğru** olduğunu değil, **değişmediğini** gösterir: geçerleme (validation) değil, doğrulama (verification) aracıdır. Varsa hatayı da dondurur | "Önce doğru çıktıları yazıp test ederim." Doğru çıktı bilinmiyor; şartname yok. Bunu yapmak, olmayan bir spec'i uydurmaktır |
| S4 | **Gölge/kanarya dağıtım · ödünleşim** | Savunulabilir her iki karar da tam puan. Aranan: gölge veya kanaryanın *neyi satın aldığını* söylemek (gerçek veride ölçüm, sınırlı maruziyet) ve açmamanın maliyetini de saymak (ürün gecikmesi, iki saatin boşa gitmesi) | "Kanarya yaparım" deyip gerekçe vermemek. Slayttaki adı tekrarlamak, kararı savunmak değildir. Diğer uç: "Toleransı geçiyorsa sorun yok, aç" |
| S5 | **Sınırı tanımak (asıl tuzak)** | **Hayır, yeterli değil.** Eksikler: kabul eşiği eğitimden *önce* yazılmış mıydı, iki sayı aynı veri ve aynı bölme yöntemiyle mi ölçüldü, çapraz doğrulama *gruplanmış* mıydı (aynı oturum/kişi aynı katta mı), 0.86 hangi taban çizgisiyle karşılaştırılıyor | "Evet, doğruluk arttıysa daha iyidir." Metriğin kendisini sorgulamadan kabul etmek. Gruplama ihlali, aynı kişinin kardeş satırları farklı katlara düştüğünde doğruluğu sahte biçimde yükseltir |

## Puanlama kuralı

Her soruda puanın **üçte biri karar, üçte ikisi gerekçe.** Doğru kavramı adıyla yazıp gerekçesiz bırakan cevap, yanlış kavramı tutarlı gerekçeyle savunan cevaptan daha az alır — çünkü ölçülen şey terim bilgisi değil, mühendislik muhakemesi.

S5'te "yeterli değil" demeden eksikleri sayan cevap tam puan alır; "yeterli" diyen cevap, gerekçesi ne olursa olsun yarıdan fazla alamaz. Bir ölçümün neyi ölçmediğini görememek, bu haftanın tek asıl hatasıdır.
