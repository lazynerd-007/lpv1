const config = {
  // Base URL for your application
  baseUrl: 'http://localhost:5174',
  
  // Test timeout in milliseconds
  timeout: 30000,
  
  // Browser settings
  browser: {
    headless: false,
    width: 1280,
    height: 720
  },
  
  // Test directories
  testDir: './tests/testsprite',
  
  // Screenshot settings
  screenshots: {
    enabled: true,
    path: './tests/testsprite/screenshots'
  },
  
  // Reporting settings
  reports: {
    outputDir: './tests/testsprite/reports',
    html: true,
    json: true
  }
};

export default config;