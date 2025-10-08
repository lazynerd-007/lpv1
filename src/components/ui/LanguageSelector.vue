<template>
  <div class="relative">
    <label :id="labelId" class="block text-sm font-medium text-theme-text mb-2">
      {{ t('languageSelection') }}
    </label>
    <div class="relative">
      <button
        ref="buttonRef"
        type="button"
        @click="openDropdown"
        @blur="handleBlur"
        class="w-full flex items-center justify-between px-3 py-2 border border-gray-300 rounded-md bg-theme-background text-theme-text hover:border-accent focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent transition-colors"
        :aria-expanded="isOpen"
        aria-haspopup="listbox"
        :aria-labelledby="labelId"
        :aria-controls="dropdownId"
        :aria-activedescendant="focusedIndex >= 0 ? `option-${focusedIndex}` : undefined"
      >
        <div class="flex items-center gap-2">
          <span class="text-lg">{{ currentLanguageInfo.flag }}</span>
          <span class="font-medium">{{ currentLanguageInfo.nativeName }}</span>
          <span class="text-sm text-theme-secondary">({{ currentLanguageInfo.name }})</span>
        </div>
        <ChevronDown 
          :class="{ 'transform rotate-180': isOpen }" 
          class="w-4 h-4 transition-transform text-theme-secondary"
        />
      </button>
      
      <Transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 scale-95"
        enter-to-class="opacity-100 scale-100"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-95"
      >
        <div
          v-if="isOpen"
          ref="dropdownRef"
          :id="dropdownId"
          class="absolute z-50 w-full mt-1 bg-theme-card border border-gray-200 rounded-md shadow-lg max-h-60 overflow-auto"
          role="listbox"
          :aria-labelledby="labelId"
          @blur="handleBlur"
        >
          <button
            v-for="(language, index) in supportedLanguages"
            :key="language.code"
            :id="`option-${index}`"
            type="button"
            @click="selectLanguage(language.code)"
            @focus="focusedIndex = index"
            class="w-full flex items-center gap-3 px-3 py-2 text-left hover:bg-accent/10 focus:bg-accent/10 focus:outline-none transition-colors"
            :class="{
              'bg-accent/20 text-accent': currentLanguage === language.code,
              'text-theme-text': currentLanguage !== language.code,
              'bg-accent/10': focusedIndex === index
            }"
            role="option"
            :aria-selected="currentLanguage === language.code"
            :tabindex="focusedIndex === index ? 0 : -1"
          >
            <span class="text-lg">{{ language.flag }}</span>
            <div class="flex-1">
              <div class="font-medium">{{ language.nativeName }}</div>
              <div class="text-sm text-theme-secondary">{{ language.name }}</div>
            </div>
            <Check 
              v-if="currentLanguage === language.code" 
              class="w-4 h-4 text-accent"
            />
          </button>
        </div>
      </Transition>
    </div>
    
    <p class="text-xs text-theme-secondary mt-1">
      {{ t('writeInLanguage') }} {{ currentLanguageInfo.nativeName }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { ChevronDown, Check } from 'lucide-vue-next'
import { useLanguage, type SupportedLanguage } from '@/composables/useLanguage'
import { useAccessibility } from '@/composables/useAccessibility'

interface Props {
  modelValue?: SupportedLanguage
}

interface Emits {
  (e: 'update:modelValue', value: SupportedLanguage): void
  (e: 'change', value: SupportedLanguage): void
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: 'en'
})

const emit = defineEmits<Emits>()

const { 
  currentLanguage, 
  currentLanguageInfo, 
  supportedLanguages, 
  setLanguage, 
  t 
} = useLanguage()

const { 
  announceToScreenReader, 
  handleArrowNavigation, 
  generateId 
} = useAccessibility()

const isOpen = ref(false)
const dropdownRef = ref<HTMLElement>()
const buttonRef = ref<HTMLElement>()
const focusedIndex = ref(-1)
const dropdownId = generateId('language-dropdown')
const labelId = generateId('language-label')

const selectLanguage = async (languageCode: SupportedLanguage, fromKeyboard = false) => {
  setLanguage(languageCode)
  emit('update:modelValue', languageCode)
  emit('change', languageCode)
  isOpen.value = false
  focusedIndex.value = -1
  
  // Return focus to button after selection
  if (fromKeyboard && buttonRef.value) {
    buttonRef.value.focus()
  }
  
  // Announce language change for screen readers
  await nextTick()
  const languageInfo = supportedLanguages.find(l => l.code === languageCode)
  const announcement = `${t('languageSelection')}: ${languageInfo?.name}`
  announceToScreenReader(announcement)
}

const handleKeydown = (event: KeyboardEvent) => {
  if (!isOpen.value) {
    if (event.key === 'Enter' || event.key === ' ' || event.key === 'ArrowDown') {
      event.preventDefault()
      openDropdown()
    }
    return
  }

  const options = dropdownRef.value?.querySelectorAll('[role="option"]') as NodeListOf<HTMLElement>
  if (!options || options.length === 0) return

  switch (event.key) {
    case 'Escape':
      event.preventDefault()
      closeDropdown()
      break
    case 'Enter':
    case ' ':
      event.preventDefault()
      if (focusedIndex.value >= 0 && focusedIndex.value < supportedLanguages.length) {
        selectLanguage(supportedLanguages[focusedIndex.value].code, true)
      }
      break
    case 'ArrowDown':
    case 'ArrowUp':
      event.preventDefault()
      const newIndex = handleArrowNavigation(
        event,
        Array.from(options),
        focusedIndex.value,
        'vertical'
      )
      focusedIndex.value = newIndex
      break
    case 'Home':
      event.preventDefault()
      focusedIndex.value = 0
      options[0].focus()
      break
    case 'End':
      event.preventDefault()
      focusedIndex.value = options.length - 1
      options[options.length - 1].focus()
      break
  }
}

const openDropdown = () => {
  isOpen.value = true
  focusedIndex.value = supportedLanguages.findIndex(lang => lang.code === currentLanguage.value)
  nextTick(() => {
    const options = dropdownRef.value?.querySelectorAll('[role="option"]') as NodeListOf<HTMLElement>
    if (options && focusedIndex.value >= 0) {
      options[focusedIndex.value]?.focus()
    }
  })
}

const closeDropdown = () => {
  isOpen.value = false
  focusedIndex.value = -1
  buttonRef.value?.focus()
}

const handleBlur = (event: FocusEvent) => {
  // Close dropdown if focus moves outside the component
  const relatedTarget = event.relatedTarget as HTMLElement
  const currentTarget = event.currentTarget as HTMLElement
  if (!relatedTarget || !currentTarget?.contains(relatedTarget)) {
    isOpen.value = false
    focusedIndex.value = -1
  }
}

// Setup keyboard listeners
onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>