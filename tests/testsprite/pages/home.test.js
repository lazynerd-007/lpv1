// Home page test
export default {
  name: 'Home Page Tests',
  tests: [
    {
      name: 'Should load home page correctly',
      test: async (browser) => {
        await browser.navigate('/');
        await browser.waitForSelector('.home-container');
        
        // Verify key elements are present
        const title = await browser.getText('h1');
        browser.assert.contains(title, 'LemonPie');
        
        // Check for movie cards
        const movieCards = await browser.findElements('.movie-card');
        browser.assert.greaterThan(movieCards.length, 0, 'Should display movie cards');
        
        // Check navigation elements
        await browser.assertElementExists('.app-header', 'Header should be present');
        await browser.assertElementExists('.app-footer', 'Footer should be present');
      }
    },
    {
      name: 'Should navigate to movie details when clicking a movie card',
      test: async (browser) => {
        await browser.navigate('/');
        await browser.waitForSelector('.movie-card');
        
        // Click the first movie card
        await browser.click('.movie-card:first-child');
        
        // Verify navigation to movie details page
        await browser.waitForNavigation();
        const currentUrl = await browser.getCurrentUrl();
        browser.assert.contains(currentUrl, '/movie/');
      }
    }
  ]
};