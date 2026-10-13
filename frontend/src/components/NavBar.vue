<template>
  <nav class="bg-[#07091a]/95 backdrop-blur-md border-b border-white/5 text-white sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex items-center justify-between h-16">

        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-3 shrink-0 group">
          <img src="/logo.png" alt="Logo" class="h-9 w-9 object-contain opacity-90 group-hover:opacity-100 transition-opacity" />
          <div class="leading-tight">
            <p class="text-xs font-extrabold tracking-[0.15em] uppercase text-white/90">
              THE EUROPE<span class="text-yellow-400">@</span>N IDOLM<span class="text-yellow-400">@</span>STER UNION
            </p>
            <p class="text-[10px] font-medium text-white/40 tracking-widest">欧洲偶像大师制作人联盟</p>
          </div>
        </RouterLink>

        <!-- Desktop nav -->
        <div class="hidden md:flex items-center gap-1">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="nav-link px-3 py-1.5 rounded-lg text-xs font-bold tracking-wide text-white/70 hover:text-white hover:bg-white/8 transition-all"
          >
            {{ link.label }}
          </RouterLink>
        </div>

        <!-- Mobile hamburger -->
        <button
          @click="isOpen = !isOpen"
          class="md:hidden p-2 rounded-lg hover:bg-white/10 transition-colors"
          aria-label="菜单"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!isOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Mobile menu -->
      <Transition name="slide">
        <div v-if="isOpen" class="md:hidden pb-4 border-t border-white/10 mt-1 pt-3 grid grid-cols-2 gap-1">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            @click="isOpen = false"
            class="px-3 py-2 rounded-lg text-xs font-bold text-white/70 hover:text-white hover:bg-white/10 transition-colors"
          >
            {{ link.label }}
          </RouterLink>
        </div>
      </Transition>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const isOpen = ref(false)

const navLinks = [
  { to: '/', label: '主页' },
  { to: '/announcements', label: '活动公告' },
  { to: '/imas-calendar', label: '偶像大师日历' },
  { to: '/gallery', label: '照片墙 Gallery' },
  { to: '/business-cards', label: '名片墙' },
  { to: '/rules', label: '规章 & 链接' },
]
</script>

<style scoped>
.nav-link.router-link-exact-active {
  color: white;
  background-color: rgba(255, 255, 255, 0.08);
  border-bottom: 2px solid #facc15;
}
.slide-enter-active,
.slide-leave-active {
  transition: all 0.18s ease;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
