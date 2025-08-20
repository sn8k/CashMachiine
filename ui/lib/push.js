/** Push helper v0.1.0 (2025-08-20) */
export async function registerPush(reg) {
  if (!('Notification' in window)) return;
  const perm = await Notification.requestPermission();
  if (perm !== 'granted') return;
  const sub = await reg.pushManager.subscribe({ userVisibleOnly: true });
  await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/notify/push`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: 0, subscription: sub }),
  }).catch(() => {});
}
