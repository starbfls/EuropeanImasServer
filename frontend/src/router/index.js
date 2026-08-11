import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AnnouncementsView from '../views/AnnouncementsView.vue'
import AnnouncementDetailView from '../views/AnnouncementDetailView.vue'
import EventRecordsView from '../views/EventRecordsView.vue'
import EventRecordDetailView from '../views/EventRecordDetailView.vue'
import GalleryView from '../views/GalleryView.vue'
import BusinessCardView from '../views/BusinessCardView.vue'
import RulesView from '../views/RulesView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/announcements', component: AnnouncementsView },
  { path: '/announcements/:id', component: AnnouncementDetailView },
  { path: '/event-records', component: EventRecordsView },
  { path: '/event-records/:id', component: EventRecordDetailView },
  { path: '/gallery', component: GalleryView },
  { path: '/business-cards', component: BusinessCardView },
  { path: '/rules', component: RulesView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})
