# Playwright Test Automation Framework

This project demonstrates automated testing of the OrangeHRM application using Playwright with TypeScript.

## Project Structure
```
PlaywrightDemo/
├── pageobjects/          # Page Object Model classes
│   ├── LoginPage.ts      # Login page interactions
│   └── AdminPage.ts      # Admin page interactions
├── tests/                # Test files
│   └── UserManagement.spec.ts  # User management test scenarios
├── testdata/            # Test data and utilities
│   └── globalData.ts    # Global data singleton for sharing data between tests
├── playwright.config.ts # Playwright configuration
├── package.json         # Project dependencies
└── tsconfig.json       # TypeScript configuration
```

## Setup and Configuration

### Prerequisites
- Node.js installed (v14 or later)
- npm (Node Package Manager)

### Installation
1. Clone the repository
2. Install dependencies:
```bash
npm install
```
3. Install Playwright browsers:
```bash
npx playwright install
```

### Configuration Files

#### playwright.config.ts
```typescript
{
  testDir: './tests',           // Directory containing test files
  timeout: 30000,              // Global timeout for tests
  use: {
    headless: false,           // Run tests in headed mode
    viewport: null,            // Use default viewport
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
    launchOptions: {
      slowMo: 1000,           // Slow down execution
      args: ['--start-maximized'] // Start browser maximized
    }
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    }
  ]
}
```

## Framework Features

### Page Object Model
- Separate page classes for different sections of the application
- Reusable methods for common actions
- Type-safe locators and methods

### Global Data Management
The framework includes a GlobalData singleton class for sharing data between test cases:
```typescript
const globalData = GlobalData.getInstance();
globalData.setValue('key', value);
const value = globalData.getValue('key');
```

### Test Structure
Tests are organized using the page object model pattern and include:
- Login functionality
- User Management operations (Create, Search, Edit, Delete)
- Automatic username generation for unique test data

## Running Tests

### Run all tests
```bash
npx playwright test
```

### Run tests with debug mode
```bash
npx playwright test --debug
```

### Run a specific test file
```bash
npx playwright test tests/UserManagement.spec.ts
```

### View test report
```bash
npx playwright show-report
```

## Test Cases
The framework includes tests for:
1. User login
2. Navigation to Admin page
3. Creating new users
4. Searching for users
5. Editing user details
6. Deleting users

## Best Practices Implemented
1. Page Object Model for better maintainability
2. Global data management for sharing test data
3. Explicit waits for better reliability
4. JavaScript-based element interactions for stability
5. Timeout management for longer operations
6. Screenshot capture on test failure
7. Proper error handling and verification steps

## Maintenance
1. Update dependencies:
```bash
npm update
```
2. Update Playwright:
```bash
npm install -D @playwright/test@latest
```

## Contributing
1. Follow the existing code structure
2. Add appropriate comments
3. Update README.md with any new features
4. Ensure all tests pass before submitting changes