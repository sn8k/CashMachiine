/** Analytics dashboard page v0.2.0 (2025-08-19) */
import { useEffect, useRef, useState } from 'react';
import { useTranslation } from '../lib/useTranslation';
import { Chart } from 'chart.js/auto';

export default function Analytics() {
  const t = useTranslation();
  const base = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  const [data, setData] = useState(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    fetch(`${base}/analytics`)
      .then(res => res.json())
      .then(setData)
      .catch(() => setData({ error: true }));
  }, [base]);

  useEffect(() => {
    if (data && !data.error && canvasRef.current) {
      const metrics = data.metrics || {};
      const chart = new Chart(canvasRef.current, {
        type: 'bar',
        data: {
          labels: Object.keys(metrics),
          datasets: [{
            label: t('analytics.metrics'),
            data: Object.values(metrics),
            backgroundColor: 'rgba(75,192,192,0.4)'
          }]
        }
      });
      return () => chart.destroy();
    }
  }, [data, t]);

  if (!data) {
    return <div className="p-4">{t('analytics.loading')}</div>;
  }

  if (data.error) {
    return <div className="p-4">{t('analytics.error')}</div>;
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{t('analytics.title')}</h1>
      <canvas ref={canvasRef} />
    </div>
  );
}
