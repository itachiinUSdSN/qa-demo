import { test, expect } from '@playwright/test';

test('adding a product increases the cart count', async ({ page }) => {
  await page.goto('./');
  const addMug = page.getByTestId('add-mug-blue');
  const cartCount = page.getByTestId('cart-count');
  await addMug.click();
  await expect(cartCount).toHaveText('1');
});

test('Clear cart resets the cart badge to 0', async ({ page }) => {
  await page.goto('./');
  const addMug = page.getByTestId('add-mug-blue');
  const addPen = page.getByTestId('add-red-pen');
  const clearCart = page.getByRole('button', { name: 'Clear cart' });
  const cartCount = page.getByTestId('cart-count');
  await addMug.click();
  await addPen.click();
  await expect(cartCount).toHaveText('2');
  await clearCart.click({ timeout: 5000 });
  await expect(cartCount).toHaveText('0');
});

test('Clear cart leaves every product in the list', async ({ page }) => {
  await page.goto('./');
  const addMug = page.getByTestId('add-mug-blue');
  const addPen = page.getByTestId('add-red-pen');
  const clearCart = page.getByRole('button', { name: 'Clear cart' });
  const items = page.getByRole('list', { name: 'Products' }).getByRole('listitem');
  await addMug.click();
  await addPen.click();
  await clearCart.click({ timeout: 5000 });
  await expect(items).toHaveCount(3);
});
