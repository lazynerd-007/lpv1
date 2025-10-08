<script setup lang="ts">
import { ref, computed } from 'vue'
import { AlertTriangle, Star, Eye, EyeOff, Info } from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'
import { useAuthStore } from '@/stores/authStore'
import { useLanguage, type SupportedLanguage } from '@/composables/useLanguage'
import { useResponsive, responsiveConfigs } from '@/composables/useResponsive'
import LemonPieRating from './LemonPieRating.vue'
import LanguageSelector from '@/components/ui/LanguageSelector.vue'
import type { Review } from '@/data/mockMovies'

interface Props {
  movieId: string
  movieTitle?: string
  editReview?: Review | null
}

const props = withDefaults(defineProps<Props>(), {
  movieTitle: '',
  editReview: null
})

const emit = defineEmits<{
  submit: [review: Omit<Review, 'id' | 'createdAt'>]
  cancel: []
}>()

const movieStore = useMovieStore()
const authStore = useAuthStore()
const { currentLanguage, t } = useLanguage()
const { 
  isMobile, 
  isTablet, 
  isTouchDevice,
  getResponsiveClasses,
  getResponsiveFontSize,
  getResponsiveSpacing,
  getTouchFriendlySize
} = useResponsive()

// Form data
const selectedLanguage = ref<SupportedLanguage>('en')
const formData = ref({
  reviewText: props.editReview?.reviewText || '',
  lemonPieRating: props.editReview?.lemonPieRating || 5,
  spoilerWarning: props.editReview?.spoilerWarning || false,
  
  // Category ratings
  storyRating: props.editReview?.storyRating || 5,
  actingRating: props.editReview?.actingRating || 5,
  cinematographyRating: props.editReview?.cinematographyRating || 5,
  productionQualityRating: props.editReview?.productionQualityRating || 5,
  culturalAuthenticityRating: props.editReview?.culturalAuthenticityRating || 5,
  
  // Nollywood tags
  nollywoodTags: props.editReview?.nollywoodTags || []
})

// Form state
const isSubmitting = ref(false)
const showSpoilerPreview = ref(false)
const errors = ref<Record<string, string>>({})

// Available Nollywood tags
const availableTags = [
  'Traditional Culture',
  'Modern Nigeria',
  'Comedy',
  'Drama',
  'Romance',
  'Action',
  'Family Values',
  'Social Issues',
  'Historical',
  'Urban Life',
  'Village Life',
  'Music & Dance',
  'Religion & Spirituality',
  'Politics',
  'Business & Money'
]

// Validation
const isFormValid = computed(() => {
  return formData.value.reviewText.trim().length >= 10 &&
         formData.value.lemonPieRating >= 1 &&
         formData.value.lemonPieRating <= 10
})

const handleLanguageChange = (language: SupportedLanguage) => {
  selectedLanguage.value = language
}

const validateForm = () => {
  errors.value = {}
  
  if (!formData.value.lemonPieRating) {
    errors.value.lemonPieRating = t('ratingRequired')
  }
  
  if (!formData.value.reviewText.trim()) {
    errors.value.reviewText = t('reviewRequired')
  } else if (formData.value.reviewText.trim().length < 10) {
    errors.value.reviewText = t('reviewTooShort')
  }
  
  return Object.keys(errors.value).length === 0
}

// Tag management
const toggleTag = (tag: string) => {
  const index = formData.value.nollywoodTags.indexOf(tag)
  if (index > -1) {
    formData.value.nollywoodTags.splice(index, 1)
  } else if (formData.value.nollywoodTags.length < 5) {
    formData.value.nollywoodTags.push(tag)
  }
}

const isTagSelected = (tag: string) => {
  return formData.value.nollywoodTags.includes(tag)
}

