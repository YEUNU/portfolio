/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./public/**/*.html"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Flutter Material Blue Color Palette
        primary: {
          50: '#E3F2FD',
          100: '#BBDEFB',
          200: '#90CAF9',
          300: '#64B5F6',
          400: '#42A5F5',
          DEFAULT: '#2196F3', // blue[500]
          500: '#2196F3',
          600: '#1E88E5',
          700: '#1976D2',
          800: '#1565C0',
          900: '#0D47A1',
          container: '#BBDEFB', // blue[100]
          on: '#FFFFFF',
          'on-container': '#0D47A1', // blue[900]
          dark: '#90CAF9', // blue[200]
          'dark-container': '#1565C0', // blue[800]
        },
        secondary: {
          DEFAULT: '#625B71',
          container: '#E8DEF8',
          on: '#FFFFFF',
          'on-container': '#1D192B',
          dark: '#CCC2DC',
          'dark-container': '#4A4458',
        },
        tertiary: {
          DEFAULT: '#7D5260',
          container: '#FFD8E4',
          on: '#FFFFFF',
          'on-container': '#31111D',
          dark: '#EFB8C8',
          'dark-container': '#633B48',
        },
        error: {
          DEFAULT: '#B3261E',
          container: '#F9DEDC',
          on: '#FFFFFF',
          'on-container': '#410E0B',
          dark: '#F2B8B5',
          'dark-container': '#8C1D18',
        },
        surface: {
          DEFAULT: '#FEF7FF',
          variant: '#E7E0EC',
          on: '#1C1B1F',
          'on-variant': '#49454F',
          dark: '#1C1B1F',
          'dark-variant': '#49454F',
          'dark-on': '#E6E1E5',
        },
        outline: {
          DEFAULT: '#79747E',
          dark: '#938F99',
        },
      },
      fontFamily: {
        sans: ['Roboto', 'Noto Sans KR', 'sans-serif'],
      },
      borderRadius: {
        'md3-none': '0px',
        'md3-xs': '4px',
        'md3-sm': '8px',
        'md3-md': '12px',
        'md3-lg': '16px',
        'md3-xl': '28px',
        'md3-full': '1000px',
      },
      boxShadow: {
        'md3-1': '0px 1px 2px 0px rgba(0, 0, 0, 0.3), 0px 1px 3px 1px rgba(0, 0, 0, 0.15)',
        'md3-2': '0px 1px 2px 0px rgba(0, 0, 0, 0.3), 0px 2px 6px 2px rgba(0, 0, 0, 0.15)',
        'md3-3': '0px 1px 3px 0px rgba(0, 0, 0, 0.3), 0px 4px 8px 3px rgba(0, 0, 0, 0.15)',
        'md3-4': '0px 2px 3px 0px rgba(0, 0, 0, 0.3), 0px 6px 10px 4px rgba(0, 0, 0, 0.15)',
        'md3-5': '0px 4px 4px 0px rgba(0, 0, 0, 0.3), 0px 8px 12px 6px rgba(0, 0, 0, 0.15)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'slide-in-left': 'slideInLeft 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(-20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        slideInLeft: {
          '0%': { opacity: '0', transform: 'translateX(20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
