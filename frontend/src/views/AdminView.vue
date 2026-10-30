<template>
  <div class="min-h-screen bg-[#f9f8f6]">
    <!-- Header -->
    <div class="bg-[#07091a] border-b border-white/5 py-12 px-4">
      <div class="max-w-5xl mx-auto flex items-end justify-between gap-4">
        <div>
          <p class="text-emerald-400/70 text-xs tracking-[0.3em] uppercase mb-2">Admin Panel</p>
          <h1 class="text-3xl font-extrabold text-white">投稿审核后台</h1>
          <p class="text-white/40 text-sm mt-2">审核访客上传的名片与照片，通过后展示在对应的墙上</p>
        </div>
        <button
          @click="handleLogout"
          class="shrink-0 text-xs font-bold text-white/60 hover:text-white border border-white/15 hover:border-white/30 rounded-lg px-3 py-1.5 transition-colors"
        >
          退出登录
        </button>
      </div>
    </div>

    <div class="max-w-5xl mx-auto px-4 py-10">
      <!-- 资源切换 -->
      <div class="flex items-center gap-2 mb-4">
        <button
          v-for="r in resources"
          :key="r.value"
          @click="switchResource(r.value)"
          class="px-4 py-2 rounded-xl text-xs font-extrabold transition-colors"
          :class="resource === r.value
            ? 'bg-gray-900 text-white'
            : 'bg-white text-gray-500 border border-gray-200 hover:border-gray-400'"
        >
          {{ r.label }}
        </button>
      </div>

      <!-- 状态筛选 -->
      <div class="flex flex-wrap items-center gap-2 mb-3">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          @click="switchTab(tab.value)"
          class="px-4 py-1.5 rounded-full text-xs font-bold transition-colors"
          :class="status === tab.value
            ? 'bg-emerald-500 text-white'
            : 'bg-white text-gray-500 border border-gray-200 hover:border-emerald-300'"
        >
          {{ tab.label }}
        </button>
        <button type="button" @click="load" :disabled="loading || busyId !== null"
          class="ml-auto px-3 py-1.5 text-xs font-bold text-gray-500 underline disabled:opacity-40">刷新列表</button>
      </div>

      <p class="mb-6 text-xs text-gray-400">待审核图片仅供管理员预览，链接过期时可刷新列表。</p>

      <p v-if="error" class="mb-5 px-4 py-3 rounded-xl text-sm font-bold bg-red-50 text-red-700 border border-red-200">
        {{ error }}
      </p>

      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div v-for="i in 4" :key="i" class="animate-pulse">
          <div class="h-40 bg-gray-200 rounded-2xl" />
        </div>
      </div>

      <div v-else-if="items.length === 0" class="text-center py-20 text-gray-400 text-sm">
        {{ status === 'pending' ? '没有待审核的投稿。' : '这里还没有内容。' }}
      </div>

      <!-- 名片 -->
      <div v-else-if="resource === 'cards'" class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div v-for="card in items" :key="card.id" class="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <p class="text-[11px] font-bold text-gray-400 mb-1.5">正面</p>
              <a :href="card.front" target="_blank" rel="noopener">
                <img :src="card.front" :alt="`${card.owner} 名片正面`"
                  class="w-full aspect-[7/4] object-contain bg-gray-50 rounded-xl border border-gray-100 hover:opacity-90 transition-opacity" />
              </a>
            </div>
            <div>
              <p class="text-[11px] font-bold text-gray-400 mb-1.5">背面</p>
              <a :href="card.back" target="_blank" rel="noopener">
                <img :src="card.back" :alt="`${card.owner} 名片背面`"
                  class="w-full aspect-[7/4] object-contain bg-gray-50 rounded-xl border border-gray-100 hover:opacity-90 transition-opacity" />
              </a>
            </div>
          </div>

          <div class="mt-4 flex items-start justify-between gap-3">
            <div class="min-w-0">
              <p class="text-sm font-extrabold text-gray-900 truncate">{{ card.owner }}</p>
              <p class="text-[11px] text-gray-400 mt-0.5">
                推：{{ card.oshi }}
                <span v-if="card.submitted_at"> · {{ card.submitted_at.replace('T', ' ') }}</span>
              </p>
            </div>
            <StatusPill :approved="card.approved" />
          </div>

          <ReviewActions :item="card" :busy="busyId === card.id"
            @approve="handleApprove(card)" @remove="handleDelete(card, `「${card.owner}」的名片`)" />
        </div>
      </div>

      <!-- 照片 -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="photo in items" :key="photo.id" class="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm">
          <a :href="photo.url" target="_blank" rel="noopener" class="block">
            <img :src="photo.thumbnail || photo.url" :alt="photo.title"
              class="w-full aspect-[4/3] object-contain bg-gray-50 rounded-xl border border-gray-100 hover:opacity-90 transition-opacity" />
          </a>

          <div class="mt-4 flex items-start justify-between gap-3">
            <div class="min-w-0">
              <p class="text-sm font-extrabold text-gray-900 truncate">{{ photo.title }}</p>
              <p class="text-[11px] text-gray-400 mt-0.5">
                {{ photo.type_label || photo.type }} · {{ photo.uploader }}
                <span v-if="photo.submitted_at"> · {{ photo.submitted_at.replace('T', ' ') }}</span>
              </p>
            </div>
            <StatusPill :approved="photo.approved" />
          </div>

          <ReviewActions :item="photo" :busy="busyId === photo.id"
            @approve="handleApprove(photo)" @remove="handleDelete(photo, `照片「${photo.title}」`)" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, h, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  approveCard, approvePhoto, clearToken,
  deleteCard, deletePhoto, listCards, listPhotos,
} from '../api/admin'

