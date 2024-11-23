/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html", 
    "./app/static/**/*.js",      
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Rajdhani', 'sans-serif'], 
      },
      colors: {
        primary: '#727459',   
        secondary: '#93ABB0', 
        light: '#CDD8DA',
        dark: '#698489',
        darkBlue: '#406789',
        highlight: '#FFE6A9', 
        accent: '#DEAA79',    
        white: '#ffffff',    
      },
    },
  },
  plugins: [],
};
