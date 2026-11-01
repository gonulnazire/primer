# Veri Sözlüğü — `data/oturumlar.csv`

**İlgili belge:** [`spec.md`](../spec.md) §10 · **Tarih:** 2026-11-01

Bu dosya `oturumlar.csv`'nin her sütununun ne olduğunu, biriminin ne olduğunu ve nasıl ölçüldüğünü tanımlar. Veri toplanmadan önce yazıldı.

## Satır birimi

**Bir satır = bir karar noktası**, bir oturum değil. Bir oturum üç karar noktası içerdiği için üç satır üretir.

Bu seçim bilinçli: oturum başına tek satır tutsaydık 15 gerçek oturum yalnızca 15 örnek verirdi ve lojistik regresyon altı özelliği öğrenemezdi. Karar noktası birimiyle aynı veri **45 örnek** veriyor. Bedeli: aynı oturumdan gelen satırlar bağımsız değil (aynı kişi, aynı profil) — bu, model kartında "bağımsızlık varsayımı tam karşılanmıyor" sınırı olarak yazılacak.

## Sütunlar

| # | Sütun | Tip / aralık | Anlamı ve nasıl ölçüldüğü |
|---|---|---|---|
| 1 | `oturum_id` | 8 haneli onaltılık | Rastgele üretilir. Kişiye geri bağlanamaz (KVKK, aşağıda) |
| 2 | `kisi_kodu` | `k1`, `k2`, `k3`, … | Anonim katılımcı ayrıştırıcısı. Kim olduğunu hiçbir yerde tutmuyoruz; yalnızca "kaç farklı kişi" sorusunu cevaplar |
| 3 | `oturum_sira` | tamsayı ≥ 1 | O kişinin kaçıncı oturumu. Öğrenme etkisini (ikinci oynayışta daha hızlı karar) sonradan inceleyebilmek için |
| 4 | `senaryo` | `donem-projesi` \| `staj-task` \| `vize-haftasi` | `spec.md` §5'teki senaryo kimliği |
| 5 | **`sahne_no`** | 1–3 | Karar noktasının sırası. **Özellik 1** |
| 6 | `sinif` | `1-2` \| `3-4` | Profil cevabı (`spec.md` §4) |
| 7 | **`sinif_kodu`** | 0 \| 1 | `1-2` → 0, `3-4` → 1. **Özellik 2** |
| 8 | `rol` | `frontend` \| `backend` \| `bilmiyorum` | Profil cevabı. **Özellik değil** — gerekçe `spec.md` §10.3 |
| 9 | `hedef` | `staj` \| `proje` \| `ogrenme` | Profil cevabı. **Özellik değil** |
| 10 | **`onceki_karar_suresi_sn`** | saniye, ≥ 0 | Bir önceki karar noktasının süresi. `sahne_no = 1` ise **0**. **Özellik 3** |
| 11 | **`onceki_okuma_orani`** | 0–1 | Bir önceki sahnenin okunma oranı. `sahne_no = 1` ise **0**. **Özellik 4** |
| 12 | **`onceki_refleks_sayisi`** | 0–2 | Bu satıra kadar refleks sayılan karar adedi. **Özellik 5** |
| 13 | **`oturum_gecen_sure_sn`** | saniye, ≥ 0 | Oturumun ilk ekranından bu karar noktasına girişe kadar geçen süre. **Özellik 6** |
| 14 | `karar_suresi_sn` | saniye, ≥ 0 | Karar noktası göründüğü andan seçim onaylanana kadar geçen süre. Etiketin kendisi buna bakmıyor (bkz. aşağıdaki etiket kuralı) ama ham süre olmadan etiket denetlenemez |
| 15 | `metin_gorunur_sure_sn` | saniye, ≥ 0 | Metin alanının ekranda **görünür** olduğu süre; sekme arka plana alınınca sayaç durur. `okuma_orani`'nın **payı** |
| 16 | `yeni_kelime_sayisi` | tamsayı > 0 | O karar noktasında **ilk kez** gösterilen kelime sayısı. `okuma_orani`'nın **paydasını** belirler |
| 17 | `okuma_orani` | 0–1 | 15 ve 16'dan türetilir, 1'de kırpılır. **Etiket girdisi** |
| 18 | `vazgecilen_dokunma` | tamsayı ≥ 0 | Bir seçeneğe basılıp tıklama tamamlanmadan vazgeçilen dokunma sayısı (`pointerdown` var, `click` yok). **Özellik değil** — gerekçe aşağıda |
| 19 | `secenek_etiketi` | `saglam` \| `orta` \| `riskli` | Seçilen seçeneğin `spec.md` §5'teki etiketi. **Özellik değil**, yalnız analiz için. Kullanıcıya hiçbir zaman gösterilmez |
| 20 | **`refleks`** | 0 \| 1 | **ETİKET.** Kuralı aşağıda |
| 21 | `golge_tahmin` | boş veya 0–1 | Gölge dağıtımda modelin o an ürettiği olasılık. Uygulama bu moddayken tahmini yazar ama **eylem yapmaz**; `refleks` ile karşılaştırılarak gerçek veride doğrulama yapılır (`RELEASE.md`) |
| 22 | `kaynak` | `gercek` \| `sentetik` | Zorunlu. Gerçek oturum sayısı bu sütundan sayılır |
| 23 | `surum` | metin | Veriyi üreten sürüm: veri toplama aşamasında `v0`, model devredeyken `web/site.json`'daki model pin'inin ilk 7 hanesi |