// Form submission
const submitReview = async () => {
  if (!validateForm() || !authStore.currentUserId) return
  
  isSubmitting.value = true
  
  try {
    const reviewData: Omit<Review, 'id' | 'createdAt'> = {
      userId: authStore.currentUserId,
      movieId: props.movieId,
      userName: authStore.user?.name || 'Anonymous',
      userAvatar: authStore.user?.avatar || '',
      lemonPieRating: formData.value.lemonPieRating,
      reviewText: formData.value.reviewText.trim(),
      reviewLanguage: selectedLanguage.value,
      spoilerWarning: formData.value.spoilerWarning,
      
      // Category ratings
      storyRating: formData.value.storyRating,
      actingRating: formData.value.actingRating,
      cinematographyRating: formData.value.cinematographyRating,
      productionQualityRating: formData.value.productionQualityRating,
      culturalAuthenticityRating: formData.value.culturalAuthenticityRating,
      
      nollywoodTags: formData.value.nollywoodTags,
      
      // Initialize voting data
      helpfulVotes: 0,
      unhelpfulVotes: 0,
      userVotes: {},
      helpfulnessScore: 0,
      
      isVerifiedCritic: authStore.isVerifiedCritic
    }
    
    emit('submit', reviewData)
  } catch (error) {
    console.error('Error submitting review:', error)
  } finally {
    isSubmitting.value = false
  }
}

const cancelReview = () => {
  emit('cancel')
}

// Character count for review text
const characterCount = computed(() => formData.value.reviewText.length)
const characterLimit = 2000
</script>

