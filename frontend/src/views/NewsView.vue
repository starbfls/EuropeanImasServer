<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <h1 class="text-3xl font-extrabold text-gray-900 mb-1">News & Reports</h1>
    <p class="text-gray-500 mb-10">Meetup reports, live viewing announcements, and community updates.</p>

    <!-- Loading skeleton -->
    <div v-if="loading" class="space-y-5">
      <div v-for="i in 4" :key="i" class="bg-white rounded-2xl shadow-md overflow-hidden flex animate-pulse">
        <div class="w-44 shrink-0 bg-gray-200" />
        <div class="p-5 flex-1 space-y-3">
          <div class="h-3 bg-gray-200 rounded w-1/4" />
          <div class="h-5 bg-gray-200 rounded w-3/4" />
          <div class="h-4 bg-gray-200 rounded w-full" />
          <div class="h-4 bg-gray-200 rounded w-2/3" />
        </div>
      </div>
    </div>

    <div v-else class="space-y-5">
      <RouterLink
        v-for="article in news"
        :key="article.id"
        :to="`/news/${article.id}`"
        class="group flex flex-col sm:flex-row bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-xl transition-all duration-300"
      >
        <div class="sm:w-44 h-48 sm:h-auto shrink-0 overflow-hidden">
          <img
            :src="article.cover_image"
            :alt="article.title"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
        </div>
        <div class="p-5 flex flex-col justify-center gap-2">
          <div class="flex items-center gap-3">
            <span class="bg-sky-100 text-sky-700 text-xs font-bold px-2.5 py-0.5 rounded-full">
              {{ article.category }}
            </span>
            <span class="text-xs text-gray-400">{{ formatDate(article.date) }}</span>
          </div>
          <h2 class="font-extrabold text-gray-900 text-lg leading-snug group-hover:text-sky-600 transition-colors">
            {{ article.title }}
          </h2>
          <p class="text-sm text-gray-500 line-clamp-2">{{ article.summary }}</p>
          <span class="text-sky-500 text-sm font-bold mt-1 group-hover:translate-x-1 transition-transform inline-block">
            Read more →
          </span>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const news = ref([])
const loading = ref(true)

const FALLBACK = [
  { id: 1, title: 'European iMas Offline Meetup — Berlin 2025', date: '2025-06-15', category: 'Meetup', summary: 'Join us for our first Berlin offline meetup!', cover_image: 'https://placehold.co/800x400/60aac4/ffffff?text=Berlin+Meetup+2025' },
  { id: 2, title: 'Live Viewing: 15th Anniversary Concert', date: '2025-05-20', category: 'Live Viewing', summary: 'Celebrate 15 years of iDOLM@STER with us!', cover_image: 'https://placehold.co/800x400/c460aa/ffffff?text=15th+Anniversary+Live' },
  { id: 3, title: 'Welcome to New Members — Spring 2025', date: '2025-04-10', category: 'Announcement', summary: 'Welcome to all our new members!', cover_image: 'https://placehold.co/800x400/aac460/ffffff?text=Welcome+New+Members' },
  { id: 4, title: 'Fan Art Showcase — March Collection', date: '2025-03-25', category: 'Fan Content', summary: 'Over 30 pieces from European producers!', cover_image: 'https://placehold.co/800x400/aa60c4/ffffff?text=Fan+Art+March' },
]

onMounted(async () => {
  try {
    const res = await fetch('/api/news')
    const data = await res.json()
    news.value = data.data
  } catch {
    news.value = FALLBACK
  } finally {
    loading.value = false
  }
})

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-GB', {
    day: 'numeric', month: 'long', year: 'numeric',
  })
}
</script>
