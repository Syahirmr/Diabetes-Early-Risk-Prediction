# Frontend E2E Validation Report

## Browser Flow Execution
- Landing: Validated
- Assessment (Double Submit Prevents): Validated
- Submit (State Recovery): Validated
- Result: Validated
- Explain Expand: Validated
- Export: Validated

## Logs
```text
Running 5 tests using 1 worker

  ok 1 tests\frontend\test_ui_flow.spec.ts:16:7 â€º Phase 5: Integration & UI Resilience â€º SCENARIO 1: Success (Happy Path E2E) (2.8s)
  x  2 tests\frontend\test_ui_flow.spec.ts:51:7 â€º Phase 5: Integration & UI Resilience â€º SCENARIO 2: Validation (BMI > 500) (7.2s)
  x  3 tests\frontend\test_ui_flow.spec.ts:81:7 â€º Phase 5: Integration & UI Resilience â€º SCENARIO 3: Timeout (Delay Jaringan > 3s) (7.5s)
  x  4 tests\frontend\test_ui_flow.spec.ts:110:7 â€º Phase 5: Integration & UI Resilience â€º SCENARIO 4: Backend Down (Simulasi API mati 500) (7.4s)
  ok 5 tests\frontend\test_ui_flow.spec.ts:132:7 â€º Phase 5: Integration & UI Resilience â€º SCENARIO 5: Explain Fail (Prediksi berhasil, Explain gagal) (3.7s)


  1) tests\frontend\test_ui_flow.spec.ts:51:7 â€º Phase 5: Integration & UI Resilience â€º SCENARIO 2: Validation (BMI > 500) 

    Error: expect(locator).toBeVisible() failed

    Locator:  getByText('Input should be less than or equal to 500')
    Expected: visible
    Received: hidden
    Timeout:  5000ms

    Call log:
      - Expect "toBeVisible" with timeout 5000ms
      - waiting for getByText('Input should be less than or equal to 500')
        13 Ã— locator resolved to <p x-show="validationErrors.bmi" x-text="validationErrors.bmi" class="text-xs text-red-500 mt-1">Input should be less than or equal to 500</p>
           - unexpected value "hidden"


      75 |     // Check Error Toast or inline error
      76 |     await expect(page.getByText('Masukkan data yang valid.')).toBeVisible();
    > 77 |     await expect(page.getByText('Input should be less than or equal to 500')).toBeVisible();
         |                                                                               ^
      78 |   });
      79 |
      80 |   // SCENARIO 3: Timeout
        at D:\SEMESTER 6\Pembelajaran Mesin\UAS\UAS_MachineLearning_Diabetes\tests\frontend\test_ui_flow.spec.ts:77:79

    Error Context: test-results\tests-frontend-test_ui_flo-a4b0f-NARIO-2-Validation-BMI-500-\error-context.md

  2) tests\frontend\test_ui_flow.spec.ts:81:7 â€º Phase 5: Integration & UI Resilience â€º SCENARIO 3: Timeout (Delay Jaringan > 3s) 

    Error: expect(locator).toBeVisible() failed

    Locator: getByText('Periksa koneksi Anda.')
    Expected: visible
    Timeout: 5000ms
    Error: element(s) not found

    Call log:
      - Expect "toBeVisible" with timeout 5000ms
      - waiting for getByText('Periksa koneksi Anda.')


      104 |
      105 |     // Should show timeout error
    > 106 |     await expect(page.getByText('Periksa koneksi Anda.')).toBeVisible({timeout: 5000});
          |                                                           ^
      107 |   });
      108 |
      109 |   // SCENARIO 4: Backend Down
        at D:\SEMESTER 6\Pembelajaran Mesin\UAS\UAS_MachineLearning_Diabetes\tests\frontend\test_ui_flow.spec.ts:106:59

    Error Context: test-results\tests-frontend-test_ui_flo-7b500--Timeout-Delay-Jaringan-3s-\error-context.md

  3) tests\frontend\test_ui_flow.spec.ts:110:7 â€º Phase 5: Integration & UI Resilience â€º SCENARIO 4: Backend Down (Simulasi API mati 500) 

    Error: expect(locator).toBeVisible() failed

    Locator: getByText('Kami belum bisa memproses sekarang.')
    Expected: visible
    Timeout: 5000ms
    Error: element(s) not found

    Call log:
      - Expect "toBeVisible" with timeout 5000ms
      - waiting for getByText('Kami belum bisa memproses sekarang.')


      126 |     await page.locator('button:has-text("Lihat Hasil Risiko")').first().click();
      127 |
    > 128 |     await expect(page.getByText('Kami belum bisa memproses sekarang.')).toBeVisible();
          |                                                                         ^
      129 |   });
      130 |
      131 |   // SCENARIO 5: Explain Fail
        at D:\SEMESTER 6\Pembelajaran Mesin\UAS\UAS_MachineLearning_Diabetes\tests\frontend\test_ui_flow.spec.ts:128:73

    Error Context: test-results\tests-frontend-test_ui_flo-62db1-Down-Simulasi-API-mati-500-\error-context.md

  3 failed
    tests\frontend\test_ui_flow.spec.ts:51:7 â€º Phase 5: Integration & UI Resilience â€º SCENARIO 2: Validation (BMI > 500) 
    tests\frontend\test_ui_flow.spec.ts:81:7 â€º Phase 5: Integration & UI Resilience â€º SCENARIO 3: Timeout (Delay Jaringan > 3s) 
    tests\frontend\test_ui_flow.spec.ts:110:7 â€º Phase 5: Integration & UI Resilience â€º SCENARIO 4: Backend Down (Simulasi API mati 500) 
  2 passed (44.1s)

```

## Status
FAIL
