import { test, expect } from '@playwright/test';

test('adding a product increases the cart count', async ({ page }) => {
  await page.goto('./');
  const addMug = page.getByRole('button', { name: 'Add to cart' }).first();
  const cartCount = page.getByTestId('cart-count');
  await addMug.click();
  await expect(cartCount).toHaveText('1');
});
