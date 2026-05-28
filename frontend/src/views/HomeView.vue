<template>
  <div>
    <!-- Hero Banner -->
    <section class="relative bg-gradient-to-br from-sky-500 via-blue-600 to-indigo-700 text-white overflow-hidden">
      <div class="absolute inset-0 bg-black/20" />
      <div class="absolute -top-24 -right-24 w-96 h-96 bg-sky-400/20 rounded-full blur-3xl pointer-events-none" />
      <div class="absolute -bottom-24 -left-24 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />

      <div class="relative max-w-6xl mx-auto px-4 py-28 flex flex-col items-center text-center gap-7">
        <img src="/logo.png" alt="European iMas" class="h-28 w-28 object-contain drop-shadow-2xl" />

        <div>
          <h1 class="text-5xl md:text-6xl font-extrabold tracking-tight leading-tight">
            THE EUROPE<span class="text-yellow-300">@</span>N
          </h1>
          <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight text-sky-200">
            IDOLM<span class="text-yellow-300">@</span>STER UNION
          </h1>
        </div>

        <p class="text-lg md:text-xl max-w-xl text-sky-100 leading-relaxed">
          Connecting producers across Europe through our shared love of iDOLM@STER.
        </p>

        <div class="flex flex-wrap gap-4 justify-center">
          <RouterLink
            to="/news"
            class="px-7 py-3 bg-white text-sky-700 rounded-full font-extrabold hover:bg-sky-50 transition-colors shadow-lg text-sm tracking-wide"
          >
            Latest News
          </RouterLink>
          <RouterLink
            to="/rules"
            class="px-7 py-3 border-2 border-white text-white rounded-full font-extrabold hover:bg-white/10 transition-colors text-sm tracking-wide"
          >
            Join the Community
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Stats bar -->
    <section class="bg-white border-b border-gray-100 shadow-sm">
      <div class="max-w-6xl mx-auto px-4 py-5 grid grid-cols-3 divide-x divide-gray-100 text-center">
        <div v-for="stat in stats" :key="stat.label" class="px-4">
          <p class="text-2xl font-extrabold text-sky-600">{{ stat.value }}</p>
          <p class="text-xs text-gray-500 mt-0.5">{{ stat.label }}</p>
        </div>
      </div>
    </section>

    <!-- Latest News -->
    <section class="max-w-6xl mx-auto px-4 py-16">
      <div class="flex items-center justify-between mb-8">
        <h2 class="text-2xl font-extrabold text-gray-900">Latest News</h2>
        <RouterLink to="/news" class="text-sky-600 font-bold text-sm hover:text-sky-800 transition-colors">
          View all →
        </RouterLink>
      </div>

      <!-- Loading skeleton -->
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="i in 3" :key="i" class="bg-white rounded-2xl shadow-md overflow-hidden animate-pulse">
          <div class="h-48 bg-gray-200" />
          <div class="p-5 space-y-3">
            <div class="h-3 bg-gray-200 rounded w-1/3" />
            <div class="h-5 bg-gray-200 rounded w-full" />
            <div class="h-4 bg-gray-200 rounded w-2/3" />
          </div>
        </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <NewsCard v-for="article in latestNews" :key="article.id" :article="article" />
      </div>
    </section>

    <!-- Branch promo band -->
    <section class="bg-gradient-to-r from-indigo-50 to-sky-50 border-y border-sky-100">
      <div class="max-w-6xl mx-auto px-4 py-12 text-center">
        <h2 class="text-xl font-extrabold text-gray-800 mb-2">All Branches Welcome</h2>
        <p class="text-sm text-gray-500 mb-8 max-w-md mx-auto">
          Whether you are a 765 Pro veteran or a Shiny Colors newcomer, there is a place for you here.
        </p>
        <div class="flex flex-wrap justify-center gap-3">
          <span v-for="branch in branches" :key="branch.name"
            class="px-4 py-2 rounded-full text-sm font-bold border-2 transition-colors"
            :class="branch.color">
            {{ branch.name }}
          </span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NewsCard from '../components/NewsCard.vue'

const latestNews = ref([])
const loading = ref(true)

const stats = [
  { value: '40+', label: 'European Producers' },
  { value: '8', label: 'Countries Represented' },
  { value: '~', label: 'Events Held' },
]

const branches = [
  { name: '765 Pro', color: 'border-orange-400 text-orange-600 bg-orange-50' },
  { name: 'Cinderella Girls', color: 'border-pink-400 text-pink-600 bg-pink-50' },
  { name: 'Million Live', color: 'border-purple-400 text-purple-600 bg-purple-50' },
  { name: 'SideM', color: 'border-blue-400 text-blue-600 bg-blue-50' },
  { name: 'Shiny Colors', color: 'border-sky-400 text-sky-600 bg-sky-50' },
  { name: 'Gakuen Idolm@ster', color: 'border-orange-400 text-orange-600 bg-orange-50' },
]

const FALLBACK_NEWS = [
  { id: 1, title: 'European iMas Offline Meetup — Dusseldorf 2026', date: '2026-06-15', category: 'Meetup', summary: 'Join us for our first Dusseldorf offline meetup!', cover_image: 'https://placehold.co/800x400/60aac4/ffffff?text=Dusseldorf+Meetup+2026' },
  { id: 2, title: 'Live Viewing: 15th Anniversary Concert', date: '2026-05-20', category: 'Live Viewing', summary: 'Celebrate 15 years of iDOLM@STER with us!', cover_image: 'https://placehold.co/800x400/c460aa/ffffff?text=15th+Anniversary+Live' },
  { id: 3, title: 'Welcome to New Members — Spring 2026', date: '2026-04-10', category: 'Announcement', summary: 'Welcome to all our new members who joined this spring!', cover_image: 'https://placehold.co/800x400/aac460/ffffff?text=Welcome+New+Members' },
]

onMounted(async () => {
  try {
    const res = await fetch('/api/news')
    const data = await res.json()
    latestNews.value = data.data.slice(0, 3)
  } catch {
    latestNews.value = FALLBACK_NEWS
  } finally {
    loading.value = false
  }
})
</script>
