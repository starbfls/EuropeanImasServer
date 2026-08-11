<template>
  <div class="min-h-screen bg-[#f9f8f6]">
    <div class="max-w-3xl mx-auto px-4 py-10">
      <RouterLink to="/announcements"
        class="inline-flex items-center gap-1.5 text-gray-500 hover:text-gray-900 text-sm font-bold mb-8 transition-colors"
      >
        ← 返回活动公告
      </RouterLink>

      <!-- Loading -->
      <div v-if="loading" class="animate-pulse space-y-4">
        <div class="h-8 bg-gray-200 rounded w-3/4" />
        <div class="h-4 bg-gray-200 rounded w-1/3" />
        <div class="h-60 bg-gray-200 rounded-2xl" />
      </div>

      <article v-else-if="item">
        <!-- Cover -->
        <div class="rounded-2xl overflow-hidden h-64 bg-gray-900 mb-8 shadow-md">
          <img :src="item.cover_image" :alt="item.title" class="w-full h-full object-cover opacity-90" />
        </div>

        <!-- Meta -->
        <div class="flex flex-wrap items-center gap-3 mb-4">
          <span class="text-xs font-extrabold px-3 py-1 rounded-full" :class="catColor(item.category)">{{ item.category }}</span>
          <span class="text-sm text-gray-400 flex items-center gap-1">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            活动日期：{{ fmt(item.date_event) }}
          </span>
          <span class="text-sm text-gray-400 flex items-center gap-1">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/></svg>
            {{ item.location }}
          </span>
        </div>

        <h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 leading-snug mb-8">{{ item.title }}</h1>

        <!-- Rendered Markdown -->
        <div class="prose prose-gray prose-headings:font-extrabold prose-a:text-yellow-600 prose-img:rounded-xl max-w-none"
          v-html="rendered" />

        <!-- External link -->
        <a v-if="item.external_link && item.external_link !== '#'"
          :href="item.external_link" target="_blank"
          class="mt-8 inline-flex items-center gap-2 px-5 py-2.5 bg-yellow-400 text-gray-900 rounded-full font-extrabold text-sm hover:bg-yellow-300 transition-colors"
        >
          前往官网
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
        </a>

        <!-- Tags -->
        <div v-if="item.tags?.length" class="mt-8 flex flex-wrap gap-2">
          <span v-for="t in item.tags" :key="t" class="text-xs bg-gray-100 text-gray-500 px-3 py-1 rounded-full">#{{ t }}</span>
        </div>
      </article>

      <div v-else class="text-center py-20 text-gray-400">
        <p class="text-lg mb-4">未找到该活动公告。</p>
        <RouterLink to="/announcements" class="text-yellow-600 font-bold">← 返回列表</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'

const route = useRoute()
const item = ref(null)
const loading = ref(true)

const rendered = computed(() => item.value?.content ? marked(item.value.content) : '')

const catColor = (c) => {
  const m = { '动漫展会': 'bg-orange-100 text-orange-700', '声优活动': 'bg-pink-100 text-pink-700', '日本文化节': 'bg-indigo-100 text-indigo-700', '制作人聚会': 'bg-sky-100 text-sky-700' }
  return m[c] ?? 'bg-gray-100 text-gray-700'
}
const fmt = (d) => new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })

onMounted(async () => {
  try {
    const r = await fetch(`/api/announcements/${route.params.id}`)
    const data = await r.json()
    if (data.success) item.value = data.data
  } catch { item.value = null }
  finally { loading.value = false }
})
</script>
