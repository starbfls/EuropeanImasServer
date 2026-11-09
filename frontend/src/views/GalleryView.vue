<template>
  <div class="min-h-screen bg-[#f9f8f6]">
    <!-- Header -->
    <div class="bg-[#07091a] border-b border-white/5 py-8 md:py-10 px-4">
      <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-between gap-5">
        <div>
          <p class="text-purple-400/70 text-xs tracking-[0.3em] uppercase mb-2">Gallery</p>
          <h1 class="text-3xl font-extrabold text-white">照片墙</h1>
          <p class="text-white/40 text-sm mt-2">现地、展会、娃娃与日常留影</p>
        </div>
        <RouterLink to="/gallery/upload"
          class="inline-flex shrink-0 items-center gap-2 rounded-full bg-purple-500 px-5 py-2.5 text-sm font-extrabold text-white shadow-lg shadow-purple-500/15 transition-colors hover:bg-purple-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-purple-400">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 16V4m0 0L7 9m5-5l5 5M4 16v4h16v-4" />
          </svg>
          上传照片
        </RouterLink>
      </div>
    </div>

    <!-- Filter -->
    <div class="bg-white border-b border-gray-100 px-4 py-3">
      <div class="max-w-6xl mx-auto flex flex-wrap gap-2">
        <button type="button" @click="activeFilters = []" :aria-pressed="activeFilters.length === 0"
          class="px-3 py-1 rounded-full text-xs font-bold transition-colors"
          :class="activeFilters.length === 0 ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-500 hover:bg-gray-200'">全部</button>
        <button
          v-for="f in filters"
          :key="f.value"
          type="button"
          :aria-pressed="activeFilters.includes(f.value)"
          @click="activeFilters = toggleTag(activeFilters, f.value)"
          class="px-3 py-1 rounded-full text-xs font-bold transition-colors"
          :class="activeFilters.includes(f.value) ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-500 hover:bg-gray-200'"
        >{{ f.label }}</button>
      </div>
      <p class="max-w-6xl mx-auto mt-2 text-[11px] leading-relaxed text-gray-400">可多选，再次点击取消；显示同时包含所选标签的照片。</p>
    </div>

    <!-- Masonry grid -->
    <div class="max-w-6xl mx-auto px-4 py-8">
      <div v-if="loadError" role="alert" class="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
        {{ loadError }}
        <button type="button" @click="loadGallery" class="ml-2 font-bold underline">重新加载</button>
      </div>
      <div v-if="loading" class="columns-2 md:columns-3 lg:columns-4 gap-4">
        <div v-for="i in 10" :key="i" class="break-inside-avoid mb-4 rounded-xl bg-gray-200 animate-pulse"
          :style="`height:${120 + (i % 3) * 70}px`" />
      </div>

      <div v-else-if="!loadError && filtered.length === 0" class="text-center py-20 text-gray-400 text-sm">
        <p>{{ activeFilters.length === 0 ? '还没有照片，分享第一张留影吧。' : '暂无同时包含这些标签的照片，可以取消部分标签。' }}</p>
        <RouterLink v-if="activeFilters.length === 0" to="/gallery/upload" class="mt-3 inline-block font-bold text-purple-600 hover:text-purple-700">上传照片 →</RouterLink>
      </div>

      <div v-else class="columns-2 md:columns-3 lg:columns-4 gap-4">
        <div
          v-for="item in filtered"
          :key="item.id"
          class="break-inside-avoid mb-4 bg-white rounded-2xl overflow-hidden shadow-sm group cursor-pointer hover:shadow-xl transition-all duration-300"
          @click="lightbox = item"
        >
          <img :src="item.thumbnail || item.url" :alt="item.title" loading="lazy"
            class="w-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
          <div class="px-3 py-2.5">
            <p class="text-xs font-bold text-gray-800 truncate">{{ item.title }}</p>
            <div class="mt-1.5 flex flex-wrap gap-1">
              <span v-for="(label, index) in photoTagLabels(item)" :key="index" class="rounded bg-purple-50 px-1.5 py-0.5 text-[10px] leading-relaxed text-purple-600">{{ label }}</span>
            </div>
            <p v-if="item.uploader" class="mt-1.5 text-[11px] text-gray-400">{{ item.uploader }}</p>
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
        <div class="bg-white rounded-2xl overflow-hidden overflow-y-auto max-h-[95dvh] max-w-3xl w-full shadow-2xl">
          <img :src="lightbox.url" :alt="lightbox.title" class="w-full max-h-[72vh] object-contain" />
          <div class="p-4 flex items-center justify-between">
            <div class="min-w-0 pr-3">
              <p class="font-extrabold text-gray-900 text-sm">{{ lightbox.title }}</p>
              <div class="mt-2 flex flex-wrap gap-1.5">
                <span v-for="(label, index) in photoTagLabels(lightbox)" :key="index" class="rounded bg-purple-50 px-2 py-0.5 text-[11px] text-purple-600">{{ label }}</span>
              </div>
              <p v-if="lightbox.uploader" class="mt-2 text-xs text-gray-400">{{ lightbox.uploader }}</p>
            </div>
            <button @click="lightbox = null"
              aria-label="关闭照片大图" class="w-8 h-8 shrink-0 flex items-center justify-center rounded-full text-gray-400 hover:text-gray-800 hover:bg-gray-100 transition-colors text-lg"
            >✕</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { publicRequest } from '../api/public'
import { matchesPhotoTags, photoTagIds, photoTagLabels, toggleTag } from '../utils/galleryTags'

// 分类列表由后端 data/content/gallery_types.json 提供，加一场 live 不用改前端
const allTypes = ref([])

const gallery = ref([])
const loading = ref(true)
const loadError = ref('')
const activeFilters = ref([])
const lightbox = ref(null)

// 筛选栏只列出"确实有照片"的分类，免得一长串空按钮
const filters = computed(() => {
  const used = new Set(gallery.value.flatMap(photoTagIds))
  return allTypes.value.filter((t) => used.has(t.id)).map((t) => ({ label: t.label, value: t.id }))
})

const filtered = computed(() =>
  gallery.value.filter(item => matchesPhotoTags(item, activeFilters.value))
)

async function loadGallery() {
  loading.value = true
  loadError.value = ''
  try {
    const [photos, types] = await Promise.all([
      publicRequest('/api/gallery'),
      publicRequest('/api/gallery/types'),
    ])
    gallery.value = photos.data
    allTypes.value = types.data
    activeFilters.value = activeFilters.value.filter(id => filters.value.some(filter => filter.value === id))
  } catch (e) {
    loadError.value = e.message
    gallery.value = []
    allTypes.value = []
  } finally {
    loading.value = false
  }
}

onMounted(loadGallery)
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>


