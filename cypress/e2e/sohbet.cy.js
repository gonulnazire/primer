/// <reference types="cypress" />

/**
 * Primer — serbest sohbet testleri (v2)
 *
 * Sohbet, spec.md §2'deki kapsam genişlemesiyle eklendi. İlk gerekçe
 * "deterministik test edilemez" idi; bu dosya o gerekçenin neden yanlış
 * olduğunun kanıtı: testler modelin ne söylediğine değil, uygulamanın
 * SÖZLEŞMESİNE bakıyor.
 *
 * Sözleşme (yayındaki paketten okundu):
 *   POST /api/chat  →  { email, message, history[], context{} }
 *   Yanıt           →  { text }  ·  hata: { error } veya HTTP != 2xx
 *
 * Saklama:
 *   localStorage['primer_user_email']       e-posta (küçük harfe çevrilmiş)
 *   localStorage['primer_chat_<eposta>']    sohbet geçmişi (JSON)
 */

const CHAT_STUB = { text: 'Bu kararı verirken hangi bilgiye sahip olmadığını fark ettin mi?' };

// Sohbeti açan yüzen butonun data-testid'i yok; erişilebilirlik etiketiyle
// bulunuyor. Etiket değişirse bu testler kırılır — kasıtlı.
const SOHBETI_AC = '[aria-label="Sokratik Yapay Zeka Mentorunu Aç"]';

function sohbetiAc() {
  cy.get(SOHBETI_AC).click();
}

function epostaGir(eposta) {
  cy.get('[data-testid="sohbet-eposta"]').type(eposta);
  cy.get('[data-testid="sohbet-eposta-onay"]').click();
}

describe('Primer — serbest sohbet', () => {
  beforeEach(() => {
    cy.intercept('POST', '**/api/chat', { statusCode: 200, body: CHAT_STUB }).as('chat');
    cy.visit('/');
    cy.clearLocalStorage();
    sohbetiAc();
  });

  // E-posta alanında İKİ doğrulama katmanı var ve sırası önemli:
  //   1) Tarayıcının HTML5 doğrulaması (<input type="email"> + type="submit")
  //   2) Uygulamanın kendi kuralı: "@" VE "." içermeli
  // Çoğu yazım hatasında birinci katman devreye girer ve kullanıcı tarayıcının
  // kendi balonunu görür — uygulamanın Türkçe uyarısı değil. İkinci katman
  // yalnızca HTML5'e göre geçerli ama uygulamaya göre geçersiz girdilerde
  // görünür (örn. nokta içermeyen alan adı). İkisi de ayrı test ediliyor.

  it('HTML5 doğrulaması: @ içermeyen adres gönderilemez', () => {
    epostaGir('gecersiz-adres');

    cy.window().then((win) => {
      expect(win.localStorage.getItem('primer_user_email'), 'saklanmamalı').to.be.null;
    });
    // Alan hâlâ ekranda: form gönderilmedi
    cy.get('[data-testid="sohbet-eposta"]').should('be.visible');
  });

  it('uygulama doğrulaması: nokta içermeyen adres Türkçe uyarı verir', () => {
    // "ad@ornek" HTML5'e göre geçerli, uygulamanın kuralına göre değil.
    epostaGir('ad@ornek');

    cy.contains('Lütfen geçerli bir e-posta adresi girin').should('be.visible');
    cy.window().then((win) => {
      expect(win.localStorage.getItem('primer_user_email'), 'saklanmamalı').to.be.null;
    });
  });

  it('geçerli e-posta küçük harfe çevrilerek saklanır', () => {
    epostaGir('  Gonul@Ornek.COM  ');

    cy.window().then((win) => {
      expect(win.localStorage.getItem('primer_user_email')).to.eq('gonul@ornek.com');
    });
    cy.get('[data-testid="sohbet-mesajlar"]').should('contain', 'Primer Sokratik Mentoru');
  });

  it('mesaj gönderilir: istek sözleşmeye uyar, cevap listeye eklenir', () => {
    epostaGir('gonul@ornek.com');

    cy.get('[data-testid="sohbet-mesaj"]').type('Rollback yapmalı mıyım?');
    cy.get('[data-testid="sohbet-gonder"]').click();

    cy.wait('@chat').its('request.body').then((body) => {
      expect(body.email, 'e-posta gönderilmeli').to.eq('gonul@ornek.com');
      expect(body.message).to.eq('Rollback yapmalı mıyım?');
      expect(body.history, 'geçmiş dizi olmalı').to.be.an('array');
    });

    // Kullanıcının mesajı ve modelin cevabı listede
    cy.get('[data-testid="sohbet-mesajlar"]')
      .should('contain', 'Rollback yapmalı mıyım?')
      .and('contain', CHAT_STUB.text);
  });

  it('gönderilen mesaj e-postaya bağlı olarak saklanır', () => {
    epostaGir('gonul@ornek.com');
    cy.get('[data-testid="sohbet-mesaj"]').type('Merhaba');
    cy.get('[data-testid="sohbet-gonder"]').click();
    cy.wait('@chat');

    cy.window().then((win) => {
      const kayit = win.localStorage.getItem('primer_chat_gonul@ornek.com');
      expect(kayit, 'e-posta anahtarıyla saklanmalı').to.be.a('string');
      expect(JSON.parse(kayit).some((m) => m.text === 'Merhaba')).to.be.true;
    });
  });

  it('boş mesajla gönder butonu pasiftir', () => {
    epostaGir('gonul@ornek.com');
    cy.get('[data-testid="sohbet-gonder"]').should('be.disabled');

    cy.get('[data-testid="sohbet-mesaj"]').type('bir şey');
    cy.get('[data-testid="sohbet-gonder"]').should('not.be.disabled');
  });

  it('"Sohbeti sıfırla" saklanan e-postayı siler', () => {
    epostaGir('gonul@ornek.com');
    cy.window().its('localStorage.primer_user_email').should('eq', 'gonul@ornek.com');

    cy.get('[data-testid="sohbet-sifirla"]').click();

    cy.window().then((win) => {
      expect(
        win.localStorage.getItem('primer_user_email'),
        'kullanıcı sakladığını silebilmeli'
      ).to.be.null;
    });
  });
});
