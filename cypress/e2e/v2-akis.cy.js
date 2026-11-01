/// <reference types="cypress" />

/**
 * Primer v2 — akış ve uyum katmanı testleri
 *
 * spec.md §7 (AC1–AC5, AC9, AC10) + AC13 · §10.2 (cevap-nötr müdahale)
 *
 * Hedef: Cypress.expose('v2Url') — repo içindeki web/ sayfası.
 *
 * YARDIMCI FONKSİYONLAR BİLİNÇLİ OLARAK TEKRARLANIYOR.
 * cypress/e2e/primer.cy.js ve sohbet.cy.js v2 çalışması boyunca tek karakter
 * değişmeyecek (spec.md §8): regresyon kanıtının değeri dosyaların AYNI
 * kalmasından geliyor. Ortak bir yardımcı dosyaya çekmek, o dosyalara dokunmak
 * demekti. ~30 satır tekrarın bedeli, regresyon kanıtını zayıflatmaktan azdır.
 *
 * SEÇENEKLER KONUMA GÖRE SEÇİLMEZ (AC10) — metinleriyle bulunurlar.
 */

const V2 = Cypress.expose('v2Url');

// spec.md §5 — her karar noktasındaki seçeneklerin ayırt edici metin parçaları
const SAGLAM = {
  'donem-projesi': ['Son çalışan commit', 'net bir süre veren', 'Çalışan 3 özelliği'],
  'staj-task': ['takım kanalına yazılı', 'yerine bakan kişiyi', 'Küçük bir test yaz'],
  'vize-haftasi': ['yargılamadan sor', 'En ağır vizeye', 'Kendi katkını açıkça'],
};
const RISKLI = {
  'donem-projesi': ['Gece boyu hatayı', 'Hiçbir şey söyleme', '8 özelliğin hepsini'],
  'staj-task': ['Hemen düzelt', 'Canlıda dene', 'stajyer işi değil'],
  'vize-haftasi': ['Hiçbir şey deme', 'Ödevi mükemmel yap', 'hiçbir not düşmeden'],
};

const SENARYOLAR = ['donem-projesi', 'staj-task', 'vize-haftasi'];

/** Gölge modu: model çalışır ama müdahale etmez (web/site.json varsayılanı). */
const GOLGE = {
  model_url: null,
  yerel_yedek: '../model/model.onnx',
  model_pin: null,
  karar_esigi: 0.6,
  golge: true,
  devreye_alma_orani: 0.0,
  surum: 'test-golge',
};

/** Tam devreye alma: eşiği geçen her oturumda duraklama açılır. */
const TAM = { ...GOLGE, golge: false, devreye_alma_orani: 1.0, surum: 'test-tam' };

function yapilandirmayiSabitle(gov) {
  // Devreye alma kararı site.json'da tutulduğu için testler modu buradan
  // yönetir — uygulamada test için açılmış bir arka kapı YOK.
  cy.intercept('GET', '**/site.json', { statusCode: 200, body: gov }).as('site');
}

function profilDoldur({ sinif = '3-4', rol = 'Backend', hedef = 'Staj bulmak' } = {}) {
  cy.get('[data-testid="profil-sinif"]').contains('button', sinif).click();
  cy.get('[data-testid="profil-rol"]').contains('button', rol).click();
  cy.get('[data-testid="profil-hedef"]').contains('button', hedef).click();
  cy.get('[data-testid="profil-devam"]').click();
}

function senaryoSec(id) {
  cy.get(`[data-testid="senaryo-${id}"]`).click();
}

/** Seçeneği metnine göre bulup tıklar — konumdan bağımsız. */
function secenegiTikla(metin) {
  cy.contains('[data-testid^="secenek-"]', metin).should('not.be.disabled').click();
}

function ucKararVer(senaryo, tablo) {
  tablo[senaryo].forEach(secenegiTikla);
}

