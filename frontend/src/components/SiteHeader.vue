<template>
  <header
    class="sticky top-0 z-50 transition-all duration-300"
    :class="scrolled
      ? 'bg-[#07091a]/98 backdrop-blur-md border-b border-white/8 shadow-lg shadow-black/30'
      : 'bg-[#07091a]/80 backdrop-blur-sm border-b border-white/0'"
  >
    <div class="max-w-7xl mx-auto px-4">
      <div
        class="flex items-center justify-between transition-all duration-300"
        :class="scrolled ? 'h-14' : 'h-16'"
      >

        <!-- ── Logo & Brand ───────────────────────────────────────────────────── -->
        <RouterLink
          to="/"
          class="flex items-center gap-3 shrink-0 group"
          aria-label="欧洲偶像大师同好会 · 主页"
        >
          <BrandLogo
            size="sm"
            class="opacity-90 group-hover:opacity-100 transition-opacity duration-300"
          />
        </RouterLink>

        <!-- ── Desktop Nav ────────────────────────────────────────────────────── -->
        <nav class="hidden md:flex items-center gap-0.5" role="navigation" aria-label="主导航">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="nav-link relative px-3 py-1.5 rounded-lg text-xs font-bold tracking-wide text-white/65 hover:text-white hover:bg-white/8 transition-all duration-150"
          >
            {{ link.label }}
          </RouterLink>
        </nav>

        <!-- ── Mobile Hamburger ───────────────────────────────────────────────── -->
        <button
          @click="mobileOpen = !mobileOpen"
          class="md:hidden p-2 rounded-lg hover:bg-white/10 active:bg-white/15 transition-colors text-white/70 hover:text-white"
          :aria-expanded="mobileOpen"
          aria-label="打开菜单"
        >
          <svg class="h-5 w-5 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              :d="mobileOpen
                ? 'M6 18L18 6M6 6l12 12'
                : 'M4 6h16M4 12h16M4 18h16'"
            />
          </svg>
        </button>
      </div>

      <!-- ── Mobile Menu ────────────────────────────────────────────────────── -->
      <Transition name="mobile-menu">
        <nav
          v-if="mobileOpen"
          class="md:hidden border-t border-white/10 pt-2 pb-4 grid grid-cols-2 gap-1"
          role="navigation"
          aria-label="移动端导航"
        >
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            @click="mobileOpen = false"
            class="mobile-nav-link px-3 py-2.5 rounded-xl text-xs font-bold text-white/65 hover:text-white hover:bg-white/10 active:bg-white/15 transition-colors flex items-center gap-1.5"
          >
            <span class="opacity-70">{{ link.icon }}</span>
            {{ link.label }}
          </RouterLink>
        </nav>
      </Transition>
    </div>
  </header>
</template>

<script setup>
import BrandLogo from './BrandLogo.vue'
import { ref, onMounted, onUnmounted } from 'vue'

// ── 滚动时缩小 ──
const scrolled = ref(false)

function handleScroll() {
  scrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// ── 移动端菜单开关 ──
const mobileOpen = ref(false)

// ── 导航项 ──
const navLinks = [
  { to: '/',               label: '主页',            icon: '🏠' },
  { to: '/announcements',  label: '活动公告',        icon: '📢' },
  { to: '/imas-calendar',  label: '偶像大师日历',    icon: '🎤' },
  { to: '/gallery',        label: '照片墙 Gallery',  icon: '🖼️' },
  { to: '/business-cards', label: '名片墙',          icon: '🪪' },
  { to: '/rules',          label: '规章 & 链接',     icon: '📋' },
]
</script>

<style scoped>
/* ── Active link ───────────────────────────────────────────────────────────── */
.nav-link.router-link-exact-active {
  color: #ffffff;
  background-color: rgba(255, 255, 255, 0.08);
}

.nav-link.router-link-exact-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 12px;
  right: 12px;
  height: 2px;
  background: #facc15;
  border-radius: 1px;
}

.mobile-nav-link.router-link-exact-active {
  color: #ffffff;
  background-color: rgba(250, 204, 21, 0.12);
  border-left: 2px solid #facc15;
}

/* ── Mobile menu animation ─────────────────────────────────────────────────── */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}
.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
