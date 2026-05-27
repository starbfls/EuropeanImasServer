<template>
  <RouterLink
    :to="`/news/${article.id}`"
    class="group block bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
  >
    <div class="overflow-hidden h-48">
      <img
        :src="article.cover_image"
        :alt="article.title"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
      />
    </div>
    <div class="p-5">
      <div class="flex items-center gap-2 mb-3">
        <span class="bg-sky-100 text-sky-700 text-xs font-bold px-2.5 py-0.5 rounded-full">
          {{ article.category }}
        </span>
        <span class="text-xs text-gray-400">{{ formatDate(article.date) }}</span>
      </div>
      <h3 class="font-extrabold text-gray-800 text-base leading-snug group-hover:text-sky-600 transition-colors mb-2">
        {{ article.title }}
      </h3>
      <p class="text-sm text-gray-500 line-clamp-2">{{ article.summary }}</p>
    </div>
  </RouterLink>
</template>

<script setup>
defineProps({ article: Object })

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-GB', {
    day: 'numeric', month: 'long', year: 'numeric',
  })
}
</script>
