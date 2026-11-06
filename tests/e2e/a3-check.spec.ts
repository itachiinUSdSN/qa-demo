import { test, expect } from '@playwright/test';

test('home page shows the main heading', async ({ page }) => {
  await page.goto('./');
  const heading = page.getByRole('heading', { level: 1 });
  await expect(heading).toBeVisible();
});
