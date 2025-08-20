/** Daily actions page v0.3.2 (2025-08-20) */
import { useEffect, useState } from 'react';
import { useTranslation } from '../lib/useTranslation';
import { useEventStream } from '../lib/useEventStream';

export default function DailyActions() {
  const t = useTranslation();
  const base = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  const [actions, setActions] = useState([]);
  const [message, setMessage] = useState('');
  const event = useEventStream();

  useEffect(() => {
    const cached = localStorage.getItem('actions');
    if (cached) setActions(JSON.parse(cached));
    fetch(`${base}/actions`)
      .then(res => res.json())
      .then(data => {
        setActions(data.actions || []);
        localStorage.setItem('actions', JSON.stringify(data.actions || []));
      })
      .catch(() => {});
  }, [base]);

  useEffect(() => {
    if (event && event.event === 'action') {
      setActions(as => {
        const updated = [...as, event.payload];
        localStorage.setItem('actions', JSON.stringify(updated));
        return updated;
      });
    }
  }, [event]);

  const check = id => {
    fetch(`${base}/actions/${id}/check`, { method: 'POST' })
      .then(res => {
        if (!res.ok) throw new Error('failed');
        setActions(as => {
          const updated = as.map(a => a.id === id ? { ...a, done: true } : a);
          localStorage.setItem('actions', JSON.stringify(updated));
          return updated;
        });
        setMessage(t('daily.checked'));
      })
      .catch(() => setMessage(t('daily.error')));
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{t('daily.title')}</h1>
      {message && <p className="mb-2 text-sm text-green-600">{message}</p>}
      <ul className="ml-5">
        {actions.map(a => (
          <li key={a.id || a} className="mb-1">
            <label className="inline-flex items-center">
              <input
                type="checkbox"
                className="mr-2"
                checked={a.done}
                onChange={() => check(a.id)}
              />
              {a.description || a.name || a}
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
}
