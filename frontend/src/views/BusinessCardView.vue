<template>
  <div class="min-h-screen bg-[#f9f8f6]">
    <!-- Header -->
    <div class="bg-[#07091a] border-b border-white/5 py-12 px-4">
      <div class="max-w-5xl mx-auto">
        <p class="text-emerald-400/70 text-xs tracking-[0.3em] uppercase mb-2">Business Card Wall</p>
        <h1 class="text-3xl font-extrabold text-white">名片墙</h1>
        <p class="text-white/40 text-sm mt-2">制作人名刺展示 — 悬停可翻面查看</p>
      </div>
    </div>

    <!-- Upload form -->
    <div class="bg-white border-b border-gray-100">
      <div class="max-w-5xl mx-auto px-4 py-8">
        <div class="flex items-start justify-between mb-5">
          <div>
            <h2 class="text-lg font-extrabold text-gray-900">上传你的名片</h2>
            <p class="text-xs text-gray-400 mt-1">上传正反两面，经审核后将展示在名片墙上。支持 JPG / PNG，单张不超过 5 MB。</p>
          </div>
          <span class="text-xs text-amber-600 bg-amber-50 border border-amber-200 px-3 py-1 rounded-full font-bold">需人工审核</span>
        </div>

        <form ref="formEl" @submit.prevent="handleSubmit" class="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
          <!-- Front upload -->
          <label class="flex flex-col items-center justify-center gap-2 border-2 border-dashed border-gray-200 rounded-2xl p-6 cursor-pointer hover:border-emerald-400 hover:bg-emerald-50/30 transition-colors group">
            <span class="text-3xl">🪪</span>
            <span class="text-xs font-bold text-gray-600 group-hover:text-emerald-600 transition-colors">上传名片正面</span>
            <span class="text-[11px] text-gray-400">点击选择图片</span>
            <input type="file" accept="image/*" class="hidden" @change="(e) => front = e.target.files[0]" />
            <span v-if="front" class="text-[11px] text-emerald-600 font-bold truncate max-w-full">✓ {{ front.name }}</span>
          </label>

          <!-- Back upload -->
          <label class="flex flex-col items-center justify-center gap-2 border-2 border-dashed border-gray-200 rounded-2xl p-6 cursor-pointer hover:border-emerald-400 hover:bg-emerald-50/30 transition-colors group">
            <span class="text-3xl">📋</span>
            <span class="text-xs font-bold text-gray-600 group-hover:text-emerald-600 transition-colors">上传名片背面</span>
            <span class="text-[11px] text-gray-400">点击选择图片</span>
            <input type="file" accept="image/*" class="hidden" @change="(e) => back = e.target.files[0]" />
            <span v-if="back" class="text-[11px] text-emerald-600 font-bold truncate max-w-full">✓ {{ back.name }}</span>
          </label>

          <!-- Submit -->
          <div class="flex flex-col gap-3">
            <input
              v-model="ownerName"
              type="text"
              placeholder="你的制作人称号（如：德国制P）"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-emerald-400 transition-colors"
              maxlength="30"
            />
            <input
              v-model="oshiName"
              type="text"
              placeholder="你推的偶像（选填）"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-emerald-400 transition-colors"
              maxlength="30"
            />
            <button
              type="submit"
              class="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-extrabold rounded-xl py-2.5 text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="submitting || !front || !back || !ownerName.trim()"
            >
              {{ submitting ? '提交中…' : '提交审核' }}
            </button>
          </div>
        </form>

        <!-- Success / Error message -->
        <Transition name="slide">
          <div v-if="submitMsg"
            class="mt-4 px-4 py-3 rounded-xl text-sm font-bold"
            :class="submitSuccess ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-red-50 text-red-700 border border-red-200'"
          >
            {{ submitMsg }}
          </div>
        </Transition>
      </div>
    </div>

    <!-- Card grid -->
    <div class="max-w-5xl mx-auto px-4 py-10">
      <h2 class="text-lg font-extrabold text-gray-900 mb-6">
        已展示名片
        <span class="text-sm font-normal text-gray-400 ml-2">共 {{ cards.length }} 张</span>
      </h2>

      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="animate-pulse">
          <div class="aspect-[7/4] bg-gray-200 rounded-2xl" />
          <div class="h-3 bg-gray-200 rounded mt-2 w-1/2" />
        </div>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="card in cards" :key="card.id" class="group">
          <!-- 翻转卡：比例按正反面里更"竖"的那张算，两面都用 contain，不裁图 -->
          <div
            class="card-flip-wrapper cursor-pointer"
            :style="{ aspectRatio: aspectOf(card.id, showBack(card.id) ? 'back' : 'front') }"
            @mouseenter="hovered = card.id"
            @mouseleave="hovered = null"
            @click="toggleFlip(card.id)"
          >
            <div class="card-flip-inner" :class="{ 'is-flipped': showBack(card.id) }">
              <!-- Front -->
              <div class="card-face card-front rounded-2xl overflow-hidden shadow-md bg-gray-100">
                <img :src="card.front" :alt="`${card.owner} 名片正面`"
                  class="w-full h-full object-contain"
                  :ref="(el) => measure(el, card.id, 'front')"
                  @load="(e) => measure(e.target, card.id, 'front')" />
              </div>
              <!-- Back -->
              <div class="card-face card-back rounded-2xl overflow-hidden shadow-md bg-gray-100">
                <img :src="card.back" :alt="`${card.owner} 名片背面`"
                  class="w-full h-full object-contain"
                  :ref="(el) => measure(el, card.id, 'back')"
                  @load="(e) => measure(e.target, card.id, 'back')" />
              </div>
            </div>
          </div>
          <div class="mt-2.5 flex items-center justify-between px-1">
            <p class="text-xs font-bold text-gray-700">{{ card.owner }}</p>
            <span class="text-[11px] text-gray-400">推：{{ card.oshi }}</span>
          </div>
        </div>
      </div>

      <div v-if="!loading && cards.length === 0" class="text-center py-20 text-gray-400 text-sm">
        暂无已审核的名片。成为第一个上传名片的制作人吧！
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'

