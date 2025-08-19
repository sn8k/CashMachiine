/** next config v0.3.0 (2025-08-19) */
const withPWA = require('next-pwa')({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
  register: true,
  skipWaiting: true,
});

module.exports = withPWA({
  reactStrictMode: true,
  i18n: {
    locales: ['fr', 'en'],
    defaultLocale: 'fr',
  },
});
