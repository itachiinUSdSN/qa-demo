import { defineConfig } from '@playwright/test';

if (!process.env.STAGING_URL) throw new Error('STAGING_URL is not set');

export default defineConfig({
  testDir: '.',
  retries: 0, // flakiness is triaged, not hidden
  reporter: [['list'], ['junit', { outputFile: '../../results/e2e.xml' }]],
  use: { baseURL: process.env.STAGING_URL, trace: 'retain-on-failure' },
});
