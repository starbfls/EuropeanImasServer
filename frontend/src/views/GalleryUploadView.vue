<template>
  <div class="min-h-screen bg-[#f9f8f6]">
    <header class="bg-[#07091a] px-4 py-8 md:py-10">
      <div class="mx-auto max-w-5xl">
        <RouterLink to="/gallery" class="inline-flex items-center gap-2 text-xs font-bold text-white/50 transition-colors hover:text-white">
          <span aria-hidden="true">←</span> 返回照片墙
        </RouterLink>
        <p class="mt-6 mb-2 text-xs uppercase tracking-[0.3em] text-purple-400/70">Share a moment</p>
        <h1 class="text-3xl font-extrabold text-white">上传照片</h1>
        <p class="mt-2 text-sm text-white/45">分享现地、展会和日常留影。无需注册，审核通过后展示在照片墙。</p>
      </div>
    </header>

    <div class="mx-auto max-w-5xl px-4 py-8 md:py-10">
      <section v-if="submitSuccess" role="status" class="rounded-2xl border border-emerald-200 bg-white px-6 py-12 text-center shadow-sm">
        <span class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-50 text-2xl text-emerald-600" aria-hidden="true">✓</span>
        <h2 class="mt-5 text-xl font-extrabold text-gray-900">照片已提交</h2>
        <p class="mt-3 text-sm leading-relaxed text-gray-500">{{ submitMsg }}</p>
        <div class="mt-7 flex flex-wrap justify-center gap-3">
          <RouterLink to="/gallery" class="rounded-full bg-purple-500 px-6 py-2.5 text-sm font-extrabold text-white transition-colors hover:bg-purple-600">返回照片墙</RouterLink>
          <button type="button" @click="continueUploading" class="rounded-full border border-gray-200 px-6 py-2.5 text-sm font-bold text-gray-600 transition-colors hover:border-purple-300 hover:text-purple-600">继续上传</button>
        </div>
      </section>

      <form v-else @submit.prevent="handleSubmit">
        <fieldset :disabled="submitting" class="grid min-w-0 gap-6 md:grid-cols-[minmax(0,1fr),minmax(0,1.2fr)]">
          <legend class="sr-only">上传照片与填写信息</legend>

          <section class="min-w-0 rounded-2xl border border-gray-100 bg-white p-5 shadow-sm md:p-6">
            <h2 class="text-sm font-extrabold text-gray-900"><span class="mr-2 text-purple-500">01</span>选择照片</h2>
            <p id="photo-hint" class="mt-2 text-xs leading-relaxed text-gray-400">支持 JPG / PNG / WEBP / GIF，单张不超过 8 MB。</p>
            <label class="relative mt-5 flex min-h-64 cursor-pointer flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed border-gray-200 bg-gray-50/50 p-5 text-center transition-colors hover:border-purple-400 hover:bg-purple-50/30 focus-within:border-purple-400 focus-within:ring-2 focus-within:ring-purple-200">
              <img v-if="preview" :src="preview" alt="待上传照片预览" class="max-h-80 max-w-full rounded-lg object-contain" />
              <svg v-else class="h-10 w-10 text-purple-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 4h16v16H4zM4 16l5-5 4 4 3-3 4 4M15 8h.01" />
              </svg>
              <span class="max-w-full break-all text-sm font-bold text-purple-600">{{ photo ? photo.name : '点击选择照片' }}</span>
              <span class="text-xs text-gray-400">{{ photo ? '点击可重新选择' : '选择一张你想分享的留影' }}</span>
              <input ref="fileInput" type="file" accept=".jpg,.jpeg,.png,.webp,.gif" aria-label="选择照片" aria-describedby="photo-hint" class="sr-only" @change="pickPhoto" />
            </label>
          </section>

          <section class="min-w-0 rounded-2xl border border-gray-100 bg-white p-5 shadow-sm md:p-6">
            <div class="flex flex-wrap items-center justify-between gap-3">
              <h2 class="text-sm font-extrabold text-gray-900"><span class="mr-2 text-purple-500">02</span>填写照片信息</h2>
              <span class="rounded-full border border-amber-200 bg-amber-50 px-2.5 py-1 text-[11px] font-bold text-amber-600">需人工审核</span>
            </div>

            <label for="photo-title" class="mt-6 block text-xs font-bold text-gray-600">照片标题 <span class="font-normal text-gray-400">必填</span></label>
            <input id="photo-title" v-model="title" type="text" required maxlength="60" placeholder="例如：伦敦 MCM 制作人合影"
              class="mt-2 w-full rounded-xl border border-gray-200 px-4 py-2.5 text-sm transition-colors focus:border-purple-400 focus:outline-none focus:ring-2 focus:ring-purple-100" />

            <fieldset class="mt-5 min-w-0">
              <legend class="text-xs font-bold text-gray-600">照片标签 <span class="font-normal text-gray-400">至少选择一项，可多选</span></legend>
              <p class="mt-2 text-[11px] leading-relaxed text-gray-400">再次点击可取消，支持跨分组选择，例如「学园现地 + mochi」。<span v-if="selectedTypes.length" class="ml-1 font-bold text-purple-600">已选 {{ selectedTypes.length }} 项</span></p>
              <p v-if="loadingTypes" role="status" class="mt-3 text-xs text-gray-400">正在加载标签…</p>
              <div v-else-if="typesError" role="alert" class="mt-3 rounded-xl border border-red-200 bg-red-50 p-3 text-xs leading-relaxed text-red-700">
                {{ typesError }}
                <button type="button" @click="loadTypes" class="ml-1 font-bold underline">重新加载标签</button>
              </div>
              <div v-else class="mt-3 space-y-3">
                <div v-for="group in groupedTypes" :key="group.name">
                  <p class="mb-1.5 text-[11px] font-bold text-gray-400">{{ group.name }}</p>
                  <div class="flex flex-wrap gap-2">
                    <button v-for="tag in group.items" :key="tag.id" type="button" :aria-pressed="selectedTypes.includes(tag.id)" @click="selectedTypes = toggleTag(selectedTypes, tag.id)"
                      class="rounded-full border px-3 py-1.5 text-xs font-bold transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-purple-400"
                      :class="selectedTypes.includes(tag.id) ? 'border-purple-500 bg-purple-500 text-white' : 'border-gray-200 bg-white text-gray-500 hover:border-purple-300'">
                      {{ tag.label }}
                    </button>
                  </div>
                </div>
              </div>
            </fieldset>

            <label for="photo-uploader" class="mt-5 block text-xs font-bold text-gray-600">制作人称号 <span class="font-normal text-gray-400">选填</span></label>
            <input id="photo-uploader" v-model="uploader" type="text" maxlength="30" placeholder="留空将以匿名制作人展示"
              class="mt-2 w-full rounded-xl border border-gray-200 px-4 py-2.5 text-sm transition-colors focus:border-purple-400 focus:outline-none focus:ring-2 focus:ring-purple-100" />

            <p v-if="submitMsg" role="alert" class="mt-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{{ submitMsg }}</p>
            <button type="submit" :disabled="submitting || !canSubmit"
              class="mt-6 w-full rounded-xl bg-purple-500 py-3 text-sm font-extrabold text-white transition-colors hover:bg-purple-600 disabled:cursor-not-allowed disabled:opacity-50">
              {{ submitting ? '正在上传，请稍候…' : '提交审核' }}
            </button>
            <p class="mt-3 text-xs leading-relaxed text-gray-400">请上传有权分享的照片。提交后需等待审核，暂时不会出现在照片墙。</p>
          </section>
        </fieldset>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { publicRequest } from '../api/public'
