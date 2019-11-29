module.exports = {
  publicPath: process.env.BASE_URL,
  pluginOptions: {
    i18n: {
      locale: process.env.I18N_LOCALE,
      fallbackLocale: process.env.I18N_FALLBACK_LOCALE,
      localeDir: 'locales',
      enableInSFC: true
    }
  }
};
