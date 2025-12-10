<template>
  <div class="dashboard-view">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-8 flex-wrap gap-3">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: white;">Pricing Dashboard</h1>
        <p class="text-body-2 mt-2" style="color: #8b8b8b;">Summary statistics and recent pricing entries</p>
      </div>
      <v-btn 
        color="primary" 
        prepend-icon="mdi-refresh" 
        :loading="loading" 
        @click="fetchData" 
        variant="flat"
        style="background: rgba(59, 130, 246, 0.2); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3);"
      >
        Refresh
      </v-btn>
    </div>

    <v-alert v-if="error" type="error" class="mb-4" closable style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); color: #fca5a5;">
      {{ error }}
    </v-alert>

    <!-- Summary Stats Row -->
    <v-row class="mb-8" v-if="summary">
      <!-- Total Entries -->
      <v-col cols="12" sm="6" md="4">
        <v-card 
          elevation="0" 
          class="h-100"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
        >
          <v-card-text class="d-flex align-center justify-space-between py-6">
            <div>
              <div class="text-caption" style="color: #8b8b8b;">Total Entries</div>
              <div class="text-h3 font-weight-bold mt-3" style="color: #3b82f6;">{{ summary.total_entries ?? 0 }}</div>
              <div class="text-caption mt-2" style="color: #606060;">Pricing records logged</div>
            </div>
            <div style="background: rgba(59, 130, 246, 0.15); padding: 12px; border-radius: 12px;">
              <v-icon size="32" color="#3b82f6">mdi-file-document</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Booked Entries -->
      <v-col cols="12" sm="6" md="4">
        <v-card 
          elevation="0" 
          class="h-100"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
        >
          <v-card-text class="d-flex align-center justify-space-between py-6">
            <div>
              <div class="text-caption" style="color: #8b8b8b;">Booked Entries</div>
              <div class="text-h3 font-weight-bold mt-3" style="color: #22c55e;">{{ summary.booked_entries ?? 0 }}</div>
              <div class="text-caption mt-2" style="color: #606060;">Successfully booked dates</div>
            </div>
            <div style="background: rgba(34, 197, 94, 0.15); padding: 12px; border-radius: 12px;">
              <v-icon size="32" color="#22c55e">mdi-check-circle</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Not Booked -->
      <v-col cols="12" sm="6" md="4">
        <v-card 
          elevation="0" 
          class="h-100"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
        >
          <v-card-text class="d-flex align-center justify-space-between py-6">
            <div>
              <div class="text-caption" style="color: #8b8b8b;">Not Booked</div>
              <div class="text-h3 font-weight-bold mt-3" style="color: #fbbf24;">{{ summary.not_booked_entries ?? 0 }}</div>
              <div class="text-caption mt-2" style="color: #606060;">Available dates</div>
            </div>
            <div style="background: rgba(251, 191, 36, 0.15); padding: 12px; border-radius: 12px;">
              <v-icon size="32" color="#fbbf24">mdi-calendar-blank</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Average Price Card -->
    <v-card 
      class="mb-8" 
      elevation="0"
      style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
    >
      <v-card-text class="py-8">
        <div class="d-flex justify-space-between align-center">
          <div>
            <div class="text-caption" style="color: #8b8b8b;">Average Listed Price</div>
            <div class="text-h2 font-weight-bold mt-2" style="color: #a855f7;">₱{{ summary.avg_listed_price ?? 0 }}</div>
          </div>
          <div style="background: rgba(168, 85, 247, 0.15); padding: 16px; border-radius: 12px;">
            <v-icon size="40" color="#a855f7">mdi-currency-php</v-icon>
          </div>
        </div>
      </v-card-text>
    </v-card>

    <!-- Recent Entries Table -->
    <v-card 
      elevation="0"
      style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
    >
      <v-card-title class="d-flex justify-space-between align-center" style="color: white;">
        <span>Recent Pricing Entries</span>
        <v-chip 
          color="primary" 
          variant="flat" 
          size="small"
          style="background: rgba(59, 130, 246, 0.2); color: #3b82f6;"
        >
          {{ entries.length }} records
        </v-chip>
      </v-card-title>
      <v-divider style="border-color: rgba(255,255,255,0.1);"></v-divider>
      <v-card-text class="py-4">
        <v-skeleton-loader v-if="loading" type="table"></v-skeleton-loader>
        <template v-else>
          <v-data-table
            :headers="headers"
            :items="entries"
            :items-per-page="10"
            elevation="0"
            style="background: transparent;"
            :class="{ 'dark-table': true }"
          >
            <template #item.listed_price="{ item }">
              <span class="font-weight-medium" style="color: #22c55e;">₱{{ item.listed_price }}</span>
            </template>
            <template #item.was_booked="{ item }">
              <v-chip 
                :color="item.was_booked === 'Yes' || item.was_booked === true ? '#22c55e' : '#606060'" 
                size="small" 
                variant="flat"
                style="color: white;"
              >
                {{ item.was_booked === 'Yes' || item.was_booked === true ? 'Booked' : 'Available' }}
              </v-chip>
            </template>
            <template #item.actions="{ item }">
              <v-btn
                icon
                variant="text"
                size="small"
                @click="confirmDelete(item)"
                title="Delete entry"
                style="color: #ef4444;"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
            <template #no-data>
              <div class="text-center py-8" style="color: #606060;">No pricing entries available.</div>
            </template>
            <template #header.data-table-select>
            </template>
          </v-data-table>
        </template>
      </v-card-text>
    </v-card>

    <!-- Delete Dialog -->
    <v-dialog v-model="showDelete" max-width="420">
      <v-card style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);">
        <v-card-title style="color: white;" class="text-h6">Delete Entry</v-card-title>
        <v-card-text class="text-body-2" style="color: #b0b0b0;">
          Delete the booking entry for <strong style="color: white;">{{ pendingDelete?.unit_id }}</strong> on 
          <strong style="color: white;">{{ pendingDelete?.date }}</strong>? This action cannot be undone.
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn variant="text" @click="closeDialog" :disabled="deleting" style="color: #606060;">Cancel</v-btn>
          <v-btn 
            variant="flat" 
            @click="performDelete" 
            :loading="deleting"
            style="background: #ef4444; color: white;"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const apiBase = import.meta.env.DEV ? 'http://localhost:5000' : ''
