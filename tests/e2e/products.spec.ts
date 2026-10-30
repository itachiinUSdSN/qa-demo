import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import fixture from '../fixtures/products.json';

const { products } = fixture;

test('the page lists the three products', async ({ page }) => {
  await page.goto('./');
  const productList = page.getByRole('list', { name: 'Products' });
  const items = productList.getByRole('listitem');
  await expect(items).toHaveCount(products.length);
  for (const product of products) {
    const item = items.filter({ hasText: product.name });
    await expect(item).toHaveCount(1);
  }
});

test('each product has an Add to cart button', async ({ page }) => {
  await page.goto('./');
  const productList = page.getByRole('list', { name: 'Products' });
  const items = productList.getByRole('listitem');
  for (const product of products) {
    const button = items.filter({ hasText: product.name }).getByRole('button', { name: 'Add to cart' });
    await expect(button).toBeVisible();
  }
});

test('the cart count starts at 0', async ({ page }) => {
  await page.goto('./');
  const cartCount = page.getByTestId('cart-count');
  await expect(cartCount).toHaveText('0');
});

test('adding two different products makes the cart count 2', async ({ page }) => {
  await page.goto('./');
  const addFirst = page.getByTestId(products[0].testId);
  const addSecond = page.getByTestId(products[1].testId);
  const cartCount = page.getByTestId('cart-count');
  await addFirst.click();
  await addSecond.click();
  await expect(cartCount).toHaveText('2');
});

test('the page has no serious or critical accessibility violations', async ({ page }) => {
  await page.goto('./');
  const results = await new AxeBuilder({ page }).analyze();
  const blocking = results.violations.filter(v => v.impact === 'serious' || v.impact === 'critical');
  expect(blocking).toEqual([]);
});
