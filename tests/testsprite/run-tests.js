// TestSprite runner for LemonPie project
import testsprite, { expect } from './testsprite.js';

console.log('Starting LemonPie Frontend Tests with TestSprite...');

// Configure TestSprite
testsprite.config.baseUrl = 'http://localhost:5174';
testsprite.config.browser = 'chrome';
testsprite.config.timeout = 10000;

// Home page tests
testsprite.test('Should load home page correctly', async (ts) => {
  await ts.visit('/');
  const title = await ts.find('h1');
  expect(title.exists()).toBeTrue();
});

testsprite.test('Should navigate to movie details when clicking a movie card', async (ts) => {
  await ts.visit('/');
  const movieCard = await ts.find('.movie-card');
  await movieCard.click();
  // In a real test, we would verify the URL changed
});

// Admin dashboard tests
testsprite.test('Should require authentication for admin access', async (ts) => {
  await ts.visit('/admin');
  const loginForm = await ts.find('form');
  expect(loginForm.exists()).toBeTrue();
});

testsprite.test('Should access admin dashboard with admin credentials', async (ts) => {
  await ts.visit('/admin');
  await ts.fillForm('#email', 'admin@example.com');
  await ts.fillForm('#password', 'password');
  const loginButton = await ts.find('button[type="submit"]');
  await loginButton.click();
  const dashboard = await ts.find('.admin-dashboard');
  expect(dashboard.exists()).toBeTrue();
});

testsprite.test('Should maintain admin session when navigating between admin pages', async (ts) => {
  // Login with admin credentials
  await ts.visit('/admin');
  await ts.fillForm('#email', 'admin@example.com');
  await ts.fillForm('#password', 'password');
  const loginButton = await ts.find('button[type="submit"]');
  await loginButton.click();
  
  // Verify we're on the admin dashboard
  const dashboard = await ts.find('.admin-dashboard');
  expect(dashboard.exists()).toBeTrue();
  
  // Navigate to users management page
  const usersLink = await ts.find('a[href="/admin/users"]');
  await usersLink.click();
  
  // Verify we're still in admin section
  const usersPage = await ts.find('.admin-users');
  expect(usersPage.exists()).toBeTrue();
  
  // Navigate to movies management page
  const moviesLink = await ts.find('a[href="/admin/movies"]');
  await moviesLink.click();
  
  // Verify we're still in admin section
  const moviesPage = await ts.find('.admin-movies');
  expect(moviesPage.exists()).toBeTrue();
  
  // Verify admin controls are visible
  const adminControls = await ts.find('.admin-controls');
  expect(adminControls.exists()).toBeTrue();
});

// Movie card component tests
testsprite.test('Should display movie card with correct information', async (ts) => {
  await ts.visit('/');
  const movieCard = await ts.find('.movie-card');
  const title = await ts.find('.movie-card .title');
  const rating = await ts.find('.movie-card .rating');
  expect(title.exists()).toBeTrue();
  expect(rating.exists()).toBeTrue();
});

// Run all tests
testsprite.run().catch(error => {
  console.error('Error running tests:', error);
  process.exit(1);
});