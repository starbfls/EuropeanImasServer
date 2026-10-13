import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AnnouncementsView from '../views/AnnouncementsView.vue'
import AnnouncementDetailView from '../views/AnnouncementDetailView.vue'
import ImasCalendarView from '../views/ImasCalendarView.vue'
import GalleryView from '../views/GalleryView.vue'
import BusinessCardView from '../views/BusinessCardView.vue'
import RulesView from '../views/RulesView.vue'
import DiscordView from '../views/DiscordView.vue'
import AdminLoginView from '../views/AdminLoginView.vue'
import AdminView from '../views/AdminView.vue'
import { verifyToken } from '../api/admin'

const routes = [
  { path: '/', component: HomeView },
  { path: '/announcements', component: AnnouncementsView },
  { path: '/announcements/:id', component: AnnouncementDetailView },
  { path: '/imas-calendar', component: ImasCalendarView },
  { path: '/gallery', component: GalleryView },
  { path: '/business-cards', component: BusinessCardView },
  { path: '/rules', component: RulesView },
  { path: '/discord', component: DiscordView },
  { path: '/admin/login', component: AdminLoginView, meta: { bare: true } },
  { path: '/admin', component: AdminView, meta: { bare: true, requiresAdmin: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: (to) => (to.hash ? { el: to.hash, top: 72 } : { top: 0 }),
})

// 后台页面需要有效的管理员令牌；这里只做跳转，真正的权限校验在后端。
router.beforeEach(async (to) => {
  if (!to.meta.requiresAdmin) return true
  if (await verifyToken()) return true
  return { path: '/admin/login', query: { redirect: to.fullPath } }
})

export default router
