// App v0.1.1 (2025-08-20)
import React, { useEffect, useState } from 'react';
import { Text, View } from 'react-native';

export default function App() {
  const [message, setMessage] = useState('CashMachiine Mobile');

  useEffect(() => {
    if (typeof navigator !== 'undefined' && 'serviceWorker' in navigator) {
      navigator.serviceWorker
        .register('/service-worker.js')
        .then(reg => {
          if (typeof Notification !== 'undefined') {
            Notification.requestPermission().then(permission => {
              if (permission === 'granted') {
                reg.pushManager
                  .subscribe({ userVisibleOnly: true })
                  .then(sub => {
                    fetch('http://localhost:8000/notify/push', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ user_id: 0, subscription: sub }),
                    }).catch(() => {});
                  })
                  .catch(() => {});
              }
            });
          }
        })
        .catch(() => {});
    }
    if (typeof localStorage !== 'undefined') {
      const cached = localStorage.getItem('welcome');
      if (cached) setMessage(cached);
      else localStorage.setItem('welcome', message);
    }
  }, [message]);

  return (
    <View>
      <Text>{message}</Text>
    </View>
  );
}
