/** Alerts subscription page v0.1.0 (2025-08-20) */
import { useState } from 'react';
import { useTranslation } from '../lib/useTranslation';

export default function Alerts() {
  const t = useTranslation();
  const [metric, setMetric] = useState('');
  const [threshold, setThreshold] = useState('');
  const [message, setMessage] = useState('');

  const subscribe = async (e) => {
    e.preventDefault();
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/alerts/subscribe`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: 1, metric, threshold: parseFloat(threshold) }),
    });
    setMessage(res.ok ? 'ok' : 'error');
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{t('alerts.title')}</h1>
      <form onSubmit={subscribe} className="space-y-4">
        <input
          className="border p-2 w-full"
          value={metric}
          onChange={e => setMetric(e.target.value)}
          placeholder={t('alerts.metric')}
        />
        <input
          className="border p-2 w-full"
          value={threshold}
          onChange={e => setThreshold(e.target.value)}
          placeholder={t('alerts.threshold')}
        />
        <button className="bg-blue-500 text-white px-4 py-2" type="submit">{t('alerts.subscribe')}</button>
      </form>
      {message && <p className="mt-4">{message}</p>}
    </div>
  );
}
