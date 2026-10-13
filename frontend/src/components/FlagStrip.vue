<template>
  <div class="flex items-center justify-center gap-[2px] sm:gap-[3px]" role="presentation" aria-hidden="true">
    <span
      v-for="cc in FLAGS"
      :key="cc"
      class="block h-[3px] w-[11px] sm:w-6 md:w-8 overflow-hidden rounded-[1px] opacity-55 hover:opacity-100 transition-opacity duration-300"
    >
      <!-- 只取国旗中间那一条，拼起来就是一根彩色细线 -->
      <img
        :src="`/assets/flags/${cc}.svg`"
        alt=""
        class="w-full h-[18px] -mt-[7px] object-cover"
        loading="lazy"
      />
    </span>
  </div>
</template>

<script setup>
// 大致按地理由西向东 / 由南向北排，不代表成员分布
const FLAGS = [
  'ie', 'gb', 'fr', 'es', 'be', 'nl', 'lu', 'ch',
  'de', 'at', 'it', 'cz', 'pl', 'hu', 'ro', 'bg',
  'dk', 'no', 'se', 'fi', 'is', 'ee', 'lt',
]
</script>