**Denetim zinciri:** 15 ÷ (16 / 200 × 60) → 17 → eşikle karşılaştır → 20. Üç sütun da dosyada olduğu için etiket, veriye bakan herkes tarafından yeniden hesaplanabilir. `train.py` bunu her koşumda yapıp CSV'deki değerle karşılaştırır; tutmazsa durur.

**Özellik sırası sözleşmedir:** 5, 7, 10, 11, 12, 13 → `model/config.json`'daki `ozellikler` dizisiyle **aynı sırada** olmak zorunda:

```
sahne_no · sinif_kodu · onceki_karar_suresi_sn · onceki_okuma_orani ·
onceki_refleks_sayisi · oturum_gecen_sure_sn
```

## Neden "seçim değiştirme" bir özellik değil

Spec'in ilk v2 taslağında 5. özellik `onceki_secim_degistirme` — *"onaydan önce kaç kez başka seçeneğe geçildiği"* — olacaktı. Uygulamayı yazarken bu ölçünün **ölçülemez** olduğu görüldü: v1 akışında seçenek tek dokunuşla onaylanıyor (`spec.md` AC3: "bir seçenek seçilir, sıradaki karar noktası gelir"). "Seçimi değiştirmek" diye bir olay yok, çünkü ayrı bir onay adımı yok.

İki yol vardı:

| Yol | Bedeli |
|---|---|
| Karar ekranına onay adımı eklemek | AC3 değişir, v1 ile akış paritesi ve regresyon hikâyesi bozulur |
| Ölçülebilen tereddüt sinyaline geçmek | Vazgeçilen dokunma seyrek bir olay; 45 satırda neredeyse hep 0 olur |

İkisi de kabul edilmedi. Yerine **`oturum_gecen_sure_sn`** konuldu: her satırda farklı, yoğun ve "yorgunluk/acele" sinyalini taşıyan bir ölçü — oturumun sonuna doğru hızlanan oyuncu ile baştan beri aceleci oyuncu arasındaki farkı taşıyor.

`vazgecilen_dokunma` yine de **kaydediliyor** (16. sütun), çünkü ölçmemek ile modele koymamak farklı şeyler: veri toplanırsa sonradan incelenebilir, toplanmazsa o sinyal sonsuza kadar kayıp. Ama seyrek olduğu bilinen bir sütunu özellik yapmak, modeli gürültüye oturtmak olurdu.

`sahne_no` ile `oturum_gecen_sure_sn` arasında doğal bir korelasyon var (sonraki sahne = daha çok geçen süre). Bu kabul edildi: ikisi aynı şey değil, çünkü aynı sahneye hızlı gelen ve yavaş gelen oyuncu farklı değerler üretiyor — ki modelin arayacağı ayrım tam olarak bu. `StandardScaler` + lojistik regresyon bu düzeyde eşdoğrusallığı taşır.

## Neden türetilmiş `onceki_*` sütunları CSV'de duruyor

