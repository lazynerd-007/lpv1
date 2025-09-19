<template>
  <div class="card bg-gray-800 shadow-lg mt-8">
    <div class="card-body">
      <h3 class="card-title text-xl mb-4 text-yellow-400">
        <Info class="w-5 h-5" />
        Review Guidelines
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div>
          <h4 class="font-semibold text-green-400 mb-2">✅ Do:</h4>
          <ul class="space-y-1 text-gray-300">
            <li>• Be honest and constructive</li>
            <li>• Focus on the movie's content</li>
            <li>• Respect different opinions</li>
            <li>• Use appropriate language</li>
          </ul>
        </div>
        <div>
          <h4 class="font-semibold text-red-400 mb-2">❌ Don't:</h4>
          <ul class="space-y-1 text-gray-300">
            <li>• Include personal attacks</li>
            <li>• Post spam or irrelevant content</li>
            <li>• Reveal major spoilers without warning</li>
            <li>• Use offensive language</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Info } from 'lucide-vue-next'
</script>