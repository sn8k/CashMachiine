/** Daily actions page v0.2.1 (2025-08-20) */
import { useEffect, useState } from 'react';
import { useTranslation } from '../lib/useTranslation';

export default function DailyActions() {
  const t = useTranslation();
  const [actions, setActions] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/actions`)
      .then(res => res.json())
      .then(data => setActions(data.actions || []))
      .catch(() => setActions([]));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{t('daily.title')}</h1>
      <ul className="list-disc ml-5">
        {actions.map((a, i) => <li key={i}>{a}</li>)}
      </ul>
    </div>
  );
}