10–13 numaralı sütunlar 14–16'dan hesaplanabilir; yine de dosyada tutuluyorlar. Gerekçe: **eğitim-servis sapmasını (train/serve skew) engellemek.** Uygulama çıkarım anında bu altı sayıyı zaten hesaplıyor; CSV'ye yazılan şey tam olarak modelin gördüğü girdi oluyor. Eğitimde ayrı, çıkarımda ayrı bir hesap yazarsak iki formülün sessizce ayrışması mümkün — bu, üretimdeki ML sistemlerinin klasik hatası.

Bedeli: aynı bilgi iki yerde. Buna karşı `train.py` her koşumda türetilmiş sütunları ham sütunlardan **yeniden hesaplayıp karşılaştırır**; tutmazsa hata verip durur. Yani tekrar, denetlenen bir tekrar.

## `okuma_orani` tanımı

```
okuma_orani = min(1, metin_gorunur_sure_sn / tahmini_okuma_suresi_sn)
tahmini_okuma_suresi_sn = yeni_kelime_sayisi / 200 * 60
```

`metin_gorunur_sure_sn`: karar noktasının metin alanının ekranda görünür olduğu toplam süre. IntersectionObserver ile ölçülür ve sekme arka plana alınırsa (`document.visibilityState`) sayaç durur — telefonda bildirime bakıp dönen bir oyuncunun o süresi okuma sayılmamalı.

`yeni_kelime_sayisi`: **o karar noktasında ilk kez gösterilen** kelime sayısı. 1. karar noktasında kriz kurulumu + soru + üç seçenek (~86 kelime); 2. ve 3.'de yalnızca soru + üç seçenek (~36 kelime), çünkü kriz kurulumu zaten okunmuştu. Toplam metni her sahnede yeniden saymak, sonraki sahneleri haksız biçimde "okumadı" tarafına iterdi.

200 kelime/dakika Türkçe ortalama okuma hızı varsayımıdır ve model kartında varsayım olarak yazılı olacak.

**Neden kaydırma oranı değil:** ilk tasarımda `okuma_orani`, metnin kaydırılarak görülen kısmının oranı olacaktı. 390×844 px ekranda kriz metinleri kaydırma gerektirmeden sığıyor — yani kaydırma sinyali herkeste 1.0 çıkar ve hiçbir şey ayırt etmez. Ekranda kalma süresi, telefonda gerçekten ayırt edici olan tek okuma sinyali.

## Etiket kuralı

```
refleks = 1   eğer   okuma_orani < 0.4
refleks = 0   aksi halde
```

Gerekçe ve bu kuralın neden iki koşulluyken tek koşula indirgendiği: `spec.md` §10.4. Özeti: iki koşullu hal (`karar_suresi < 6 AND okuma_orani < 0.5`) bu ekran boyutunda tek koşula çöküyordu ve sabit 6 saniye, 1. sahnenin 2,4 kat fazla okuma yükünü görmezden geliyordu.

`karar_suresi_sn` yine de 14. sütunda **kaydediliyor**: etiketin kendisi artık orana baksa da, ham süre olmadan etiket sonradan denetlenemez. `train.py` her koşumda `okuma_orani`'nı ham sürelerden yeniden hesaplayıp etiketi yeniden türetir ve CSV'deki `refleks` sütunuyla karşılaştırır.

Eşik veri görüldükten sonra değiştirilmeyecek. Değiştirilirse bu, etiketi modele uydurmak olur.

## KVKK ve gizlilik

Toplanmayan alanlar: **ad, soyad, e-posta, telefon, öğrenci numarası, cihaz kimliği, IP, konum, tarayıcı parmak izi, zaman damgası.**

- `oturum_id` rastgele üretilir, hiçbir kişiye bağlanmaz.
- `kisi_kodu` elle girilen `k1`/`k2`/`k3`'tür; hangi kodun kime ait olduğu hiçbir yerde yazılı değildir ve veriyi toplayanın aklı dışında kaydı yoktur.
- Zaman damgası bilinçli olarak yok: `oturum_sira` sıralama için yeterli, zaman damgası ise başka kayıtlarla eşleştirilerek yeniden kimliklendirmeye açık kapı bırakır.
- Veri tarayıcıda üretilir ve kullanıcının kendi indirdiği CSV dosyasıyla taşınır; sunucuya hiçbir şey gönderilmez.

v1'deki sohbet e-postasından farkı: orada e-posta bir kimlik değil etiketti ama **saklanıyordu** (`spec.md` §2). Burada hiçbir kişisel alan hiç toplanmıyor.