const summary = ref({})
const entries = ref([])
const loading = ref(false)
const error = ref('')
const showDelete = ref(false)
const pendingDelete = ref(null)
const deleting = ref(false)

const headers = [
  { title: 'Date', key: 'date' },
  { title: 'Unit', key: 'unit_id' },
  { title: 'Price', key: 'listed_price' },
  { title: 'Status', key: 'was_booked' },
  { title: 'Lead Time', key: 'lead_time' },
  { title: 'Day', key: 'day_of_week' },
  { title: '', key: 'actions', sortable: false },
]

async function fetchData() {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch(`${apiBase}/api/dashboard`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    summary.value = data.summary_stats || {}
    entries.value = data.dashboard_data || []
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load dashboard data'
  } finally {
    loading.value = false
  }
}

function confirmDelete(item) {
  pendingDelete.value = item
  showDelete.value = true
}

function closeDialog() {
  showDelete.value = false
  pendingDelete.value = null
}

async function performDelete() {
  if (!pendingDelete.value) return
  deleting.value = true
  try {
    const res = await fetch(`${apiBase}/api/delete-booking/${pendingDelete.value.id}`, {
      method: 'DELETE',
    })
    if (!res.ok) {
      const detail = await res.json().catch(() => ({}))
      throw new Error(detail.error || `HTTP ${res.status}`)
    }
    closeDialog()
    fetchData()
  } catch (err) {
    console.error(err)
    error.value = err.message || 'Failed to delete entry'
  } finally {
    deleting.value = false
  }
}

onMounted(fetchData)
</script>
