<template>
  <div class="relative min-h-screen bg-[#07091a] text-white">
    <div aria-hidden="true" class="pointer-events-none fixed inset-0 z-0">
      <div class="absolute -top-40 right-0 h-[32rem] w-[32rem] rounded-full blur-[140px] opacity-[0.16]"
        :style="{ background: `radial-gradient(circle, ${accent} 0%, transparent 70%)` }" />
    </div>

    <div class="relative z-10 max-w-4xl mx-auto px-4 py-10 md:py-14">
      <RouterLink to="/announcements"
        class="font-mono-num inline-flex items-center gap-2 text-xs tracking-wider text-white/45 hover:text-white mb-10 transition-colors">
        ← BACK TO INDEX
      </RouterLink>

      <!-- 加载中 -->
      <div v-if="loading" class="animate-pulse space-y-5">
        <div class="h-10 w-3/4 rounded bg-white/10" />
        <div class="h-4 w-1/3 rounded bg-white/10" />
        <div class="h-64 rounded-2xl bg-white/10" />
      </div>

      <article v-else-if="item">
        <!-- 标题 -->
        <div class="flex items-center gap-3 mb-5">
          <img :src="flagSrc" alt="" class="h-3.5 w-5 object-cover rounded-[2px]" />
          <span class="font-mono-num text-[11px] tracking-[0.25em] uppercase" :style="{ color: accent }">
            {{ item.category }}
          </span>
        </div>

        <h1 class="font-display text-4xl md:text-6xl font-bold leading-[0.95] tracking-tight">{{ item.title }}</h1>
        <p v-if="item.title_local" class="mt-3 text-sm text-white/40">{{ item.title_local }}</p>

        <!-- 时间 / 地点 -->
        <dl class="mt-9 grid sm:grid-cols-3 gap-px bg-white/10 border border-white/10 rounded-2xl overflow-hidden">
          <div class="bg-[#07091a] p-5">
            <dt class="text-[10px] tracking-[0.25em] uppercase text-white/30 mb-2">Date</dt>
            <dd class="font-mono-num text-xl font-bold" :style="{ color: accent }">{{ shortRange }}</dd>
            <dd class="font-mono-num text-xs text-white/40 mt-1">{{ item.date_event.slice(0, 4) }}</dd>
          </div>
          <div class="bg-[#07091a] p-5">
            <dt class="text-[10px] tracking-[0.25em] uppercase text-white/30 mb-2">Venue</dt>
            <dd class="font-display text-sm font-bold leading-snug">{{ item.venue || item.location }}</dd>
          </div>
          <div class="bg-[#07091a] p-5">
            <dt class="text-[10px] tracking-[0.25em] uppercase text-white/30 mb-2">City</dt>
            <dd class="font-display text-sm font-bold leading-snug">{{ item.city }}</dd>
            <dd class="text-xs text-white/40 mt-1">{{ item.country }}</dd>
          </div>
        </dl>

        <!-- 主视觉 -->
        <figure v-if="item.cover_image" class="mt-9 rounded-2xl overflow-hidden border border-white/12 bg-[#0b0e22]">
          <img :src="item.cover_image" :alt="`${item.title} 主视觉`" @error="hideImg"
            class="w-full max-h-[62vh] object-contain" />
          <figcaption v-if="item.cover_credit" class="px-4 py-3 border-t border-white/10 text-[11px] text-white/45">
            {{ item.cover_credit }}
          </figcaption>
        </figure>

        <p class="mt-9 text-base leading-relaxed text-white/60">{{ item.summary }}</p>

        <!-- 正文 -->
        <div v-if="rendered"
          class="mt-10 prose prose-invert prose-sm md:prose-base max-w-none
                 prose-headings:font-display prose-headings:font-bold
                 prose-p:text-white/60 prose-li:text-white/60 prose-strong:text-white
                 prose-a:no-underline prose-a:border-b prose-a:border-white/25 hover:prose-a:border-white
                 prose-hr:border-white/10"
          :style="{ '--tw-prose-links': accent }"
          v-html="rendered" />

        <!-- 嘉宾 -->
        <section v-if="item.guests?.length" class="mt-14">
          <div class="flex items-end justify-between gap-4 mb-6 pb-4 border-b border-white/10">
            <h2 class="font-display text-2xl font-bold">确认出席嘉宾</h2>
            <span class="font-mono-num text-2xl font-bold text-white/15">
              {{ String(item.guests.length).padStart(2, '0') }}
            </span>
          </div>
          <p v-if="item.guests_note" class="text-xs leading-relaxed text-white/35 mb-6">{{ item.guests_note }}</p>

          <div v-for="section in guestSections" :key="section.label" class="mb-8 last:mb-0">
            <div v-if="section.label" class="flex items-center gap-3 mb-4">
              <span class="font-mono-num text-[11px] tracking-[0.2em] uppercase" :style="{ color: accent }">
                {{ section.label }}
              </span>
              <span class="flex-1 h-px bg-white/10" />
              <span class="font-mono-num text-[11px] text-white/25">{{ section.guests.length }}</span>
            </div>

            <ul class="grid grid-cols-2 sm:grid-cols-3 gap-4">
              <li v-for="g in section.guests" :key="g.name"
                class="group rounded-2xl overflow-hidden border border-white/10 bg-[#0b0e22] hover:border-white/25 transition-colors">
                <div class="overflow-hidden bg-[#10142c]"
                    :class="g.image ? 'aspect-[4/5]' : 'aspect-[3/2]'">
                  <img v-if="g.image" :src="g.image" :alt="g.name" loading="lazy" @error="hideImg"
                    class="w-full h-full object-cover grayscale-[65%] group-hover:grayscale-0 transition-all duration-500" />
                  <div v-else class="w-full h-full flex items-center justify-center"
                    :style="{ background: `radial-gradient(120% 120% at 30% 10%, ${accent}2e 0%, transparent 62%), #10142c` }">
                    <span class="font-display text-3xl font-bold text-white/20">{{ initials(g.name) }}</span>
                  </div>
                </div>
                <div class="p-3.5">
                  <p class="font-display text-sm font-bold truncate">{{ g.name }}</p>
                  <p v-if="g.name_local" class="text-[11px] text-white/45 mt-0.5 truncate">{{ g.name_local }}</p>
                  <p class="text-[10px] text-white/35 mt-1.5">{{ g.role }}<span v-if="g.note"> · {{ g.note }}</span></p>
                </div>
              </li>
            </ul>
          </div>
        </section>

        <!-- 官网 -->
        <a v-if="item.external_link && item.external_link !== '#'"
          :href="item.external_link" target="_blank" rel="noopener"
          class="font-display mt-12 inline-flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-bold text-[#07091a] transition-transform hover:-translate-y-0.5"
          :style="{ backgroundColor: accent }">
          前往官方网站 <span aria-hidden="true">↗</span>
        </a>

        <!-- 标签 -->
        <div v-if="item.tags?.length" class="mt-10 flex flex-wrap gap-2">
          <span v-for="t in item.tags" :key="t"
            class="font-mono-num text-[11px] text-white/40 border border-white/10 px-3 py-1 rounded-full">#{{ t }}</span>
        </div>
      </article>

      <div v-else class="text-center py-24 text-white/40">
        <p class="font-display text-xl mb-5">未找到该活动。</p>
        <RouterLink to="/announcements" class="font-mono-num text-sm text-yellow-400">← 返回活动索引</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import fallbackEvents from '../data/eventsFallback'

