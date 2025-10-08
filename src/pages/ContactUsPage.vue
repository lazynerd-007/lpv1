<script setup lang="ts">
import { ref } from 'vue'
import { MapPin, Phone, Mail, Facebook, Twitter, Instagram, Youtube } from 'lucide-vue-next'

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
  'Movie Review Feedback',
  'Technical Support',
  'Partnership Opportunity',
  'Nollywood Industry Collaboration',
  'Content Suggestion',
  'Bug Report',
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
    <div class="bg-gradient-to-r from-yellow-500 to-orange-500 text-white py-16">
      <div class="container mx-auto px-4">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">Get in Touch</h1>
        <p class="text-white max-w-3xl text-lg">Ready to share your thoughts on Nollywood? Have feedback about our platform? We'd love to hear from you! Our team is here to help you make the most of your LemonNPie experience.</p>
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="container mx-auto px-4 py-12">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Contact Form -->
        <div class="lg:col-span-2 bg-theme-card rounded-lg shadow-md p-6 md:p-8">
          <h2 class="text-2xl font-bold mb-6 text-theme-text">Send Us a Message</h2>
          
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
              <label for="name" class="block text-theme-primary font-medium mb-2">Full Name *</label>
              <input 
                type="text" 
                id="name" 
                v-model="formData.name" 
                class="w-full px-4 py-2 border border-theme-border rounded-lg focus:ring-2 focus:ring-theme-primary focus:border-theme-primary outline-none transition-colors bg-theme-surface text-theme-primary" 
                :class="errors.name ? 'border-red-500' : 'border-theme-border'" 
                aria-required="true"
                :aria-invalid="errors.name ? true : false"
                aria-describedby="name-error"
                placeholder="Enter your full name"
              >
              <p v-if="errors.name" id="name-error" class="mt-1 text-red-500 text-sm">{{ errors.name }}</p>
            </div>
            
            <!-- Email Field -->
            <div class="mb-4">
              <label for="email" class="block text-theme-primary font-medium mb-2">Email Address *</label>
              <input 
                type="email" 
                id="email" 
                v-model="formData.email" 
                class="w-full px-4 py-2 border border-theme-border rounded-lg focus:ring-2 focus:ring-theme-primary focus:border-theme-primary outline-none transition-colors bg-theme-surface text-theme-primary" 
                :class="errors.email ? 'border-red-500' : 'border-theme-border'" 
                aria-required="true"
                :aria-invalid="errors.email ? true : false"
                aria-describedby="email-error"
                placeholder="your.email@example.com"
              >
              <p v-if="errors.email" id="email-error" class="mt-1 text-red-500 text-sm">{{ errors.email }}</p>
            </div>
            
            <!-- Phone Field (Optional) -->
            <div class="mb-4">
              <label for="phone" class="block text-theme-primary font-medium mb-2">Phone Number <span class="text-theme-muted">(Optional)</span></label>
              <input 
                 type="tel" 
                 id="phone" 
                 v-model="formData.phone" 
                 class="w-full px-4 py-2 border border-theme-border rounded-lg focus:ring-2 focus:ring-theme-primary focus:border-theme-primary outline-none transition-colors bg-theme-surface text-theme-primary"
                 aria-required="false"
                 placeholder="+234 xxx xxx xxxx"
               >
            </div>
            
            <!-- Subject Dropdown -->
            <div class="mb-4">
              <label for="subject" class="block text-theme-primary font-medium mb-2">Subject</label>
              <select 
                 id="subject" 
                 v-model="formData.subject" 
                 class="w-full px-4 py-2 border border-theme-border rounded-lg focus:ring-2 focus:ring-theme-primary focus:border-theme-primary outline-none transition-colors bg-theme-surface text-theme-primary"
               >
                <option v-for="option in subjectOptions" :key="option" :value="option">{{ option }}</option>
              </select>
            </div>
            
            <!-- Message Field -->
            <div class="mb-6">
              <label for="message" class="block text-theme-primary font-medium mb-2">Message <span class="text-red-500">*</span></label>
              <textarea 
                id="message" 
                v-model="formData.message" 
                rows="5" 
                class="w-full px-4 py-2 border border-theme-border rounded-lg focus:ring-2 focus:ring-theme-primary focus:border-theme-primary outline-none transition-colors bg-theme-surface text-theme-primary" 
                :class="errors.message ? 'border-red-500' : 'border-theme-border'" 
                aria-required="true"
                :aria-invalid="errors.message ? true : false"
                aria-describedby="message-error"
                placeholder="Tell us about your experience with Nollywood movies, suggestions for the platform, or any questions you have..."
              ></textarea>
              <p v-if="errors.message" id="message-error" class="mt-1 text-red-500 text-sm">{{ errors.message }}</p>
            </div>
            
            <!-- Submit Button -->
            <div>
              <button 
                type="submit" 
                class="bg-theme-primary hover:bg-theme-primary-hover text-white font-medium py-3 px-8 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-theme-primary focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                :disabled="isSubmitting"
                :aria-busy="isSubmitting"
              >
                <Mail class="w-4 h-4" />
                <span v-if="isSubmitting">Sending...</span>
                <span v-else>Send Message</span>
              </button>
            </div>
          </form>
        </div>
        
        <!-- Contact Information -->
         <div class="bg-theme-card rounded-lg shadow-md p-6 md:p-8 h-fit">
          <h2 class="text-2xl font-bold mb-6 text-theme-text">Contact Information</h2>
          
          <div class="space-y-6">
            <!-- Address -->
            <div class="flex items-start">
              <div class="flex-shrink-0 bg-theme-primary/10 p-3 rounded-full mr-4">
                <MapPin class="h-6 w-6 text-theme-primary" />
              </div>
              <div>
                <h3 class="font-medium text-theme-primary">Address</h3>
                <p class="text-theme-muted mt-1">Plot 123, Nollywood Boulevard<br>Victoria Island, Lagos<br>Nigeria</p>
              </div>
            </div>
            
            <!-- Phone -->
            <div class="flex items-start">
              <div class="flex-shrink-0 bg-theme-primary/10 p-3 rounded-full mr-4">
                <Phone class="h-6 w-6 text-theme-primary" />
              </div>
              <div>
                <h3 class="font-medium text-theme-primary">Phone</h3>
                <p class="text-theme-muted mt-1">+234 (0) 901 234 5678<br>+234 (0) 803 456 7890</p>
              </div>
            </div>
            
            <!-- Email -->
            <div class="flex items-start">
              <div class="flex-shrink-0 bg-theme-primary/10 p-3 rounded-full mr-4">
                <Mail class="h-6 w-6 text-theme-primary" />
              </div>
              <div>
                <h3 class="font-medium text-theme-primary">Email</h3>
                <p class="text-theme-muted mt-1">hello@lemonnpie.com<br>support@lemonnpie.com</p>
              </div>
            </div>
            
            <!-- Social Media -->
            <div>
              <h3 class="font-medium text-theme-text mb-3">Follow Us</h3>
              <div class="flex space-x-4">
                <!-- Facebook -->
                 <a href="https://facebook.com/lemonnpie" class="bg-theme-surface p-3 rounded-full hover:bg-theme-surface-hover transition-colors group" aria-label="Follow us on Facebook">
                   <Facebook class="h-5 w-5 text-theme-muted group-hover:text-theme-primary transition-colors" />
                 </a>
                 <!-- Twitter -->
                 <a href="https://twitter.com/lemonnpie" class="bg-theme-surface p-3 rounded-full hover:bg-theme-surface-hover transition-colors group" aria-label="Follow us on Twitter">
                   <Twitter class="h-5 w-5 text-theme-muted group-hover:text-theme-primary transition-colors" />
                 </a>
                 <!-- Instagram -->
                 <a href="https://instagram.com/lemonnpie" class="bg-theme-surface p-3 rounded-full hover:bg-theme-surface-hover transition-colors group" aria-label="Follow us on Instagram">
                  <Instagram class="h-5 w-5 text-theme-muted group-hover:text-theme-primary transition-colors" />
                </a>
                <!-- YouTube -->
                 <a href="https://youtube.com/lemonnpie" class="bg-theme-surface p-3 rounded-full hover:bg-theme-surface-hover transition-colors group" aria-label="Subscribe to our YouTube channel">
                  <Youtube class="h-5 w-5 text-theme-muted group-hover:text-theme-primary transition-colors" />
                </a>
              </div>
            </div>
          </div>
          

          
          <!-- Business Hours -->
          <div class="mt-8">
            <h3 class="font-medium text-theme-primary mb-3">Business Hours</h3>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-theme-muted">Monday - Friday</span>
                <span class="text-theme-primary">9:00 AM - 6:00 PM</span>
              </div>
              <div class="flex justify-between">
                <span class="text-theme-muted">Saturday</span>
                <span class="text-theme-primary">10:00 AM - 4:00 PM</span>
              </div>
              <div class="flex justify-between">
                <span class="text-theme-muted">Sunday</span>
                <span class="text-theme-primary">Closed</span>
              </div>
              <div class="mt-3 pt-3 border-t border-theme-border">
                <p class="text-theme-muted text-xs">All times are in West Africa Time (WAT)</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>