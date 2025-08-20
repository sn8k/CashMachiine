/** Goal creation page v0.2.2 (2025-08-20) */
import { useEffect, useState } from 'react';
import { useTranslation } from '../lib/useTranslation';
import { useEventStream } from '../lib/useEventStream';

export default function Goals() {
  const t = useTranslation();
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');
  const [orders, setOrders] = useState([]);
  const event = useEventStream();

  const submitGoal = async (e) => {
    e.preventDefault();
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/goals`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
    });
    setMessage(res.ok ? t('goals.success') : t('goals.error'));
  };

  useEffect(() => {
    if (event && event.event === 'order') {
      setOrders(os => [...os, event.payload]);
    }
  }, [event]);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{t('goals.title')}</h1>
      <form onSubmit={submitGoal} className="space-y-4">
        <input
          className="border p-2 w-full"
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder={t('goals.placeholder')}
        />
        <button className="bg-blue-500 text-white px-4 py-2" type="submit">{t('goals.submit')}</button>
      </form>
      {message && <p className="mt-4">{message}</p>}
      {orders.length > 0 && (
        <ul className="mt-4 list-disc ml-5">
          {orders.map((o, i) => (
            <li key={i}>{o.description || o.id || JSON.stringify(o)}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
