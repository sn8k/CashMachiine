/** Scenario runner page v0.1.0 (2025-08-20) */
import { useState } from 'react';
import { useTranslation } from '../lib/useTranslation';

export default function WhatIf() {
  const t = useTranslation();
  const [name, setName] = useState('');
  const [result, setResult] = useState(null);

  const runScenario = async (e) => {
    e.preventDefault();
    const base = process.env.NEXT_PUBLIC_WHATIF_URL || 'http://localhost:8000';
    const res = await fetch(`${base}/scenarios/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
    });
    if (res.ok) {
      const { id } = await res.json();
      const r = await fetch(`${base}/scenarios/${id}`);
      if (r.ok) {
        setResult(await r.json());
      }
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{t('whatif.title')}</h1>
      <form onSubmit={runScenario} className="space-y-4">
        <input
          className="border p-2 w-full"
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder={t('whatif.placeholder')}
        />
        <button className="bg-blue-500 text-white px-4 py-2" type="submit">
          {t('whatif.run')}
        </button>
      </form>
      {result && <pre className="mt-4 text-sm">{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
