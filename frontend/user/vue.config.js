module.exports = {
  publicPath: process.env.APP_BASEPATH,
  pluginOptions: {
    i18n: {
      locale: process.env.I18N_LOCALE,
      fallbackLocale: process.env.I18N_FALLBACK_LOCALE,
      localeDir: 'locales',
      enableInSFC: false
    }
  }
};
