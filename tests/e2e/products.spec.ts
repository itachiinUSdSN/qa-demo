import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { readFileSync } from 'fs';
import { join } from 'path';

const products: { names: string[] } = JSON.parse(
  readFileSync(join(__dirname, '../fixtures/products.json'), 'utf-8'),
);

test('page lists the three products', async ({ page }) => {
  await page.goto('./');
  const items = page.getByRole('listitem');
  await expect(items).toHaveCount(products.names.length);
  for (const name of products.names) {
    const item = page.getByRole('listitem').filter({ hasText: name });
    await expect(item).toBeVisible();
  }
});

test('each product has an Add to cart button', async ({ page }) => {
  await page.goto('./');
  const buttons = page.getByRole('button', { name: 'Add to cart' });
  await expect(buttons).toHaveCount(products.names.length);
});

test('cart count starts at 0', async ({ page }) => {
  await page.goto('./');
  const cartCount = page.getByTestId('cart-count');
  await expect(cartCount).toHaveText('0');
});

test('adding two different products makes the cart count 2', async ({ page }) => {
  await page.goto('./');
  const addMug = page.getByTestId('add-mug-blue');
  const addPen = page.getByTestId('add-red-pen');
  const cartCount = page.getByTestId('cart-count');
  await addMug.click();
  await addPen.click();
  await expect(cartCount).toHaveText('2');
});

test('page has no serious or critical accessibility violations', async ({ page }) => {
  await page.goto('./');
  const results = await new AxeBuilder({ page }).analyze();
  const serious = results.violations.filter(v => v.impact === 'serious' || v.impact === 'critical');
  expect(serious).toEqual([]);
});
