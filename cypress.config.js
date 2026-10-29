const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    // Testler YAYINDAKİ uygulamaya karşı koşar; değerlendirilecek olan bu.
    baseUrl: 'https://primer-1.ai.studio',

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
