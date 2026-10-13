<template>
  <div class="relative min-h-screen bg-[#07091a] text-white overflow-hidden layer-grain">
    <!-- 环境光 -->
    <div aria-hidden="true" class="pointer-events-none absolute inset-0">
      <div class="absolute -top-40 left-1/3 h-[34rem] w-[34rem] rounded-full blur-[150px] opacity-[0.15]"
        style="background: radial-gradient(circle, #5865F2 0%, transparent 70%)" />
      <div class="absolute -bottom-40 right-1/4 h-[30rem] w-[30rem] rounded-full blur-[150px] opacity-[0.1]"
        style="background: radial-gradient(circle, #FFCC00 0%, transparent 70%)" />
    </div>

    <section class="relative z-10 max-w-4xl mx-auto px-4 py-20 md:py-28">
      <div class="grid md:grid-cols-[1fr,auto] gap-10 md:gap-14 items-center">
        <!-- ── 文案 ── -->
        <div>
          <div class="flex items-center gap-3 mb-6">
            <span class="h-px w-10 bg-[#5865F2]/70" />
            <p class="font-mono-num text-[11px] tracking-[0.35em] uppercase text-[#8b93f7]">Discord</p>
          </div>

          <h1 class="font-display font-bold leading-[0.95] tracking-tight">
            <span class="block text-[clamp(2.5rem,8vw,4.5rem)] text-white">正在创建中</span>
            <span class="block text-[clamp(1.1rem,3vw,1.8rem)] text-white/25 mt-2">Under Construction</span>
          </h1>

          <p class="mt-8 max-w-md text-sm leading-relaxed text-white/45">
            欧洲 iM@S Discord 服务器还在搭建，频道分区和规则整理好之后会第一时间在这里放出邀请链接。
            在那之前，欢迎先加入 QQ 制作人群，和大家一起等。
          </p>

          <!-- 进度条 -->
          <div class="mt-9 max-w-sm">
            <div class="flex items-baseline justify-between mb-2">
              <span class="font-mono-num text-[10px] tracking-[0.25em] uppercase text-white/30">Setup</span>
              <span class="font-mono-num text-[11px] text-[#8b93f7]">施工中</span>
            </div>
            <div class="h-1.5 rounded-full bg-white/8 overflow-hidden">
              <div class="progress h-full rounded-full bg-gradient-to-r from-[#5865F2] to-[#8b93f7]" />
            </div>
          </div>

          <div class="mt-10 flex flex-wrap gap-3">
            <RouterLink
              to="/rules"
              class="px-6 py-2.5 bg-eu-gold text-gray-900 rounded-full font-extrabold text-sm hover:bg-eu-gold-soft transition-colors shadow-lg shadow-eu-gold/25"
            >
              先加 QQ 群
            </RouterLink>
            <RouterLink
              to="/"
              class="px-6 py-2.5 border border-white/20 text-white/75 rounded-full font-bold text-sm hover:border-white/50 hover:text-white transition-colors"
            >
              返回主页
            </RouterLink>
          </div>
        </div>

        <!-- ── 莉莉娅 Q 版立绘 ── -->
        <div class="justify-self-center md:justify-self-end order-first md:order-none">
          <div class="relative">
            <div class="absolute inset-x-4 bottom-2 h-10 rounded-full blur-2xl opacity-40"
              style="background: radial-gradient(ellipse, #5865F2 0%, transparent 70%)" />
            <div class="relative float h-56 w-36 md:h-80 md:w-52 overflow-hidden">
              <img
                :src="liljaSd"
                alt="葛城莉莉娅 Q 版立绘"
                width="1500"
                height="2000"
                class="absolute top-[-30%] left-1/2 -translate-x-1/2 h-[150%] w-auto max-w-none drop-shadow-[0_18px_28px_rgba(0,0,0,0.45)]"
              />
            </div>
          </div>
          <p class="mt-4 text-center font-mono-num text-[10px] tracking-[0.25em] uppercase text-white/25">
            Coming soon
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import liljaSd from '../../Katsuragi_Lilja_SD.png'
</script>

<style scoped>
/* 进度条来回跑，表示"在做但还没做完" */
.progress {
  width: 38%;
  animation: crawl 3.2s ease-in-out infinite;
}
@keyframes crawl {
  0%,
  100% { margin-left: 0; }
  50%  { margin-left: 62%; }
}

.float { animation: float 4s ease-in-out infinite; }
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-9px); }
}

@media (prefers-reduced-motion: reduce) {
  .progress, .float { animation: none; }
}
</style>
