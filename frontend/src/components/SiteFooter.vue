<template>
  <footer class="bg-[#07091a] border-t border-white/8 text-white/50">
    <div class="max-w-7xl mx-auto px-4 py-12 grid grid-cols-1 md:grid-cols-4 gap-10">

      <!-- Brand -->
      <div class="md:col-span-2">
        <BrandLogo size="sm" align="start" class="mb-4 opacity-85" />
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
            <img src="/assets/brand/group-avatar.png" alt="群头像"
              class="w-8 h-8 rounded-full shrink-0 ring-1 ring-white/15 group-hover:ring-white/40 transition-all" />
            <div>
              <p class="text-xs font-bold text-white/60 group-hover:text-white/90 transition-colors">QQ 制作人群</p>
              <p class="text-[11px] text-white/30">前往规章页面查看二维码</p>
            </div>
          </RouterLink>
          <!-- Discord -->
          <RouterLink to="/discord" class="flex items-center gap-2.5 group">
            <span class="w-8 h-8 rounded-full bg-[#5865F2]/85 flex items-center justify-center shrink-0 ring-1 ring-white/10 group-hover:ring-white/35 transition-all">
              <svg class="h-4 w-4 text-white" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M20.3 4.4A19.8 19.8 0 0 0 15.4 3l-.3.5c1.6.4 2.9 1 4.2 1.9a14 14 0 0 0-12.6 0A13 13 0 0 1 11 3.5L10.7 3a19.8 19.8 0 0 0-5 1.4C2.6 9 1.8 13.4 2.2 17.8a19.9 19.9 0 0 0 6 3l1.2-1.8c-.7-.2-1.3-.5-1.9-.9l.4-.3a14.2 14.2 0 0 0 12.2 0l.4.3c-.6.4-1.2.7-1.9 1l1.2 1.7a19.9 19.9 0 0 0 6-3c.5-5.1-.8-9.5-3.5-13.4ZM8.9 15.1c-1.2 0-2.1-1.1-2.1-2.4S7.7 10.3 9 10.3s2.1 1.1 2.1 2.4-1 2.4-2.1 2.4Zm6.3 0c-1.2 0-2.1-1.1-2.1-2.4s.9-2.4 2.1-2.4 2.1 1.1 2.1 2.4-.9 2.4-2.1 2.4Z"/>
              </svg>
            </span>
            <div>
              <p class="text-xs font-bold text-white/60 group-hover:text-white/90 transition-colors">Discord 服务器</p>
              <p class="text-[11px] text-white/30">正在创建中</p>
            </div>
          </RouterLink>
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
import BrandLogo from './BrandLogo.vue'
const navLinks = [
  { to: '/', label: '主页' },
  { to: '/announcements', label: '活动公告' },
  { to: '/imas-calendar', label: '偶像大师日历' },
  { to: '/gallery', label: '照片墙 Gallery' },
  { to: '/business-cards', label: '名片墙' },
  { to: '/rules', label: '规章 & 链接' },
]
</script>
