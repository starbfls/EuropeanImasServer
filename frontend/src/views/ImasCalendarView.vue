<template>
  <div class="relative min-h-screen bg-[#07091a] text-white overflow-x-hidden">

    <!-- ═══ 环境光 ═══════════════════════════════════════════════════════ -->
    <div aria-hidden="true" class="pointer-events-none fixed inset-0 z-0">
      <div class="absolute -top-40 right-0 h-[32rem] w-[32rem] rounded-full blur-[140px] opacity-[0.16]"
        style="background: radial-gradient(circle, #ff7bac 0%, transparent 70%)" />
      <div class="absolute top-1/2 -left-40 h-[34rem] w-[34rem] rounded-full blur-[150px] opacity-[0.13]"
        style="background: radial-gradient(circle, #4fc3f7 0%, transparent 70%)" />
    </div>

    <!-- ═══ 刊头 ═════════════════════════════════════════════════════════ -->
    <header class="relative layer-grain layer-grid border-b border-white/10">
      <div class="relative z-10 max-w-6xl mx-auto px-4 pt-16 pb-12 md:pt-24 md:pb-14">
        <div class="flex items-center gap-3 mb-8">
          <span class="h-px w-10 bg-pink-400/60" />
          <p class="font-mono-num text-[11px] tracking-[0.35em] uppercase text-pink-300/80">
            Official Live Schedule
          </p>
        </div>

        <h1 class="font-display font-bold leading-[0.85] tracking-tight">
          <span class="block text-[clamp(2.5rem,10vw,6.5rem)] text-white">IDOLM@STER</span>
          <span class="block text-[clamp(2.5rem,10vw,6.5rem)] text-white/25">LIVE CALENDAR</span>
        </h1>

        <p class="mt-8 max-w-xl text-sm leading-relaxed text-white/45">
          日本官方的偶像大师系列演唱会与活动日程。时间为日本本地时间（JST），欧洲观看直播请自行换算时差
          （夏令时 −7 小时，冬令时 −8 小时）。
        </p>

        <!-- 下一场倒计时 -->
        <div v-if="next" class="mt-10 inline-flex flex-wrap items-center gap-x-5 gap-y-2 rounded-2xl border px-5 py-4"
          :style="{ borderColor: next.accent + '55', background: next.accent + '12' }">
          <img v-if="next.cover_image && !failedImages.has(next.id)" :src="next.cover_image"
            :alt="`${next.title_local || next.title} 官方主视觉`"
            class="h-12 w-20 shrink-0 rounded-lg object-cover border border-white/10"
            @error="failedImages.add(next.id)" />
          <span class="font-mono-num text-[10px] tracking-[0.3em] uppercase" :style="{ color: next.accent }">Next</span>
          <span class="font-display text-base font-bold">{{ next.title_local || next.title }}</span>
          <span class="font-mono-num text-sm" :style="{ color: next.accent }">{{ shortRange(next) }}</span>
          <span class="font-mono-num text-xs text-white/50">
            {{ daysTo(next) > 0 ? `还有 ${daysTo(next)} 天` : daysTo(next) === 0 ? '今日开演' : '进行中' }}
          </span>
        </div>
      </div>
    </header>

    <!-- ═══ 品牌筛选 ═════════════════════════════════════════════════════ -->
    <div class="sticky top-14 z-20 bg-[#07091a]/92 backdrop-blur-md border-b border-white/10">
      <div class="max-w-6xl mx-auto px-4 py-3 flex items-center gap-2 overflow-x-auto scrollbar-none">
        <span class="font-mono-num text-[10px] tracking-[0.2em] uppercase text-white/30 shrink-0 pr-1">Brand</span>
        <button v-for="b in brands" :key="b.label"
          @click="activeBrand = b.label"
          class="shrink-0 flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold border transition-colors"
          :class="activeBrand === b.label ? 'text-[#07091a]' : 'border-white/12 text-white/55 hover:text-white hover:border-white/30'"
          :style="activeBrand === b.label ? { backgroundColor: b.accent, borderColor: b.accent } : {}">
          <span v-if="b.accent && activeBrand !== b.label" class="h-1.5 w-1.5 rounded-full"
            :style="{ backgroundColor: b.accent }" />
          {{ b.label }}
        </button>
      </div>
    </div>

    <!-- ═══ 日历 ═════════════════════════════════════════════════════════ -->
    <section class="relative z-10 max-w-6xl mx-auto px-4 py-14">
      <div v-if="loading" class="space-y-4">
        <div v-for="i in 5" :key="i" class="h-48 md:h-44 rounded-2xl bg-white/5 animate-pulse" />
      </div>

      <template v-else>
        <div v-for="group in grouped" :key="group.key" class="mb-12 last:mb-0">
          <!-- 月份标头 -->
          <div class="flex items-center gap-4 mb-5">
            <div class="flex items-baseline gap-2">
              <span class="font-mono-num text-4xl md:text-5xl font-bold text-transparent leading-none"
                style="-webkit-text-stroke: 1.5px rgba(255,255,255,0.18)">{{ group.month }}</span>
              <span class="font-mono-num text-sm text-white/30">/ {{ group.year }}</span>
            </div>
            <span class="flex-1 h-px bg-white/10" />
            <span class="font-mono-num text-xs text-white/30">{{ group.events.length }}</span>
          </div>

          <!-- 公演卡片 -->
          <ul class="space-y-3">
            <li v-for="e in group.events" :key="e.id" v-reveal class="reveal">
              <article class="group relative overflow-hidden rounded-2xl border border-white/10 bg-[#0b0e22] hover:border-white/25 transition-colors">
                <span class="absolute left-0 top-0 bottom-0 w-[3px]" :style="{ backgroundColor: e.accent }" />

                <div class="grid md:grid-cols-[200px,minmax(0,1fr),auto] gap-4 md:gap-6 items-start p-5 pl-6">
                  <!-- 日期 + 官方主视觉 -->
                  <div class="space-y-3">
                    <div>
                      <p class="font-mono-num text-2xl font-bold leading-none" :style="{ color: e.accent }">
                        {{ shortRange(e) }}
                      </p>
                      <p class="font-mono-num text-[11px] text-white/35 mt-1.5">
                        {{ weekdaySpan(e) }} · JST
                      </p>
                    </div>

                    <a :href="e.link" target="_blank" rel="noopener"
                      class="block rounded-xl overflow-hidden border border-white/10 hover:border-white/25 transition-colors"
                      :title="e.cover_credit || '官方主视觉'">
                      <figure class="relative aspect-[16/10] bg-[#10142c]">
                        <img v-if="e.cover_image && !failedImages.has(e.id)" :src="e.cover_image"
                          :alt="`${e.title_local || e.title} 官方主视觉`" loading="lazy"
                          class="absolute inset-0 h-full w-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
                          @error="failedImages.add(e.id)" />
                        <!-- 无主视觉时退回品牌色块 -->
                        <div v-else class="absolute inset-0 flex items-center justify-center p-3 text-center"
                          :style="{ background: `radial-gradient(120% 120% at 25% 0%, ${e.accent}33 0%, transparent 62%), #10142c` }">
                          <span class="font-display text-xs font-bold leading-tight text-white/35">{{ e.brand_local }}</span>
                        </div>
                      </figure>
                    </a>
                  </div>

                  <!-- 主体 -->
                  <div class="min-w-0">
                    <div class="flex flex-wrap items-center gap-2 mb-2">
                      <span class="text-[10px] font-bold px-2 py-0.5 rounded-full border"
                        :style="{ color: e.accent, borderColor: e.accent + '55', background: e.accent + '14' }">
                        {{ e.brand_local }}
                      </span>
                      <span class="font-mono-num text-[10px] text-white/30 uppercase tracking-wider">{{ e.type }}</span>
                    </div>

                    <h3 class="font-display text-base md:text-lg font-bold leading-snug break-words">
                      {{ e.title }}
                    </h3>
                    <p v-if="e.title_local" class="text-xs text-white/45 mt-1">{{ e.title_local }}</p>

                    <p class="text-xs text-white/50 mt-3 flex items-start gap-1.5">
                      <svg class="h-3.5 w-3.5 mt-px shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                      <span>{{ e.venue }}<span v-if="e.venue_local" class="text-white/30"> · {{ e.venue_local }}</span>，{{ e.city }}</span>
                    </p>

                    <p v-if="e.note" class="text-xs text-white/40 mt-2 leading-relaxed">{{ e.note }}</p>
                  </div>

                  <!-- 倒计时 / 官网 -->
                  <div class="flex md:flex-col items-center md:items-end gap-3 md:gap-2 shrink-0">
                    <span class="font-mono-num text-[11px] px-2.5 py-1 rounded-full border border-white/10 text-white/45 whitespace-nowrap">
                      {{ daysTo(e) > 0 ? `D-${daysTo(e)}` : daysTo(e) === 0 ? 'TODAY' : '开演中' }}
                    </span>
                    <a :href="e.link" target="_blank" rel="noopener"
                      class="font-mono-num text-[11px] text-white/40 hover:text-white border-b border-transparent hover:border-white/40 transition-colors whitespace-nowrap">
                      官网 ↗
                    </a>
                  </div>
                </div>
              </article>
            </li>
          </ul>
        </div>

        <p v-if="filtered.length === 0" class="text-center py-20 text-white/30 text-sm">
          该品牌暂无已公布的公演。
        </p>

        <p class="mt-12 font-mono-num text-[11px] leading-relaxed text-white/25">
          数据更新于 2026-10-13 · 日程整理自
          <a href="https://idolmaster-official.jp/live_event/" target="_blank" rel="noopener"
            class="underline decoration-white/20 hover:text-white/60">偶像大师官方门户</a>
          、各公演官方网站及 ASOBI STAGE 官方页面，购票与最终日程请以官方公告为准<br />
          各公演主视觉取自对应官方网站，仅作活动识别用途<br />
          THE IDOLM@STER 及相关名称、主视觉版权归 BANDAI NAMCO Entertainment Inc. 所有
        </p>
      </template>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import imasFallback from '../data/imasFallback'

