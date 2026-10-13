<template>
  <div class="relative min-h-screen bg-[#07091a] text-white overflow-x-hidden">

    <!-- ═══ 环境光 ═══════════════════════════════════════════════════════ -->
    <div aria-hidden="true" class="pointer-events-none fixed inset-0 z-0">
      <div class="absolute -top-40 -left-32 h-[34rem] w-[34rem] rounded-full blur-[140px] opacity-[0.18]"
        style="background: radial-gradient(circle, #e8434f 0%, transparent 70%)" />
      <div class="absolute top-1/3 -right-40 h-[38rem] w-[38rem] rounded-full blur-[150px] opacity-[0.14]"
        style="background: radial-gradient(circle, #60aac4 0%, transparent 70%)" />
      <div class="absolute bottom-0 left-1/3 h-[30rem] w-[30rem] rounded-full blur-[130px] opacity-[0.10]"
        style="background: radial-gradient(circle, #facc15 0%, transparent 70%)" />
    </div>

    <!-- ═══ 刊头 ═════════════════════════════════════════════════════════ -->
    <header class="relative layer-grain layer-grid border-b border-white/10">
      <div class="relative z-10 max-w-6xl mx-auto px-4 pt-16 pb-12 md:pt-24 md:pb-16">

        <div class="flex items-center gap-3 mb-8">
          <span class="h-px w-10 bg-yellow-400/60" />
          <p class="font-mono-num text-[11px] tracking-[0.35em] uppercase text-yellow-400/80">
            Event Index · 2026 / 2027
          </p>
        </div>

        <h1 class="font-display font-bold leading-[0.85] tracking-tight">
          <span class="block text-[clamp(2.75rem,11vw,7.5rem)] text-white">EUROPEAN</span>
          <span class="block text-[clamp(2.75rem,11vw,7.5rem)] text-white/25">ACG EVENTS</span>
        </h1>

        <p class="mt-8 max-w-xl text-sm leading-relaxed text-white/45">
          欧洲的超大型动漫、游戏与日本文化展会。日期、场馆与嘉宾信息均引自各展会官网，
          最终以主办方公告为准。
        </p>

        <dl class="mt-10 grid grid-cols-3 gap-px bg-white/10 border border-white/10 rounded-2xl overflow-hidden max-w-lg">
          <div v-for="s in stats" :key="s.label" class="bg-[#07091a] px-4 py-5">
            <dd class="font-mono-num text-3xl font-bold text-white">{{ s.value }}</dd>
            <dt class="mt-1 text-[10px] tracking-[0.2em] uppercase text-white/35">{{ s.label }}</dt>
          </div>
        </dl>
      </div>

      <!-- 跑马灯 -->
      <div class="marquee-host relative z-10 border-t border-white/10 py-3 overflow-hidden">
        <div class="marquee-track">
          <div v-for="pass in 2" :key="pass" class="flex shrink-0 items-center">
            <span v-for="e in items" :key="`${pass}-${e.id}`" class="flex items-center">
              <span class="font-display text-sm font-bold tracking-wide text-white/55 px-5">{{ e.title }}</span>
              <span class="font-mono-num text-[11px] text-white/25">{{ shortRange(e) }}</span>
              <span class="mx-5 text-white/15">◆</span>
            </span>
          </div>
        </div>
      </div>
    </header>

    <!-- ═══ 加载中 ═══════════════════════════════════════════════════════ -->
    <div v-if="loading" class="relative z-10 max-w-6xl mx-auto px-4 py-20 space-y-4">
      <div v-for="i in 5" :key="i" class="h-24 rounded-2xl bg-white/5 animate-pulse" />
    </div>

    <template v-else>
      <!-- ═══ 详解活动（有嘉宾名单的）══════════════════════════════════════ -->
      <section v-for="(ev, idx) in detailed" :key="ev.id" class="relative z-10 border-b border-white/10">
        <div class="max-w-6xl mx-auto px-4 py-16 md:py-24">

          <div v-reveal class="reveal flex flex-wrap items-center gap-4 mb-10">
            <span class="font-mono-num text-xs tracking-[0.3em] uppercase px-3 py-1.5 rounded-full border"
              :style="{ color: ev.accent, borderColor: ev.accent + '66', background: ev.accent + '14' }">
              {{ idx === 0 ? '▸ Next Up' : '▸ Also On' }}
            </span>
            <span class="font-mono-num text-xs text-white/50">
              {{ daysTo(ev) > 0 ? `距开展还有 ${daysTo(ev)} 天` : daysTo(ev) === 0 ? '今日开展' : '进行中 / 已开展' }}
            </span>
          </div>

          <div class="grid lg:grid-cols-[1.15fr,0.85fr] gap-10 lg:gap-14 items-start">

            <!-- 左：信息 -->
            <div v-reveal class="reveal">
              <div class="flex items-start gap-5">
                <span class="font-display text-6xl md:text-7xl font-bold leading-none text-transparent shrink-0"
                  style="-webkit-text-stroke: 1.5px rgba(255,255,255,0.22)">
                  {{ String(idx + 1).padStart(2, '0') }}
                </span>
                <div class="min-w-0">
                  <h2 class="font-display text-4xl md:text-6xl font-bold leading-[0.95] tracking-tight">
                    {{ ev.title }}
                  </h2>
                  <p v-if="ev.title_local" class="mt-2 text-sm text-white/40">{{ ev.title_local }}</p>
                </div>
              </div>

              <!-- 时间 / 地点 -->
              <div class="mt-10 grid sm:grid-cols-2 gap-px bg-white/10 border border-white/10 rounded-2xl overflow-hidden">
                <div class="bg-[#07091a] p-5">
                  <p class="text-[10px] tracking-[0.25em] uppercase text-white/30 mb-2">Date · 时间</p>
                  <p class="font-mono-num text-2xl font-bold" :style="{ color: ev.accent }">
                    {{ shortRange(ev) }}
                  </p>
                  <p class="font-mono-num text-xs text-white/40 mt-1">{{ yearOf(ev) }} · {{ weekdaySpan(ev) }}</p>
                </div>
                <div class="bg-[#07091a] p-5">
                  <p class="text-[10px] tracking-[0.25em] uppercase text-white/30 mb-2">Venue · 地点</p>
                  <p class="font-display text-base font-bold text-white leading-snug">{{ ev.venue }}</p>
                  <p class="text-xs text-white/45 mt-1 flex items-center gap-1.5">
                    <img :src="flagSrc(ev.country_code)" alt="" class="h-3 w-4 object-cover rounded-[2px]" />
                    {{ ev.city }}，{{ ev.country }}
                  </p>
                </div>
              </div>

              <p v-if="ev.highlight"
                class="mt-6 inline-flex items-center gap-2 text-xs font-bold px-3 py-1.5 rounded-lg border border-white/10 bg-white/5">
                <span :style="{ color: ev.accent }">★</span>{{ ev.highlight }}
              </p>

              <p class="mt-6 text-sm leading-relaxed text-white/55">{{ ev.summary }}</p>

              <div class="mt-8 flex flex-wrap gap-3">
                <RouterLink :to="`/announcements/${ev.id}`"
                  class="font-display inline-flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-bold text-[#07091a] transition-transform hover:-translate-y-0.5"
                  :style="{ backgroundColor: ev.accent }">
                  活动详情 <span aria-hidden="true">→</span>
                </RouterLink>
                <a :href="ev.external_link" target="_blank" rel="noopener"
                  class="font-display inline-flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-bold border border-white/15 text-white/80 hover:bg-white/5 hover:border-white/30 transition-colors">
                  官方网站 <span aria-hidden="true">↗</span>
                </a>
              </div>
            </div>

            <!-- 右：官方主视觉 -->
            <div v-reveal class="reveal">
              <figure class="relative">
                <div class="absolute -inset-4 rounded-[2rem] blur-2xl opacity-25"
                  :style="{ background: `radial-gradient(circle at 50% 30%, ${ev.accent}, transparent 70%)` }" />
                <div class="relative rounded-2xl overflow-hidden border border-white/12 bg-[#0b0e22]">
                  <img :src="ev.cover_image" :alt="`${ev.title} 官方主视觉`"
                    class="w-full object-cover" loading="lazy" @error="onImgError" />
                  <figcaption class="px-4 py-3 border-t border-white/10">
                    <p class="font-mono-num text-[10px] tracking-[0.2em] uppercase text-white/35">Key Visual</p>
                    <p class="text-[11px] text-white/50 mt-1">{{ ev.cover_credit || '官方主视觉' }}</p>
                  </figcaption>
                </div>
              </figure>
            </div>
          </div>

          <!-- ── 嘉宾 ─────────────────────────────────────────────────── -->
          <div v-if="ev.guests?.length" class="mt-20">
            <div v-reveal class="reveal flex items-end justify-between gap-4 mb-4 pb-4 border-b border-white/10">
              <div>
                <p class="font-mono-num text-[11px] tracking-[0.3em] uppercase text-white/35 mb-2">Guests</p>
                <h3 class="font-display text-2xl md:text-3xl font-bold">确认出席嘉宾</h3>
              </div>
              <span class="font-mono-num text-3xl font-bold text-white/15">
                {{ String(ev.guests.length).padStart(2, '0') }}
              </span>
            </div>

            <p v-if="ev.guests_note" class="text-xs leading-relaxed text-white/35 mb-8">{{ ev.guests_note }}</p>

            <!-- 有分组就按分组展示 -->
            <div v-for="section in guestSections(ev)" :key="section.label" class="mb-10 last:mb-0">
              <div v-if="section.label" class="flex items-center gap-3 mb-4">
                <span class="font-mono-num text-[11px] tracking-[0.2em] uppercase" :style="{ color: ev.accent }">
                  {{ section.label }}
                </span>
                <span class="flex-1 h-px bg-white/10" />
                <span class="font-mono-num text-[11px] text-white/25">{{ section.guests.length }}</span>
              </div>

              <ul class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
                <li v-for="(g, i) in section.guests" :key="g.name" v-reveal
                  class="reveal group relative rounded-2xl overflow-hidden border border-white/10 bg-[#0b0e22] hover:border-white/25 transition-colors"
                  :style="{ transitionDelay: `${Math.min(i, 8) * 45}ms` }">
                  <div class="overflow-hidden bg-[#10142c]"
                    :class="g.image ? 'aspect-[4/5]' : 'aspect-[3/2]'">
                    <img v-if="g.image" :src="g.image" :alt="g.name" loading="lazy" @error="onImgError"
                      class="w-full h-full object-cover grayscale-[65%] group-hover:grayscale-0 group-hover:scale-[1.04] transition-all duration-500" />
                    <!-- 无官方照片时用字体排版块 -->
                    <div v-else class="w-full h-full flex items-center justify-center"
                      :style="{ background: `radial-gradient(120% 120% at 30% 10%, ${ev.accent}2e 0%, transparent 62%), #10142c` }">
                      <span class="font-display text-4xl font-bold text-white/20 group-hover:text-white/35 transition-colors">
                        {{ initials(g.name) }}
                      </span>
                    </div>
                  </div>
                  <div class="p-3.5">
                    <p class="font-display text-sm font-bold leading-tight truncate">{{ g.name }}</p>
                    <p v-if="g.name_local" class="text-[11px] text-white/45 mt-0.5 truncate">{{ g.name_local }}</p>
                    <div class="mt-2 flex items-center gap-1.5 flex-wrap">
                      <span class="text-[10px] font-bold px-2 py-0.5 rounded-full border border-white/12 text-white/60">
                        {{ g.role }}
                      </span>
                    </div>
                    <p v-if="g.note" class="text-[10px] text-white/30 mt-1.5 leading-relaxed">{{ g.note }}</p>
                  </div>
                </li>
              </ul>
            </div>

            <p class="mt-6 font-mono-num text-[11px] text-white/30">
              嘉宾名单引自
              <a :href="ev.external_link" target="_blank" rel="noopener"
                class="underline decoration-white/20 hover:text-white/60">官网</a>，展前仍可能追加或变动。
            </p>
          </div>
        </div>
      </section>

      <!-- ═══ 其余活动索引 ═══════════════════════════════════════════════ -->
      <section v-if="rest.length" id="event-index" class="relative z-10 scroll-mt-20">
        <div class="max-w-6xl mx-auto px-4 py-14">
          <div class="flex items-center gap-4 mb-6">
            <h3 class="font-display text-2xl font-bold">更多大型展会</h3>
            <span class="flex-1 h-px bg-white/10" />
            <span class="font-mono-num text-xs text-white/30">{{ rest.length }}</span>
          </div>

          <ul class="border-t border-white/10">
            <li v-for="e in rest" :key="e.id" v-reveal class="reveal">
              <RouterLink :to="`/announcements/${e.id}`"
                class="group relative grid grid-cols-[auto,1fr,auto] sm:grid-cols-[auto,1.6fr,1fr,auto] items-center gap-4 sm:gap-6 py-6 border-b border-white/10 hover:bg-white/[0.03] transition-colors">
                <span class="absolute left-0 top-0 bottom-0 w-[2px] scale-y-0 group-hover:scale-y-100 origin-top transition-transform duration-300"
                  :style="{ backgroundColor: e.accent }" />

                <span class="font-mono-num text-xs text-white/25 w-7 pl-2 sm:pl-3">
                  {{ String(e.id).padStart(2, '0') }}
                </span>

                <div class="min-w-0">
                  <div class="flex items-center gap-2.5">
                    <img :src="flagSrc(e.country_code)" alt="" class="h-3 w-4 object-cover rounded-[2px] shrink-0" />
                    <h4 class="font-display text-lg sm:text-2xl font-bold truncate group-hover:translate-x-1 transition-transform">
                      {{ e.title }}
                    </h4>
                  </div>
                  <p class="text-xs text-white/40 mt-1.5 truncate">{{ e.venue }} · {{ e.city }}</p>
                  <p v-if="e.highlight" class="sm:hidden text-[11px] mt-1.5" :style="{ color: e.accent }">
                    ★ {{ e.highlight }}
                  </p>
                </div>

                <div class="hidden sm:block min-w-0">
                  <p class="font-mono-num text-base font-bold" :style="{ color: e.accent }">{{ shortRange(e) }}</p>
                  <p v-if="e.highlight" class="text-[11px] text-white/35 mt-1 truncate">★ {{ e.highlight }}</p>
                </div>

                <span class="font-mono-num text-xs text-white/25 group-hover:text-white transition-colors pr-1">
                  <span class="sm:hidden">{{ shortRange(e) }}</span>
                  <span class="hidden sm:inline" aria-hidden="true">→</span>
                </span>
              </RouterLink>
            </li>
          </ul>

          <p class="mt-14 font-mono-num text-[11px] leading-relaxed text-white/25">
            数据更新于 2026-10-13 · 日期、场馆与嘉宾信息引自各展会官网，主办方调整后以官网为准<br />
            所有活动名称、Logo 与图片版权归各主办方所有
          </p>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import fallbackEvents from '../data/eventsFallback'

