<template>
  <div class="min-h-screen bg-theme-background">
    <!-- Hero Section -->
    <div class="hero min-h-96 bg-gradient-to-r from-yellow-500 to-orange-500">
      <div class="hero-content text-center">
        <div class="max-w-2xl">
          <h1 class="mb-5 text-5xl font-bold text-white">About LemonNPie</h1>
          <p class="mb-5 text-xl text-yellow-100">
            Nigeria's premier platform for authentic Nollywood movie reviews, ratings, and community discussions
          </p>
          <div class="flex justify-center space-x-4 mt-6">
            <div class="badge badge-lg bg-white text-yellow-600 font-semibold">🍋 Fresh Reviews</div>
            <div class="badge badge-lg bg-white text-orange-600 font-semibold">🥧 Quality Content</div>
            <div class="badge badge-lg bg-white text-green-600 font-semibold">🎬 Nollywood Focus</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-12">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- Our Story -->
        <div class="card bg-theme-card shadow-xl">
          <div class="card-body">
            <h2 class="card-title text-3xl mb-4 text-theme-accent">
              <Clapperboard class="w-8 h-8" />
              Our Story
            </h2>
            <p class="text-theme-secondary leading-relaxed mb-4">
              Founded in Lagos in 2024, LemonNPie emerged from a simple observation: Nollywood needed a dedicated space 
              where authentic voices could share honest opinions about our beloved films. We started as film enthusiasts 
              who believed that every movie, from blockbusters to indie gems, deserves thoughtful critique.
            </p>
            <p class="text-theme-secondary leading-relaxed mb-4">
              Our founders, having grown up watching classics like "Living in Bondage" and "Glamour Girls," 
              witnessed Nollywood's evolution firsthand. We created LemonNPie to bridge the gap between traditional 
              film criticism and the vibrant, unfiltered opinions of everyday Nollywood fans.
            </p>
            <p class="text-theme-secondary leading-relaxed mb-4">
              The name "LemonNPie" reflects our philosophy: some films might be sour like lemons (needing improvement), 
              while others are sweet like pie (deserving celebration). Both perspectives are valuable in our community.
            </p>
            <p class="text-theme-secondary leading-relaxed">
              Today, we're proud to serve thousands of Nollywood enthusiasts across Nigeria and the diaspora, 
              fostering discussions that help elevate our industry's storytelling standards.
            </p>
          </div>
        </div>

        <!-- Our Mission -->
        <div class="card bg-theme-card shadow-xl">
          <div class="card-body">
            <h2 class="card-title text-3xl mb-4 text-theme-accent">
              <Target class="w-8 h-8" />
              Our Mission
            </h2>
            <div class="space-y-6">
              <div class="flex items-start space-x-4">
                <div class="badge badge-warning badge-lg text-lg">🍋</div>
                <div>
                  <h3 class="font-semibold text-theme-primary text-lg">Authentic Reviews</h3>
                  <p class="text-theme-secondary">Provide honest, culturally-aware reviews that respect Nollywood's unique storytelling traditions while maintaining critical integrity</p>
                </div>
              </div>
              <div class="flex items-start space-x-4">
                <div class="badge badge-success badge-lg text-lg">🥧</div>
                <div>
                  <h3 class="font-semibold text-theme-primary text-lg">Community Building</h3>
                  <p class="text-theme-secondary">Connect Nollywood enthusiasts from Lagos to London, creating a global community that celebrates Nigerian cinema</p>
                </div>
              </div>
              <div class="flex items-start space-x-4">
                <div class="badge badge-info badge-lg text-lg">🎬</div>
                <div>
                  <h3 class="font-semibold text-theme-primary text-lg">Industry Growth</h3>
                  <p class="text-theme-secondary">Support filmmakers and actors by providing constructive feedback that helps elevate Nollywood's global reputation</p>
                </div>
              </div>
              <div class="flex items-start space-x-4">
                <div class="badge badge-accent badge-lg text-lg">🌍</div>
                <div>
                  <h3 class="font-semibold text-theme-primary text-lg">Cultural Preservation</h3>
                  <p class="text-theme-secondary">Document and celebrate the evolution of Nigerian cinema, preserving our stories for future generations</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Rating System Explanation -->
      <div class="card bg-theme-card shadow-xl mt-12">
        <div class="card-body">
          <h2 class="card-title text-3xl mb-6 text-center text-theme-accent">
            Understanding Our Lemon 🍋 & Pie 🥧 Rating System
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="text-center">
              <div class="text-6xl mb-4">🍋</div>
              <h3 class="text-2xl font-bold text-yellow-600 mb-2">Fresh Lemons</h3>
              <p class="text-theme-secondary mb-4">
                Movies that are sour, disappointing, or need significant improvement. 
                Even the sourest lemon can teach us something about storytelling!
              </p>
              <div class="badge badge-warning mt-2">Rating: 1-4</div>
            </div>
            <div class="text-center">
              <div class="text-6xl mb-4">🍯</div>
              <h3 class="text-2xl font-bold text-orange-500 mb-2">Sweet Honey</h3>
              <p class="text-theme-secondary mb-4">
                Movies that are decent and watchable, with some sweet moments 
                but room for improvement in storytelling or production.
              </p>
              <div class="badge badge-info mt-2">Rating: 5-6</div>
            </div>
            <div class="text-center">
              <div class="text-6xl mb-4">🥧</div>
              <h3 class="text-2xl font-bold text-green-600 mb-2">Delicious Pies</h3>
              <p class="text-theme-secondary mb-4">
                Movies that are sweet, satisfying, and worth watching. 
                These films represent the best of Nollywood storytelling!
              </p>
              <div class="badge badge-success mt-2">Rating: 7-10</div>
            </div>
          </div>
          <div class="mt-8 p-4 bg-theme-background rounded-lg">
            <h4 class="text-lg font-semibold text-theme-primary mb-2">Why This System?</h4>
            <p class="text-theme-secondary">
              Our rating system reflects the Nigerian way of expressing opinions - honest, direct, and with a touch of humor. 
              We believe in constructive criticism that helps our industry grow while celebrating excellence when we see it.
            </p>
          </div>
        </div>
      </div>

      <!-- Platform Features -->
      <div class="card bg-theme-card shadow-xl mt-12">
        <div class="card-body">
          <h2 class="card-title text-3xl mb-6 text-center text-theme-accent">
            <Star class="w-8 h-8" />
            What Makes LemonNPie Special
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="text-center p-4">
              <div class="text-4xl mb-3">🎭</div>
              <h4 class="font-semibold text-theme-primary mb-2">Cultural Context</h4>
              <p class="text-sm text-theme-secondary">Reviews that understand Nigerian culture and storytelling traditions</p>
            </div>
            <div class="text-center p-4">
              <div class="text-4xl mb-3">🌍</div>
              <h4 class="font-semibold text-theme-primary mb-2">Global Community</h4>
              <p class="text-sm text-theme-secondary">Connect with Nollywood fans from Nigeria to the diaspora</p>
            </div>
            <div class="text-center p-4">
              <div class="text-4xl mb-3">📱</div>
              <h4 class="font-semibold text-theme-primary mb-2">Mobile First</h4>
              <p class="text-sm text-theme-secondary">Optimized for mobile viewing and on-the-go movie discovery</p>
            </div>
            <div class="text-center p-4">
              <div class="text-4xl mb-3">🏆</div>
              <h4 class="font-semibold text-theme-primary mb-2">Quality Focus</h4>
              <p class="text-sm text-theme-secondary">Promoting excellence in Nollywood filmmaking and storytelling</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Team Section -->
      <div class="text-center mt-16">
        <h2 class="text-4xl font-bold text-theme-primary mb-8">Meet Our Team</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="card bg-theme-card shadow-lg">
            <div class="card-body items-center text-center">
              <div class="avatar">
                <div class="w-24 rounded-full bg-gradient-to-r from-yellow-400 to-orange-500 flex items-center justify-center">
                  <User class="w-12 h-12 text-white" />
                </div>
              </div>
              <h3 class="card-title text-theme-primary">Adaeze Okafor</h3>
              <p class="text-theme-accent font-medium">Founder & Chief Reviewer</p>
              <p class="text-sm text-theme-secondary mt-2">Film Studies graduate from University of Lagos with 15+ years analyzing Nollywood cinema. Passionate about authentic storytelling.</p>
            </div>
          </div>
          <div class="card bg-theme-card shadow-lg">
            <div class="card-body items-center text-center">
              <div class="avatar">
                <div class="w-24 rounded-full bg-gradient-to-r from-orange-400 to-red-500 flex items-center justify-center">
                  <User class="w-12 h-12 text-white" />
                </div>
              </div>
              <h3 class="card-title text-theme-primary">Emeka Nwankwo</h3>
              <p class="text-theme-accent font-medium">Technical Director</p>
              <p class="text-sm text-theme-secondary mt-2">Software engineer and movie buff building the future of Nollywood film discovery with cutting-edge technology.</p>
            </div>
          </div>
          <div class="card bg-theme-card shadow-lg">
            <div class="card-body items-center text-center">
              <div class="avatar">
                <div class="w-24 rounded-full bg-gradient-to-r from-green-400 to-blue-500 flex items-center justify-center">
                  <User class="w-12 h-12 text-white" />
                </div>
              </div>
              <h3 class="card-title text-theme-primary">Kemi Adebayo</h3>
              <p class="text-theme-accent font-medium">Community Manager</p>
              <p class="text-sm text-theme-secondary mt-2">Digital marketing expert connecting Nollywood fans across continents and fostering meaningful film discussions.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Contact Section -->
      <div class="card bg-theme-card shadow-xl mt-16">
        <div class="card-body text-center">
          <h2 class="card-title text-3xl mb-4 justify-center text-theme-primary">
            <Mail class="w-8 h-8" />
            Get In Touch
          </h2>
          <p class="text-theme-secondary mb-6">
            Have questions, suggestions, or want to collaborate? We'd love to hear from you! 
            Join our growing community of Nollywood enthusiasts.
          </p>
          <div class="flex flex-wrap justify-center gap-4">
            <a href="mailto:hello@lemonnpie.com" class="btn btn-primary">
              <Mail class="w-4 h-4" />
              Email Us
            </a>
            <a href="/contact" class="btn btn-outline btn-primary">
              <MessageCircle class="w-4 h-4" />
              Contact Form
            </a>
            <a href="#" class="btn btn-accent">
              <Users class="w-4 h-4" />
              Join Community
            </a>
          </div>
          <div class="mt-6 text-sm text-theme-tertiary">
            <p>📍 Based in Lagos, Nigeria | Serving Nollywood fans worldwide</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Clapperboard, Target, User, Mail, MessageCircle, Star, Users } from 'lucide-vue-next'

// Set page title
const title = 'About Us - LemonNPie'
if (typeof document !== 'undefined') {
  document.title = title
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>