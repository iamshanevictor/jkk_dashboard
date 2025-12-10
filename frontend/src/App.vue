<template>
  <v-app>
    <v-main class="bg-grey-lighten-4">
      <v-container class="py-8" max-width="1200">
        <v-row class="mb-6" align="center" justify="space-between">
          <v-col cols="12" md="8">
            <h1 class="text-h4 font-weight-bold mb-2">Rentalytics Frontend (Vue)</h1>
            <p class="text-body-1 text-grey-darken-1">
              This Vue + Vuetify app is built and served from Flask. Data is fetched from the existing API.
            </p>
          </v-col>
          <v-col cols="12" md="4" class="d-flex justify-end">
            <v-btn color="primary" prepend-icon="mdi-database" @click="refresh">
              Refresh Data
            </v-btn>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="8">
            <v-card elevation="2">
              <v-card-title class="d-flex align-center justify-space-between">
                <span class="text-h6">Properties</span>
                <v-chip color="primary" variant="tonal">{{ properties.length }} total</v-chip>
              </v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-alert v-if="error" type="error" class="mb-4" dense>{{ error }}</v-alert>
                <template v-else>
                  <v-skeleton-loader
                    v-if="loading"
                    type="list-item-two-line, list-item-two-line, list-item-two-line"
                  />
                  <v-list v-else-if="properties.length">
                    <v-list-item
                      v-for="prop in properties"
                      :key="prop.unit_id"
                      :title="prop.property_name"
                      :subtitle="prop.unit_id"
                    >
                      <template #append>
                        <v-chip color="success" size="small" class="text-caption">{{ prop.unit_id }}</v-chip>
                      </template>
                    </v-list-item>
                  </v-list>
                  <v-alert v-else type="info" variant="tonal" density="comfortable">
                    No properties found. Add properties via the existing backend.
                  </v-alert>
                </template>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card elevation="2">
              <v-card-title class="text-h6">API Status</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-list density="compact">
                  <v-list-item>
                    <v-list-item-title>Backend</v-list-item-title>
                    <v-chip :color="statusColor" variant="flat" size="small">{{ statusText }}</v-chip>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Endpoint</v-list-item-title>
                    <v-list-item-subtitle>{{ apiBase }}/api/properties</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Use Flask origin in dev; same origin in production
const apiBase = import.meta.env.DEV ? 'http://localhost:5000' : ''
const properties = ref([])
const loading = ref(false)
const error = ref('')
const status = ref('unknown')

const statusText = computed(() => {
  if (status.value === 'ok') return 'OK'
  if (status.value === 'error') return 'Error'
  return 'Unknown'
})

const statusColor = computed(() => {
  if (status.value === 'ok') return 'success'
  if (status.value === 'error') return 'error'
  return 'grey'
})

async function fetchProperties() {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch(`${apiBase}/api/properties`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    properties.value = await res.json()
    status.value = 'ok'
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load properties'
    status.value = 'error'
  } finally {
    loading.value = false
  }
}

function refresh() {
  fetchProperties()
}

onMounted(() => {
  fetchProperties()
})
</script>

<style>
body {
  font-family: 'Roboto', sans-serif;
}
</style>
