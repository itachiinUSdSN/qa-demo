import { test, expect } from '@playwright/test';

test('adding a product increases the cart count', async ({ page }) => {
  await page.goto('./');
  const addMug = page.getByTestId('add-blue-mug');
  const cartCount = page.getByTestId('cart-count');
  await addMug.click();
  await expect(cartCount).toHaveText('1');
});
