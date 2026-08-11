<template>
  <div>
    <!-- ── Hero ─────────────────────────────────────────────────────────────── -->
    <section class="relative h-screen min-h-[620px] overflow-hidden select-none">
      <StarCanvas />

      <!-- Bottom-to-next-section fade -->
      <div class="absolute bottom-0 inset-x-0 h-32 bg-gradient-to-t from-[#f9f8f6] to-transparent z-20 pointer-events-none" />

      <!-- ── Idol characters ── -->
      <!-- Frederica — far left -->
      <div
        class="absolute bottom-0 left-0 z-10 hidden lg:flex flex-col items-end group cursor-default"
        @mouseenter="bubble = 'frederica'"
        @mouseleave="bubble = null"
      >
        <Transition name="pop">
          <div
            v-if="bubble === 'frederica'"
            class="mb-2 mr-4 bg-white/95 backdrop-blur text-gray-800 text-xs rounded-2xl rounded-bl-none px-4 py-3 shadow-xl max-w-[180px] leading-relaxed border border-yellow-200/60"
          >
            星星们都在注视着你呢……制作人，欧洲的夜晚，芙蕾德莉卡一直等着你♡
            <span class="block mt-1 text-[10px] text-yellow-500 font-bold">— 宫本芙蕾德莉卡</span>
          </div>
        </Transition>
        <img src="/Frederica.png" alt="宫本芙蕾德莉卡"
          class="h-[62vh] max-h-96 object-contain object-bottom drop-shadow-2xl transition-transform duration-500 group-hover:-translate-y-2"
        />
      </div>

      <!-- Emily — inner left -->
      <div
        class="absolute bottom-0 left-[14%] z-10 hidden xl:flex flex-col items-center group cursor-default"
        @mouseenter="bubble = 'emily'"
        @mouseleave="bubble = null"
      >
        <Transition name="pop">
          <div
            v-if="bubble === 'emily'"
            class="mb-2 bg-white/95 backdrop-blur text-gray-800 text-xs rounded-2xl rounded-bl-none px-4 py-3 shadow-xl max-w-[180px] leading-relaxed border border-pink-200/60"
          >
            Smile♪ 制作人，欢迎来到我们的联盟！今天也要元气满满哦！☆
            <span class="block mt-1 text-[10px] text-pink-500 font-bold">— 艾米丽·斯图亚特</span>
          </div>
        </Transition>
        <img src="/emily.png" alt="艾米丽·斯图亚特"
          class="h-[52vh] max-h-80 object-contain object-bottom drop-shadow-2xl transition-transform duration-500 group-hover:-translate-y-2"
        />
      </div>

      <!-- Shika — inner right -->
      <div
        class="absolute bottom-0 right-[14%] z-10 hidden xl:flex flex-col items-center group cursor-default"
        @mouseenter="bubble = 'shika'"
        @mouseleave="bubble = null"
      >
        <Transition name="pop">
          <div
            v-if="bubble === 'shika'"
            class="mb-2 bg-white/95 backdrop-blur text-gray-800 text-xs rounded-2xl rounded-br-none px-4 py-3 shadow-xl max-w-[180px] leading-relaxed border border-sky-200/60"
          >
            制作人来啦——！诗花很高兴认识你！一起做好朋友吧？✿
            <span class="block mt-1 text-[10px] text-sky-500 font-bold">— 诗花</span>
          </div>
        </Transition>
        <img src="/shika.png" alt="诗花"
          class="h-[52vh] max-h-80 object-contain object-bottom drop-shadow-2xl transition-transform duration-500 group-hover:-translate-y-2"
        />
      </div>

      <!-- Lilja — far right -->
      <div
        class="absolute bottom-0 right-0 z-10 hidden lg:flex flex-col items-start group cursor-default"
        @mouseenter="bubble = 'lilja'"
        @mouseleave="bubble = null"
      >
        <Transition name="pop">
          <div
            v-if="bubble === 'lilja'"
            class="mb-2 ml-4 bg-white/95 backdrop-blur text-gray-800 text-xs rounded-2xl rounded-br-none px-4 py-3 shadow-xl max-w-[180px] leading-relaxed border border-purple-200/60"
          >
            欢迎，制作人。北方的极光，与星光一同为你闪耀。
            <span class="block mt-1 text-[10px] text-purple-500 font-bold">— 葛城莉莉娅</span>
          </div>
        </Transition>
        <img src="/lilja.png" alt="葛城莉莉娅"
          class="h-[62vh] max-h-96 object-contain object-bottom drop-shadow-2xl transition-transform duration-500 group-hover:-translate-y-2"
        />
      </div>

      <!-- ── Center content ── -->
      <div class="relative z-30 flex flex-col items-center justify-center h-full text-center px-4 pb-16">
        <img src="/logo.png" alt="Logo"
          class="w-[72vw] sm:w-[52vw] md:w-[38vw] lg:w-[28vw] max-w-[380px] h-auto object-contain drop-shadow-[0_0_40px_rgba(250,204,21,0.65)] mb-6 animate-pulse-slow"
        />

        <!-- Star decoration -->
        <div class="flex items-center gap-3 mb-4">
          <span class="text-yellow-400/60 text-lg">✦</span>
          <span class="text-white/30 text-xs tracking-[0.3em] uppercase font-medium">European Fan Community</span>
          <span class="text-yellow-400/60 text-lg">✦</span>
        </div>

        <h1 class="text-4xl md:text-6xl font-extrabold leading-tight tracking-tight text-white drop-shadow-lg">
          468 PRODUCTION
        </h1>
        <p class="mt-4 text-base md:text-lg text-white/50 font-medium tracking-[0.15em]">
          THE EUROPE<span class="text-yellow-400">@</span>N<br />
          IDOLM<span class="text-yellow-400">@</span>STER BRANCH
        </p>

        <div class="mt-10 flex flex-wrap gap-3 justify-center">
          <RouterLink
            to="/announcements"
            class="px-6 py-2.5 bg-yellow-400 text-gray-900 rounded-full font-extrabold text-sm hover:bg-yellow-300 transition-colors shadow-lg shadow-yellow-400/20"
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

        <!-- Scroll hint -->
        <div class="absolute bottom-6 flex flex-col items-center gap-1 text-white/20 animate-bounce">
          <span class="text-[11px] tracking-widest">SCROLL</span>
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </div>
      </div>
    </section>

    <!-- ── 快速入口 ──────────────────────────────────────────────────────────── -->
    <section class="bg-[#f9f8f6] py-16 px-4">
      <div class="max-w-6xl mx-auto">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <RouterLink
            v-for="entry in quickEntries"
            :key="entry.to"
            :to="entry.to"
            class="group relative overflow-hidden rounded-2xl p-6 flex flex-col gap-3 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
            :class="entry.bg"
          >
            <span class="text-3xl">{{ entry.icon }}</span>
            <div>
              <p class="font-extrabold text-white text-base leading-tight">{{ entry.label }}</p>
              <p class="text-white/60 text-xs mt-1">{{ entry.en }}</p>
            </div>
            <p class="text-white/75 text-xs leading-relaxed">{{ entry.desc }}</p>
            <span class="text-white/50 text-xs mt-auto group-hover:text-white/80 transition-colors">前往 →</span>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ── 最新活动公告 ──────────────────────────────────────────────────────── -->
    <section class="bg-white py-16 px-4">
      <div class="max-w-6xl mx-auto">
        <SectionHeading zh="最新活动公告" en="Latest Announcements" link="/announcements" />

        <div v-if="loadingAnn" class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div v-for="i in 3" :key="i" class="rounded-2xl bg-gray-100 animate-pulse h-56" />
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <RouterLink
            v-for="item in announcements"
            :key="item.id"
            :to="`/announcements/${item.id}`"
            class="group block rounded-2xl overflow-hidden border border-gray-100 hover:border-yellow-200 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300"
          >
            <div class="h-36 overflow-hidden bg-gray-900">
              <img :src="item.cover_image" :alt="item.title" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 group-hover:scale-105 transition-all duration-500" />
            </div>
            <div class="p-4">
              <div class="flex items-center gap-2 mb-2">
                <span class="text-[10px] font-extrabold px-2 py-0.5 rounded-full" :class="categoryColor(item.category)">
                  {{ item.category }}
                </span>
                <span class="text-xs text-gray-400">{{ formatDate(item.date_event) }}</span>
              </div>
              <p class="font-extrabold text-gray-900 text-sm leading-snug group-hover:text-yellow-700 transition-colors line-clamp-2">{{ item.title }}</p>
              <p class="text-xs text-gray-400 mt-1.5 flex items-center gap-1">
                <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                {{ item.location }}
              </p>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ── 最新活动记录 ──────────────────────────────────────────────────────── -->
    <section class="bg-[#f9f8f6] py-16 px-4">
      <div class="max-w-6xl mx-auto">
        <SectionHeading zh="最新活动记录" en="Event Records" link="/event-records" />

        <div v-if="loadingRec" class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div v-for="i in 3" :key="i" class="rounded-2xl bg-gray-200 animate-pulse h-64" />
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <RouterLink
            v-for="item in records"
            :key="item.id"
            :to="`/event-records/${item.id}`"
            class="group block bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300"
          >
            <div class="h-44 overflow-hidden">
              <img :src="item.cover_image" :alt="item.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
            </div>
            <div class="p-5">
              <div class="flex items-center gap-2 mb-2">
                <span class="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-sky-100 text-sky-700">{{ item.category }}</span>
                <span class="text-xs text-gray-400">{{ formatDate(item.date) }}</span>
              </div>
              <p class="font-extrabold text-gray-900 text-sm leading-snug group-hover:text-sky-700 transition-colors line-clamp-2">{{ item.title }}</p>
              <p class="text-xs text-gray-500 mt-2 line-clamp-2">{{ item.summary }}</p>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ── 欧洲制作人 ────────────────────────────────────────────────────────── -->
    <section class="bg-[#07091a] py-14 px-4 text-center">
      <div class="max-w-4xl mx-auto">
        <p class="text-white/30 text-xs tracking-[0.3em] uppercase mb-3">Our Community</p>
        <h2 class="text-2xl md:text-3xl font-extrabold text-white mb-3">
          散落在欧洲各地的制作人们
        </h2>
        <p class="text-white/40 text-sm leading-relaxed max-w-xl mx-auto mb-10">
          从北海之滨到地中海沿岸，偶像大师的歌声连接着每一位欧洲制作人。
          无论你身在哪个国家，这里都有你的位置。
        </p>
        <div class="flex flex-wrap justify-center gap-2">
          <span
            v-for="branch in branches"
            :key="branch.name"
            class="px-4 py-1.5 rounded-full text-xs font-bold border transition-colors"
            :class="branch.cls"
          >{{ branch.name }}</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import StarCanvas from '../components/StarCanvas.vue'