const items = ref([])
const loading = ref(true)

/* ── 滚动进场指令 ──────────────────────────────────────────────────── */
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
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' })
    io.observe(el)
  },
}

/* ── 派生数据 ──────────────────────────────────────────────────────── */
const todayIso = () => {
  const now = new Date()
  const local = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
  return local.toISOString().slice(0, 10)
}

const sorted = computed(() =>
  [...items.value]
    .filter(e => (e.date_end || e.date_event) >= todayIso())
    .sort((a, b) => a.date_event.localeCompare(b.date_event))
)

/** 有嘉宾名单的活动做成完整详解版块 */
const detailed = computed(() => sorted.value.filter(e => e.guests?.length))
const rest = computed(() => sorted.value.filter(e => !e.guests?.length))

/** 嘉宾按 group 字段分组；没有分组字段就返回单组 */
const guestSections = (ev) => {
  const guests = ev.guests ?? []
  if (!guests.some(g => g.group)) return [{ label: '', guests }]
  const map = new Map()
  for (const g of guests) {
    const key = g.group || '其他'
    if (!map.has(key)) map.set(key, [])
    map.get(key).push(g)
  }
  return [...map].map(([label, list]) => ({ label, guests: list }))
}

const stats = computed(() => [
  { value: items.value.length, label: 'Events' },
  { value: new Set(items.value.map(e => e.country)).size, label: 'Countries' },
  { value: items.value.reduce((n, e) => n + (e.guests?.length ?? 0), 0), label: 'Guests' },
])

