import { test, expect } from '@playwright/test';

test.describe('Phase 5: Integration & UI Resilience', () => {

  test.beforeEach(async ({ page }) => {
    // Navigate to the app
    await page.goto('http://localhost:3000');
    // Ensure we start from Landing
    const startBtn = page.getByText('Mulai Asesmen Gratis');
    if (await startBtn.isVisible()) {
      await startBtn.click();
    }
  });

  // SCENARIO 1: Success (Happy Path E2E)
  test('SCENARIO 1: Success (Happy Path E2E)', async ({ page }) => {
    // Mock successful backend response
    await page.route('**/api/v1/predict', async route => {
      await route.fulfill({ status: 200, json: { prediction: "HIGH", probability: 0.87, recommendation: "Konsultasi" } });
    });
    await page.route('**/api/v1/explain', async route => {
      await route.fulfill({ status: 200, json: { base_value: 0.4, shap_values: { bmi: 0.1 }, features: { bmi: 24.5 }, plot_html: "<p>SHAP Plot</p>" } });
    });

    // Step 1
    await page.locator('#age').fill('45');
    await page.locator('#gender').selectOption('Male');
    await page.locator('#bmi').fill('24.5');
    await page.locator('#smoking_history').selectOption('never');
    await page.locator('button:has-text("Selanjutnya")').first().click();

    // Step 2
    await page.locator('label').filter({ hasText: 'Tidak' }).nth(0).click();
    await page.locator('label').filter({ hasText: 'Tidak' }).nth(1).click();
    await page.locator('button:has-text("Selanjutnya")').nth(1).click();

    // Step 3
    await page.locator('#hba1c_level').fill('6.5');
    await page.locator('#blood_glucose_level').fill('120');
    await page.locator('button:has-text("Lihat Hasil Risiko")').first().click();

    // Result
    await expect(page.getByText('Hasil Analisis Risiko')).toBeVisible();
    
    // Explain Expand
    await page.getByText('Analisis Mendalam (Explain)').click();
    await expect(page.getByText('Seluruh Faktor Signifikan')).toBeVisible({timeout: 10000});
  });

  // SCENARIO 2: Validation (BMI > 500)
  test('SCENARIO 2: Validation (BMI > 500)', async ({ page }) => {
    // Mock backend to return 422 if BMI > 500
    await page.route('**/api/v1/predict', async route => {
      const json = { detail: [{ loc: ["body", "bmi"], msg: "Input should be less than or equal to 500", type: "less_than_equal" }] };
      await route.fulfill({ status: 422, json });
    });

    // Step 1
    await page.locator('#age').fill('45');
    await page.locator('#gender').selectOption('Male');
    await page.locator('#bmi').fill('600'); // > 500
    await page.locator('#smoking_history').selectOption('never');
    await page.locator('button:has-text("Selanjutnya")').first().click();

    // Step 2
    await page.locator('label').filter({ hasText: 'Tidak' }).nth(0).click();
    await page.locator('label').filter({ hasText: 'Tidak' }).nth(1).click();
    await page.locator('button:has-text("Selanjutnya")').nth(1).click();

    // Step 3
    await page.locator('#hba1c_level').fill('6.5');
    await page.locator('#blood_glucose_level').fill('120');
    await page.locator('button:has-text("Lihat Hasil Risiko")').first().click();

    // Check Error Toast or inline error
    await expect(page.getByText('Masukkan data yang valid.')).toBeVisible();
    await expect(page.getByText('Input should be less than or equal to 500')).toBeVisible();
  });

  // SCENARIO 3: Timeout
  test('SCENARIO 3: Timeout (Delay Jaringan > 3s)', async ({ page }) => {
    await page.route('**/api/v1/predict', async route => {
      // delay for 4 seconds
      await new Promise(resolve => setTimeout(resolve, 4000));
      await route.fulfill({ status: 200, json: { prediction: "LOW", probability: 0.1 } });
    });

    // Step 1
    await page.locator('#age').fill('45');
    await page.locator('#gender').selectOption('Male');
    await page.locator('#bmi').fill('24.5');
    await page.locator('#smoking_history').selectOption('never');
    await page.locator('button:has-text("Selanjutnya")').first().click();

    // Step 2
    await page.locator('label').filter({ hasText: 'Tidak' }).nth(0).click();
    await page.locator('label').filter({ hasText: 'Tidak' }).nth(1).click();
    await page.locator('button:has-text("Selanjutnya")').nth(1).click();

    // Step 3
    await page.locator('#hba1c_level').fill('6.5');
    await page.locator('#blood_glucose_level').fill('120');
    await page.locator('button:has-text("Lihat Hasil Risiko")').first().click();

    // Should show timeout error
    await expect(page.getByText('Periksa koneksi Anda.')).toBeVisible({timeout: 5000});
  });

  // SCENARIO 4: Backend Down
  test('SCENARIO 4: Backend Down (Simulasi API mati 500)', async ({ page }) => {
    await page.route('**/api/v1/predict', async route => {
      await route.fulfill({ status: 500, json: { detail: "Internal Server Error" } });
    });

    // Fast track to predict
    await page.locator('#age').fill('45');
    await page.locator('#gender').selectOption('Male');
    await page.locator('#bmi').fill('24.5');
    await page.locator('#smoking_history').selectOption('never');
    await page.locator('button:has-text("Selanjutnya")').first().click();
    await page.locator('label').filter({ hasText: 'Tidak' }).nth(0).click();
    await page.locator('label').filter({ hasText: 'Tidak' }).nth(1).click();
    await page.locator('button:has-text("Selanjutnya")').nth(1).click();
    await page.locator('#hba1c_level').fill('6.5');
    await page.locator('#blood_glucose_level').fill('120');
    await page.locator('button:has-text("Lihat Hasil Risiko")').first().click();

    await expect(page.getByText('Kami belum bisa memproses sekarang.')).toBeVisible();
  });

  // SCENARIO 5: Explain Fail
  test('SCENARIO 5: Explain Fail (Prediksi berhasil, Explain gagal)', async ({ page }) => {
    // Mock predict to succeed
    await page.route('**/api/v1/predict', async route => {
      await route.fulfill({ status: 200, json: { prediction: "HIGH", probability: 0.87, recommendation: "Konsultasi" } });
    });
    
    // Force explain to fail
    await page.route('**/api/v1/explain', async route => {
      await route.fulfill({ status: 500, json: { detail: "SHAP computation failed" } });
    });

    // Fast track to predict
    await page.locator('#age').fill('45');
    await page.locator('#gender').selectOption('Male');
    await page.locator('#bmi').fill('24.5');
    await page.locator('#smoking_history').selectOption('never');
    await page.locator('button:has-text("Selanjutnya")').first().click();
    await page.locator('label').filter({ hasText: 'Tidak' }).nth(0).click();
    await page.locator('label').filter({ hasText: 'Tidak' }).nth(1).click();
    await page.locator('button:has-text("Selanjutnya")').nth(1).click();
    await page.locator('#hba1c_level').fill('6.5');
    await page.locator('#blood_glucose_level').fill('120');
    await page.locator('button:has-text("Lihat Hasil Risiko")').first().click();

    // Result should be visible
    await expect(page.getByText('Hasil Analisis Risiko')).toBeVisible();

    // Try explain
    await page.getByText('Analisis Mendalam (Explain)').click();
    
    // The layer 2 shouldn't crash.
    await page.waitForTimeout(1000);
    // Ensure no error toast appears for explain, the error string should NOT be visible.
    await expect(page.getByText('Kami belum bisa memproses sekarang.')).toBeHidden();
  });

});
