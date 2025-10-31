import { Page, expect } from '@playwright/test';
import { GlobalData } from '../testdata/globalData';

export class AdminPage {
  readonly page: Page;
  globalData = GlobalData.getInstance();

  constructor(page: Page) {
    this.page = page;
  }

  async navigateToAdmin() {
    await this.page.getByRole('link', { name: 'Admin' }).click();
    await expect(this.page).toHaveURL(/admin/);
  }

  async addUser(employeeName: string, password: string) {
    await this.page.getByRole('button', { name: 'Add' }).click();
    await this.page.locator('(//div[@class="oxd-select-text-input"])[1]').click();
    await this.page.waitForTimeout(1000);
    await this.page.keyboard.press('ArrowDown');
    await this.page.keyboard.press('Enter');
    await this.page.locator('(//div[@class="oxd-select-text-input"])[2]').click();
    await this.page.waitForTimeout(1000);
    await this.page.keyboard.press('ArrowDown');
    await this.page.keyboard.press('Enter');
    await this.page.locator('input[placeholder="Type for hints..."]').fill('test');
    await this.page.waitForTimeout(2000);
    await this.page.keyboard.press('ArrowDown');
    await this.page.keyboard.press('Enter');
    const generatedUsername = `user_${Date.now()}_${Math.floor(Math.random() * 10000)}`;
    this.globalData.setValue('lastCreatedUsername', generatedUsername);
    await this.page.locator('(//input[@autocomplete="off"])[1]').fill(generatedUsername);
    await this.page.locator('input[type="password"]').first().fill(password);
    await this.page.locator('input[type="password"]').last().fill(password);
    await this.page.waitForTimeout(1000);
    await this.page.locator('//button[@type="submit"]').click();
    return generatedUsername;
  }

  async searchUser(username: string) {
    // const button = this.page.locator('//div[@class="oxd-table-filter-header-options"]//button[@type="button"]');
    // await button.waitFor();
    // const element = await this.page.$('//div[@class="oxd-table-filter-header-options"]//button[@type="button"]'); 
    // if (element) {
    //    await element.evaluate((el) => (el as HTMLElement).click());
    // }
    await this.page.locator('//div[@class="oxd-form-row"]//input[@class="oxd-input oxd-input--active"]').fill(username);
    await this.page.waitForTimeout(1000);
    await this.page.locator('//button[@type="submit"]').click();
    await this.page.waitForTimeout(2000);
    const locator = await this.page.locator('//div[@class="orangehrm-horizontal-padding orangehrm-vertical-padding"]/span');
    await expect(locator).toHaveText('(1) Record Found');
  }

  async editUser() {
    await this.page.locator('//i[@class="oxd-icon bi-pencil-fill"]').waitFor();
    await this.page.locator('//i[@class="oxd-icon bi-pencil-fill"]').click();
    await this.page.waitForTimeout(2000);
    await this.page.locator('(//div[@class="oxd-select-text-input"])[1]').click();
    await this.page.waitForTimeout(1000);
    await this.page.locator('//div[@class="oxd-select-option"]/span').waitFor();
    await this.page.locator('//div[@class="oxd-select-option"]/span').click();
    // await this.page.keyboard.press('ArrowDown');
    // await this.page.keyboard.press('Enter');
    await this.page.waitForTimeout(1000);
    await this.page.locator('//button[@type="submit"]').click();

  }

  async deleteUser() {
    await this.page.locator('.oxd-checkbox-input').first().click();
    await this.page.locator('button:has-text("Delete Selected")').click();
    await this.page.locator('button:has-text("Yes, Delete")').click();
    await expect(this.page.locator('div.oxd-toast')).toContainText('Successfully Deleted');
  }
}