// ─── Inline heading component ─────────────────────────────────────────────────
const SectionHeading = {
  props: ['zh', 'en', 'link'],
  template: `
    <div class="flex items-end justify-between mb-8">
      <div>
        <p class="text-xs text-gray-400 tracking-widest uppercase mb-1">{{ en }}</p>
        <h2 class="text-2xl font-extrabold text-gray-900">{{ zh }}</h2>
      </div>
      <RouterLink :to="link" class="text-sm font-bold text-sky-500 hover:text-sky-700 transition-colors shrink-0">
        查看全部 →
      </RouterLink>
    </div>
  `,
}

// ─── Data ─────────────────────────────────────────────────────────────────────
const bubble = ref(null)
const announcements = ref([])
const records = ref([])
const loadingAnn = ref(true)
const loadingRec = ref(true)

const quickEntries = [
  { to: '/announcements', label: '活动公告', en: 'Announcements', icon: '📢', bg: 'bg-gradient-to-br from-amber-500 to-orange-600', desc: '近期欧洲日本文化活动、演出及展会资讯' },
  { to: '/event-records', label: '活动记录', en: 'Event Records', icon: '📖', bg: 'bg-gradient-to-br from-sky-500 to-blue-700', desc: '制作人聚会、观影、展会的图文实录' },
  { to: '/gallery', label: '照片墙', en: 'Gallery', icon: '🖼️', bg: 'bg-gradient-to-br from-purple-500 to-indigo-700', desc: '聚会留影、痛车、祭坛与周边展示' },
  { to: '/business-cards', label: '名片墙', en: 'Business Cards', icon: '🪪', bg: 'bg-gradient-to-br from-emerald-500 to-teal-700', desc: '制作人名刺展示，欢迎上传你的名片' },
]

