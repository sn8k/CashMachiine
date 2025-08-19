// sample.spec.ts v0.1.0 (2025-01-14)
import { test, expect } from '@playwright/test';

test('UI displays example domain title', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example Domain/);
});

test('API responds with JSON', async ({ request }) => {
  const response = await request.get('https://httpbin.org/get');
  expect(response.ok()).toBeTruthy();
});
