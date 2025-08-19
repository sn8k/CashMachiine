/** Analytics dashboard page v0.1.0 (2025-08-19) */
import { useEffect, useState } from 'react';
import { useTranslation } from '../lib/useTranslation';

export default function Analytics() {
  const t = useTranslation();
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/analytics`)
      .then(res => res.json())
      .then(setData)
      .catch(() => setData({ error: 'unavailable' }));
  }, []);

  if (!data) {
    return <div className="p-4">{t('analytics.loading')}</div>;
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{t('analytics.title')}</h1>
      <pre className="bg-gray-100 p-2 text-sm overflow-x-auto">{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
