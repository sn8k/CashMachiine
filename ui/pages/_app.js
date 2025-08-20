/** Custom App v0.2.2 (2025-08-20) */
import { useEffect } from 'react';
import Head from 'next/head';
import '../styles/globals.css';
import { registerPush } from '../lib/push';

export default function App({ Component, pageProps }) {
  useEffect(() => {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker
        .register('/service-worker.js')
        .then(reg => registerPush(reg))
        .catch(() => {});
    }
  }, []);
  return (
    <>
      <Head>
        <link rel="manifest" href="/manifest.json" />
      </Head>
      <Component {...pageProps} />
    </>
  );
}
