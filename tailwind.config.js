/** @type {import('tailwindcss').Config} */

export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,ts,vue}"],
  theme: {
    container: {
      center: true,
    },
    extend: {
      colors: {
        'nollywood-gold': '#FFD700',
        'nigerian-green': '#008751',
        'vibrant-orange': '#FF6B35',
        'lemon-yellow': '#FFEB3B',
        'pie-brown': '#8D4E2A',
        'deep-navy': '#1A1B2E',
        'cream-white': '#FFF8E1',
      },
    },
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      {
        light: {
          "primary": "#FFD700",
          "secondary": "#008751",
          "accent": "#FF6B35",
          "neutral": "#1A1B2E",
          "base-100": "#FFF8E1",
          "info": "#3ABFF8",
          "success": "#10B981",
          "warning": "#F59E0B",
          "error": "#F87272",
        },
        dark: {
          "primary": "#FFD700",
          "secondary": "#008751",
          "accent": "#FF6B35",
          "neutral": "#FFF8E1",
          "base-100": "#1A1B2E",
          "info": "#3ABFF8",
          "success": "#10B981",
          "warning": "#F59E0B",
          "error": "#F87272",
        },
      },
    ],
  },
};
