<template>
  <v-app>
    <v-app-bar flat color="white" class="border-b">
      <v-app-bar-title class="text-primary text-h6 font-weight-bold">Rentalytics</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        variant="text"
        :color="isActive(item.to) ? 'primary' : 'grey-darken-1'"
        class="text-capitalize"
      >
        {{ item.label }}
      </v-btn>
    </v-app-bar>

    <v-main class="bg-grey-lighten-4 min-h-screen">
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/data-entry', label: 'Data Entry' },
  { to: '/insights', label: 'Insights' },
  { to: '/manage', label: 'Manage' },
]

function isActive(path) {
  return route.path === path
}
</script>

<style>
body {
  font-family: 'Roboto', sans-serif;
  background-color: #f5f5f5;
}
</style>
