import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 1,
  reporter: 'html',

  use: {
    trace: 'on-first-retry',
    actionTimeout: 60000,
    navigationTimeout: 60000,
    baseURL: 'https://opensource-demo.orangehrmlive.com',
    screenshot: 'only-on-failure',
    headless: false,
    viewport: null,
    launchOptions: {
      slowMo: 1000,
      args: [
        '--start-maximized',
        '--window-size=1920,1080'
      ]
    },
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    //{
      //name: 'firefox',
      //use: { ...devices['Desktop Firefox'] },
    //},
    //{
      //name: 'webkit',
      //use: { ...devices['Desktop Safari'] },
    //},
  ],
});