const items = ref([])
const loading = ref(true)
const activeBrand = ref('全部')
// 主视觉加载失败的活动 id，渲染时退回品牌色块
const failedImages = reactive(new Set())

const vReveal = {
  mounted(el) {
    if (!('IntersectionObserver' in window)) {
      el.classList.add('is-visible')
      return
    }
    const io = new IntersectionObserver(([entry], obs) => {
      if (entry.isIntersecting) {
        el.classList.add('is-visible')
        obs.unobserve(el)
      }
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' })
    io.observe(el)
  },
}

// 合同 / 对バン公演用 brands_local 列出参演品牌，让两边的品牌筛选都能找到它
const brandsOf = (e) => (e.brands_local?.length ? e.brands_local : [e.brand_local])

const localTodayIso = () => {
  const now = new Date()
  return new Date(now.getTime() - now.getTimezoneOffset() * 60000).toISOString().slice(0, 10)
}

// 后端数据未及时清理时，页面也不会继续展示已经结束的活动
const upcoming = computed(() => items.value.filter(e => (e.date_end || e.date_start) >= localTodayIso()))

const brands = computed(() => {
  const seen = new Map()
  // 先扫单品牌公演取色，免得合同公演的混合色顶掉品牌本色
  for (const collabPass of [false, true]) {
    for (const e of upcoming.value) {
      if (Boolean(e.brands_local?.length) !== collabPass) continue
      for (const label of brandsOf(e)) {
        if (!seen.has(label)) seen.set(label, e.accent)
      }
    }
  }
  return [{ label: '全部', accent: '#facc15' },
    ...[...seen].map(([label, accent]) => ({ label, accent }))]
})

const filtered = computed(() =>
  activeBrand.value === '全部'
    ? upcoming.value
    : upcoming.value.filter(e => brandsOf(e).includes(activeBrand.value))
)

const grouped = computed(() => {
  const byMonth = new Map()
  for (const e of [...filtered.value].sort((a, b) => a.date_start.localeCompare(b.date_start))) {
    const key = e.date_start.slice(0, 7)
    if (!byMonth.has(key)) byMonth.set(key, [])
    byMonth.get(key).push(e)
  }
  return [...byMonth.entries()].map(([key, events]) => ({
    key,
    year: key.slice(0, 4),
    month: key.slice(5, 7),
    events,
  }))
})

const next = computed(() => {
  return [...upcoming.value].sort((a, b) => a.date_start.localeCompare(b.date_start))[0] ?? null
})

const md = (iso) => iso.slice(5).replace('-', '.')
const shortRange = (e) => (e.date_end && e.date_end !== e.date_start)
  ? `${md(e.date_start)} — ${md(e.date_end)}`
  : md(e.date_start)

const weekdaySpan = (e) => {
  const w = (iso) => new Date(iso + 'T00:00:00').toLocaleDateString('zh-CN', { weekday: 'short' })
  return e.date_end && e.date_end !== e.date_start ? `${w(e.date_start)} — ${w(e.date_end)}` : w(e.date_start)
}

const daysTo = (e) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return Math.round((new Date(e.date_start + 'T00:00:00') - today) / 86400000)
}

onMounted(async () => {
  try {
    const r = await fetch('/api/imas-events')
    items.value = (await r.json()).data
  } catch {
    items.value = imasFallback
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.scrollbar-none {
  scrollbar-width: none;
}
.scrollbar-none::-webkit-scrollbar {
  display: none;
}
</style>
