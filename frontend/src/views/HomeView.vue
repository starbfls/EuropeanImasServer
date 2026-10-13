<template>
  <div>
    <!-- ── Hero ─────────────────────────────────────────────────────────────── -->
    <section class="relative isolate h-screen min-h-[620px] overflow-hidden select-none">
      <StarCanvas />

      <!-- Bottom-to-next-section fade -->
      <div class="absolute bottom-0 inset-x-0 h-32 bg-gradient-to-t from-[#07091a] to-transparent z-20 pointer-events-none" />

      <!-- ── 四位欧洲出身的偶像，各说各的母语 ── -->
      <div
        v-for="d in idols"
        :key="d.key"
        class="absolute bottom-0 flex-col group cursor-default"
        :class="[heroLayout[d.key].show, heroLayout[d.key].pos, heroLayout[d.key].align]"
        @mouseenter="bubble = d.key"
        @mouseleave="bubble = null"
      >
        <!-- 对话框独立于立绘层级，显示在中央 logo / 国旗条上方 -->
        <div class="relative z-40 mb-2 min-h-[24px] flex items-end" :class="heroLayout[d.key].bubble">
          <Transition name="pop" mode="out-in">
            <div
              v-if="bubble === d.key"
              key="bubble"
              :lang="d.lang"
              class="bg-white/95 backdrop-blur text-gray-800 text-[11px] rounded-2xl px-3.5 py-2.5 shadow-xl max-w-[196px] leading-relaxed border"
              :style="{ borderColor: d.accent + '99' }"
            >
              {{ d.greeting }}
              <span class="mt-1.5 flex items-center gap-1.5 text-[10px] font-bold" :style="{ color: d.accent }">
                <img :src="`/assets/flags/${d.cc}.svg`" :alt="d.country"
                  class="h-2.5 w-3.5 rounded-[1px] object-cover" />
                {{ d.name }}
              </span>
            </div>
            <p
              v-else
              key="plate"
              class="font-mono-num text-[10px] tracking-[0.2em] whitespace-nowrap text-white/28 flex items-center gap-1.5"
            >
              <img :src="`/assets/flags/${d.cc}.svg`" :alt="d.country"
                class="h-2.5 w-3.5 rounded-[1px] object-cover opacity-55" />
              {{ d.cc.toUpperCase() }}
            </p>
          </Transition>
        </div>

        <img
          :src="d.img" :alt="d.name"
          class="relative z-10 object-contain object-bottom drop-shadow-2xl transition-transform duration-500"
          :class="[heroLayout[d.key].size, bubble === d.key ? '-translate-y-2' : '']"
        />
      </div>

      <!-- ── 中央：艺术字 logo + 国旗细线 + 入口 ── -->
      <div class="relative z-30 flex flex-col items-center justify-center h-full text-center px-4 pb-16 pointer-events-none">
        <BrandLogo size="lg" class="drop-shadow-[0_0_46px_rgba(63,120,200,0.35)]" />

        <!-- 欧洲国旗拼成的一条细线 -->
        <FlagStrip class="mt-7 max-w-full" />

        <p class="mt-7 text-sm md:text-base text-white/45 tracking-wide">
          散布在欧洲各地的偶像大师制作人同好会
        </p>

        <div class="mt-9 flex flex-wrap gap-3 justify-center pointer-events-auto">
          <RouterLink
            to="/announcements"
            class="px-6 py-2.5 bg-eu-gold text-gray-900 rounded-full font-extrabold text-sm hover:bg-eu-gold-soft transition-colors shadow-lg shadow-eu-gold/25"
          >
            活动公告
          </RouterLink>
          <RouterLink
            to="/rules"
            class="px-6 py-2.5 border border-white/30 text-white/80 rounded-full font-bold text-sm hover:border-white/60 hover:text-white transition-colors backdrop-blur-sm"
          >
            加入我们
          </RouterLink>
        </div>

        <div class="absolute bottom-6 flex flex-col items-center gap-1 text-white/20 animate-bounce">
          <span class="font-mono-num text-[11px] tracking-widest">SCROLL</span>
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </div>
      </div>
    </section>

    <!-- ── 四大板块：首页的主角 ──────────────────────────────────────────── -->
    <section class="relative bg-[#07091a] layer-grain py-20 md:py-28 px-4 overflow-hidden">
      <!-- 四块主色的环境光 -->
      <div aria-hidden="true" class="pointer-events-none absolute inset-0">
        <div class="absolute -top-32 left-1/4 h-[30rem] w-[30rem] rounded-full blur-[150px] opacity-[0.13]"
          style="background: radial-gradient(circle, #3d8ee0 0%, transparent 70%)" />
        <div class="absolute -bottom-40 right-1/4 h-[30rem] w-[30rem] rounded-full blur-[150px] opacity-[0.11]"
          style="background: radial-gradient(circle, #f2994a 0%, transparent 70%)" />
      </div>

      <div class="relative z-10 max-w-6xl mx-auto">
        <div class="flex items-end justify-between gap-6 mb-12">
          <div>
            <p class="font-mono-num text-[11px] tracking-[0.35em] uppercase text-white/30 mb-3">Sections</p>
            <h2 class="font-display text-3xl md:text-4xl font-bold text-white">四个板块</h2>
          </div>
          <FlagStrip class="hidden md:flex pb-2 opacity-70" />
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-5">
          <RouterLink
            v-for="(entry, i) in quickEntries"
            :key="entry.to"
            :to="entry.to"
            class="group relative flex flex-col overflow-hidden rounded-2xl border border-white/10 bg-[#0b0e22] p-6 pt-7 transition-all duration-300 hover:-translate-y-1"
            :style="{ '--accent': entry.accent }"
          >
            <!-- 顶部一道主色，hover 时铺满 -->
            <span class="absolute inset-x-0 top-0 h-[3px] origin-left scale-x-[0.28] group-hover:scale-x-100 transition-transform duration-500"
              :style="{ backgroundColor: entry.accent }" />

            <!-- 巨大的描边序号 -->
            <span
              class="pointer-events-none absolute -right-2 -top-3 font-mono-num text-[5.5rem] font-bold leading-none text-transparent transition-all duration-500 group-hover:-top-1"
              :style="{ '-webkit-text-stroke': `1.5px ${entry.accent}`, opacity: 0.16 }"
            >{{ String(i + 1).padStart(2, '0') }}</span>

            <p class="font-mono-num text-[10px] tracking-[0.28em] uppercase transition-colors duration-300"
              :style="{ color: entry.accent }">{{ entry.en }}</p>

            <h3 class="font-display text-2xl font-bold text-white mt-3 leading-tight">{{ entry.label }}</h3>

            <p class="text-xs leading-relaxed text-white/40 mt-3 mb-8">{{ entry.desc }}</p>

            <span class="mt-auto inline-flex items-center gap-2 font-mono-num text-[11px] text-white/35 group-hover:text-white transition-colors">
              ENTER
              <span class="inline-block transition-transform duration-300 group-hover:translate-x-1.5">&rarr;</span>
            </span>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ── 最新活动公告 ──────────────────────────────────────────────────────── -->
    <section class="bg-[#0b0e22] py-16 md:py-20 px-4">
      <div class="max-w-6xl mx-auto">
        <div class="flex items-end justify-between gap-4 mb-8">
          <div>
            <p class="font-mono-num text-[11px] tracking-[0.3em] uppercase text-eu-gold/70 mb-2">
              Latest Announcements
            </p>
            <h2 class="font-display text-2xl md:text-3xl font-bold text-white">最新活动公告</h2>
          </div>
          <RouterLink to="/announcements"
            class="font-mono-num shrink-0 text-xs text-white/50 hover:text-white border-b border-white/20 hover:border-white transition-colors">
            查看全部 →
          </RouterLink>
        </div>

        <div v-if="loadingAnn" class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div v-for="i in 3" :key="i" class="rounded-2xl bg-white/5 animate-pulse h-64" />
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <RouterLink
            v-for="item in announcements"
            :key="item.id"
            :to="`/announcements/${item.id}`"
            class="group block rounded-2xl overflow-hidden border border-white/10 bg-[#07091a] hover:border-white/25 hover:-translate-y-0.5 transition-all duration-300"
          >
            <!-- 有官方主视觉就用图，没有就用字体排版块 -->
            <div class="h-40 overflow-hidden bg-[#07091a] relative">
              <img v-if="item.cover_image" :src="item.cover_image" :alt="item.title"
                class="w-full h-full object-cover opacity-75 group-hover:opacity-100 group-hover:scale-105 transition-all duration-500" />
              <div v-else class="w-full h-full flex items-end p-4 relative"
                :style="{ background: `radial-gradient(120% 120% at 15% 0%, ${item.accent || '#FFCC00'}33 0%, transparent 60%), #07091a` }">
                <span class="absolute top-3 right-3 font-mono-num text-[11px] text-white/30">
                  {{ (item.date_event || '').slice(0, 4) }}
                </span>
                <p class="font-display text-xl font-bold text-white/90 leading-tight group-hover:translate-x-1 transition-transform">
                  {{ item.title }}
                </p>
              </div>
            </div>
            <div class="p-5">
              <div class="flex items-center gap-2 mb-2.5">
                <span class="text-[10px] font-bold px-2 py-0.5 rounded-full border"
                  :style="{ color: item.accent || '#FFCC00',
                            borderColor: (item.accent || '#FFCC00') + '55',
                            background: (item.accent || '#FFCC00') + '14' }">
                  {{ item.category }}
                </span>
                <span class="font-mono-num text-[11px] text-white/30">{{ formatDate(item.date_event) }}</span>
              </div>
              <p class="font-display font-bold text-white text-sm leading-snug line-clamp-2">{{ item.title }}</p>
              <p class="text-xs text-white/40 mt-2 flex items-center gap-1.5">
                <svg class="h-3 w-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                {{ item.location }}
              </p>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ── 偶像大师活动日历 ──────────────────────────────────────────────────── -->
    <section class="bg-[#0b0e22] py-16 px-4">
      <div class="max-w-6xl mx-auto">
        <div class="flex items-end justify-between gap-4 mb-8">
          <div>
            <p class="font-mono-num text-[11px] tracking-[0.3em] uppercase text-pink-300/70 mb-2">
              Official Live Schedule
            </p>
            <h2 class="font-display text-2xl md:text-3xl font-bold text-white">偶像大师活动日历</h2>
            <p class="text-white/35 text-sm mt-2">日本官方演唱会与活动日程（JST）</p>
          </div>
          <RouterLink to="/imas-calendar"
            class="font-mono-num shrink-0 text-xs text-white/50 hover:text-white border-b border-white/20 hover:border-white transition-colors">
            全部日程 →
          </RouterLink>
        </div>

        <div v-if="loadingImas" class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div v-for="i in 3" :key="i" class="rounded-2xl bg-white/5 animate-pulse h-40" />
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <RouterLink
            v-for="item in imasEvents"
            :key="item.id"
            to="/imas-calendar"
            class="group relative block rounded-2xl overflow-hidden border border-white/10 bg-[#07091a] hover:border-white/25 transition-colors p-5"
          >
            <span class="absolute left-0 top-0 bottom-0 w-[3px]" :style="{ backgroundColor: item.accent }" />
            <div class="flex items-center gap-2 mb-3">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full border"
                :style="{ color: item.accent, borderColor: item.accent + '55', background: item.accent + '14' }">
                {{ item.brand_local }}
              </span>
              <span class="font-mono-num text-[10px] text-white/30 uppercase tracking-wider">{{ item.type }}</span>
            </div>
            <p class="font-mono-num text-xl font-bold" :style="{ color: item.accent }">
              {{ imasRange(item) }}
            </p>
            <p class="font-display text-sm font-bold text-white leading-snug mt-2.5 line-clamp-2">
              {{ item.title_local || item.title }}
            </p>
            <p class="text-xs text-white/40 mt-2 truncate">{{ item.venue_local || item.venue }}，{{ item.city }}</p>
          </RouterLink>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import StarCanvas from '../components/StarCanvas.vue'
