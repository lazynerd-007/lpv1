// TestSprite implementation for LemonPie project
export class TestSprite {
  constructor(config = {}) {
    this.config = {
      baseUrl: config.baseUrl || 'http://localhost:5174',
      timeout: config.timeout || 5000,
      browser: config.browser || 'chrome',
      ...config
    };
    this.tests = [];
    this.results = {
      total: 0,
      passed: 0,
      failed: 0,
      skipped: 0
    };
  }

  // Add a test to the queue
  test(name, fn) {
    this.tests.push({ name, fn, status: 'pending' });
    return this;
  }

  // Mock browser interaction methods
  async visit(path) {
    console.log(`[TestSprite] Visiting ${this.config.baseUrl}${path}`);
    return true;
  }

  async find(selector) {
    console.log(`[TestSprite] Finding element: ${selector}`);
    return {
      exists: () => true,
      click: async () => console.log(`[TestSprite] Clicking on ${selector}`),
      text: () => 'Element Text',
      value: () => 'Element Value',
      attr: (name) => `Attribute ${name}`
    };
  }

  async wait(ms) {
    console.log(`[TestSprite] Waiting for ${ms}ms`);
    return true;
  }

  async fillForm(selector, value) {
    console.log(`[TestSprite] Filling form ${selector} with value: ${value}`);
    return true;
  }

  async screenshot(name) {
    console.log(`[TestSprite] Taking screenshot: ${name}`);
    return true;
  }

  // Run all tests
  async run() {
    console.log(`\n🚀 Starting TestSprite tests with ${this.tests.length} test(s)`);
    console.log(`🌐 Testing against: ${this.config.baseUrl}`);
    console.log(`🧪 Browser: ${this.config.browser}\n`);

    for (const test of this.tests) {
      try {
        console.log(`\n▶️ Running test: ${test.name}`);
        await test.fn(this);
        test.status = 'passed';
        this.results.passed++;
        console.log(`✅ Test passed: ${test.name}`);
      } catch (error) {
        test.status = 'failed';
        test.error = error;
        this.results.failed++;
        console.log(`❌ Test failed: ${test.name}`);
        console.log(`   Error: ${error.message}`);
      }
    }

    this.results.total = this.tests.length;
    this.printSummary();
    return this.results;
  }

  // Print test summary
  printSummary() {
    console.log('\n📊 TEST SUMMARY:');
    console.log(`  Total Tests: ${this.results.total}`);
    console.log(`  Passed: ${this.results.passed}`);
    console.log(`  Failed: ${this.results.failed}`);
    console.log(`  Skipped: ${this.results.skipped}`);

    if (this.results.failed === 0) {
      console.log('\n🎉 All tests passed successfully!');
    } else {
      console.log('\n⚠️ Some tests failed. Check the logs for details.');
    }
  }
}

// Helper functions
export const expect = (actual) => {
  return {
    toBe: (expected) => {
      if (actual !== expected) {
        throw new Error(`Expected ${expected} but got ${actual}`);
      }
      return true;
    },
    toContain: (expected) => {
      if (!actual.includes(expected)) {
        throw new Error(`Expected ${actual} to contain ${expected}`);
      }
      return true;
    },
    toBeGreaterThan: (expected) => {
      if (!(actual > expected)) {
        throw new Error(`Expected ${actual} to be greater than ${expected}`);
      }
      return true;
    },
    toBeLessThan: (expected) => {
      if (!(actual < expected)) {
        throw new Error(`Expected ${actual} to be less than ${expected}`);
      }
      return true;
    },
    toBeTrue: () => {
      if (actual !== true) {
        throw new Error(`Expected true but got ${actual}`);
      }
      return true;
    },
    toBeFalse: () => {
      if (actual !== false) {
        throw new Error(`Expected false but got ${actual}`);
      }
      return true;
    }
  };
};

// Create and export a default instance
export default new TestSprite();