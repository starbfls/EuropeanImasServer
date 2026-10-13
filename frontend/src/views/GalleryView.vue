<template>
  <div class="min-h-screen bg-[#f9f8f6]">
    <!-- Header -->
    <div class="bg-[#07091a] border-b border-white/5 py-12 px-4">
      <div class="max-w-6xl mx-auto">
        <p class="text-purple-400/70 text-xs tracking-[0.3em] uppercase mb-2">Gallery</p>
        <h1 class="text-3xl font-extrabold text-white">照片墙</h1>
        <p class="text-white/40 text-sm mt-2">现地、展会、娃娃与日常留影 — 无需注册，欢迎投稿</p>
      </div>
    </div>

    <!-- 上传 -->
    <div class="bg-white border-b border-gray-100">
      <div class="max-w-6xl mx-auto px-4 py-8">
        <div class="flex items-start justify-between gap-4 mb-5">
          <div>
            <h2 class="text-lg font-extrabold text-gray-900">上传你的照片</h2>
            <p class="text-xs text-gray-400 mt-1">
              无需注册，经审核后将展示在照片墙上。支持 JPG / PNG / WEBP / GIF，单张不超过 8 MB。
            </p>
          </div>
          <span class="shrink-0 text-xs text-amber-600 bg-amber-50 border border-amber-200 px-3 py-1 rounded-full font-bold">需人工审核</span>
        </div>

        <form @submit.prevent="handleSubmit" class="grid grid-cols-1 md:grid-cols-[minmax(0,1fr),minmax(0,1.2fr)] gap-4 items-start">
          <!-- 选图 -->
          <label class="flex flex-col items-center justify-center gap-2 border-2 border-dashed border-gray-200 rounded-2xl p-6 cursor-pointer hover:border-purple-400 hover:bg-purple-50/30 transition-colors group min-h-[168px]">
            <template v-if="preview">
              <img :src="preview" alt="预览" class="max-h-28 rounded-lg object-contain" />
              <span class="text-[11px] text-purple-600 font-bold truncate max-w-full">✓ {{ photo.name }}</span>
              <span class="text-[11px] text-gray-400">点击可重新选择</span>
            </template>
            <template v-else>
              <span class="text-3xl">🖼️</span>
              <span class="text-xs font-bold text-gray-600 group-hover:text-purple-600 transition-colors">选择照片</span>
              <span class="text-[11px] text-gray-400">点击选择图片</span>
            </template>
            <input type="file" accept="image/*" class="hidden" @change="pickPhoto" />
          </label>

          <!-- 表单 -->
          <div class="flex flex-col gap-3">
            <input
              v-model="title"
              type="text"
              placeholder="照片标题（如：杜塞尔多夫聚餐）"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-purple-400 transition-colors"
              maxlength="60"
            />
            <div class="space-y-2.5">
              <div v-for="g in groupedTypes" :key="g.name">
                <p class="text-[10px] font-bold tracking-wider text-gray-400 mb-1.5">{{ g.name }}</p>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="t in g.items"
                    :key="t.id"
                    type="button"
                    @click="type = t.id"
                    class="px-3.5 py-1.5 rounded-full text-xs font-bold border transition-colors"
                    :class="type === t.id
                      ? 'bg-purple-500 border-purple-500 text-white'
                      : 'bg-white border-gray-200 text-gray-500 hover:border-purple-300'"
                  >{{ t.label }}</button>
                </div>
              </div>
            </div>
            <input
              v-model="uploader"
              type="text"
              placeholder="你的制作人称号（选填）"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-purple-400 transition-colors"
              maxlength="30"
            />
            <button
              type="submit"
              class="w-full bg-purple-500 hover:bg-purple-600 text-white font-extrabold rounded-xl py-2.5 text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="submitting || !photo || !title.trim() || !type"
            >
              {{ submitting ? '提交中…' : '提交审核' }}
            </button>
          </div>
        </form>

        <Transition name="fade">
          <div v-if="submitMsg"
            class="mt-4 px-4 py-3 rounded-xl text-sm font-bold"
            :class="submitSuccess
              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
              : 'bg-red-50 text-red-700 border border-red-200'"
          >
            {{ submitMsg }}
          </div>
        </Transition>
      </div>
    </div>

    <!-- Filter -->
    <div class="bg-white border-b border-gray-100 px-4 py-3">
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
            <span class="text-[11px] text-gray-400">{{ item.type_label || item.type }}<template v-if="item.uploader"> · {{ item.uploader }}</template></span>
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
              <span class="text-xs text-gray-400">{{ lightbox.type_label || lightbox.type }}<template v-if="lightbox.uploader"> · {{ lightbox.uploader }}</template></span>
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

// 分类列表由后端 data/gallery_types.json 提供，加一场 live 不用改前端
const allTypes = ref([])

const gallery = ref([])
const loading = ref(true)
const activeFilter = ref('all')
const lightbox = ref(null)

// 投稿表单里按 group 分组展示
const groupedTypes = computed(() => {
  const groups = []
  for (const t of allTypes.value) {
    const name = t.group || '其他'
    let g = groups.find((x) => x.name === name)
    if (!g) groups.push((g = { name, items: [] }))
    g.items.push(t)
  }
  return groups
})

// 筛选栏只列出"确实有照片"的分类，免得一长串空按钮
const filters = computed(() => {
  const used = new Set(gallery.value.map((i) => i.type))
  return [
    { label: '全部', value: 'all' },
    ...allTypes.value.filter((t) => used.has(t.id)).map((t) => ({ label: t.label, value: t.id })),
  ]
})

const filtered = computed(() =>
  activeFilter.value === 'all' ? gallery.value : gallery.value.filter((i) => i.type === activeFilter.value)
)

// ── 投稿 ──────────────────────────────────────────────────────────────
const photo = ref(null)
const preview = ref('')
const title = ref('')
const type = ref('')
const uploader = ref('')
const submitting = ref(false)
const submitMsg = ref('')
const submitSuccess = ref(false)

function pickPhoto(e) {
  const file = e.target.files[0]
  if (!file) return
  photo.value = file
  if (preview.value) URL.revokeObjectURL(preview.value)
  preview.value = URL.createObjectURL(file)
}

function resetForm() {
  photo.value = null
  if (preview.value) URL.revokeObjectURL(preview.value)
  preview.value = ''
  title.value = ''
  type.value = ''
  uploader.value = ''
}

async function handleSubmit() {
  submitting.value = true
  submitMsg.value = ''
  try {
    const fd = new FormData()
    fd.append('photo', photo.value)
    fd.append('title', title.value.trim())
    fd.append('type', type.value)
    fd.append('uploader', uploader.value.trim())

    const r = await fetch('/api/gallery', { method: 'POST', body: fd })
    const body = await r.json()
    if (!r.ok || !body.success) throw new Error(body.error || '提交失败，请稍后再试')

    submitSuccess.value = true
    submitMsg.value = body.message
    resetForm()
  } catch (e) {
    submitSuccess.value = false
    submitMsg.value = e.message
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  try {
    const [photos, types] = await Promise.all([
      fetch('/api/gallery').then((r) => r.json()),
      fetch('/api/gallery/types').then((r) => r.json()),
    ])
    gallery.value = photos.data
    allTypes.value = types.data
  } catch {
    // 后端不可用时不再塞占位图，直接走空状态
    gallery.value = []
    allTypes.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>