const router = useRouter()

// ── 两个小的展示组件，名片和照片共用 ──────────────────────────────────
const StatusPill = (props) =>
  h('span', {
    class: 'shrink-0 text-[11px] font-bold px-2.5 py-1 rounded-full border ' +
      (props.approved
        ? 'text-emerald-600 bg-emerald-50 border-emerald-200'
        : 'text-amber-600 bg-amber-50 border-amber-200'),
  }, props.approved ? '已通过' : '待审核')
StatusPill.props = ['approved']

const ReviewActions = (props, { emit }) =>
  h('div', { class: 'mt-4 flex gap-2' }, [
    props.item.approved ? null : h('button', {
      onClick: () => emit('approve'),
      disabled: props.busy,
      class: 'flex-1 bg-emerald-500 hover:bg-emerald-600 text-white font-extrabold rounded-xl py-2 text-xs transition-colors disabled:opacity-40',
    }, '通过审核'),
    h('button', {
      onClick: () => emit('remove'),
      disabled: props.busy,
      class: 'flex-1 bg-white hover:bg-red-50 text-red-600 border border-red-200 font-extrabold rounded-xl py-2 text-xs transition-colors disabled:opacity-40',
    }, props.item.approved ? '下架删除' : '驳回删除'),
  ])
ReviewActions.props = ['item', 'busy']
ReviewActions.emits = ['approve', 'remove']

// ── 状态 ──────────────────────────────────────────────────────────────
const resources = [
  { value: 'cards', label: '名片墙' },
  { value: 'photos', label: '照片墙' },
]
const tabs = [
  { value: 'pending', label: '待审核' },
  { value: 'approved', label: '已通过' },
  { value: 'all', label: '全部' },
]

const items = ref([])
const resource = ref('cards')
const status = ref('pending')
const loading = ref(true)
const busyId = ref(null)
const error = ref('')
let previewTimer
let loadVersion = 0

const api = computed(() =>
  resource.value === 'cards'
    ? { list: listCards, approve: approveCard, remove: deleteCard }
    : { list: listPhotos, approve: approvePhoto, remove: deletePhoto }
)

function handleError(e) {
  if (e.status === 401) {
    router.replace('/admin/login')
    return
  }
  error.value = e.message
}

async function load() {
  const version = ++loadVersion
  clearTimeout(previewTimer)
  loading.value = true
  error.value = ''
  try {
    const rows = await api.value.list(status.value)
    if (version !== loadVersion) return
    items.value = rows
    const expiry = Math.min(...rows.filter(item => item.preview_expires_in).map(item => item.preview_expires_in))
    if (Number.isFinite(expiry)) previewTimer = setTimeout(load, Math.max(30, expiry - 60) * 1000)
  } catch (e) {
    if (version === loadVersion) handleError(e)
  } finally {
    if (version === loadVersion) loading.value = false
  }
}

function switchResource(value) {
  resource.value = value
  load()
}

function switchTab(value) {
  status.value = value
  load()
}

async function handleApprove(item) {
  busyId.value = item.id
  try {
    await api.value.approve(item.id)
    await load()
  } catch (e) {
    handleError(e)
  } finally {
    busyId.value = null
  }
}

async function handleDelete(item, label) {
  if (!confirm(`确定删除${label}？存储中的图片也会一并删除。`)) return
  busyId.value = item.id
  try {
    await api.value.remove(item.id)
    await load()
  } catch (e) {
    handleError(e)
  } finally {
    busyId.value = null
  }
}

function handleLogout() {
  clearToken()
  router.replace('/admin/login')
}

onMounted(load)
onUnmounted(() => {
  ++loadVersion
  clearTimeout(previewTimer)
})
</script>
