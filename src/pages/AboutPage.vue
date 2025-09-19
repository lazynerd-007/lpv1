<template>
  <div class="min-h-screen bg-yellow-50">
    <!-- Hero Section -->
    <div class="hero min-h-96 bg-yellow-500">
      <div class="hero-content text-center">
        <div class="max-w-md">
          <h1 class="mb-5 text-5xl font-bold text-white">About LemonNPie</h1>
          <p class="mb-5 text-xl text-yellow-100">
            Your ultimate destination for Nollywood movie reviews and ratings
          </p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-12">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- Our Story -->
        <div class="card bg-white shadow-xl">
          <div class="card-body">
            <h2 class="card-title text-3xl mb-4 text-orange-600">
              <Clapperboard class="w-8 h-8" />
              Our Story
            </h2>
            <p class="text-gray-700 leading-relaxed mb-4">
              LemonNPie was born from a passion for Nollywood cinema and the need for a dedicated platform 
              where fans can discover, review, and celebrate the rich storytelling tradition of Nigerian films.
            </p>
            <p class="text-gray-700 leading-relaxed mb-4">
              We believe every movie deserves honest feedback, whether it's a fresh "Lemon" that needs improvement 
              or a delicious "Pie" that deserves all the praise.
            </p>
            <p class="text-gray-700 leading-relaxed">
              Our unique rating system reflects the vibrant culture and honest opinions of the Nollywood community.
            </p>
          </div>
        </div>

        <!-- Our Mission -->
        <div class="card bg-white shadow-xl">
          <div class="card-body">
            <h2 class="card-title text-3xl mb-4 text-yellow-600">
              <Target class="w-8 h-8" />
              Our Mission
            </h2>
            <div class="space-y-4">
              <div class="flex items-start space-x-3">
                <div class="badge badge-warning badge-lg">🍋</div>
                <div>
                  <h3 class="font-semibold text-gray-800">Honest Reviews</h3>
                  <p class="text-gray-600">Provide authentic, unbiased reviews of Nollywood films</p>
                </div>
              </div>
              <div class="flex items-start space-x-3">
                <div class="badge badge-success badge-lg">🥧</div>
                <div>
                  <h3 class="font-semibold text-gray-800">Community Building</h3>
                  <p class="text-gray-600">Connect Nollywood enthusiasts worldwide</p>
                </div>
              </div>
              <div class="flex items-start space-x-3">
                <div class="badge badge-info badge-lg">🎬</div>
                <div>
                  <h3 class="font-semibold text-gray-800">Industry Support</h3>
                  <p class="text-gray-600">Support and promote quality Nollywood productions</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Rating System Explanation -->
      <div class="card bg-yellow-100 shadow-xl mt-12">
        <div class="card-body">
          <h2 class="card-title text-3xl mb-6 text-center text-orange-700">
            Understanding Our Lemon 🍋 & Pie 🥧 Rating System
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="text-center">
              <div class="text-6xl mb-4">🍋</div>
              <h3 class="text-2xl font-bold text-yellow-600 mb-2">Fresh Lemons</h3>
              <p class="text-gray-700">
                Movies that are sour, disappointing, or need significant improvement. 
                Even the sourest lemon can teach us something!
              </p>
              <div class="badge badge-warning mt-2">Rating: 1-4</div>
            </div>
            <div class="text-center">
              <div class="text-6xl mb-4">🥧</div>
              <h3 class="text-2xl font-bold text-orange-600 mb-2">Delicious Pies</h3>
              <p class="text-gray-700">
                Movies that are sweet, satisfying, and worth watching. 
                These films represent the best of Nollywood storytelling!
              </p>
              <div class="badge badge-success mt-2">Rating: 6-10</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Team Section -->
      <div class="text-center mt-16">
        <h2 class="text-4xl font-bold text-gray-800 mb-8">Meet Our Team</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="card bg-white shadow-lg">
            <div class="card-body items-center text-center">
              <div class="avatar">
                <div class="w-24 rounded-full bg-gradient-to-r from-yellow-400 to-orange-500 flex items-center justify-center">
                  <User class="w-12 h-12 text-white" />
                </div>
              </div>
              <h3 class="card-title">Adaeze Okafor</h3>
              <p class="text-gray-600">Founder & Chief Reviewer</p>
              <p class="text-sm text-gray-500">Nollywood enthusiast with 15+ years of film analysis experience</p>
            </div>
          </div>
          <div class="card bg-white shadow-lg">
            <div class="card-body items-center text-center">
              <div class="avatar">
                <div class="w-24 rounded-full bg-gradient-to-r from-orange-400 to-red-500 flex items-center justify-center">
                  <User class="w-12 h-12 text-white" />
                </div>
              </div>
              <h3 class="card-title">Emeka Nwankwo</h3>
              <p class="text-gray-600">Technical Director</p>
              <p class="text-sm text-gray-500">Building the future of Nollywood film discovery</p>
            </div>
          </div>
          <div class="card bg-white shadow-lg">
            <div class="card-body items-center text-center">
              <div class="avatar">
                <div class="w-24 rounded-full bg-gradient-to-r from-green-400 to-blue-500 flex items-center justify-center">
                  <User class="w-12 h-12 text-white" />
                </div>
              </div>
              <h3 class="card-title">Kemi Adebayo</h3>
              <p class="text-gray-600">Community Manager</p>
              <p class="text-sm text-gray-500">Connecting Nollywood fans across the globe</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Contact Section -->
      <div class="card bg-white shadow-xl mt-16">
        <div class="card-body text-center">
          <h2 class="card-title text-3xl mb-4 justify-center text-gray-800">
            <Mail class="w-8 h-8" />
            Get In Touch
          </h2>
          <p class="text-gray-600 mb-6">
            Have questions, suggestions, or want to collaborate? We'd love to hear from you!
          </p>
          <div class="flex flex-wrap justify-center gap-4">
            <a href="mailto:hello@lemonnpie.com" class="btn btn-primary">
              <Mail class="w-4 h-4" />
              Email Us
            </a>
            <a href="#" class="btn btn-outline btn-primary">
              <MessageCircle class="w-4 h-4" />
              Join Our Community
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Clapperboard, Target, User, Mail, MessageCircle } from 'lucide-vue-next'

// Set page title
const title = 'About Us - LemonNPie'
if (typeof document !== 'undefined') {
  document.title = title
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>