const route = useRoute()
const item = ref(null)
const loading = ref(true)

const accent = computed(() => item.value?.accent || '#facc15')
const flagSrc = computed(() => `/assets/flags/${item.value?.country_code || 'jp'}.svg`)
const rendered = computed(() => (item.value?.content ? marked(item.value.content) : ''))

const shortRange = computed(() => {
  const e = item.value
  if (!e) return ''
  const md = (iso) => iso.slice(5).replace('-', '.')
  return e.date_end && e.date_end !== e.date_event ? `${md(e.date_event)} — ${md(e.date_end)}` : md(e.date_event)
})

/** 嘉宾按 group 字段分组；没有分组字段就返回单组 */
const guestSections = computed(() => {
  const guests = item.value?.guests ?? []
  if (!guests.some(g => g.group)) return [{ label: '', guests }]
  const map = new Map()
  for (const g of guests) {
    const key = g.group || '其他'
    if (!map.has(key)) map.set(key, [])
    map.get(key).push(g)
  }
  return [...map].map(([label, list]) => ({ label, guests: list }))
})

const initials = (name) => (name || '')
  .split(/[\s.]+/)
  .filter(Boolean)
  .slice(0, 2)
  .map(w => w[0].toUpperCase())
  .join('')

const hideImg = (ev) => { ev.target.style.visibility = 'hidden' }

onMounted(async () => {
  const id = Number(route.params.id)
  try {
    const r = await fetch(`/api/announcements/${id}`)
    const body = await r.json()
    item.value = body.success ? body.data : null
  } catch {
    // 后端未启动时退回本地快照（无正文）
    item.value = fallbackEvents.find(e => e.id === id) ?? null
  } finally {
    loading.value = false
  }
})
</script>
