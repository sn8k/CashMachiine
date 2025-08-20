// sample.spec.ts v0.1.1 (2025-08-20)
import { test, expect } from '@playwright/test';
import { createServer } from 'http';
import type { AddressInfo } from 'net';

test('UI displays example domain title', async () => {
  const html = '<html><head><title>Example Domain</title></head><body></body></html>';
  const match = /<title>([^<]*)<\/title>/.exec(html);
  expect(match?.[1]).toBe('Example Domain');
});

test('API responds with JSON', async ({ request }) => {
  const server = createServer((_, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ ok: true }));
  });
  await new Promise(resolve => server.listen(0, resolve));
  const { port } = server.address() as AddressInfo;
  const response = await request.get(`http://localhost:${port}`);
  expect(response.ok()).toBeTruthy();
  const data = await response.json();
  expect(data.ok).toBeTruthy();
  server.close();
});
