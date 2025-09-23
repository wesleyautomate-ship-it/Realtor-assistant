import { test, expect } from '@playwright/test';

// Helper to take named screenshots into the test output dir
async function snap(page, name: string) {
  await page.screenshot({ path: `screenshots/${name}.png`, fullPage: true });
}

test.describe('PropertyPro AI Frontend Mockup - Visual walkthrough', () => {
  test('Dashboard and navigation', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/PropertyPro|Laura|Real Estate/i);

    // Initial dashboard
    await snap(page, '01-dashboard');

    // Open Command Center and capture
    const commandBtn = page.getByRole('button', { name: /\+/ });
    await commandBtn.click();
    await page.waitForTimeout(250);
    await snap(page, '02-command-center');

    // Close Command Center (look for Close text)
    await page.getByText(/Close/i).click();

    // Navigate bottom nav: Tasks
    await page.getByText(/^Tasks$/).click();
    await page.waitForTimeout(200);
    await snap(page, '03-tasks');

    // Chat view
    await page.getByText(/^Chat$/).click();
    await page.waitForTimeout(200);
    await snap(page, '04-chat');

    // Analytics/Profile tab
    const analytics = page.getByText(/Profile|Analytics/);
    await analytics.click();
    await page.waitForTimeout(200);
    await snap(page, '05-analytics');

    // Back to Dashboard
    await page.getByText(/^Dashboard$/).click();
    await page.waitForTimeout(200);
    await snap(page, '06-dashboard-return');
  });

  test('Feature actions from dashboard cards', async ({ page }) => {
    await page.goto('/');
    await snap(page, 'actions-01-dashboard');

    // Click Marketing if present
    const marketing = page.getByText(/^Marketing$/);
    if (await marketing.isVisible().catch(() => false)) {
      await marketing.click();
      await page.waitForTimeout(250);
      await snap(page, 'actions-02-marketing');
    }

    // Navigate to Tasks again and capture
    await page.getByText(/^Tasks$/).click();
    await page.waitForTimeout(200);
    await snap(page, 'actions-03-tasks');
  });
});
