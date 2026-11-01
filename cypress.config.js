const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    // Testler YAYINDAKİ uygulamaya karşı koşar; değerlendirilecek olan bu.
    baseUrl: 'https://primer-1.ai.studio',

    // v2 (model katmanı) spec'leri AYRI bir hedefe koşar: repo içindeki
    // web/ sayfası. baseUrl'e dokunulmadı, çünkü v1 regresyon takımının
    // yayındaki uygulamaya koşması regresyon kanıtının ta kendisi.
    //   yerel : npm run v2   -> http://localhost:4173/web/
    //   yayın : npx cypress run -x v2Url=https://<kullanici>.github.io/primer/web/
    //
    // `env` değil `expose`: Cypress 16, `Cypress.env()`'i kaldırdı. Gizli
    // olmayan yapılandırma `expose` ile verilip `Cypress.expose()` ile okunuyor;
    // `env`/`cy.env()` artık gizli değerler için.
    expose: {
      v2Url: 'http://localhost:4173/web/',
    },

    // spec.md AC7 — hedef cihaz iPhone 14
    viewportWidth: 390,
    viewportHeight: 844,

    // Koşum videosu otomatik kaydedilir; demo videosunun ham kaynağı budur.
    video: true,
    videosFolder: 'cypress/videos',
    screenshotOnRunFailure: true,

    // Canlı siteye karşı koşuyoruz; ağ gecikmesine pay bırak.
    defaultCommandTimeout: 15000,
    pageLoadTimeout: 30000,

    supportFile: false,
    retries: { runMode: 1, openMode: 0 },
  },
});
