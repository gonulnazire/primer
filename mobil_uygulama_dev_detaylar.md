# Mobil Uygulama Geliştirme Dersi - Kişiselleştirilmiş Öğrenme Uygulaması Ödevi

Bu rehber, ders transkriptleri, toplantı notları ve ders sunumu (`SE Primer — Ödev.pptx`) analiz edilerek; zamanı kısıtlı olan ve önce temel işlevleri (MVP) hayata geçirmek isteyen bir öğrenci için en baştan detaylı bir şekilde hazırlanmıştır.

---

## 1. Ödevin Vizyonu ve Temel Amacı

* **Konsept:** Neil Stephenson’ın *"The Diamond Age"* romanındaki **"The Primer"** (Kişiye/çocuğa uyum sağlayan, düşündüren akıllı kitap) konseptinden ilham alınmıştır. Amacımız, düz bir anlatım veya sınav yerine; yazılım mühendisliği öğrencisinin kariyer gelişimine veya hedeflediği role uyum sağlayan interaktif bir **mobil öğrenme simülasyonu** geliştirmektir.
* **Yaklaşım:** Kod yazmaktan çok **ürün kararı, spesifikasyon (spec) ve doğrulama** becerilerini öne çıkarmak. Yapay zekâ size doğrudan cevabı vermez; Sokratik yöntemle sizi sorgulamaya ve araştırmaya yönlendirir.
* **Strateji (MVP Önceliği):** Zamanınız çok az olduğu için önce temel işlevleri (Giriş, Kriz Senaryosu, Karar Verme, Sonuç ve Sokratik Geri Bildirim) ayağa kaldırın. Detayları vaktiniz kalırsa ekleyin.

---

## 2. Kapsam ve Gereksinimler

### Yapılacaklar (Kapsam İçi)
1. **Telefonda Çalışan Uygulama:** Google AI Studio / Stitch kullanılarak tasarlanmış ve telefonda görüntülenebilen en az **3 ekranlı** interaktif yapı.
2. **Kişiselleştirme:** Uygulamanın açılışında kullanıcıdan (seviye, rol, hedef vb.) bilgiler alınarak akışın kişiye uyarlanması.
3. **Senaryo Tabanlı Karar Mekanizmaları:** Örneğin sağlık sektörü veya nöbetçi mühendislik krizleri üzerinden en az 2-3 karar noktası ve farklı sonlar (İyi / Kötü son).
4. **Spesifikasyon Dosyası (`spec.md`):** Problem tanımı, kapsam dışı bırakılanlar ve en az 5 kabul örneği.
5. **Test ve Doğrulama:** Cypress kullanılarak uçtan uca (E2E) testlerin koşulması ve 60 saniyelik demo video elde edilmesi. Gerçek bir arkadaşa test ettirip geri bildirim raporuna eklenmesi.

### Kapsam Dışı (Vakit Kazanmak İçin İlk Aşamada Yapılmayacaklar)
* Karmaşık kullanıcı hesap yönetimi, veritabanı entegrasyonu ve üyelik sistemleri.
* Native (yerel) mobil uygulama mağazası süreçleri (Web tabanlı mobil görünüm veya AI Studio önizlemesi yeterlidir).
* İkinci derece detay modüller ve süslü animasyonlar.

---

## 3. Ödev Adımları ve Teslim Kriterleri (Adım Adım Yol Haritası)

### Adım 1: Spesifikasyon Yazımı (`spec.md`)
* **İçerik:** Problem tanımı, kapsam içi/dışı unsurlar, en az 5 kabul örneği (Acceptance Criteria) ve akış şeması.
* **İpucu:** *"Bir arkadaşına oynat. İlk takıldığı yer, spec’indeki görünmez varsayımdır. Onu kabul örneği yap."*

### Adım 2: Arayüz Tasarımı (Stitch / DESIGN.md)
* Google Stitch aracı kullanılarak 3 ana ekran tasarlanır:
  1. *Giriş / Profil Seçimi Ekranı*
  2. *Kriz Senaryosu ve Karar Ekranı*
  3. *Sonuç ve Sokratik Geri Bildirim Ekranı*
* Tasarım notları repoya `DESIGN.md` olarak eklenir.

### Adım 3: Çalışan Uygulama (AI Studio)
* Ekranlar ve `spec.md` detayları AI Studio'ya verilerek uygulamanın çalışır hâle getirilmesi sağlanır.
* QR kod ile telefonda test edilir.

### Adım 4: Değerlendirme Raporu (Evaluator & Tutor Eval)
* 20 farklı öğrenci cevabı / senaryo simülasyonu simüle edilerek yapay zekânın cevabı verip vermediği (Sokratik kurala uyup uymadığı) etiketlenir ve hata oranları rapora eklenir.

### Adım 5: Test ve Demo (Cypress)
* Cypress ile tüm yollar E2E test edilir.
* Süreçten 60 saniyelik bir demo video çekilerek rapora eklenir.

---

## 4. Puanlama Kriterleri (100 Puan Üzerinden)

* **spec.md (20 Puan):** Problem, kapsam dışı unsurlar, 5 kabul örneği ve akış şeması.
* **Tasarım (15 Puan):** Stitch ekranları ve `DESIGN.md` uyumu.
* **Çalışan Uygulama (20 Puan):** AI Studio linki; telefonda baştan sona oynanabilir olması.
* **Tutor Eval (25 Puan):** 20 cevap analizi, hata türleri, oranlar ve örnek sayısı.
* **Cypress Demo (10 Puan):** Tüm yolların E2E test edilmesi ve 60 sn demo video.
* **Ürün Kararı / README (10 Puan):** Yapmadığınız 3 özellik ve her biri için tek cümlelik gerekçe.