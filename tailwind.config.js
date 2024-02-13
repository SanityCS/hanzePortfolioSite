/** @type {import('tailwindcss').Config} */

const colors = require('tailwindcss/colors')

module.exports = {
  content: ["./templates/*.html"],
  theme: {
    extend: {},
    colors: {
      black: colors.black,
      purple: colors.purple,
      gray: colors.gray,
      white: colors.white,
      indigo: colors.indigo,
      red: colors.red,
      teal: colors.teal,
      yellow: colors.yellow,
      blue: colors.blue,

    },
  },
  plugins: [],
}

