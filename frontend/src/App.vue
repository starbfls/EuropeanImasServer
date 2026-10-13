<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <SiteHeader v-if="!bare" />
    <main class="flex-1">
      <RouterView />
    </main>
    <SiteFooter v-if="!bare" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import SiteHeader from './components/SiteHeader.vue'
import SiteFooter from './components/SiteFooter.vue'

const route = useRoute()
// 管理后台不显示前台的导航与页脚
const bare = computed(() => route.meta.bare === true)
</script>
