/// <reference types="cypress" />

/**
 * Primer — uçtan uca testler
 *
 * Her test spec.md §7'deki bir kabul örneğine bağlıdır; test adında geçer.
 * Hedef: https://primer-1.ai.studio (cypress.config.js'teki baseUrl)
 *
 * SEÇENEKLER KONUMA GÖRE SEÇİLMEZ.
 * spec.md AC10 gereği seçeneklerin ekrandaki sırası karıştırılır, çünkü sabit
 * sıra cevabı sızdırır (arkadaş testi bulgusu: "hep birinci şık doğru").
 * Bu yüzden testler seçenekleri `secenek-N` indeksiyle değil, spec.md §5'te
 * tanımlı metinleriyle bulur. Metin spec'in parçası; konum değil.
 */

const SOKRATIK_STUB = {
  fallback: false,
  text:
    'Son çalışan commit\'e dönmeyi seçtin. O commit\'in gerçekten ' +
    'çalıştığını nereden biliyordun? Kaybolan iş kimin işiydi?',
};

// spec.md §6.1 — S1/S6 yasaklı kalıp listesi
const YASAKLI = [
  'yapmalısın', 'yapmalıydın', 'etmelisin', 'etmeliydin',
  'şunu yap', 'şöyle yap', 'en iyisi', 'doğru cevap', 'doğrusu şu',
  'tavsiyem', 'öneriyorum', 'yanlış yaptın', 'hata yaptın', 'kötü bir seçim',
];

// spec.md §5 — her karar noktasındaki "saglam" ve "riskli" seçeneklerin
// ayırt edici metin parçaları, karar sırasıyla.
const SAGLAM = {
  'donem-projesi': ['Son çalışan commit', 'Net bir süre veren', 'Çalışan 3 özelliği'],
  'staj-task': ['takım kanalına yazılı', 'yerine bakan kişiyi', 'Küçük bir test yaz'],
  'vize-haftasi': ['yargılamadan sor', 'En ağır vizeye', 'Kendi katkını açıkça'],
};
const RISKLI = {
  'donem-projesi': ['Gece boyu hatayı', 'Hiçbir şey söyleme', '8 özelliğin hepsini'],
  'staj-task': ['Hemen düzelt', 'Canlıda dene', 'stajyer işi değil'],
  'vize-haftasi': ['Hiçbir şey deme', 'Ödevi mükemmel yap', 'hiçbir not düşmeden'],
};

const SENARYOLAR = ['donem-projesi', 'staj-task', 'vize-haftasi'];

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
  cy.contains('[data-testid^="secenek-"]', metin).click();
}

/** Bir senaryonun üç kararını verilen tabloya göre verir. */
function ucKararVer(senaryo, tablo) {
  tablo[senaryo].forEach(secenegiTikla);
}

