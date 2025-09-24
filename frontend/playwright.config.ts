import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30 * 1000,
  fullyParallel: true,
  reporter: [['list'], ['html', { outputFolder: 'pw-report' }]],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    viewport: { width: 390, height: 844 }, // Mobile-first (iPhone 12-ish)
  },
  webServer: {
    command: 'npm run dev -- --host 0.0.0.0 --port 3000',
    url: 'http://localhost:3000',
    reuseExistingServer: true,
    cwd: __dirname,
    timeout: 120 * 1000,
  },
});