import BrandLogo from '../components/BrandLogo.vue'
import FlagStrip from '../components/FlagStrip.vue'
import idols from '../data/idols'
import fallbackEvents from '../data/eventsFallback'
import imasFallback from '../data/imasFallback'

// ─── Data ─────────────────────────────────────────────────────────────────────
// hero 里被点亮的偶像 key，星座和立绘共用这一个状态
const bubble = ref(null)
const announcements = ref([])
const imasEvents = ref([])
const loadingAnn = ref(true)
const loadingImas = ref(true)

// 四人在 hero 里的站位；人物本身的数据在 data/idols.js
const heroLayout = {
  frederica: { show: 'hidden lg:flex', pos: 'left-0',      align: 'items-end',    size: 'h-[58vh] max-h-96', bubble: 'mr-4 rounded-bl-none' },
  emily:     { show: 'hidden xl:flex', pos: 'left-[14%]',  align: 'items-center', size: 'h-[49vh] max-h-80', bubble: 'rounded-bl-none' },
  shika:     { show: 'hidden xl:flex', pos: 'right-[14%]', align: 'items-center', size: 'h-[49vh] max-h-80', bubble: 'rounded-br-none' },
  lilja:     { show: 'hidden lg:flex', pos: 'right-0',     align: 'items-start',  size: 'h-[58vh] max-h-96', bubble: 'ml-4 rounded-br-none' },
}