describe('Primer v2 — akış', () => {
  beforeEach(() => {
    yapilandirmayiSabitle(GOLGE);
    cy.visit(V2);
    cy.clearLocalStorage();
  });

  it('AC1 — profil tamamlanmadan menüye geçilemez', () => {
    cy.get('[data-testid="profil-devam"]').should('be.disabled');

    cy.get('[data-testid="profil-sinif"]').contains('button', '3-4').click();
    cy.get('[data-testid="profil-devam"]').should('be.disabled');

    cy.get('[data-testid="profil-rol"]').contains('button', 'Backend').click();
    cy.get('[data-testid="profil-devam"]').should('be.disabled');

    cy.get('[data-testid="profil-hedef"]').contains('button', 'Staj bulmak').click();
    cy.get('[data-testid="profil-devam"]').should('not.be.disabled');
  });

  it('AC2 — kriz metni hedef role göre değişir', () => {
    profilDoldur({ rol: 'Backend' });
    senaryoSec('donem-projesi');
    cy.get('[data-testid="kriz-metni"]').should('contain', 'veritabanı');

    cy.visit(V2);
    profilDoldur({ rol: 'Frontend' });
    senaryoSec('donem-projesi');
    cy.get('[data-testid="kriz-metni"]')
      .should('contain', 'build')
      .and('not.contain', 'veritabanı');
  });

  it('AC4 — üç sağlam karar İYİ SON üretir', () => {
    profilDoldur();
    senaryoSec('donem-projesi');
    ucKararVer('donem-projesi', SAGLAM);

    cy.get('[data-testid="sonuc-bandi"]')
      .should('be.visible')
      .and('contain', 'İYİ SON')
      .and('contain', '3/3 sağlam karar');
  });

  it('AC5 — üç riskli karar KÖTÜ SON üretir', () => {
    profilDoldur();
    senaryoSec('vize-haftasi');
    ucKararVer('vize-haftasi', RISKLI);

    cy.get('[data-testid="sonuc-bandi"]')
      .should('be.visible')
      .and('contain', 'KÖTÜ SON')
      .and('contain', '0/3 sağlam karar');
  });

  it('AC9 — Türkçe büyük harf kuralı (lang="tr")', () => {
    cy.get('html').should('have.attr', 'lang', 'tr');

    profilDoldur();
    senaryoSec('staj-task');
    ucKararVer('staj-task', SAGLAM);

    // CSS text-transform: uppercase dile duyarlı; lang="en" altında "İ" yerine
    // "I" çıkar. Hesaplanmış metni tarayıcıdan okuyoruz.
    cy.contains('.etiket', 'Simülasyon özeti').then(($e) => {
      const gorunen = $e[0].textContent;
      expect(gorunen.toLocaleUpperCase('tr')).to.contain('SİMÜLASYON');
      expect($e).to.have.css('text-transform', 'uppercase');
    });
  });

  it('AC10 — sağlam seçenek dokuz karar noktasının hepsinde aynı konumda değil', () => {
    const konumlar = [];
    profilDoldur();

    cy.wrap(SENARYOLAR).each((senaryo) => {
      senaryoSec(senaryo);
      cy.wrap(SAGLAM[senaryo]).each((metin) => {
        cy.contains('[data-testid^="secenek-"]', metin)
          .invoke('attr', 'data-testid')
          .then((id) => konumlar.push(id));
        secenegiTikla(metin);
      });
      cy.get('[data-testid="bastan-basla"]').click();
    });

    cy.then(() => {
      expect(konumlar, '9 karar noktası örneklenmeli').to.have.length(9);
      const benzersiz = new Set(konumlar);
      expect(
        benzersiz.size,
        `sağlam seçenek hep aynı konumda: ${[...benzersiz].join(', ')}`
      ).to.be.greaterThan(1);
    });
  });

  it('AC7 — 390px genişlikte yatay kaydırma yok, dokunma hedefleri ≥44px', () => {
    // v1'de bu kabul örneği var (primer.cy.js); v2 sayfası aynı hedef cihazda
    // (390×844) oynanacağı için aynı kısıt burada da geçerli olmalı.
    profilDoldur();
    senaryoSec('donem-projesi');

    cy.document().then((belge) => {
      expect(
        belge.documentElement.scrollWidth,
        'yatay kaydırma oluşmamalı'
      ).to.be.at.most(belge.documentElement.clientWidth + 1);
    });

    cy.get('[data-testid^="secenek-"]').each(($s) => {
      expect($s[0].getBoundingClientRect().height, 'seçenek yüksekliği').to.be.at.least(44);
    });
  });

  it('veri toplama — her karar bir satır üretir ve sözleşmeye uyar', () => {
    cy.get('[data-testid="kisi-kodu"]').type('k1');
    profilDoldur();
    senaryoSec('donem-projesi');
    ucKararVer('donem-projesi', SAGLAM);

    cy.get('[data-testid="satir-sayisi"]').should('have.text', '3');
    cy.get('[data-testid="oturum-sayisi"]').should('have.text', '1');

    cy.window().then((pencere) => {
      const satirlar = JSON.parse(pencere.localStorage.getItem('primer_v2_satirlar'));
      expect(satirlar).to.have.length(3);

      satirlar.forEach((s, i) => {
        expect(s.sahne_no, 'sahne sırası').to.equal(i + 1);
        expect(s.kisi_kodu).to.equal('k1');
        expect(s.senaryo).to.equal('donem-projesi');
        expect(s.secenek_etiketi).to.equal('saglam');
        expect(s.kaynak).to.equal('gercek');
        expect(s.refleks).to.be.oneOf([0, 1]);
        expect(s.okuma_orani).to.be.within(0, 1);
        expect(s.oturum_id).to.match(/^[0-9a-f]{8}$/);
      });

      // KVKK (data/SOZLUK.md): kişisel alan HİÇ toplanmıyor
      const yasak = ['ad', 'isim', 'eposta', 'email', 'telefon', 'ip', 'konum',
        'cihaz', 'zaman', 'timestamp'];
      yasak.forEach((alan) => {
        expect(Object.keys(satirlar[0]), `yasak alan: ${alan}`).not.to.include(alan);
      });

      // Özellikler k'dan ÖNCE bilinenlerden türer: 1. sahnede geçmiş sıfır
      expect(satirlar[0].onceki_karar_suresi_sn).to.equal(0);
      expect(satirlar[0].onceki_okuma_orani).to.equal(0);
      expect(satirlar[0].onceki_refleks_sayisi).to.equal(0);
    });
  });
});

