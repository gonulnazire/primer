/// <reference types="cypress" />

/**
 * Primer v2 — DİFERANSİYEL (PARİTE) TESTİ
 *
 * spec.md AC12 · tests/parite.py (test kahini) · model/config.json (sözleşme)
 *
 * Ne kanıtlıyor: aynı model.onnx'i çalıştıran İKİ BAĞIMSIZ sistem — tarayıcıdaki
 * onnxruntime-web ve Python onnxruntime — aynı referans girdilerde aynı cevabı
 * veriyor. Tek bir sistemin kendi kendini test etmesi bunu gösteremez: özellik
 * sırası kayarsa veya tip dönüşümü bozulursa tek taraflı test yine geçer,
 * çünkü yanlışı iki tarafta da aynı şekilde yapar.
 *
 * Hedef: Cypress.expose('v2Url') — v1 baseUrl'ü DEĞİL (bkz. cypress.config.js).
 */

const V2 = Cypress.expose('v2Url');

describe('Primer v2 — diferansiyel test', () => {
  it('AC12 — tarayıcı çıkarımı Python kahiniyle 1e-4 toleransında uyuşur', () => {
    cy.readFile('tests/parite.json').then((referans) => {
      expect(referans.girdiler, 'beş referans girdi').to.have.length(5);

      cy.visit(V2 + '?parite=1');

      // Model inmeden karşılaştırma yapmanın anlamı yok; "hazır" bekleniyor.
      cy.get('[data-testid="parite-durumu"]', { timeout: 30000 })
        .should('contain', 'hazır');

      cy.get('#parite-govde tr').should('have.length', referans.girdiler.length);

      referans.girdiler.forEach((girdi, i) => {
        cy.get(`[data-testid="parite-p-${i}"]`)
          .invoke('text')
          .then((metin) => {
            const pUygulama = Number(metin);
            expect(pUygulama, `girdi ${i + 1} sayı olmalı`).not.to.be.NaN;

            const fark = Math.abs(pUygulama - girdi.p_kahin);
            expect(
              fark,
              `girdi ${i + 1} (${girdi.aciklama}) — ` +
              `uygulama ${pUygulama}, kahin ${girdi.p_kahin}`
            ).to.be.lessThan(referans.tolerans);
          });
      });
    });
  });

  it('eşiğin iki yanı da örnekleniyor — parite testi yalnız kolay bölgeyi ölçmesin', () => {
    // Beş girdinin hepsi eşiğin aynı tarafında olsaydı test, modelin ayrım
    // yaptığı bölgeyi hiç görmezdi.
    cy.readFile('model/config.json').then((config) => {
      cy.readFile('tests/parite.json').then((referans) => {
        const esik = config.karar_esigi;
        const ustunde = referans.girdiler.filter((g) => g.p_kahin >= esik).length;
        const altinda = referans.girdiler.filter((g) => g.p_kahin < esik).length;

        expect(ustunde, `karar eşiğinin (${esik}) üstünde girdi`).to.be.greaterThan(0);
        expect(altinda, `karar eşiğinin (${esik}) altında girdi`).to.be.greaterThan(0);
      });
    });
  });

  it('özellik sırası sözleşmesi: config.json ile parite.json aynı', () => {
    // Sıra sözleşmedir (spec.md §10.3). İki dosya ayrışırsa parite testi
    // "aynı sayı" demeye devam eder ama farklı bir soruyu cevaplamış olur.
    cy.readFile('model/config.json').then((config) => {
      cy.readFile('tests/parite.json').then((referans) => {
        expect(referans.ozellikler).to.deep.equal(config.girdi.ozellikler);
        expect(config.girdi.bicim[1]).to.equal(config.girdi.ozellikler.length);
      });
    });
  });
});
