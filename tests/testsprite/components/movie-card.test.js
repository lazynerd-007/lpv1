// Movie Card component test
export default {
  name: 'Movie Card Component Tests',
  tests: [
    {
      name: 'Should display movie card with correct information',
      test: async (browser) => {
        await browser.navigate('/');
        await browser.waitForSelector('.movie-card');
        
        // Check movie card elements
        await browser.assertElementExists('.movie-card img', 'Movie poster should be present');
        await browser.assertElementExists('.movie-card .movie-title', 'Movie title should be present');
        await browser.assertElementExists('.movie-card .lemon-pie-rating', 'Rating should be present');
      }
    }
  ]
};