import { toggleTag } from '../utils/galleryTags'

const allTypes = ref([])
const loadingTypes = ref(true)
const typesError = ref('')
const fileInput = ref(null)
const photo = ref(null)
const preview = ref('')
const title = ref('')
const selectedTypes = ref([])
const uploader = ref('')
const submitting = ref(false)
const submitSuccess = ref(false)
const submitMsg = ref('')

const groupedTypes = computed(() => {
  const groups = new Map()
  for (const tag of allTypes.value) {
    const name = tag.group || '其他'
    if (!groups.has(name)) groups.set(name, [])
    groups.get(name).push(tag)
  }
  return [...groups].map(([name, items]) => ({ name, items }))
})

const canSubmit = computed(() => Boolean(photo.value && title.value.trim()
  && !loadingTypes.value && selectedTypes.value.length
  && selectedTypes.value.every(id => allTypes.value.some(tag => tag.id === id))))

function releasePreview() {
  if (preview.value) URL.revokeObjectURL(preview.value)
  preview.value = ''
}

function clearPhoto() {
  releasePreview()
  photo.value = null
  if (fileInput.value) fileInput.value.value = ''
}

function pickPhoto(event) {
  const file = event.target.files[0]
  if (!file) return
  submitMsg.value = ''
  if (file.size > 8 * 1024 * 1024) {
    clearPhoto()
    submitMsg.value = '单张图片不能超过 8 MB，请压缩后重新选择。'
    return
  }
  releasePreview()
  photo.value = file
  preview.value = URL.createObjectURL(file)
}

async function loadTypes() {
  loadingTypes.value = true
  typesError.value = ''
  try {
    allTypes.value = (await publicRequest('/api/gallery/types')).data
    if (!allTypes.value.length) throw new Error('暂时没有可用标签，请稍后重试。')
    selectedTypes.value = selectedTypes.value.filter(id => allTypes.value.some(tag => tag.id === id))
  } catch (error) {
    allTypes.value = []
    typesError.value = error.message
  } finally {
    loadingTypes.value = false
  }
}

async function handleSubmit() {
  if (submitting.value || !canSubmit.value) return
  submitting.value = true
  submitMsg.value = ''
  try {
    const form = new FormData()
    form.append('photo', photo.value)
    form.append('title', title.value.trim())
    for (const id of selectedTypes.value) form.append('types', id)
    form.append('uploader', uploader.value.trim())
    const body = await publicRequest('/api/gallery', { method: 'POST', body: form })
    submitMsg.value = body.message || '正在等待审核，审核通过后将展示在照片墙。'
    submitSuccess.value = true
    clearPhoto()
    title.value = ''
    selectedTypes.value = []
    uploader.value = ''
  } catch (error) {
    submitMsg.value = error.message
  } finally {
    submitting.value = false
  }
}

function continueUploading() {
  submitSuccess.value = false
  submitMsg.value = ''
}

onMounted(loadTypes)
onBeforeUnmount(releasePreview)
</script>