// 主色取自 logo 里「欧洲活動部」四个字的配色
const quickEntries = [
  { to: '/announcements',  label: '活动公告',     en: 'Announcements',  accent: '#3d8ee0', desc: '近期欧洲日本文化活动、演出及展会资讯' },
  { to: '/imas-calendar',  label: '偶像大师日历', en: 'Live Calendar',  accent: '#f2c94c', desc: '日本官方演唱会与活动日程' },
  { to: '/gallery',        label: '照片墙',       en: 'Gallery',        accent: '#3fc9a0', desc: '聚会留影、痛车、祭坛与周边展示' },
  { to: '/business-cards', label: '名片墙',       en: 'Business Cards', accent: '#f2994a', desc: '制作人名刺展示，欢迎上传你的名片' },
]

const upcomingAnnouncements = (events) => {
  const now = new Date()
  const local = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
  const today = local.toISOString().slice(0, 10)
  return events
    .filter(e => (e.date_end || e.date_event) >= today)
    .sort((a, b) => a.date_event.localeCompare(b.date_event))
}

const upcomingImasEvents = (events) => {
  const now = new Date()
  const local = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
  const today = local.toISOString().slice(0, 10)
  return events
    .filter(e => (e.date_end || e.date_start) >= today)
    .sort((a, b) => a.date_start.localeCompare(b.date_start))
}

