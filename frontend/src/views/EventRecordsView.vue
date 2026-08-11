<template>
  <div class="min-h-screen bg-[#f9f8f6]">
    <!-- Header -->
    <div class="bg-[#07091a] border-b border-white/5 py-12 px-4">
      <div class="max-w-5xl mx-auto">
        <p class="text-sky-400/70 text-xs tracking-[0.3em] uppercase mb-2">Event Records</p>
        <h1 class="text-3xl font-extrabold text-white">活动记录</h1>
        <p class="text-white/40 text-sm mt-2">制作人聚会、观影、展会的图文实录</p>
      </div>
    </div>

    <!-- List -->
    <div class="max-w-5xl mx-auto px-4 py-10">
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div v-for="i in 4" :key="i" class="bg-white rounded-2xl animate-pulse h-64" />
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <RouterLink
          v-for="item in items"
          :key="item.id"
          :to="`/event-records/${item.id}`"
          class="group block bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
        >
          <div class="h-52 overflow-hidden">
            <img :src="item.cover_image" :alt="item.title"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />
          </div>
          <div class="p-5">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-[10px] font-extrabold px-2.5 py-0.5 rounded-full bg-sky-100 text-sky-700">{{ item.category }}</span>
              <span class="text-xs text-gray-400">{{ fmt(item.date) }}</span>
              <span class="text-xs text-gray-300">·</span>
              <span class="text-xs text-gray-400">{{ item.author }}</span>
            </div>
            <h2 class="font-extrabold text-gray-900 text-base leading-snug group-hover:text-sky-700 transition-colors mb-2">
              {{ item.title }}
            </h2>
            <p class="text-xs text-gray-500 line-clamp-2">{{ item.summary }}</p>
            <span class="inline-block mt-3 text-sky-500 text-xs font-bold group-hover:translate-x-0.5 transition-transform">阅读全文 →</span>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const items = ref([])
const loading = ref(true)

const fmt = (d) => new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })

onMounted(async () => {
  try {
    const r = await fetch('/api/event-records')
    items.value = (await r.json()).data
  } catch {
    items.value = [
      { id: 1, title: '【聚会记录】2026年春 杜塞尔多夫制作人聚会', date: '2026-06-18', category: '聚会记录', author: '联盟管理组', summary: '六月的杜塞尔多夫，14位制作人第一次正式线下聚首。', cover_image: 'https://placehold.co/800x400/1a2035/60aac4?text=杜塞尔多夫聚会' },
      { id: 2, title: '【观影记录】Shiny Colors 阿姆斯特丹同步观影', date: '2026-05-25', category: '观影记录', author: '联盟管理组', summary: '12位制作人共同守候来自东京的演唱会直播。', cover_image: 'https://placehold.co/800x400/20103a/aa60c4?text=ShinyColors观影' },
      { id: 3, title: '【展会记录】AnimagiC 2025 — 曼海姆见闻录', date: '2026-01-10', category: '展会记录', author: 'Frederica制P', summary: '首次以联盟名义参加德国动漫展的完整体验报告。', cover_image: 'https://placehold.co/800x400/1a1530/60c4aa?text=AnimagiC+2025' },
    ]
  } finally {
    loading.value = false
  }
})
</script>
