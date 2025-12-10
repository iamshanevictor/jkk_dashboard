<template>
  <v-container class="py-8">
    <div class="d-flex align-center justify-space-between mb-6 flex-wrap gap-3">
      <div>
        <h2 class="text-h5 font-weight-bold mb-1">Pricing Dashboard</h2>
        <p class="text-body-2 text-grey-darken-1">Summary statistics and recent pricing entries</p>
      </div>
      <v-btn color="primary" prepend-icon="mdi-refresh" :loading="loading" @click="fetchData">
        Refresh
      </v-btn>
    </div>

    <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

    <v-row class="mb-6" v-if="summary">
      <v-col cols="12" md="4">
        <v-card color="blue-lighten-5" border="blue" class="h-100">
          <v-card-text>
            <div class="text-subtitle-1 text-blue-darken-3">Total Entries</div>
            <div class="text-h4 font-weight-bold text-blue-darken-2">{{ summary.total_entries ?? 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card color="green-lighten-5" border="green" class="h-100">
          <v-card-text>
            <div class="text-subtitle-1 text-green-darken-3">Booked Entries</div>
            <div class="text-h4 font-weight-bold text-green-darken-2">{{ summary.booked_entries ?? 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card color="red-lighten-5" border="red" class="h-100">
          <v-card-text>
            <div class="text-subtitle-1 text-red-darken-3">Not Booked Entries</div>
            <div class="text-h4 font-weight-bold text-red-darken-2">{{ summary.not_booked_entries ?? 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-card class="mb-6">
      <v-card-text class="text-h6">Average Listed Price: ₱{{ summary.avg_listed_price ?? 0 }}</v-card-text>
    </v-card>

    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span class="text-h6">Recent Pricing Entries</span>
        <v-chip color="primary" variant="tonal" size="small">{{ entries.length }} rows</v-chip>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-skeleton-loader v-if="loading" type="table"></v-skeleton-loader>
        <template v-else>
          <v-data-table
            :headers="headers"
            :items="entries"
            :items-per-page="10"
            class="elevation-0"
          >
            <template #item.listed_price="{ item }">
              ₱{{ item.listed_price }}
            </template>
            <template #item.was_booked="{ item }">
              <v-chip :color="item.was_booked === 'Yes' || item.was_booked === true ? 'success' : 'grey'" size="small" variant="flat">
                {{ item.was_booked === 'Yes' || item.was_booked === true ? 'Yes' : 'No' }}
              </v-chip>
            </template>
            <template #item.actions="{ item }">
              <v-btn
                icon
                color="red"
                variant="text"
                @click="confirmDelete(item)"
                :title="`Delete booking ${item.unit_id}`"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
            <template #no-data>
              <div class="text-center py-6 text-grey">No pricing entries available.</div>
            </template>
          </v-data-table>
        </template>
      </v-card-text>
    </v-card>

    <v-dialog v-model="showDelete" max-width="420">
      <v-card>
        <v-card-title class="text-h6">Delete Booking Entry</v-card-title>
        <v-card-text>
          Are you sure you want to delete the booking entry for
          <strong>{{ pendingDelete?.unit_id }}</strong> on
          <strong>{{ pendingDelete?.date }}</strong>? This action cannot be undone.
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn variant="text" @click="closeDialog" :disabled="deleting">Cancel</v-btn>
          <v-btn color="red" variant="flat" @click="performDelete" :loading="deleting">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
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
  { title: 'Unit ID', key: 'unit_id' },
  { title: 'Listed Price (₱)', key: 'listed_price' },
  { title: 'Booked?', key: 'was_booked' },
  { title: 'Lead Time', key: 'lead_time' },
  { title: 'Day', key: 'day_of_week' },
  { title: 'Actions', key: 'actions', sortable: false },
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
