// Admin page test
export default {
  name: 'Admin Dashboard Tests',
  tests: [
    {
      name: 'Should require authentication for admin access',
      test: async (browser) => {
        // Try to access admin page directly
        await browser.navigate('/admin');
        
        // Should redirect to login page
        await browser.waitForNavigation();
        const currentUrl = await browser.getCurrentUrl();
        browser.assert.contains(currentUrl, '/login', 'Should redirect to login when not authenticated');
      }
    },
    {
      name: 'Should access admin dashboard with admin credentials',
      test: async (browser) => {
        // Login with admin credentials
        await browser.navigate('/login');
        await browser.waitForSelector('form');
        await browser.type('input[type="email"]', 'adebayo@example.com');
        await browser.type('input[type="password"]', 'password123');
        await browser.click('button[type="submit"]');
        
        // Navigate to admin
        await browser.waitForNavigation();
        await browser.navigate('/admin');
        
        // Verify admin dashboard loads
        await browser.waitForSelector('.admin-dashboard');
        const title = await browser.getText('h1');
        browser.assert.contains(title, 'Admin Dashboard');
      }
    },
    {
      name: 'Should maintain admin session when navigating between admin pages',
      test: async (browser) => {
        // Login with admin credentials
        await browser.navigate('/login');
        await browser.waitForSelector('form');
        await browser.type('input[type="email"]', 'adebayo@example.com');
        await browser.type('input[type="password"]', 'password123');
        await browser.click('button[type="submit"]');
        
        // Navigate to admin dashboard
        await browser.waitForNavigation();
        await browser.navigate('/admin');
        await browser.waitForSelector('.admin-dashboard');
        
        // Navigate to users management page within admin
        await browser.click('a[href="/admin/users"]');
        await browser.waitForNavigation();
        await browser.waitForSelector('.admin-users');
        
        // Verify still in admin section (not logged out)
        const currentUrl = await browser.getCurrentUrl();
        browser.assert.contains(currentUrl, '/admin/users', 'Should remain in admin section');
        
        // Navigate to another admin page
        await browser.click('a[href="/admin/movies"]');
        await browser.waitForNavigation();
        await browser.waitForSelector('.admin-movies');
        
        // Verify still in admin section
        const newUrl = await browser.getCurrentUrl();
        browser.assert.contains(newUrl, '/admin/movies', 'Should navigate to movies admin page without logging out');
        
        // Verify admin controls are visible
        const adminControls = await browser.find('.admin-controls');
        browser.assert.exists(adminControls, 'Admin controls should be visible');
      }
    }
  ]
};