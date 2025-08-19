/** Translation hook v0.1.0 (2025-08-20) */
import { useRouter } from 'next/router';
import en from '../public/locales/en.json';
import fr from '../public/locales/fr.json';

const resources = { en, fr };

export function useTranslation() {
  const { locale } = useRouter();
  const dict = resources[locale] || resources.fr;
  return (path) => path.split('.').reduce((res, key) => res?.[key], dict) || path;
}
