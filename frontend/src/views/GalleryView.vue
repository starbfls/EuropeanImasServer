<template>
  <div class="min-h-screen bg-[#f9f8f6]">
    <!-- Header -->
    <div class="bg-[#07091a] border-b border-white/5 py-12 px-4">
      <div class="max-w-6xl mx-auto">
        <p class="text-purple-400/70 text-xs tracking-[0.3em] uppercase mb-2">Gallery</p>
        <h1 class="text-3xl font-extrabold text-white">照片墙</h1>
        <p class="text-white/40 text-sm mt-2">聚会留影、痛车、祭坛与周边展示</p>
      </div>
    </div>

    <!-- Filter -->
    <div class="bg-white border-b border-gray-100 px-4 py-3 sticky top-16 z-10">
      <div class="max-w-6xl mx-auto flex flex-wrap gap-2">
        <button
          v-for="f in filters"
          :key="f.value"
          @click="activeFilter = f.value"
          class="px-3 py-1 rounded-full text-xs font-bold transition-colors"
          :class="activeFilter === f.value ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-500 hover:bg-gray-200'"
        >{{ f.label }}</button>
      </div>
    </div>

    <!-- Masonry grid -->
    <div class="max-w-6xl mx-auto px-4 py-10">
      <div v-if="loading" class="columns-2 md:columns-3 lg:columns-4 gap-4">
        <div v-for="i in 10" :key="i" class="break-inside-avoid mb-4 rounded-xl bg-gray-200 animate-pulse"
          :style="`height:${120 + (i % 3) * 70}px`" />
      </div>

      <div v-else-if="filtered.length === 0" class="text-center py-20 text-gray-400 text-sm">
        该分类暂无照片。
      </div>

      <div v-else class="columns-2 md:columns-3 lg:columns-4 gap-4">
        <div
          v-for="item in filtered"
          :key="item.id"
          class="break-inside-avoid mb-4 bg-white rounded-2xl overflow-hidden shadow-sm group cursor-pointer hover:shadow-xl transition-all duration-300"
          @click="lightbox = item"
        >
          <img :src="item.thumbnail" :alt="item.title"
            class="w-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
          <div class="px-3 py-2.5">
            <p class="text-xs font-bold text-gray-800 truncate">{{ item.title }}</p>
            <span class="text-[11px] text-gray-400">{{ item.type }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Lightbox -->
    <Transition name="fade">
      <div v-if="lightbox"
        class="fixed inset-0 bg-black/85 z-50 flex items-center justify-center p-4"
        @click.self="lightbox = null"
      >
        <div class="bg-white rounded-2xl overflow-hidden max-w-3xl w-full shadow-2xl">
          <img :src="lightbox.url" :alt="lightbox.title" class="w-full max-h-[72vh] object-contain" />
          <div class="p-4 flex items-center justify-between">
            <div>
              <p class="font-extrabold text-gray-900 text-sm">{{ lightbox.title }}</p>
              <span class="text-xs text-gray-400">{{ lightbox.type }}</span>
            </div>
            <button @click="lightbox = null"
              class="w-8 h-8 flex items-center justify-center rounded-full text-gray-400 hover:text-gray-800 hover:bg-gray-100 transition-colors text-lg"
            >✕</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const gallery = ref([])
const loading = ref(true)
const activeFilter = ref('all')
const lightbox = ref(null)

const filters = [
  { label: '全部', value: 'all' },
  { label: '聚会', value: '聚会' },
  { label: '痛车', value: '痛车' },
  { label: '祭坛', value: '祭坛' },
  { label: 'Cosplay', value: 'Cosplay' },
  { label: '周边', value: '周边' },
]

const filtered = computed(() =>
  activeFilter.value === 'all' ? gallery.value : gallery.value.filter(i => i.type === activeFilter.value)
)

onMounted(async () => {
  try {
    const r = await fetch('/api/gallery')
    gallery.value = (await r.json()).data
  } catch {
    gallery.value = [
      { id: 1, title: '杜塞尔多夫聚会合影 2026', type: '聚会', url: 'https://placehold.co/800x533/60aac4/ffffff?text=杜塞尔多夫合影', thumbnail: 'https://placehold.co/400x267/60aac4/ffffff?text=杜塞尔多夫合影' },
      { id: 2, title: '阿姆斯特丹痛车', type: '痛车', url: 'https://placehold.co/600x900/c460aa/ffffff?text=痛车', thumbnail: 'https://placehold.co/400x600/c460aa/ffffff?text=痛车' },
      { id: 3, title: '芙蕾德莉卡祭坛', type: '祭坛', url: 'https://placehold.co/700x700/aa60c4/ffffff?text=祭坛', thumbnail: 'https://placehold.co/400x400/aa60c4/ffffff?text=祭坛' },
    ]
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>


