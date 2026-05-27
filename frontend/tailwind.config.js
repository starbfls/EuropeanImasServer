/** @type {import('tailwindcss').Config} */
import typographyPlugin from '@tailwindcss/typography'

export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Nunito', 'sans-serif'],
      },
      colors: {
        imas: {
          blue: '#60aac4',
          pink: '#c460aa',
          purple: '#aa60c4',
          green: '#aac460',
        },
      },
    },
  },
  plugins: [typographyPlugin],
}