/* ── 格式化 ────────────────────────────────────────────────────────── */
const md = (iso) => iso.slice(5).replace('-', '.')
const shortRange = (e) => (e.date_end && e.date_end !== e.date_event)
  ? `${md(e.date_event)} — ${md(e.date_end)}`
  : md(e.date_event)
const yearOf = (e) => e.date_event.slice(0, 4)
const weekdaySpan = (e) => {
  const w = (iso) => new Date(iso + 'T00:00:00').toLocaleDateString('zh-CN', { weekday: 'short' })
  return e.date_end && e.date_end !== e.date_event ? `${w(e.date_event)} — ${w(e.date_end)}` : w(e.date_event)
}
const daysTo = (e) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return Math.round((new Date(e.date_event + 'T00:00:00') - today) / 86400000)
}

const flagSrc = (code) => `/assets/flags/${code || 'jp'}.svg`
const onImgError = (ev) => { ev.target.style.visibility = 'hidden' }

/** 无照片嘉宾用姓名首字母做排版块 */
const initials = (name) => (name || '')
  .split(/[\s.]+/)
  .filter(Boolean)
  .slice(0, 2)
  .map(w => w[0].toUpperCase())
  .join('')

onMounted(async () => {
  try {
    const r = await fetch('/api/announcements')
    items.value = (await r.json()).data
  } catch {
    // 后端未启动时用本地快照，页面依然完整
    items.value = fallbackEvents
  } finally {
    loading.value = false
  }
})
</script>
