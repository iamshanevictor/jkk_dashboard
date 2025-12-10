<template>
  <div class="manage-view">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-8 flex-wrap gap-3">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: white;">Property Management</h1>
        <p class="text-body-2 mt-2" style="color: #8b8b8b;">Add and manage vacation rental units</p>
      </div>
      <v-btn 
        color="success" 
        prepend-icon="mdi-refresh" 
        :loading="loading" 
        @click="fetchProperties" 
        variant="flat"
        style="background: rgba(34, 197, 94, 0.2); color: #22c55e; border: 1px solid rgba(34, 197, 94, 0.3);"
      >
        Refresh
      </v-btn>
    </div>

    <!-- Add Property Form -->
    <v-card 
      class="mb-8" 
      elevation="0"
      style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
    >
      <v-card-title style="color: white;">Add New Property</v-card-title>
      <v-divider style="border-color: rgba(255,255,255,0.1);"></v-divider>
      <v-card-text class="py-6">
        <v-form @submit.prevent="submit" ref="formRef">
          <v-row>
            <v-col cols="12">
              <v-text-field 
                v-model="form.property_name" 
                label="Property Name" 
                variant="outlined" 
                density="compact" 
                required
                style="--v-field-background-color: #1a1a1a;"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field 
                v-model.number="form.bedrooms" 
                label="Bedrooms" 
                type="number" 
                min="0" 
                variant="outlined" 
                density="compact" 
                required
                style="--v-field-background-color: #1a1a1a;"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field 
                v-model.number="form.bathrooms" 
                label="Bathrooms" 
                type="number" 
                step="0.5" 
                min="0" 
                variant="outlined" 
                density="compact" 
                required
                style="--v-field-background-color: #1a1a1a;"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field 
                v-model.number="form.max_guests" 
                label="Max Guests" 
                type="number" 
                min="1" 
                variant="outlined" 
                density="compact" 
                required
                style="--v-field-background-color: #1a1a1a;"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field 
                v-model="form.amenities" 
                label="Amenities (comma separated)" 
                variant="outlined" 
                density="compact"
                style="--v-field-background-color: #1a1a1a;"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field 
                v-model="form.quality_keywords" 
                label="Quality Keywords (comma separated)" 
                variant="outlined" 
                density="compact"
                style="--v-field-background-color: #1a1a1a;"
              ></v-text-field>
            </v-col>
          </v-row>
          <div class="d-flex justify-end">
            <v-btn 
              type="submit" 
              :loading="submitting" 
              prepend-icon="mdi-plus"
              variant="flat"
              style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white;"
            >
              Add Property
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>

    <!-- Properties List -->
    <v-card 
      elevation="0"
      style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
    >
      <v-card-title class="d-flex justify-space-between align-center" style="color: white;">
        <span>Properties</span>
        <v-chip 
          color="primary" 
          variant="flat" 
          size="small"
          style="background: rgba(59, 130, 246, 0.2); color: #3b82f6;"
        >
          {{ properties.length }}
        </v-chip>
      </v-card-title>
      <v-divider style="border-color: rgba(255,255,255,0.1);"></v-divider>
      <v-card-text class="py-4">
        <v-skeleton-loader v-if="loading" type="table"></v-skeleton-loader>
        <template v-else>
          <v-data-table 
            :headers="headers" 
            :items="properties" 
            :items-per-page="15" 
            elevation="0"
            style="background: transparent;"
            :class="{ 'dark-table': true }"
          >
            <template #item.bed_bath="{ item }">
              <span style="color: white;">{{ item.bedrooms }}/{{ item.bathrooms }}</span>
            </template>
            <template #item.actions="{ item }">
              <v-btn 
                icon 
                variant="text" 
                size="small" 
                @click="confirmDelete(item)"
                style="color: #ef4444;"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
            <template #no-data>
              <div class="text-center py-8" style="color: #606060;">No properties yet. Add one to get started.</div>
            </template>
          </v-data-table>
        </template>
      </v-card-text>
    </v-card>

    <!-- Delete Dialog -->
    <v-dialog v-model="showDelete" max-width="420">
      <v-card style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);">
        <v-card-title style="color: white;" class="text-h6">Delete Property</v-card-title>
        <v-card-text style="color: #b0b0b0;">
          Delete <strong style="color: white;">{{ pendingDelete?.property_name }}</strong>? This action cannot be undone.
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn variant="text" @click="closeDelete" :disabled="deleting" style="color: #606060;">Cancel</v-btn>
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

    <!-- Snackbar -->
    <v-snackbar 
      v-model="snackbar.show" 
      :color="snackbar.color" 
      :timeout="2200"
      style="background: rgba(0,0,0,0.8) !important;"
    >
      {{ snackbar.message }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'

const apiBase = import.meta.env.DEV ? 'http://localhost:5000' : ''
const loading = ref(false)
const submitting = ref(false)
const deleting = ref(false)
const properties = ref([])
const showDelete = ref(false)
const pendingDelete = ref(null)
const formRef = ref(null)
const snackbar = reactive({ show: false, message: '', color: 'success' })

const form = reactive({
  property_name: '',
  bedrooms: null,
  bathrooms: null,
  max_guests: null,
  amenities: '',
  quality_keywords: '',
})

const headers = [
  { title: 'Unit ID', key: 'unit_id' },
  { title: 'Name', key: 'property_name' },
  { title: 'Bed/Bath', key: 'bed_bath' },
  { title: 'Guests', key: 'max_guests' },
  { title: '', key: 'actions', sortable: false },
]

function toast(message, color = 'success') {
  snackbar.message = message
  snackbar.color = color
  snackbar.show = true
}

async function fetchProperties() {
  loading.value = true
  try {
    const res = await fetch(`${apiBase}/api/properties/all`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    properties.value = await res.json()
  } catch (err) {
    console.error(err)
    toast('Failed to load properties', 'error')
  } finally {
    loading.value = false
  }
}

async function submit() {
  submitting.value = true
  try {
    const payload = {
      ...form,
      bedrooms: Number(form.bedrooms),
      bathrooms: Number(form.bathrooms),
      max_guests: Number(form.max_guests),
    }

    const res = await fetch(`${apiBase}/api/properties`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    if (!res.ok) {
      const detail = await res.json().catch(() => ({}))
      throw new Error(detail.error || `HTTP ${res.status}`)
    }
    toast('Property added successfully')
    resetForm()
    fetchProperties()
  } catch (err) {
    console.error(err)
    toast(err.message || 'Failed to add property', 'error')
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  form.property_name = ''
  form.bedrooms = null
  form.bathrooms = null
  form.max_guests = null
  form.amenities = ''
  form.quality_keywords = ''
  formRef.value?.resetValidation?.()
}

function confirmDelete(item) {
  pendingDelete.value = item
  showDelete.value = true
}

function closeDelete() {
  showDelete.value = false
  pendingDelete.value = null
}

async function performDelete() {
  if (!pendingDelete.value) return
  deleting.value = true
  try {
    const res = await fetch(`${apiBase}/api/properties/${pendingDelete.value.id}`, {
      method: 'DELETE',
    })
    if (!res.ok) {
      const detail = await res.json().catch(() => ({}))
      throw new Error(detail.error || `HTTP ${res.status}`)
    }
    toast('Property deleted')
    closeDelete()
    fetchProperties()
  } catch (err) {
    console.error(err)
    toast(err.message || 'Failed to delete property', 'error')
  } finally {
    deleting.value = false
  }
}

onMounted(fetchProperties)
</script>
