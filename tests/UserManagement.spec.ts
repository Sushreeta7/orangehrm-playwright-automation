import { test } from '@playwright/test';
import { LoginPage } from '../pageobjects/LoginPage';
import { AdminPage } from '../pageobjects/AdminPage';
import { GlobalData } from '../testdata/globalData';

// Get global data instance
const globalData = GlobalData.getInstance();

test.describe('OrangeHRM User Management', () => {
  let loginPage: LoginPage;
  let adminPage: AdminPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    adminPage = new AdminPage(page);

    await loginPage.goto();
    await loginPage.login('Admin', 'admin123');
  });

  // test('Navigate to Admin page', async ({ page }) => {
  //   await adminPage.navigateToAdmin();
  // });

  test('Add a New User, search , edit and then delete', async ({ page }) => {
    test.setTimeout(120000); // Increase timeout to 2 minutes
    await adminPage.navigateToAdmin();
    const username = await adminPage.addUser('Orange Test', 'Password@123');
    await page.waitForTimeout(5000); // Wait for 2 seconds before searching
    await adminPage.searchUser(username);
    await page.waitForTimeout(2000);
    await adminPage.editUser();
    await page.waitForTimeout(2000);
    await adminPage.deleteUser();
    await page.waitForTimeout(2000);
  });


});
