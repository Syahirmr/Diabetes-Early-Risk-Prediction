import { test, expect } from '@playwright/test';

test.describe('Diabetes Risk Assessment Flow', () => {

  test.beforeEach(async ({ page }) => {
    page.on('console', msg => console.log(`BROWSER LOG: ${msg.text()}`));
    page.on('pageerror', err => console.log(`BROWSER ERROR: ${err.message}`));
    // Navigate to the app
    await page.goto('http://localhost:3000');
  });

  test('E2E Flow: Landing -> Assessment -> Result -> Explain', async ({ page }) => {
    // 1. Landing
    await expect(page.getByText('Mulai Asesmen Gratis')).toBeVisible();
    await page.screenshot({ path: 'reports/screenshot_landing.png' });
    await page.getByText('Mulai Asesmen Gratis').click();

    // 2. Assessment Step 1: Profil Dasar
    await expect(page.getByRole('heading', { name: 'Profil Dasar' })).toBeVisible();
    await page.screenshot({ path: 'reports/screenshot_assessment.png' });
    await page.locator('input[placeholder="Contoh: 45"]').fill('45');
    await page.locator('select').first().selectOption('Male');
    await page.locator('input[placeholder="Contoh: 24.5"]').fill('24.5');
    await page.locator('select').nth(1).selectOption('never');
    
    await page.locator('button:has-text("Selanjutnya")').first().click();

    // Step 2: Riwayat Penyakit
    await expect(page.getByRole('heading', { name: 'Riwayat Penyakit' })).toBeVisible();
    await page.locator('label').filter({ hasText: 'Tidak' }).nth(0).click();
    await page.locator('label').filter({ hasText: 'Tidak' }).nth(1).click();
    
    await page.locator('button:has-text("Selanjutnya")').nth(1).click();

    // Step 3: Parameter Klinis
    await expect(page.getByRole('heading', { name: 'Parameter Klinis' })).toBeVisible();
    await page.locator('input[placeholder="Contoh: 6.5"]').fill('6.5');
    await page.locator('input[placeholder="Contoh: 120"]').fill('120');
    
    // Submit
    await page.locator('button:has-text("Lihat Hasil Risiko")').first().click();

    // 3. Result
    await expect(page.getByText('Hasil Analisis Risiko')).toBeVisible();
    await page.screenshot({ path: 'reports/screenshot_result.png' });
    
    // 4. Explain Expand
    await page.getByText('Analisis Mendalam (Explain)').click();
    // It should load shap data, wait for it
    await expect(page.getByText('Seluruh Faktor Signifikan')).toBeVisible({timeout: 10000});

    // 5. Export
    await expect(page.getByText('Cetak/PDF')).toBeVisible();
  });

  test('Validation and State Recovery', async ({ page }) => {
    // Navigate and fill some data
    await page.goto('http://localhost:3000');
    await page.waitForTimeout(500); // Wait for init
    
    await page.getByText('Mulai Asesmen Gratis').click();
    
    // Fill first field
    await page.locator('input[placeholder="Contoh: 45"]').fill('50');
    
    // Reload page
    await page.reload();
    await page.waitForTimeout(1000);
    
    // It should automatically stay on assessment form due to hash #assessment
    await expect(page.getByRole('heading', { name: 'Profil Dasar' })).toBeVisible();
    
    const val = await page.locator('input[placeholder="Contoh: 45"]').inputValue();
    expect(val).toBe('50');
  });

});