const branches = [
  { name: '765 Pro', cls: 'border-orange-500/50 text-orange-300 hover:border-orange-400' },
  { name: '灰姑娘女孩', cls: 'border-pink-500/50 text-pink-300 hover:border-pink-400' },
  { name: '百万现场', cls: 'border-purple-500/50 text-purple-300 hover:border-purple-400' },
  { name: 'SideM', cls: 'border-blue-500/50 text-blue-300 hover:border-blue-400' },
  { name: '闪耀色彩', cls: 'border-sky-500/50 text-sky-300 hover:border-sky-400' },
  { name: '学园偶像大师', cls: 'border-yellow-500/50 text-yellow-300 hover:border-yellow-400' },
]

const FALLBACK_ANN = [
  { id: 1, title: 'AnimagiC 2026 - 曼海姆', date_event: '2026-08-28', category: '动漫展会', location: '曼海姆，德国', cover_image: 'https://placehold.co/800x400/1a2035/e8c547?text=AnimagiC+2026' },
  { id: 2, title: 'Japan Expo 2026 - 巴黎', date_event: '2026-07-02', category: '动漫展会', location: '巴黎，法国', cover_image: 'https://placehold.co/800x400/1a3520/e8c547?text=Japan+Expo+2026' },
  { id: 5, title: '制作人聚会 - 杜塞尔多夫', date_event: '2026-09-05', category: '制作人聚会', location: '杜塞尔多夫，德国', cover_image: 'https://placehold.co/800x400/0f1e35/e8c547?text=制作人聚会' },
]
const FALLBACK_REC = [
  { id: 1, title: '【聚会记录】2026年春 杜塞尔多夫制作人聚会', date: '2026-06-18', category: '聚会记录', summary: '六月的杜塞尔多夫，14位制作人第一次正式线下聚首。', cover_image: 'https://placehold.co/800x400/1a2035/60aac4?text=杜塞尔多夫聚会' },
  { id: 2, title: '【观影记录】Shiny Colors 阿姆斯特丹同步观影', date: '2026-05-25', category: '观影记录', summary: '12位制作人共同守候一场来自东京的演唱会直播。', cover_image: 'https://placehold.co/800x400/20103a/aa60c4?text=ShinyColors+观影' },
  { id: 3, title: '【展会记录】AnimagiC 2025 — 曼海姆见闻录', date: '2026-01-10', category: '展会记录', summary: '首次以联盟名义参加德国动漫展的完整体验报告。', cover_image: 'https://placehold.co/800x400/1a1530/60c4aa?text=AnimagiC+2025' },
]

const categoryColor = (cat) => {
  const map = {
    '动漫展会': 'bg-orange-100 text-orange-700',
    '声优活动': 'bg-pink-100 text-pink-700',
    '日本文化节': 'bg-indigo-100 text-indigo-700',
    '制作人聚会': 'bg-sky-100 text-sky-700',
    '音乐演出': 'bg-purple-100 text-purple-700',
  }
  return map[cat] ?? 'bg-gray-100 text-gray-700'
}

const formatDate = (d) =>
  new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })

onMounted(async () => {
  try {
    const r = await fetch('/api/announcements')
    announcements.value = (await r.json()).data.slice(0, 3)
  } catch { announcements.value = FALLBACK_ANN }
  finally { loadingAnn.value = false }

  try {
    const r = await fetch('/api/event-records')
    records.value = (await r.json()).data.slice(0, 3)
  } catch { records.value = FALLBACK_REC }
  finally { loadingRec.value = false }
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
