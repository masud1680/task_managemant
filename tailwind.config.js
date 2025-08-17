/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", //Template at the project lavel
    "./**/templates/**/*.html" // Templates inside apps 
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

