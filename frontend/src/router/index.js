import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NewsView from '../views/NewsView.vue'
import NewsDetailView from '../views/NewsDetailView.vue'
import GalleryView from '../views/GalleryView.vue'
import RulesView from '../views/RulesView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/news', component: NewsView },
  { path: '/news/:id', component: NewsDetailView },
  { path: '/gallery', component: GalleryView },
  { path: '/rules', component: RulesView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})
