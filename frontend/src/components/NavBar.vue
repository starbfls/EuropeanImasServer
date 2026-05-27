<template>
  <nav class="bg-gradient-to-r from-sky-600 to-blue-700 text-white shadow-lg sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4">
      <div class="flex items-center justify-between h-16">

        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-3 shrink-0">
          <img src="/logo.png" alt="EU iMas Logo" class="h-10 w-10 object-contain drop-shadow" />
          <div class="leading-tight">
            <p class="text-sm font-extrabold tracking-widest uppercase">
              THE EUROPE<span class="text-yellow-300">@</span>N
            </p>
            <p class="text-xs font-semibold text-sky-200 tracking-wider uppercase">
              IDOLM<span class="text-yellow-200">@</span>STER UNION
            </p>
          </div>
        </RouterLink>

        <!-- Desktop nav -->
        <div class="hidden md:flex items-center gap-1">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="px-4 py-2 rounded-lg text-sm font-bold tracking-wide transition-colors hover:bg-white/10 nav-link"
          >
            {{ link.label }}
          </RouterLink>
        </div>

        <!-- Mobile hamburger -->
        <button
          @click="isOpen = !isOpen"
          class="md:hidden p-2 rounded-lg hover:bg-sky-700 transition-colors"
          aria-label="Toggle menu"
        >
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!isOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Mobile dropdown -->
      <Transition name="slide">
        <div v-if="isOpen" class="md:hidden pb-3 flex flex-col gap-1">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            @click="isOpen = false"
            class="px-3 py-2 rounded-lg text-sm font-bold hover:bg-sky-700 transition-colors"
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
  { to: '/', label: 'Home' },
  { to: '/news', label: 'News' },
  { to: '/gallery', label: 'Gallery' },
  { to: '/rules', label: 'Rules & Links' },
]
</script>

<style scoped>
.nav-link.router-link-exact-active {
  background-color: rgba(255, 255, 255, 0.15);
  border-bottom: 2px solid white;
}
.slide-enter-active,
.slide-leave-active {
  transition: all 0.2s ease;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
