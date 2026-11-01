# `data/ham/` — uygulamadan indirilen ham oturum dosyaları

Veri toplama modunda (`web/index.html` → "CSV indir") indirilen dosyalar **olduğu gibi** buraya konur. Dosya adı önemli değil; `veri_derle.py` bu dizindeki tüm `*.csv` dosyalarını okur.

```bash
python data/veri_derle.py --sentetik 60
```

Bu komut: ham dosyaları okur → şemayı ve etiket tutarlılığını doğrular → sentetik takviyeyi ekler → `data/oturumlar.csv` yazar.

## Neden ham dosyalar ayrı duruyor

`oturumlar.csv` **türetilmiş** bir dosya: her derlemede yeniden yazılıyor. Ham indirmeleri ayrı tutmak, türetilmiş dosya bozulduğunda veya etiket kuralı denetlenmek istendiğinde geri dönülecek bir kaynak bırakıyor. Toplanan gerçek veri yeniden üretilemez; sentetik veri her zaman yeniden üretilebilir (tohum 42).

## Toplama notu

Her katılımcı için `kisi_kodu` alanına `k1`, `k2`, `k3` gibi anonim bir kod girilir. **Hangi kodun kime ait olduğu hiçbir yere yazılmaz.** Ad, e-posta, numara, konum veya zaman damgası toplanmaz; `veri_derle.py` bu adlarda bir sütun görürse derlemeyi durdurur.

Hedef: **en az 15 gerçek oturum** (ör. 3 kişiye 5'er oturum) = 45 karar satırı.
