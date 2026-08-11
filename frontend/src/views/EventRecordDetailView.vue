<template>
  <div class="min-h-screen bg-[#f9f8f6]">
    <div class="max-w-3xl mx-auto px-4 py-10">
      <RouterLink to="/event-records"
        class="inline-flex items-center gap-1.5 text-gray-500 hover:text-gray-900 text-sm font-bold mb-8 transition-colors"
      >
        ← 返回活动记录
      </RouterLink>

      <!-- Loading -->
      <div v-if="loading" class="animate-pulse space-y-4">
        <div class="h-8 bg-gray-200 rounded w-3/4" />
        <div class="h-4 bg-gray-200 rounded w-1/2" />
        <div class="h-64 bg-gray-200 rounded-2xl" />
      </div>

      <article v-else-if="item">
        <!-- Cover -->
        <div class="rounded-2xl overflow-hidden h-64 shadow-md mb-8">
          <img :src="item.cover_image" :alt="item.title" class="w-full h-full object-cover" />
        </div>

        <!-- Meta -->
        <div class="flex flex-wrap items-center gap-3 mb-4">
          <span class="text-xs font-extrabold px-3 py-1 rounded-full bg-sky-100 text-sky-700">{{ item.category }}</span>
          <span class="text-sm text-gray-400">{{ fmt(item.date) }}</span>
          <span class="text-sm text-gray-300">·</span>
          <span class="text-sm text-gray-400">作者：{{ item.author }}</span>
        </div>

        <h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 leading-snug mb-8">{{ item.title }}</h1>

        <!-- Rendered Markdown -->
        <div class="prose prose-gray prose-headings:font-extrabold prose-blockquote:border-sky-300 prose-a:text-sky-600 prose-img:rounded-xl max-w-none"
          v-html="rendered"
        />

        <!-- Event photos -->
        <div v-if="item.photos?.length" class="mt-12">
          <h2 class="text-lg font-extrabold text-gray-900 mb-4">活动相册</h2>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
            <img
              v-for="(p, i) in item.photos"
              :key="i"
              :src="p"
              class="w-full aspect-video object-cover rounded-xl hover:scale-[1.02] transition-transform cursor-pointer"
              @click="lightbox = p"
            />
          </div>
        </div>

        <!-- Tags -->
        <div v-if="item.tags?.length" class="mt-8 flex flex-wrap gap-2">
          <span v-for="t in item.tags" :key="t" class="text-xs bg-gray-100 text-gray-500 px-3 py-1 rounded-full">#{{ t }}</span>
        </div>
      </article>

      <div v-else class="text-center py-20 text-gray-400">
        <p class="text-lg mb-4">未找到该记录。</p>
        <RouterLink to="/event-records" class="text-sky-600 font-bold">← 返回列表</RouterLink>
      </div>
    </div>

    <!-- Lightbox -->
    <Transition name="fade">
      <div v-if="lightbox" class="fixed inset-0 bg-black/85 z-50 flex items-center justify-center p-4" @click="lightbox = null">
        <img :src="lightbox" class="max-w-3xl w-full max-h-[85vh] object-contain rounded-2xl shadow-2xl" />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'

const route = useRoute()
const item = ref(null)
const loading = ref(true)
const lightbox = ref(null)

const rendered = computed(() => item.value?.content ? marked(item.value.content) : '')
const fmt = (d) => new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })

onMounted(async () => {
  try {
    const r = await fetch(`/api/event-records/${route.params.id}`)
    const data = await r.json()
    if (data.success) item.value = data.data
  } catch { item.value = null }
  finally { loading.value = false }
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
