import { ref, computed } from 'vue'

export type SupportedLanguage = 'en' | 'ig' | 'yo' | 'ha' | 'pcm'

export interface LanguageOption {
  code: SupportedLanguage
  name: string
  nativeName: string
  flag: string
}

const currentLanguage = ref<SupportedLanguage>('en')

export const supportedLanguages: LanguageOption[] = [
  { code: 'en', name: 'English', nativeName: 'English', flag: '🇬🇧' },
  { code: 'ig', name: 'Igbo', nativeName: 'Asụsụ Igbo', flag: '🇳🇬' },
  { code: 'yo', name: 'Yoruba', nativeName: 'Èdè Yorùbá', flag: '🇳🇬' },
  { code: 'ha', name: 'Hausa', nativeName: 'Harshen Hausa', flag: '🇳🇬' },
  { code: 'pcm', name: 'Nigerian Pidgin', nativeName: 'Naija Pidgin', flag: '🇳🇬' }
]

// Translation keys for review form
export const translations = {
  en: {
    writeReview: 'Write a Review',
    editReview: 'Edit Review',
    overallRating: 'Overall Rating',
    storyRating: 'Story',
    actingRating: 'Acting',
    cinematographyRating: 'Cinematography',
    productionQualityRating: 'Production Quality',
    culturalAuthenticityRating: 'Cultural Authenticity',
    culturalAuthenticityDesc: 'How well does this movie represent Nigerian culture, values, and authentic storytelling? Consider language use, cultural practices, social dynamics, and genuine Nigerian experiences.',
    yourReview: 'Your Review',
    reviewPlaceholder: 'Share your thoughts about this movie. What did you like or dislike? How was the story, acting, and production quality?',
    spoilerWarning: 'This review contains spoilers',
    spoilerDesc: 'Check this box if your review reveals important plot points, endings, or surprises that might spoil the movie for other viewers.',
    nollywoodTags: 'Nollywood Tags',
    selectUpTo5: 'Select up to 5',
    submitReview: 'Submit Review',
    updateReview: 'Update Review',
    submitting: 'Submitting...',
    cancel: 'Cancel',
    languageSelection: 'Review Language',
    writeInLanguage: 'Write your review in',
    ratingRequired: 'Overall rating is required',
    reviewRequired: 'Review text is required',
    reviewTooShort: 'Review must be at least 10 characters long',
    imageLoading: 'Loading image...',
    imageError: 'Failed to load image'
  },
  ig: {
    writeReview: 'Dee Nyocha',
    editReview: 'Dozie Nyocha',
    overallRating: 'Ọnụọgụgụ Niile',
    storyRating: 'Akụkọ',
    actingRating: 'Ime Ihe Nkiri',
    cinematographyRating: 'Ịse Foto',
    productionQualityRating: 'Ogo Mmepụta',
    culturalAuthenticityRating: 'Ezi Omenala',
    culturalAuthenticityDesc: 'Kedu ka ihe nkiri a si egosipụta omenala Naịjirịa, ụkpụrụ, na ezi akụkọ? Tụlee ojiji asụsụ, omenaala, mmekọrịta ọha na eze, na ezigbo ahụmịhe Naịjirịa.',
    yourReview: 'Nyocha Gị',
    reviewPlaceholder: 'Kọwaa echiche gị maka ihe nkiri a. Gịnị masịrị gị ma ọ bụ nke na-amasịghị gị? Kedu ka akụkọ ahụ, ime ihe nkiri, na ogo mmepụta dị?',
    spoilerWarning: 'Nyocha a nwere ihe nkpuchi',
    spoilerDesc: 'Chọọ igbe a ma ọ bụrụ na nyocha gị na-ekpughe isi ihe dị mkpa, njedebe, ma ọ bụ ihe ijuanya nke nwere ike imebi ihe nkiri ahụ maka ndị na-ekiri ndị ọzọ.',
    nollywoodTags: 'Akara Nollywood',
    selectUpTo5: 'Họrọ ruo 5',
    submitReview: 'Zipu Nyocha',
    updateReview: 'Melite Nyocha',
    submitting: 'Na-ezipu...',
    cancel: 'Kagbuo',
    languageSelection: 'Asụsụ Nyocha',
    writeInLanguage: 'Dee nyocha gị na',
    ratingRequired: 'Ọnụọgụgụ niile achọrọ',
    reviewRequired: 'Ederede nyocha achọrọ',
    reviewTooShort: 'Nyocha ga-abụ opekata mpe mkpụrụedemede 10',
    imageLoading: 'Na-ebu onyonyo...',
    imageError: 'Enweghị ike ibu onyonyo'
  },
  yo: {
    writeReview: 'Kọ Àyẹ̀wò',
    editReview: 'Ṣàtúnkọ Àyẹ̀wò',
    overallRating: 'Àpapọ̀ Ìdíwọ̀n',
    storyRating: 'Ìtàn',
    actingRating: 'Ṣíṣe Eré',
    cinematographyRating: 'Yíya Fọ́tò',
    productionQualityRating: 'Ìdára Ìṣelọ́pọ̀',
    culturalAuthenticityRating: 'Òtítọ́ Àṣà',
    culturalAuthenticityDesc: 'Báwo ni fíìmù yìí ṣe ń ṣàfihàn àṣà Nàìjíríà, àwọn ìlànà, àti òtítọ́ ìtàn-sọ? Rò nípa lílo èdè, àṣà àwọn ènìyàn, ìbáṣepọ̀ àwùjọ, àti òtítọ́ ìrírí Nàìjíríà.',
    yourReview: 'Àyẹ̀wò Rẹ',
    reviewPlaceholder: 'Sọ èrò rẹ nípa fíìmù yìí. Kí ni ó wù ọ́ tàbí tí kò wù ọ́? Báwo ni ìtàn náà, ṣíṣe eré, àti ìdára ìṣelọ́pọ̀ ṣe rí?',
    spoilerWarning: 'Àyẹ̀wò yìí ní àwọn ìfihàn',
    spoilerDesc: 'Ṣàmì àpótí yìí tí àyẹ̀wò rẹ bá ń ṣàfihàn àwọn kókó pàtàkì, ìparí, tàbí àwọn ìyàlẹ́nu tí ó lè ba fíìmù náà jẹ́ fún àwọn olùwòran mìíràn.',
    nollywoodTags: 'Àwọn Àmì Nollywood',
    selectUpTo5: 'Yan títí dé 5',
    submitReview: 'Fi Àyẹ̀wò Ránṣẹ́',
    updateReview: 'Ṣàtúnṣe Àyẹ̀wò',
    submitting: 'Ń fi ránṣẹ́...',
    cancel: 'Fagilee',
    languageSelection: 'Èdè Àyẹ̀wò',
    writeInLanguage: 'Kọ àyẹ̀wò rẹ ní',
    ratingRequired: 'Àpapọ̀ ìdíwọ̀n nílò',
    reviewRequired: 'Ọ̀rọ̀ àyẹ̀wò nílò',
    reviewTooShort: 'Àyẹ̀wò gbọ́dọ̀ jẹ́ ó kéré jù lẹ́tà 10',
    imageLoading: 'N gbe aworan...',
    imageError: 'Ko le gbe aworan'
  },
  ha: {
    writeReview: 'Rubuta Bita',
    editReview: 'Gyara Bita',
    overallRating: 'Jimlar Kimanta',
    storyRating: 'Labari',
    actingRating: 'Yin Wasan Kwaikwayo',
    cinematographyRating: 'Daukar Hoto',
    productionQualityRating: 'Ingancin Samarwa',
    culturalAuthenticityRating: 'Gaskiyar Al\'ada',
    culturalAuthenticityDesc: 'Ta yaya wannan fim ɗin ya wakilci al\'adun Najeriya, ƙa\'idodi, da gaskiyar ba da labari? Yi la\'akari da amfani da harshe, al\'adun mutane, hulɗar al\'umma, da ainihin gogewa na Najeriya.',
    yourReview: 'Bitar Ka',
    reviewPlaceholder: 'Faɗa tunaninka game da wannan fim. Me ka so ko abin da ba ka so? Yaya labarin, yin wasan kwaikwayo, da ingancin samarwa suke?',
    spoilerWarning: 'Wannan bita tana ɗauke da abubuwan ɓarna',
    spoilerDesc: 'Duba wannan akwatin idan bitar ka ta bayyana mahimman abubuwan labari, ƙarshe, ko abubuwan mamaki da za su iya ɓarna fim ɗin ga sauran masu kallo.',
    nollywoodTags: 'Alamun Nollywood',
    selectUpTo5: 'Zaɓa har zuwa 5',
    submitReview: 'Aika Bita',
    updateReview: 'Sabunta Bita',
    submitting: 'Ana aikawa...',
    cancel: 'Soke',
    languageSelection: 'Harshen Bita',
    writeInLanguage: 'Rubuta bitar ka da',
    ratingRequired: 'Jimlar kimanta ana bukata',
    reviewRequired: 'Rubutun bita ana bukata',
    reviewTooShort: 'Bita dole ta zama aƙalla haruffa 10',
    imageLoading: 'Ana ɗaukar hoto...',
    imageError: 'Ba a iya ɗaukar hoto ba'
  },
  pcm: {
    writeReview: 'Write Review',
    editReview: 'Edit Review',
    overallRating: 'Overall Rating',
    storyRating: 'Story',
    actingRating: 'Acting',
    cinematographyRating: 'Camera Work',
    productionQualityRating: 'Production Quality',
    culturalAuthenticityRating: 'How Real E Be',
    culturalAuthenticityDesc: 'How well dis movie show Naija culture, values, and real-real story? Think about how dem use language, culture things, how people dey relate, and real Naija experience.',
    yourReview: 'Your Review',
    reviewPlaceholder: 'Talk wetin you think about dis movie. Wetin you like or no like? How the story, acting, and production quality be?',
    spoilerWarning: 'Dis review get spoiler',
    spoilerDesc: 'Check dis box if your review go tell important things wey happen, ending, or surprise wey fit spoil the movie for other people wey wan watch.',
    nollywoodTags: 'Nollywood Tags',
    selectUpTo5: 'Pick up to 5',
    submitReview: 'Send Review',
    updateReview: 'Update Review',
    submitting: 'Dey send...',
    cancel: 'Cancel',
    languageSelection: 'Review Language',
    writeInLanguage: 'Write your review for',
    ratingRequired: 'Overall rating dey required',
    reviewRequired: 'Review text dey required',
    reviewTooShort: 'Review must be at least 10 letters',
    imageLoading: 'Dey load picture...',
    imageError: 'Picture no fit load'
  }
}

export function useLanguage() {
  const setLanguage = (lang: SupportedLanguage) => {
    currentLanguage.value = lang
    localStorage.setItem('lemonpie-language', lang)
  }

  const getLanguage = () => {
    const saved = localStorage.getItem('lemonpie-language') as SupportedLanguage
    if (saved && supportedLanguages.find(l => l.code === saved)) {
      currentLanguage.value = saved
    }
    return currentLanguage.value
  }

  const t = (key: keyof typeof translations.en) => {
    return translations[currentLanguage.value]?.[key] || translations.en[key]
  }

  const currentLanguageInfo = computed(() => 
    supportedLanguages.find(l => l.code === currentLanguage.value) || supportedLanguages[0]
  )

  // Initialize language from localStorage
  getLanguage()

  return {
    currentLanguage: computed(() => currentLanguage.value),
    currentLanguageInfo,
    supportedLanguages,
    setLanguage,
    getLanguage,
    t
  }
}