/** Home page v0.2.3 (2025-08-20) */
import Link from 'next/link';
import { useTranslation } from '../lib/useTranslation';

export default function Home() {
  const t = useTranslation();
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{t('home.title')}</h1>
      <ul className="list-disc ml-5">
        <li><Link href="/goals">{t('home.createGoal')}</Link></li>
        <li><Link href="/daily-actions">{t('home.dailyActions')}</Link></li>
        <li><Link href="/analytics">{t('home.analytics')}</Link></li>
        <li><Link href="/alerts">{t('home.alerts')}</Link></li>
      </ul>
    </div>
  );
}