describe('Primer — uçtan uca', () => {
  beforeEach(() => {
    // Sokratik çağrı varsayılan olarak sabitlenir: testler modelin o anki
    // metnine değil uygulamanın sözleşmesine bakmalı. Ayrıca canlı uç nokta
    // hız sınırlı (bkz. TUTOR-EVAL.md §4.3) — gerçek çağrı testleri kırardı.
    cy.intercept('POST', '**/api/socratic', {
      statusCode: 200,
      body: SOKRATIK_STUB,
    }).as('sokratik');

    cy.visit('/');
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

    // Aynı senaryo, farklı rol → farklı teknik detay
    cy.visit('/');
    profilDoldur({ rol: 'Frontend' });
    senaryoSec('donem-projesi');
    cy.get('[data-testid="kriz-metni"]')
      .should('contain', 'Build pipeline')
      .and('not.contain', 'veritabanı');
  });

  it('AC3 — karar noktaları sırayla gelir, geri dönüş yoktur', () => {
    profilDoldur();
    senaryoSec('donem-projesi');

    // İlerleme göstergesi bilgi verir, gezinme aracı değildir
    cy.get('[data-testid="ilerleme"]').find('button').should('have.length', 0);

    secenegiTikla(SAGLAM['donem-projesi'][0]);
    cy.get('[data-testid="ilerleme"]').find('button').should('have.length', 0);
    // Sıradaki karar geldi: ikinci karar noktasının seçeneği görünür
    cy.contains('[data-testid^="secenek-"]', SAGLAM['donem-projesi'][1]).should('exist');
  });

  it('AC4 — üç sağlam karar İYİ SON üretir (senaryo A)', () => {
    profilDoldur();
    senaryoSec('donem-projesi');
    ucKararVer('donem-projesi', SAGLAM);

    cy.get('[data-testid="sonuc-bandi"]')
      .should('contain', 'İYİ SON')
      .and('contain', '3/3 sağlam karar');
  });

  it('AC5 — üç riskli karar KÖTÜ SON üretir (senaryo A)', () => {
    profilDoldur();
    senaryoSec('donem-projesi');
    ucKararVer('donem-projesi', RISKLI);

    cy.get('[data-testid="sonuc-bandi"]')
      .should('contain', 'KÖTÜ SON')
      .and('contain', '0/3 sağlam karar');
  });

  it('AC4/AC5 — senaryo B her iki sona da ulaşır', () => {
    profilDoldur();
    senaryoSec('staj-task');
    ucKararVer('staj-task', SAGLAM);
    cy.get('[data-testid="sonuc-bandi"]').should('contain', 'İYİ SON');

    cy.get('[data-testid="bastan-basla"]').click();
    senaryoSec('staj-task');
    ucKararVer('staj-task', RISKLI);
    cy.get('[data-testid="sonuc-bandi"]').should('contain', 'KÖTÜ SON');
  });

  it('AC4/AC5 — senaryo C her iki sona da ulaşır', () => {
    profilDoldur();
    senaryoSec('vize-haftasi');
    ucKararVer('vize-haftasi', SAGLAM);
    cy.get('[data-testid="sonuc-bandi"]').should('contain', 'İYİ SON');

    cy.get('[data-testid="bastan-basla"]').click();
    senaryoSec('vize-haftasi');
    ucKararVer('vize-haftasi', RISKLI);
    cy.get('[data-testid="sonuc-bandi"]').should('contain', 'KÖTÜ SON');
  });

  it('AC6 — Sokratik blok soru içerir ve yasaklı kalıp içermez', () => {
    profilDoldur();
    senaryoSec('donem-projesi');
    ucKararVer('donem-projesi', SAGLAM);

    cy.wait('@sokratik');
    cy.get('[data-testid="sokratik-blok"]')
      .should('be.visible')
      .invoke('text')
      .then((metin) => {
        const t = metin.trim();
        expect(t, 'boş olmamalı').to.not.equal('');
        expect(t, 'soru içermeli').to.include('?');

        const kucuk = t.toLocaleLowerCase('tr');
        const bulunan = YASAKLI.filter((k) => kucuk.includes(k.toLocaleLowerCase('tr')));
        expect(bulunan, `yasaklı kalıp: ${bulunan.join(', ')}`).to.be.empty;
      });
  });

  it('AC6 — model cevap veremezse yedek soru gösterilir', () => {
    // Hız sınırında vekil {fallback:true} döner (bkz. TUTOR-EVAL.md §4.3).
    // Ekran bu durumda da Sokratik kalmalı.
    cy.intercept('POST', '**/api/socratic', {
      statusCode: 200,
      body: { fallback: true },
    }).as('sokratikDustu');

    profilDoldur();
    senaryoSec('donem-projesi');
    ucKararVer('donem-projesi', SAGLAM);

    cy.wait('@sokratikDustu');
    cy.get('[data-testid="sokratik-blok"]')
      .should('be.visible')
      .and('contain', 'Rehber şu an cevap veremedi')
      .and('contain', '?');
  });

  it('AC7 — 390px genişlikte yatay kaydırma yok, hedefler ≥44px', () => {
    profilDoldur();

    cy.document().then((d) => {
      expect(
        d.documentElement.scrollWidth,
        'yatay kaydırma oluşmamalı'
      ).to.be.at.most(d.documentElement.clientWidth);
    });

    senaryoSec('donem-projesi');
    cy.get('[data-testid="secenek-0"]').then(($el) => {
      expect($el[0].getBoundingClientRect().height, 'dokunma hedefi').to.be.at.least(44);
    });

    cy.document().then((d) => {
      expect(d.documentElement.scrollWidth).to.be.at.most(d.documentElement.clientWidth);
    });
  });

  it('AC8 — baştan başla kararları sıfırlar, profili korur', () => {
    profilDoldur({ rol: 'Backend' });
    senaryoSec('donem-projesi');
    ucKararVer('donem-projesi', SAGLAM);
    cy.get('[data-testid="sonuc-bandi"]').should('contain', 'İYİ SON');

    cy.get('[data-testid="bastan-basla"]').click();

    // Menüye döndük, profil ekranına değil
    cy.get('[data-testid="senaryo-donem-projesi"]').should('be.visible');

    // Profil korunmuş: rol hâlâ backend olduğu için kriz metni aynı varyant
    senaryoSec('donem-projesi');
    cy.get('[data-testid="kriz-metni"]').should('contain', 'veritabanı');

    // Kararlar sıfırlanmış: baştan üç karar verilebiliyor
    ucKararVer('donem-projesi', SAGLAM);
    cy.get('[data-testid="sonuc-bandi"]').should('contain', '3/3 sağlam karar');
  });

  it('AC9 — Türkçe büyük harf kuralı (lang="tr")', () => {
    cy.document().its('documentElement.lang').should('eq', 'tr');

    // lang="en" altında "Simülasyon Özeti" → "SIMÜLASYON ÖZETI" olurdu.
    // Hatalı büyük harf kalıbı hiçbir ekranda görünmemeli.
    profilDoldur();
    senaryoSec('donem-projesi');
    ucKararVer('donem-projesi', SAGLAM);
    cy.get('body').should('not.contain', 'ÖZETI');
  });

  it('AC10 — sağlam seçenek hep aynı konumda değildir', () => {
    // Arkadaş testi bulgusu: sıra sabitken "hep birinci şık doğru" öğrenilebiliyor
    // ve ürünün tek iddiası çöküyor. Üç senaryonun dokuz karar noktası örneklenir.
    const konumlar = [];

    profilDoldur();

    cy.wrap(SENARYOLAR).each((senaryo) => {
      senaryoSec(senaryo);
      cy.wrap(SAGLAM[senaryo]).each((metin) => {
        cy.contains('[data-testid^="secenek-"]', metin)
          .invoke('attr', 'data-testid')
          .then((id) => {
            konumlar.push(id);
          });
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
});