describe('Primer v2 — uyum katmanı (AC13)', () => {
  beforeEach(() => {
    cy.clearLocalStorage();
  });

  it('AC13a — hızlı (okumadan) oynayınca yansıma duraklaması açılır ve seçenekler pasifleşir', () => {
    yapilandirmayiSabitle(TAM);
    cy.visit(V2);

    // Yapılandırmanın gerçekten UYGULAMAYA ULAŞTIĞINI önce kanıtla. Aksi halde
    // stub sessizce kaçarsa uygulama gerçek site.json'u (gölge modu) okur ve
    // "duraklama yok" sonucu doğru görünür — yanlış sebepten.
    cy.wait('@site');
    cy.get('[data-testid="model-durumu"]', { timeout: 30000 }).should('have.text', 'hazır');
    cy.get('[data-testid="model-modu"]').should('contain', 'tam');

    profilDoldur();
    senaryoSec('donem-projesi');

    // 1. karar noktasında geçmiş yok -> duraklama beklenmiyor
    cy.get('[data-testid="yansima"]').should('not.be.visible');

    // Hemen tıkla: metin okunmadı -> refleks etiketi -> 2. sahnede duraklama
    secenegiTikla(SAGLAM['donem-projesi'][0]);

    cy.get('[data-testid="yansima"]').should('be.visible');
    cy.get('[data-testid="yansima"]').should('contain', 'neyi varsayıyorsun');

    // Duraklama süresince seçilemez
    cy.get('[data-testid="secenek-0"]').should('be.disabled');

    // Müdahale CEVAP-NÖTR olmalı (spec.md §10.2): duraklama metni hiçbir
    // seçeneğin metnini içermemeli, hiçbirini işaret etmemeli.
    cy.get('[data-testid="yansima"]').invoke('text').then((metin) => {
      [...SAGLAM['donem-projesi'], ...RISKLI['donem-projesi']].forEach((parca) => {
        expect(metin, 'duraklama bir seçeneği ima etmemeli').not.to.contain(parca);
      });
    });

    // 3 saniye sonra açılır
    cy.get('[data-testid="secenek-0"]', { timeout: 10000 }).should('not.be.disabled');
    cy.get('[data-cy="p"]').should('not.have.text', '—');
  });

  it('AC13b — metni okuyarak oynayınca duraklama HİÇ açılmaz', () => {
    // AC13'ün ikinci yönü. Yalnız "duraklama görünüyor" test edilirse her
    // zaman duraklatan bir uygulama da geçer; model hiç çalışmasa bile.
    yapilandirmayiSabitle(TAM);
    cy.visit(V2);
    cy.get('[data-testid="model-durumu"]', { timeout: 30000 }).should('have.text', 'hazır');

    profilDoldur();
    senaryoSec('donem-projesi');

    // 1. sahnenin okuma yükü ~16.5 sn; eşik 0.4 -> en az ~6.6 sn gerekiyor.
    // 10 sn bekleyince okuma oranı ~0.6 çıkar ve karar refleks sayılmaz.
    cy.wait(10000);
    secenegiTikla(SAGLAM['donem-projesi'][0]);

    cy.get('[data-testid="secenek-0"]').should('not.be.disabled');
    cy.get('[data-testid="yansima"]').should('not.be.visible');

    cy.window().then((pencere) => {
      const satirlar = JSON.parse(pencere.localStorage.getItem('primer_v2_satirlar'));
      expect(satirlar[0].refleks, 'okuyan oyuncu refleks sayılmamalı').to.equal(0);
      expect(satirlar[0].okuma_orani).to.be.greaterThan(0.4);
    });
  });

  it('gölge modunda model çalışır ama MÜDAHALE ETMEZ', () => {
    // RELEASE.md — gölge dağıtımın tanımı: tahmin üretilir ve kaydedilir,
    // kullanıcı deneyimi değişmez. Kanarya öncesi güvenlik ağı budur.
    yapilandirmayiSabitle(GOLGE);
    cy.visit(V2);
    cy.wait('@site');
    cy.get('[data-testid="model-durumu"]', { timeout: 30000 }).should('have.text', 'hazır');
    cy.get('[data-testid="model-modu"]').should('contain', 'gölge');

    profilDoldur();
    senaryoSec('donem-projesi');
    secenegiTikla(SAGLAM['donem-projesi'][0]);   // hızlı -> eşik aşılır

    cy.get('[data-testid="yansima"]').should('not.be.visible');
    cy.get('[data-testid="secenek-0"]').should('not.be.disabled');

    cy.window().then((pencere) => {
      const satirlar = JSON.parse(pencere.localStorage.getItem('primer_v2_satirlar'));
      // Tahmin KAYDEDİLMİŞ olmalı: karşılaştırma verisini gölge mod üretir
      expect(Number(satirlar[0].golge_tahmin)).to.be.within(0, 1);
    });
  });
});
