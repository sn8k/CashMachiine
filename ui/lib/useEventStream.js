/** WebSocket event hook v0.1.0 (2025-08-20) */
import { useEffect, useState } from 'react';

export function useEventStream() {
  const [event, setEvent] = useState(null);
  useEffect(() => {
    const base = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const ws = new WebSocket(base.replace('http', 'ws') + '/ws');
    ws.onmessage = e => {
      try {
        setEvent(JSON.parse(e.data));
      } catch {
        // ignore invalid JSON
      }
    };
    return () => ws.close();
  }, []);
  return event;
}
