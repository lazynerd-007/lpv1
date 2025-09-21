<script setup lang="ts">
import { ref } from 'vue';

// Form data
const formData = ref({
  name: '',
  email: '',
  phone: '',
  subject: 'General Inquiry',
  message: ''
});

// Form validation
const errors = ref({
  name: '',
  email: '',
  message: ''
});

const subjectOptions = [
  'General Inquiry',
  'Technical Support',
  'Feedback',
  'Partnership',
  'Other'
];

// Form submission status
const isSubmitting = ref(false);
const submitStatus = ref({
  show: false,
  success: false,
  message: ''
});

// Validate email format
const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Form validation
const validateForm = (): boolean => {
  let isValid = true;
  errors.value = {
    name: '',
    email: '',
    message: ''
  };

  // Validate name
  if (!formData.value.name.trim()) {
    errors.value.name = 'Name is required';
    isValid = false;
  }

  // Validate email
  if (!formData.value.email.trim()) {
    errors.value.email = 'Email is required';
    isValid = false;
  } else if (!validateEmail(formData.value.email)) {
    errors.value.email = 'Please enter a valid email address';
    isValid = false;
  }

  // Validate message
  if (!formData.value.message.trim()) {
    errors.value.message = 'Message is required';
    isValid = false;
  }

  return isValid;
};

// Handle form submission
const handleSubmit = async () => {
  if (!validateForm()) {
    return;
  }

  isSubmitting.value = true;

  try {
    // Simulate API call with timeout
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Show success message
    submitStatus.value = {
      show: true,
      success: true,
      message: 'Thank you for your message! We will get back to you soon.'
    };
    
    // Reset form
    formData.value = {
      name: '',
      email: '',
      phone: '',
      subject: 'General Inquiry',
      message: ''
    };
  } catch (error) {
    // Show error message
    submitStatus.value = {
      show: true,
      success: false,
      message: 'Something went wrong. Please try again later.'
    };
  } finally {
    isSubmitting.value = false;
    
    // Hide status message after 5 seconds
    setTimeout(() => {
      submitStatus.value.show = false;
    }, 5000);
  }
};
</script>

