<template>
  <footer class="bg-[#07091a] border-t border-white/8 text-white/50">
    <div class="max-w-7xl mx-auto px-4 py-12 grid grid-cols-1 md:grid-cols-4 gap-10">

      <!-- Brand -->
      <div class="md:col-span-2">
        <div class="flex items-center gap-3 mb-4">
          <img src="/logo.png" alt="Logo" class="h-8 w-8 object-contain opacity-80" />
          <p class="text-white font-extrabold text-xs tracking-widest uppercase">
            THE EUROPE<span class="text-yellow-400">@</span>N IDOLM<span class="text-yellow-400">@</span>STER UNION
          </p>
        </div>
        <p class="text-xs leading-relaxed text-white/40 max-w-sm">
          欧洲偶像大师制作人联盟，是由散布在欧洲各地的偶像大师爱好者自发组成的同好社群。<br />
          This is an unofficial fan community. Not affiliated with Bandai Namco Entertainment or BNSI.
        </p>
      </div>

      <!-- Quick links -->
      <div>
        <h3 class="text-white/80 font-bold text-xs uppercase tracking-wider mb-4">快速导航</h3>
        <ul class="space-y-2">
          <li v-for="link in navLinks" :key="link.to">
            <RouterLink :to="link.to" class="text-xs text-white/40 hover:text-white/80 transition-colors">
              {{ link.label }}
            </RouterLink>
          </li>
        </ul>
      </div>

      <!-- Community -->
      <div>
        <h3 class="text-white/80 font-bold text-xs uppercase tracking-wider mb-4">加入社群</h3>
        <div class="space-y-4">
          <!-- QQ group link -->
          <RouterLink to="/rules" class="flex items-center gap-2.5 group">
            <span class="w-7 h-7 rounded-lg bg-sky-500/80 flex items-center justify-center text-white text-xs font-black shrink-0">
              Q
            </span>
            <div>
              <p class="text-xs font-bold text-white/60 group-hover:text-white/90 transition-colors">QQ 制作人群</p>
              <p class="text-[11px] text-white/30">前往规章页面查看二维码</p>
            </div>
          </RouterLink>
          <!-- Discord -->
          <a href="#" class="flex items-center gap-2.5 group">
            <span class="w-7 h-7 rounded-lg bg-indigo-500/80 flex items-center justify-center text-white text-xs font-black shrink-0">
              D
            </span>
            <div>
              <p class="text-xs font-bold text-white/60 group-hover:text-white/90 transition-colors">Discord 服务器</p>
              <p class="text-[11px] text-white/30">European iMas Community</p>
            </div>
          </a>
        </div>
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="border-t border-white/5 py-4">
      <p class="text-center text-[11px] text-white/20">
        © {{ new Date().getFullYear() }} THE EUROPE@N IDOLM@STER UNION &nbsp;·&nbsp; 非官方粉丝社区 &nbsp;·&nbsp; Fan Community Site
      </p>
    </div>
  </footer>
</template>

<script setup>
const navLinks = [
  { to: '/', label: '主页' },
  { to: '/announcements', label: '活动公告' },
  { to: '/event-records', label: '活动记录' },
  { to: '/gallery', label: '照片墙 Gallery' },
  { to: '/business-cards', label: '名片墙' },
  { to: '/rules', label: '规章 & 链接' },
]
</script>