const FALLBACK_ANN = upcomingAnnouncements(fallbackEvents).slice(0, 3)
const FALLBACK_IMAS = upcomingImasEvents(imasFallback).slice(0, 3)


const formatDate = (d) =>
  new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })

const imasRange = (e) => {
  const md = (iso) => iso.slice(5).replace('-', '.')
  return e.date_end && e.date_end !== e.date_start ? `${md(e.date_start)} — ${md(e.date_end)}` : md(e.date_start)
}

onMounted(async () => {
  try {
    const r = await fetch('/api/announcements')
    announcements.value = upcomingAnnouncements((await r.json()).data).slice(0, 3)
  } catch { announcements.value = FALLBACK_ANN }
  finally { loadingAnn.value = false }

  try {
    const r = await fetch('/api/imas-events')
    imasEvents.value = upcomingImasEvents((await r.json()).data).slice(0, 3)
  } catch { imasEvents.value = FALLBACK_IMAS }
  finally { loadingImas.value = false }
})
</script>

<style scoped>
@keyframes pulse-slow {
  0%, 100% { opacity: 1; filter: drop-shadow(0 0 16px rgba(250,204,21,0.5)); }
  50%       { opacity: 0.85; filter: drop-shadow(0 0 32px rgba(250,204,21,0.8)); }
}
.animate-pulse-slow { animation: pulse-slow 3s ease-in-out infinite; }

.pop-enter-active { transition: all 0.18s cubic-bezier(.34,1.56,.64,1); }
.pop-leave-active { transition: all 0.12s ease; }
.pop-enter-from   { opacity: 0; transform: translateY(6px) scale(0.95); }
.pop-leave-to     { opacity: 0; transform: translateY(4px) scale(0.97); }
</style>
