<template>
  <v-app theme="dark">
    <!-- Sidebar Navigation -->
    <v-navigation-drawer
      v-model="drawer"
      :permanent="!mobileView"
      :temporary="mobileView"
      class="sidebar"
      color="#1a1a1a"
      width="280"
    >
      <div class="pa-6 text-center border-b border-white border-opacity-10">
        <div class="text-h6 font-weight-bold text-white">Rentalytics</div>
        <div class="text-caption text-grey-lighten-2">Pricing Analytics</div>
      </div>

      <div class="pa-4">
        <div class="text-uppercase text-xs font-weight-bold text-grey-lighten-1 mb-3">Menu</div>
        <v-list nav dense class="pa-0">
          <v-list-item
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            :active="isActive(item.to)"
            @click="mobileView && (drawer = false)"
            class="mb-1"
          >
            <template #prepend>
              <v-icon class="mr-3">{{ item.icon }}</v-icon>
            </template>
            <v-list-item-title class="text-sm">{{ item.label }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </div>

      <v-divider class="my-4 border-white border-opacity-10"></v-divider>

      <div class="pa-4">
        <div class="text-uppercase text-xs font-weight-bold text-grey-lighten-1 mb-3">General</div>
        <v-list nav dense class="pa-0">
          <v-list-item @click="$router.push('/manage')">
            <template #prepend>
              <v-icon class="mr-3">mdi-cog</v-icon>
            </template>
            <v-list-item-title class="text-sm">Settings</v-list-item-title>
          </v-list-item>
        </v-list>
      </div>
    </v-navigation-drawer>

    <!-- Top App Bar -->
    <v-app-bar color="#2a2a2a" elevation="2" class="px-6 border-b border-white border-opacity-10">
      <v-app-bar-nav-icon
        v-if="mobileView"
        @click.stop="drawer = !drawer"
      ></v-app-bar-nav-icon>
      <v-app-bar-title class="text-h6 font-weight-bold text-white">{{ pageTitle }}</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn icon="mdi-magnify" variant="text"></v-btn>
      <v-btn icon="mdi-bell-outline" variant="text"></v-btn>
      <v-btn icon="mdi-account-circle" variant="text"></v-btn>
    </v-app-bar>

    <!-- Main Content -->
    <v-main class="app-main">
      <v-container fluid class="py-8 px-8">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useDisplay } from 'vuetify'

const route = useRoute()
const { mdAndUp } = useDisplay()
const drawer = ref(true)

const navItems = [
  { to: '/', label: 'Home', icon: 'mdi-home' },
  { to: '/dashboard', label: 'Dashboard', icon: 'mdi-view-dashboard' },
  { to: '/data-entry', label: 'Data Entry', icon: 'mdi-calendar-edit' },
  { to: '/insights', label: 'Insights', icon: 'mdi-chart-line' },
  { to: '/manage', label: 'Manage', icon: 'mdi-database' },
]

const mobileView = computed(() => !mdAndUp.value)

const pageTitle = computed(() => {
  const item = navItems.find(i => i.to === route.path)
  return item?.label || 'Rentalytics'
})

function isActive(path) {
  return route.path === path
}
</script>

<style scoped>
.app-main {
  background: #1a1a1a !important;
}

.sidebar {
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.5);
}

/* Table styling */
:deep(.v-table__wrapper) {
  background: transparent;
}

:deep(.v-table thead tr) {
  background: transparent;
}

:deep(.v-table tbody tr) {
  background: transparent;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

:deep(.v-table tbody tr:hover) {
  background: rgba(255, 255, 255, 0.03);
}

:deep(.v-table td),
:deep(.v-table th) {
  color: rgba(255, 255, 255, 0.7);
  border-color: transparent;
}

:deep(.v-table th) {
  color: rgba(255, 255, 255, 0.5);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 12px;
}

/* Card styling */
:deep(.v-card) {
  background: #2a2a2a !important;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.v-card__title) {
  color: white;
}

:deep(.v-card__subtitle) {
  color: rgba(255, 255, 255, 0.6);
}

:deep(.v-card__text) {
  color: rgba(255, 255, 255, 0.7);
}

/* Input fields */
:deep(.v-field__input) {
  color: white;
}

:deep(.v-field--outlined) {
  border-color: rgba(255, 255, 255, 0.1);
}

:deep(.v-field--focused.v-field--outlined) {
  border-color: rgba(255, 255, 255, 0.3);
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

/* Button styling */
:deep(.v-btn) {
  text-transform: none !important;
}

/* List items */
:deep(.v-list-item) {
  color: rgba(255, 255, 255, 0.7);
}

:deep(.v-list-item--active) {
  background: rgba(59, 130, 246, 0.15) !important;
  color: #3b82f6;
}

:deep(.v-list-item--active .v-icon) {
  color: #3b82f6 !important;
}

:deep(.v-list-item:hover) {
  background: rgba(255, 255, 255, 0.05);
}

/* Divider */
:deep(.v-divider) {
  border-color: rgba(255, 255, 255, 0.1) !important;
}

/* Progress bar */
:deep(.v-progress-linear) {
  background: rgba(255, 255, 255, 0.1);
}

/* Alert */
:deep(.v-alert) {
  background: rgba(255, 255, 255, 0.05) !important;
}

/* Dialog/Modal */
:deep(.v-overlay__scrim) {
  background: rgba(0, 0, 0, 0.7);
}

:deep(.v-dialog__content .v-card) {
  background: #2a2a2a !important;
}

/* Checkbox */
:deep(.v-checkbox__input) {
  color: #3b82f6;
}
</style>
  color: #b0b0b0;
}

:deep(.v-data-table th) {
  color: #8b8b8b !important;
  background: transparent !important;
  font-weight: 600;
}

:deep(.v-data-table td) {
  color: #b0b0b0;
}

:deep(.v-data-table tbody tr:hover) {
  background: rgba(59, 130, 246, 0.05) !important;
}

:deep(.v-text-field--outlined .v-field) {
  --v-field-background-color: #1a1a1a;
}

:deep(.v-field__outline) {
  --v-border-color: rgba(255, 255, 255, 0.15);
}

:deep(.v-field__input) {
  color: #b0b0b0;
}

:deep(.v-field__input::placeholder) {
  color: #606060;
}

:deep(.v-label) {
  color: #8b8b8b !important;
}

:deep(.v-field--focused .v-field__outline) {
  --v-border-color: rgba(59, 130, 246, 0.5);
}
</style>

<style scoped>
:deep(.sidebar) {
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.v-list-item--active) {
  background-color: rgba(255, 255, 255, 0.1);
  border-left: 3px solid #4caf50;
}

:deep(.v-list-item) {
  border-radius: 8px;
  margin-bottom: 4px;
}

:deep(.v-app-bar) {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
}
</style>
