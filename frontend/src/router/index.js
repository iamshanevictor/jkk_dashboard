import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
  { path: '/dashboard', name: 'dashboard', component: () => import('../views/DashboardView.vue') },
  { path: '/data-entry', name: 'data-entry', component: () => import('../views/DataEntryView.vue') },
  { path: '/insights', name: 'insights', component: () => import('../views/InsightsView.vue') },
  { path: '/manage', name: 'manage', component: () => import('../views/ManageView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
