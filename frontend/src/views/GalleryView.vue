<template>
  <div class="max-w-6xl mx-auto px-4 py-12">
    <h1 class="text-3xl font-extrabold text-gray-900 mb-1">Gallery</h1>
    <p class="text-gray-500 mb-8">Event photos, itasha, fan altars, and community memories.</p>

    <!-- Filter tabs -->
    <div class="flex flex-wrap gap-2 mb-8">
      <button
        v-for="f in filters"
        :key="f.value"
        @click="activeFilter = f.value"
        class="px-4 py-1.5 rounded-full text-sm font-bold transition-colors"
        :class="activeFilter === f.value
          ? 'bg-sky-500 text-white shadow'
          : 'bg-white text-gray-600 border border-gray-200 hover:border-sky-300 hover:text-sky-600'"
      >
        {{ f.label }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="columns-2 md:columns-3 lg:columns-4 gap-4">
      <div
        v-for="i in 8"
        :key="i"
        class="break-inside-avoid mb-4 rounded-xl bg-gray-200 animate-pulse"
        :style="`height: ${120 + (i % 3) * 60}px`"
      />
    </div>

    <!-- Masonry grid -->
    <div v-else class="columns-2 md:columns-3 lg:columns-4 gap-4">
      <div
        v-for="item in filteredGallery"
        :key="item.id"
        class="break-inside-avoid mb-4 bg-white rounded-xl overflow-hidden shadow-md group cursor-pointer hover:shadow-xl transition-all duration-300"
        @click="lightboxItem = item"
      >
        <img
          :src="item.thumbnail"
          :alt="item.title"
          class="w-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
        <div class="p-3">
          <p class="text-xs font-bold text-gray-800 truncate">{{ item.title }}</p>
          <span class="text-xs text-gray-400 capitalize">{{ item.type }}</span>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="!loading && filteredGallery.length === 0" class="text-center py-20">
      <p class="text-gray-400">No items in this category yet.</p>
    </div>

    <!-- Lightbox -->
    <Transition name="fade">
      <div
        v-if="lightboxItem"
        class="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
        @click.self="lightboxItem = null"
      >
        <div class="bg-white rounded-2xl overflow-hidden max-w-3xl w-full shadow-2xl">
          <img
            :src="lightboxItem.url"
            :alt="lightboxItem.title"
            class="w-full max-h-[70vh] object-contain"
          />
          <div class="p-4 flex items-center justify-between">
            <div>
              <p class="font-extrabold text-gray-900">{{ lightboxItem.title }}</p>
              <span class="text-sm text-gray-400 capitalize">{{ lightboxItem.type }}</span>
            </div>
            <button
              @click="lightboxItem = null"
              class="w-8 h-8 flex items-center justify-center rounded-full text-gray-400 hover:text-gray-700 hover:bg-gray-100 transition-colors text-lg leading-none"
            >
              ✕
            </button>
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
const lightboxItem = ref(null)

const filters = [
  { label: 'All', value: 'all' },
  { label: 'Meetups', value: 'meetup' },
  { label: 'Itasha', value: 'itasha' },
  { label: 'Fan Altars', value: 'altar' },
  { label: 'Cosplay', value: 'cosplay' },
  { label: 'Merchandise', value: 'merchandise' },
]

const filteredGallery = computed(() =>
  activeFilter.value === 'all'
    ? gallery.value
    : gallery.value.filter(i => i.type === activeFilter.value)
)

const FALLBACK = [
  { id: 1, title: 'Berlin Meetup 2024 — Group Photo', type: 'meetup', url: 'https://placehold.co/800x533/60aac4/ffffff?text=Berlin+Group+Photo', thumbnail: 'https://placehold.co/400x267/60aac4/ffffff?text=Berlin+Group+Photo' },
  { id: 2, title: 'Itasha at Amsterdam Comic Con', type: 'itasha', url: 'https://placehold.co/600x900/c460aa/ffffff?text=Amsterdam+Itasha', thumbnail: 'https://placehold.co/400x600/c460aa/ffffff?text=Amsterdam+Itasha' },
  { id: 3, title: 'Fan Altar — Cinderella Girls', type: 'altar', url: 'https://placehold.co/700x700/aa60c4/ffffff?text=Fan+Altar+CG', thumbnail: 'https://placehold.co/400x400/aa60c4/ffffff?text=Fan+Altar+CG' },
  { id: 4, title: 'Paris Live Viewing Party', type: 'meetup', url: 'https://placehold.co/800x533/60c4aa/ffffff?text=Paris+Live+Viewing', thumbnail: 'https://placehold.co/400x267/60c4aa/ffffff?text=Paris+Live+Viewing' },
  { id: 5, title: 'Merchandise Collection Display', type: 'merchandise', url: 'https://placehold.co/800x600/c4aa60/ffffff?text=Merch+Collection', thumbnail: 'https://placehold.co/400x300/c4aa60/ffffff?text=Merch+Collection' },
  { id: 6, title: 'London Cosplay — Shiny Colors', type: 'cosplay', url: 'https://placehold.co/600x900/6084c4/ffffff?text=London+Cosplay', thumbnail: 'https://placehold.co/400x600/6084c4/ffffff?text=London+Cosplay' },
  { id: 7, title: 'Madrid Game Night', type: 'meetup', url: 'https://placehold.co/800x533/aac460/ffffff?text=Madrid+Game+Night', thumbnail: 'https://placehold.co/400x267/aac460/ffffff?text=Madrid+Game+Night' },
  { id: 8, title: 'Fan Altar — Million Live', type: 'altar', url: 'https://placehold.co/700x700/c460aa/ffffff?text=Fan+Altar+ML', thumbnail: 'https://placehold.co/400x400/c460aa/ffffff?text=Fan+Altar+ML' },
  { id: 9, title: 'Rome Itasha Showcase', type: 'itasha', url: 'https://placehold.co/800x533/aa60c4/ffffff?text=Rome+Itasha', thumbnail: 'https://placehold.co/400x267/aa60c4/ffffff?text=Rome+Itasha' },
]

onMounted(async () => {
  try {
    const res = await fetch('/api/gallery')
    const data = await res.json()
    gallery.value = data.data
  } catch {
    gallery.value = FALLBACK
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
