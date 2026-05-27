<template>
  <footer class="bg-gray-900 text-gray-400 pt-12 pb-6 mt-auto">
    <div class="max-w-6xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-10">

      <!-- Brand -->
      <div>
        <p class="text-white font-extrabold text-sm tracking-widest uppercase mb-3">
          THE EUROPE<span class="text-yellow-400">@</span>N IDOLM<span class="text-yellow-400">@</span>STER UNION
        </p>
        <p class="text-xs leading-relaxed">
          A fan community for European producers to connect, share, and celebrate our love of iDOLM@STER. Not affiliated with Bandai Namco Entertainment or BNSI.
        </p>
      </div>

      <!-- Quick links -->
      <div>
        <h3 class="text-white font-bold text-xs uppercase tracking-wider mb-4">Quick Links</h3>
        <ul class="space-y-2">
          <li v-for="link in navLinks" :key="link.to">
            <RouterLink :to="link.to" class="text-xs hover:text-white transition-colors">
              {{ link.label }}
            </RouterLink>
          </li>
        </ul>
      </div>

      <!-- Community -->
      <div>
        <h3 class="text-white font-bold text-xs uppercase tracking-wider mb-4">Join the Community</h3>
        <div class="space-y-3">
          <a href="#" class="flex items-center gap-3 group hover:text-white transition-colors">
            <span class="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-xs font-bold shrink-0">D</span>
            <div>
              <p class="text-xs font-semibold group-hover:text-white transition-colors">Discord Server</p>
              <p class="text-xs text-gray-600">European iMas Community</p>
            </div>
          </a>
          <a href="#" class="flex items-center gap-3 group hover:text-white transition-colors">
            <span class="w-7 h-7 rounded-lg bg-sky-500 flex items-center justify-center text-white text-xs font-bold shrink-0">Q</span>
            <div>
              <p class="text-xs font-semibold group-hover:text-white transition-colors">QQ Group</p>
              <p class="text-xs text-gray-600">欧洲偶像大师制作人群</p>
            </div>
          </a>
        </div>
      </div>
    </div>

    <div class="max-w-6xl mx-auto px-4 mt-10 pt-6 border-t border-gray-800 text-center text-xs text-gray-600">
      © {{ new Date().getFullYear() }} THE EUROPE@N IDOLM@STER UNION — Fan Community Site
    </div>
  </footer>
</template>

<script setup>
const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/news', label: 'News' },
  { to: '/gallery', label: 'Gallery' },
  { to: '/rules', label: 'Rules & Links' },
]
</script>
