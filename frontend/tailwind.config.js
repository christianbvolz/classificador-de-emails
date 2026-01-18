/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#10b981',    // Emerald 500
        secondary: '#14b8a6',  // Teal 500
      }
    },
  },
  plugins: [],
}
