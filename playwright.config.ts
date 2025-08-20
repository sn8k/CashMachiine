// playwright.config.ts v0.1.1 (2025-08-20)
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  reporter: [['html', { outputFolder: 'tests/e2e/reports', open: 'never' }]],
  use: {
    browserName: 'chromium',
    executablePath: '/usr/bin/chromium-browser',
    headless: true,
  },
});
