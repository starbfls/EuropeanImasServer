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
        // 欧盟旗配色：午夜蓝底 + 星环金。站点的黄色统一走 eu-gold
        eu: {
          gold: '#FFCC00',
          'gold-soft': '#FFE066',
          'gold-deep': '#D9A400',
          navy: '#07091a',
        },
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
