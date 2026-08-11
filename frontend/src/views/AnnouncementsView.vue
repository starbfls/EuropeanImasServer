<template>
  <div class="min-h-screen bg-[#f9f8f6]">
    <!-- Page header -->
    <div class="bg-[#07091a] border-b border-white/5 py-12 px-4">
      <div class="max-w-5xl mx-auto">
        <p class="text-yellow-400/70 text-xs tracking-[0.3em] uppercase mb-2">Announcements</p>
        <h1 class="text-3xl font-extrabold text-white">活动公告</h1>
        <p class="text-white/40 text-sm mt-2">近期欧洲日本文化相关活动、演出及展会资讯</p>
      </div>
    </div>

    <!-- Filter -->
    <div class="bg-white border-b border-gray-100 px-4 py-3 sticky top-16 z-10">
      <div class="max-w-5xl mx-auto flex flex-wrap gap-2">
        <button
          v-for="f in filters"
          :key="f"
          @click="activeFilter = f"
          class="px-3 py-1 rounded-full text-xs font-bold transition-colors"
          :class="activeFilter === f ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-500 hover:bg-gray-200'"
        >{{ f }}</button>
      </div>
    </div>

    <!-- List -->
    <div class="max-w-5xl mx-auto px-4 py-10">
      <div v-if="loading" class="space-y-4">
        <div v-for="i in 4" :key="i" class="bg-white rounded-2xl animate-pulse h-32" />
      </div>

      <div v-else class="space-y-4">
        <RouterLink
          v-for="item in filtered"
          :key="item.id"
          :to="`/announcements/${item.id}`"
          class="group flex flex-col sm:flex-row bg-white rounded-2xl overflow-hidden hover:shadow-lg transition-all duration-300 hover:-translate-y-0.5 border border-gray-100 hover:border-yellow-200"
        >
          <div class="sm:w-52 h-36 sm:h-auto shrink-0 overflow-hidden bg-gray-900">
            <img :src="item.cover_image" :alt="item.title"
              class="w-full h-full object-cover opacity-80 group-hover:opacity-100 group-hover:scale-105 transition-all duration-500"
            />
          </div>
          <div class="p-5 flex flex-col justify-between gap-3 flex-1">
            <div>
              <div class="flex flex-wrap items-center gap-2 mb-2">
                <span class="text-[10px] font-extrabold px-2.5 py-0.5 rounded-full" :class="categoryColor(item.category)">
                  {{ item.category }}
                </span>
                <span class="text-xs text-gray-400 flex items-center gap-1">
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                  活动日期 {{ formatDate(item.date_event) }}
                </span>
              </div>
              <h2 class="font-extrabold text-gray-900 text-base leading-snug group-hover:text-yellow-700 transition-colors">
                {{ item.title }}
              </h2>
              <p class="text-xs text-gray-400 mt-1.5 flex items-center gap-1">
                <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                {{ item.location }}
              </p>
            </div>
            <p class="text-xs text-gray-500 line-clamp-2">{{ item.summary }}</p>
            <span class="text-yellow-600 text-xs font-bold group-hover:translate-x-0.5 transition-transform inline-block">查看详情 →</span>
          </div>
        </RouterLink>

        <div v-if="filtered.length === 0" class="text-center py-16 text-gray-400 text-sm">该分类暂无活动公告。</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const items = ref([])
const loading = ref(true)
const activeFilter = ref('全部')

const filters = ['全部', '动漫展会', '声优活动', '制作人聚会', '日本文化节', '音乐演出']

const filtered = computed(() =>
  activeFilter.value === '全部' ? items.value : items.value.filter(i => i.category === activeFilter.value)
)

const categoryColor = (cat) => {
  const map = { '动漫展会': 'bg-orange-100 text-orange-700', '声优活动': 'bg-pink-100 text-pink-700', '日本文化节': 'bg-indigo-100 text-indigo-700', '制作人聚会': 'bg-sky-100 text-sky-700', '音乐演出': 'bg-purple-100 text-purple-700' }
  return map[cat] ?? 'bg-gray-100 text-gray-700'
}
const formatDate = (d) => new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })

onMounted(async () => {
  try {
    const r = await fetch('/api/announcements')
    items.value = (await r.json()).data
  } catch {
    items.value = [
      { id: 1, title: 'AnimagiC 2026 - 曼海姆', date_event: '2026-08-28', category: '动漫展会', location: '曼海姆，德国', summary: '德国知名动漫展 AnimagiC 将于8月在曼海姆举办。', cover_image: 'https://placehold.co/800x400/1a2035/e8c547?text=AnimagiC+2026' },
      { id: 2, title: 'Japan Expo 2026 - 巴黎', date_event: '2026-07-02', category: '动漫展会', location: '巴黎，法国', summary: '欧洲最大的日本文化展会在巴黎盛大开幕。', cover_image: 'https://placehold.co/800x400/1a3520/e8c547?text=Japan+Expo+2026' },
      { id: 5, title: '制作人联盟聚会 - 杜塞尔多夫', date_event: '2026-09-05', category: '制作人聚会', location: '杜塞尔多夫，德国', summary: '欧洲制作人联盟2026年秋季线下聚会。', cover_image: 'https://placehold.co/800x400/0f1e35/e8c547?text=制作人聚会' },
    ]
  } finally {
    loading.value = false
  }
})
</script>
