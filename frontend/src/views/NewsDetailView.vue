<template>
  <div class="max-w-3xl mx-auto px-4 py-12">
    <RouterLink
      to="/news"
      class="inline-flex items-center gap-1 text-sky-600 font-bold text-sm mb-8 hover:text-sky-800 transition-colors"
    >
      ← Back to News
    </RouterLink>

    <!-- Loading -->
    <div v-if="loading" class="animate-pulse space-y-4">
      <div class="h-8 bg-gray-200 rounded w-3/4" />
      <div class="h-4 bg-gray-200 rounded w-1/3" />
      <div class="h-64 bg-gray-200 rounded-2xl" />
      <div class="space-y-2 mt-6">
        <div class="h-4 bg-gray-200 rounded" />
        <div class="h-4 bg-gray-200 rounded w-5/6" />
        <div class="h-4 bg-gray-200 rounded w-4/6" />
      </div>
    </div>

    <!-- Article -->
    <article v-else-if="article">
      <div class="flex items-center gap-3 mb-4">
        <span class="bg-sky-100 text-sky-700 text-xs font-extrabold px-3 py-1 rounded-full">
          {{ article.category }}
        </span>
        <span class="text-sm text-gray-400">{{ formatDate(article.date) }}</span>
      </div>

      <h1 class="text-3xl md:text-4xl font-extrabold text-gray-900 leading-tight mb-6">
        {{ article.title }}
      </h1>

      <img
        :src="article.cover_image"
        :alt="article.title"
        class="w-full h-64 object-cover rounded-2xl shadow-md mb-10"
      />

      <!-- Rendered Markdown -->
      <div
        class="prose prose-sky prose-headings:font-extrabold prose-a:text-sky-600 prose-img:rounded-xl max-w-none"
        v-html="renderedContent"
      />

      <!-- Tags -->
      <div v-if="article.tags?.length" class="mt-10 flex flex-wrap gap-2">
        <span
          v-for="tag in article.tags"
          :key="tag"
          class="text-xs bg-gray-100 text-gray-600 px-3 py-1 rounded-full"
        >
          #{{ tag }}
        </span>
      </div>
    </article>

    <!-- Not found -->
    <div v-else class="text-center py-24">
      <p class="text-gray-400 text-lg mb-4">Article not found.</p>
      <RouterLink to="/news" class="text-sky-600 font-bold hover:text-sky-800 transition-colors">
        ← Back to News
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'

const route = useRoute()
const article = ref(null)
const loading = ref(true)

const renderedContent = computed(() => {
  if (!article.value?.content) return ''
  return marked(article.value.content)
})

onMounted(async () => {
  try {
    const res = await fetch(`/api/news/${route.params.id}`)
    const data = await res.json()
    if (data.success) {
      article.value = data.data
    }
  } catch {
    article.value = null
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