const cards = ref([])
const loading = ref(true)
const front = ref(null)
const back = ref(null)
const ownerName = ref('')
const oshiName = ref('')
const formEl = ref(null)
const submitting = ref(false)
const submitMsg = ref('')
const submitSuccess = ref(false)

async function handleSubmit() {
  submitting.value = true
  submitMsg.value = ''
  try {
    const form = new FormData()
    form.append('front', front.value)
    form.append('back', back.value)
    form.append('owner', ownerName.value.trim())
    form.append('oshi', oshiName.value.trim())

    const r = await fetch('/api/business-cards', { method: 'POST', body: form })
    const body = await r.json()
    if (!r.ok || !body.success) throw new Error(body.error || '提交失败')

    submitSuccess.value = true
    submitMsg.value = body.message
    front.value = null
    back.value = null
    ownerName.value = ''
    oshiName.value = ''
    formEl.value?.reset()
  } catch (e) {
    submitSuccess.value = false
    submitMsg.value = `${e.message}，请稍后重试。`
  } finally {
    submitting.value = false
  }
}

// ── 卡片比例：名片有横版也有竖版，容器跟着当前显示的那一面走 ──────────
// 正反面比例一致时（绝大多数情况）翻面不会有任何尺寸变化；
// 只有正反朝向不同的卡片才会在翻面时改变高度，两面都能完整显示。
const DEFAULT_ASPECT = 7 / 4
const dims = reactive({})

// 走两条路：ref 回调覆盖"图片已在缓存里、load 早于监听器绑定"的情况，
// @load 覆盖正常网络加载。两边都调这个函数，重复写入同一个值无副作用。
function measure(el, id, side) {
  if (!el) return
  const { naturalWidth: w, naturalHeight: h } = el
  if (!w || !h) return
  const ratio = Math.min(Math.max(w / h, 0.5), 2.4)
  if (!dims[id]) dims[id] = {}
  if (dims[id][side] !== ratio) dims[id][side] = ratio
}

function aspectOf(id, side) {
  const d = dims[id]
  if (!d) return DEFAULT_ASPECT
  return d[side] ?? d.front ?? d.back ?? DEFAULT_ASPECT
}

// 翻面：桌面端悬停，触屏点击。两者都走同一个状态，
// 尺寸直接写成内联 style，避免 CSS 变量 + :hover 之间的层叠问题。
const flipped = reactive(new Set())
const hovered = ref(null)

const showBack = (id) => hovered.value === id || flipped.has(id)

function toggleFlip(id) {
  flipped.has(id) ? flipped.delete(id) : flipped.add(id)
}

onMounted(async () => {
  try {
    const r = await fetch('/api/business-cards')
    cards.value = (await r.json()).data
  } catch {
    // 后端不可用时不再塞占位图，直接走空状态
    cards.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.card-flip-wrapper {
  perspective: 900px;
  transition: aspect-ratio 0.55s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-flip-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transition: transform 0.55s cubic-bezier(0.4, 0, 0.2, 1);
}
.card-flip-inner.is-flipped { transform: rotateY(180deg); }

.card-face {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}
.card-back { transform: rotateY(180deg); }

.slide-enter-active, .slide-leave-active { transition: all 0.2s ease; }
.slide-enter-from, .slide-leave-to { opacity: 0; transform: translateY(-4px); }
</style>