<template>
  <div :class="[
    'bg-theme-card rounded-lg shadow-lg',
    getResponsiveSpacing(responsiveConfigs.cardSpacing)
  ]">
    <h3 :class="[
      'font-semibold text-theme-text',
      getResponsiveFontSize({ base: 'text-lg', sm: 'text-xl', md: 'text-2xl' }),
      getResponsiveSpacing({ base: 'mb-4', sm: 'mb-6' })
    ]">
      {{ editReview ? 'Edit Review' : 'Write a Review' }}
      <span v-if="movieTitle" :class="[
        'text-theme-secondary font-normal block',
        getResponsiveFontSize({ base: 'text-sm', sm: 'text-base' }),
        { 'mt-1': isMobile }
      ]"> 
        {{ isMobile ? '' : 'for ' }}{{ movieTitle }}
      </span>
    </h3>
    
    <form @submit.prevent="submitReview" :class="[
      getResponsiveSpacing({ base: 'space-y-4', sm: 'space-y-6' })
    ]">
      <!-- Language Selection -->
      <LanguageSelector 
        v-model="selectedLanguage"
        @change="handleLanguageChange"
      />
      
      <!-- Overall Rating -->
      <div>
        <label :class="[
          'block font-medium text-theme-text',
          getResponsiveFontSize({ base: 'text-sm', md: 'text-base' }),
          getResponsiveSpacing({ base: 'mb-2', sm: 'mb-3' })
        ]">
          {{ t('overallRating') }} <span class="text-red-500">*</span>
        </label>
        <div :class="[
          'flex items-center',
          isMobile ? 'flex-col gap-3' : 'gap-4'
        ]">
          <LemonPieRating 
            v-model:rating="formData.lemonPieRating"
            :editable="true"
            :size="isMobile ? 'md' : 'lg'"
          />
          <span :class="[
            'text-theme-text font-semibold',
            getResponsiveFontSize({ base: 'text-base', sm: 'text-lg' })
          ]">{{ formData.lemonPieRating }}/10</span>
        </div>
        <p v-if="errors.lemonPieRating" class="text-red-500 text-sm mt-1">{{ errors.lemonPieRating }}</p>
      </div>
      
      <!-- Category Ratings -->
      <div :class="[
        'grid gap-4',
        getResponsiveClasses({ xs: 'grid-cols-1', md: 'grid-cols-2' })
      ]">
        <!-- Story Rating -->
        <div>
          <label :class="[
            'block font-medium text-theme-text',
            getResponsiveFontSize({ base: 'text-sm', md: 'text-base' }),
            getResponsiveSpacing({ base: 'mb-2', sm: 'mb-3' })
          ]">{{ t('storyRating') }}</label>
          <div class="flex items-center gap-2">
            <input 
              v-model.number="formData.storyRating"
              type="range" 
              min="1" 
              max="10" 
              step="0.5"
              :class="[
                'flex-1 bg-gray-200 rounded-lg appearance-none cursor-pointer slider',
                getTouchFriendlySize('h-2', 'h-3')
              ]"
            >
            <span :class="[
              'text-theme-text font-medium',
              isMobile ? 'w-10 text-sm' : 'w-12'
            ]">{{ formData.storyRating }}/10</span>
          </div>
        </div>
        
        <!-- Acting Rating -->
        <div>
          <label :class="[
            'block font-medium text-theme-text',
            getResponsiveFontSize({ base: 'text-sm', md: 'text-base' }),
            getResponsiveSpacing({ base: 'mb-2', sm: 'mb-3' })
          ]">{{ t('actingRating') }}</label>
          <div class="flex items-center gap-2">
            <input 
              v-model.number="formData.actingRating"
              type="range" 
              min="1" 
              max="10" 
              step="0.5"
              :class="[
                'flex-1 bg-gray-200 rounded-lg appearance-none cursor-pointer slider',
                getTouchFriendlySize('h-2', 'h-3')
              ]"
            >
            <span :class="[
              'text-theme-text font-medium',
              isMobile ? 'w-10 text-sm' : 'w-12'
            ]">{{ formData.actingRating }}/10</span>
          </div>
        </div>
        
        <!-- Cinematography Rating -->
        <div>
          <label :class="[
            'block font-medium text-theme-text',
            getResponsiveFontSize({ base: 'text-sm', md: 'text-base' }),
            getResponsiveSpacing({ base: 'mb-2', sm: 'mb-3' })
          ]">{{ t('cinematographyRating') }}</label>
          <div class="flex items-center gap-2">
            <input 
              v-model.number="formData.cinematographyRating"
              type="range" 
              min="1" 
              max="10" 
              step="0.5"
              :class="[
                'flex-1 bg-gray-200 rounded-lg appearance-none cursor-pointer slider',
                getTouchFriendlySize('h-2', 'h-3')
              ]"
            >
            <span :class="[
              'text-theme-text font-medium',
              isMobile ? 'w-10 text-sm' : 'w-12'
            ]">{{ formData.cinematographyRating }}/10</span>
          </div>
        </div>
        
        <!-- Production Quality Rating -->
        <div>
          <label :class="[
            'block font-medium text-theme-text',
            getResponsiveFontSize({ base: 'text-sm', md: 'text-base' }),
            getResponsiveSpacing({ base: 'mb-2', sm: 'mb-3' })
          ]">Production Quality</label>
          <div class="flex items-center gap-2">
            <input 
              v-model.number="formData.productionQualityRating"
              type="range" 
              min="1" 
              max="10" 
              step="0.5"
              :class="[
                'flex-1 bg-gray-200 rounded-lg appearance-none cursor-pointer slider',
                getTouchFriendlySize('h-2', 'h-3')
              ]"
            >
            <span :class="[
              'text-theme-text font-medium',
              isMobile ? 'w-10 text-sm' : 'w-12'
            ]">{{ formData.productionQualityRating }}/10</span>
          </div>
        </div>
      </div>
      
      <!-- Cultural Authenticity Rating -->
      <div :class="[
        'bg-accent/10 rounded-lg border border-accent/20',
        getResponsiveSpacing({ base: 'p-3', sm: 'p-4' })
      ]">
        <div :class="[
          'flex gap-2',
          isMobile ? 'flex-col' : 'items-start',
          getResponsiveSpacing({ base: 'mb-2', sm: 'mb-3' })
        ]">
          <Info :class="[
            'text-accent',
            isMobile ? 'w-4 h-4' : 'w-5 h-5 mt-0.5'
          ]" />
          <div class="flex-1">
            <label :class="[
              'block font-medium text-theme-text',
              getResponsiveFontSize({ base: 'text-sm', md: 'text-base' }),
              getResponsiveSpacing({ base: 'mb-1', sm: 'mb-2' })
            ]">
              Cultural Authenticity <span class="text-accent">(Nollywood Specific)</span>
            </label>
            <p :class="[
              'text-theme-secondary',
              getResponsiveFontSize({ base: 'text-xs', sm: 'text-sm' }),
              getResponsiveSpacing({ base: 'mb-2', sm: 'mb-3' })
            ]">
              How well does this movie represent Nigerian culture, values, and authentic storytelling? Consider language use, cultural practices, social dynamics, and genuine Nigerian experiences.
            </p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <input 
            v-model.number="formData.culturalAuthenticityRating"
            type="range" 
            min="1" 
            max="10" 
            step="0.5"
            :class="[
              'flex-1 bg-gray-200 rounded-lg appearance-none cursor-pointer slider',
              getTouchFriendlySize('h-2', 'h-3')
            ]"
          >
          <span :class="[
            'text-theme-text font-medium',
            isMobile ? 'w-10 text-sm' : 'w-12'
          ]">{{ formData.culturalAuthenticityRating }}/10</span>
        </div>
      </div>
      
      <!-- Review Text -->
      <div>
        <label :class="[
          'block font-medium text-theme-text',
          getResponsiveFontSize({ base: 'text-sm', md: 'text-base' }),
          getResponsiveSpacing({ base: 'mb-2', sm: 'mb-3' })
        ]">
          {{ t('yourReview') }} <span class="text-red-500">*</span>
        </label>
        <textarea
          v-model="formData.reviewText"
          :rows="isMobile ? '4' : '6'"
          :class="[
            'w-full border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent resize-vertical',
            getResponsiveSpacing({ base: 'px-3 py-2', sm: 'px-4 py-3' }),
            getTouchFriendlySize('text-sm', 'text-base'),
            { 'border-red-500': errors.reviewText }
          ]"
          :placeholder="t('reviewPlaceholder')"
          :aria-label="t('yourReview')"
        ></textarea>
        <div :class="[
          'flex items-center mt-1',
          isMobile ? 'flex-col gap-1' : 'justify-between'
        ]">
          <p v-if="errors.reviewText" class="text-red-500 text-sm">{{ errors.reviewText }}</p>
          <div :class="[
            'text-theme-secondary',
            getResponsiveFontSize({ base: 'text-xs', sm: 'text-sm' }),
            isMobile && !errors.reviewText ? '' : 'ml-auto'
          ]">
            {{ characterCount }}/{{ characterLimit }} characters
          </div>
        </div>
      </div>
      
      <!-- Enhanced Spoiler Controls -->
      <div class="bg-warning/10 p-4 rounded-lg border border-warning/20">
        <div class="flex items-start gap-3">
          <AlertTriangle class="w-5 h-5 text-warning mt-0.5" />
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-2">
              <input 
                id="spoiler-warning"
                v-model="formData.spoilerWarning"
                type="checkbox"
                class="w-4 h-4 text-accent bg-gray-100 border-gray-300 rounded focus:ring-accent focus:ring-2"
                :aria-describedby="formData.spoilerWarning ? 'spoiler-help' : undefined"
              >
              <label for="spoiler-warning" class="text-sm font-medium text-theme-text">
                {{ t('spoilerWarning') }}
              </label>
            </div>
            <p id="spoiler-help" class="text-xs text-theme-secondary mb-3">
              {{ t('spoilerDesc') }}
            </p>
            
            <!-- Spoiler Preview -->
            <div v-if="formData.spoilerWarning" class="mt-3">
              <div class="flex items-center gap-2 mb-2">
                <button 
                  type="button"
                  @click="showSpoilerPreview = !showSpoilerPreview"
                  class="flex items-center gap-1 text-xs text-warning hover:text-warning/80"
                >
                  <Eye v-if="!showSpoilerPreview" class="w-3 h-3" />
                  <EyeOff v-else class="w-3 h-3" />
                  {{ showSpoilerPreview ? 'Hide' : 'Show' }} spoiler preview
                </button>
              </div>
              
              <div class="relative">
                <div 
                  v-if="!showSpoilerPreview"
                  class="absolute inset-0 bg-warning/20 backdrop-blur-sm rounded flex items-center justify-center z-10"
                >
                  <span class="text-xs font-medium text-warning">Spoiler content hidden</span>
                </div>
                <div 
                  class="text-xs text-theme-secondary p-2 bg-theme-background/50 rounded border"
                  :class="{ 'blur-sm': !showSpoilerPreview }"
                >
                  {{ formData.reviewText || 'Your review text will appear here...' }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Nollywood Tags -->
      <div>
        <label class="block text-sm font-medium text-theme-text mb-2">
          Nollywood Tags <span class="text-theme-secondary">(Select up to 5)</span>
        </label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="tag in availableTags"
            :key="tag"
            type="button"
            @click="toggleTag(tag)"
            class="px-3 py-1 text-xs rounded-full border transition-colors"
            :class="{
              'bg-accent text-white border-accent': isTagSelected(tag),
              'bg-theme-background text-theme-text border-gray-300 hover:border-accent': !isTagSelected(tag),
              'opacity-50 cursor-not-allowed': !isTagSelected(tag) && formData.nollywoodTags.length >= 5
            }"
            :disabled="!isTagSelected(tag) && formData.nollywoodTags.length >= 5"
          >
            {{ tag }}
          </button>
        </div>
        <p class="text-xs text-theme-secondary mt-1">
          Selected: {{ formData.nollywoodTags.length }}/5
        </p>
      </div>
      
      <!-- Form Actions -->
      <div :class="[
        'border-t border-gray-200',
        getResponsiveSpacing({ base: 'pt-3', sm: 'pt-4' }),
        isMobile ? 'flex flex-col gap-3' : 'flex gap-3'
      ]">
        <button
          type="submit"
          :disabled="!isFormValid || isSubmitting"
          :class="[
            'bg-accent hover:bg-accent/90 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors',
            isMobile ? 'w-full order-1' : 'flex-1',
            getTouchFriendlySize('py-2 px-4', 'py-3 px-6'),
            getResponsiveFontSize({ base: 'text-sm', sm: 'text-base' })
          ]"
          :aria-label="isSubmitting ? t('submitting') : (editReview ? t('updateReview') : t('submitReview'))"
        >
          {{ isSubmitting ? t('submitting') : (editReview ? t('updateReview') : t('submitReview')) }}
        </button>
        <button
          type="button"
          @click="cancelReview"
          :class="[
            'border border-gray-300 text-theme-text hover:bg-gray-50 rounded-lg transition-colors',
            isMobile ? 'w-full order-2' : 'px-6',
            getTouchFriendlySize('py-2 px-4', 'py-3 px-6'),
            getResponsiveFontSize({ base: 'text-sm', sm: 'text-base' })
          ]"
        >
          Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
/* Custom slider styles */
.slider::-webkit-slider-thumb {
  appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #f59e0b;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider::-webkit-slider-track {
  width: 100%;
  height: 8px;
  cursor: pointer;
  background: #e5e7eb;
  border-radius: 4px;
}

.slider::-moz-range-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #f59e0b;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider::-moz-range-track {
  width: 100%;
  height: 8px;
  cursor: pointer;
  background: #e5e7eb;
  border-radius: 4px;
  border: none;
}
</style>