<template>
  <div class="bg-theme-background min-h-screen">
    <!-- Hero Section -->
    <div class="bg-gray-900 text-white py-12">
      <div class="container mx-auto px-4">
        <h1 class="text-3xl md:text-4xl font-bold mb-2">Contact Us</h1>
        <p class="text-gray-300 max-w-2xl">Have questions or feedback? We'd love to hear from you. Fill out the form below and our team will get back to you as soon as possible.</p>
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="container mx-auto px-4 py-12">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Contact Form -->
        <div class="lg:col-span-2 bg-theme-card rounded-lg shadow-md p-6 md:p-8">
          <h2 class="text-2xl font-bold mb-6 text-gray-800">Send Us a Message</h2>
          
          <!-- Status Message -->
          <div 
            v-if="submitStatus.show" 
            class="mb-6 p-4 rounded-md" 
            :class="submitStatus.success ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200'"
            role="alert"
          >
            {{ submitStatus.message }}
          </div>
          
          <form @submit.prevent="handleSubmit" novalidate>
            <!-- Name Field -->
            <div class="mb-4">
              <label for="name" class="block text-gray-700 font-medium mb-2">Name <span class="text-red-500">*</span></label>
              <input 
                type="text" 
                id="name" 
                v-model="formData.name" 
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-400 focus:border-orange-400 outline-none transition-colors" 
                :class="errors.name ? 'border-red-500' : 'border-gray-300'" 
                aria-required="true"
                :aria-invalid="errors.name ? true : false"
                aria-describedby="name-error"
              >
              <p v-if="errors.name" id="name-error" class="mt-1 text-red-500 text-sm">{{ errors.name }}</p>
            </div>
            
            <!-- Email Field -->
            <div class="mb-4">
              <label for="email" class="block text-gray-700 font-medium mb-2">Email <span class="text-red-500">*</span></label>
              <input 
                type="email" 
                id="email" 
                v-model="formData.email" 
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-400 focus:border-orange-400 outline-none transition-colors" 
                :class="errors.email ? 'border-red-500' : 'border-gray-300'" 
                aria-required="true"
                :aria-invalid="errors.email ? true : false"
                aria-describedby="email-error"
              >
              <p v-if="errors.email" id="email-error" class="mt-1 text-red-500 text-sm">{{ errors.email }}</p>
            </div>
            
            <!-- Phone Field (Optional) -->
            <div class="mb-4">
              <label for="phone" class="block text-gray-700 font-medium mb-2">Phone Number <span class="text-gray-500">(Optional)</span></label>
              <input 
                 type="tel" 
                 id="phone" 
                 v-model="formData.phone" 
                 class="w-full px-4 py-2 border border-theme-border rounded-lg focus:ring-2 focus:ring-orange-400 focus:border-orange-400 outline-none transition-colors bg-theme-surface"
                 aria-required="false"
               >
            </div>
            
            <!-- Subject Dropdown -->
            <div class="mb-4">
              <label for="subject" class="block text-gray-700 font-medium mb-2">Subject</label>
              <select 
                 id="subject" 
                 v-model="formData.subject" 
                 class="w-full px-4 py-2 border border-theme-border rounded-lg focus:ring-2 focus:ring-orange-400 focus:border-orange-400 outline-none transition-colors bg-theme-surface"
               >
                <option v-for="option in subjectOptions" :key="option" :value="option">{{ option }}</option>
              </select>
            </div>
            
            <!-- Message Field -->
            <div class="mb-6">
              <label for="message" class="block text-gray-700 font-medium mb-2">Message <span class="text-red-500">*</span></label>
              <textarea 
                id="message" 
                v-model="formData.message" 
                rows="5" 
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-400 focus:border-orange-400 outline-none transition-colors" 
                :class="errors.message ? 'border-red-500' : 'border-gray-300'" 
                aria-required="true"
                :aria-invalid="errors.message ? true : false"
                aria-describedby="message-error"
              ></textarea>
              <p v-if="errors.message" id="message-error" class="mt-1 text-red-500 text-sm">{{ errors.message }}</p>
            </div>
            
            <!-- Submit Button -->
            <div>
              <button 
                type="submit" 
                class="bg-orange-500 hover:bg-orange-600 text-white font-medium py-2 px-6 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="isSubmitting"
                :aria-busy="isSubmitting"
              >
                <span v-if="isSubmitting">Sending...</span>
                <span v-else>Send Message</span>
              </button>
            </div>
          </form>
        </div>
        
        <!-- Contact Information -->
         <div class="bg-theme-card rounded-lg shadow-md p-6 md:p-8 h-fit">
          <h2 class="text-2xl font-bold mb-6 text-gray-800">Contact Information</h2>
          
          <div class="space-y-6">
            <!-- Address -->
            <div class="flex items-start">
              <div class="flex-shrink-0 bg-orange-100 p-3 rounded-full mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <h3 class="font-medium text-gray-800">Address</h3>
                <p class="text-gray-600 mt-1">123 Movie Lane<br>Hollywood, CA 90210<br>United States</p>
              </div>
            </div>
            
            <!-- Phone -->
            <div class="flex items-start">
              <div class="flex-shrink-0 bg-orange-100 p-3 rounded-full mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
              </div>
              <div>
                <h3 class="font-medium text-gray-800">Phone</h3>
                <p class="text-gray-600 mt-1">+1 (555) 123-4567</p>
              </div>
            </div>
            
            <!-- Email -->
            <div class="flex items-start">
              <div class="flex-shrink-0 bg-orange-100 p-3 rounded-full mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <h3 class="font-medium text-gray-800">Email</h3>
                <p class="text-gray-600 mt-1">contact@lemonnpie.com</p>
              </div>
            </div>
            
            <!-- Social Media -->
            <div>
              <h3 class="font-medium text-gray-800 mb-3">Follow Us</h3>
              <div class="flex space-x-4">
                <!-- Facebook -->
                 <a href="#" class="bg-theme-surface p-2 rounded-full hover:bg-theme-surface-hover transition-colors" aria-label="Facebook">
                   <svg class="h-5 w-5 text-gray-700" fill="currentColor" viewBox="0 0 24 24">
                     <path d="M18.77 7.46H14.5v-1.9c0-.9.6-1.1 1-1.1h3V.5h-4.33C10.24.5 9.5 3.44 9.5 5.32v2.15h-3v4h3v12h5v-12h3.85l.42-4z"/>
                   </svg>
                 </a>
                 <!-- Twitter -->
                 <a href="#" class="bg-theme-surface p-2 rounded-full hover:bg-theme-surface-hover transition-colors" aria-label="Twitter">
                   <svg class="h-5 w-5 text-gray-700" fill="currentColor" viewBox="0 0 24 24">
                     <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                   </svg>
                 </a>
                 <!-- Instagram -->
                 <a href="#" class="bg-theme-surface p-2 rounded-full hover:bg-theme-surface-hover transition-colors" aria-label="Instagram">
                  <svg class="h-5 w-5 text-gray-700" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>
          
          <!-- Google Map -->
          <div class="mt-8">
            <h3 class="font-medium text-gray-800 mb-3">Our Location</h3>
            <div class="aspect-video bg-theme-surface rounded-lg overflow-hidden">
              <!-- Replace with actual Google Maps embed code -->
              <iframe 
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3305.7152203627526!2d-118.32504548478038!3d34.0937756805959!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x80c2bf20e4c82873%3A0x14015754d926dadb!2sHollywood%20Sign!5e0!3m2!1sen!2sus!4v1628544755945!5m2!1sen!2sus" 
                width="100%" 
                height="100%" 
                style="border:0;" 
                :allowfullscreen="true" 
                loading="lazy"
                title="Google Maps location of LemonNPie"
              ></iframe>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>