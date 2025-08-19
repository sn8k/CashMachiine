// playwright.config.ts v0.1.0 (2025-01-14)
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  reporter: [['html', { outputFolder: 'tests/e2e/reports', open: 'never' }]],
});
