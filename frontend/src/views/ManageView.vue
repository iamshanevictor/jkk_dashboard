<template>
  <v-container class="py-8">
    <div class="text-center mb-6">
      <h2 class="text-h5 font-weight-bold mb-2">Property Management</h2>
      <p class="text-body-2 text-grey-darken-1">Add and manage individual property units used for pricing analytics.</p>
    </div>

    <v-card class="mb-6">
      <v-card-title>Property Details</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-form @submit.prevent="submit" ref="formRef">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.property_name" label="Property Name" required></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field v-model.number="form.bedrooms" label="Bedrooms" type="number" min="0" required></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field v-model.number="form.bathrooms" label="Bathrooms" type="number" step="0.5" min="0" required></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field v-model.number="form.max_guests" label="Max Guests" type="number" min="1" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.amenities" label="Amenities (comma separated)"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.quality_keywords" label="Quality Keywords (comma separated)"></v-text-field>
            </v-col>
          </v-row>
          <div class="d-flex justify-end">
            <v-btn color="primary" type="submit" :loading="submitting" prepend-icon="mdi-plus-circle">Add Property</v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span class="text-h6">Properties</span>
        <v-btn icon="mdi-refresh" variant="text" :loading="loading" @click="fetchProperties"></v-btn>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-skeleton-loader v-if="loading" type="table"></v-skeleton-loader>
        <template v-else>
          <v-data-table :headers="headers" :items="properties" :items-per-page="10" class="elevation-0">
            <template #item.bed_bath="{ item }">
              {{ item.bedrooms }}/{{ item.bathrooms }}
            </template>
            <template #item.actions="{ item }">
              <v-btn icon color="red" variant="text" @click="confirmDelete(item)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
            <template #no-data>
              <div class="text-center py-6 text-grey">No properties yet.</div>
            </template>
          </v-data-table>
        </template>
      </v-card-text>
    </v-card>

    <v-dialog v-model="showDelete" max-width="420">
      <v-card>
        <v-card-title class="text-h6">Delete Property</v-card-title>
        <v-card-text>
          Delete <strong>{{ pendingDelete?.property_name }}</strong>? This cannot be undone.
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn variant="text" @click="closeDelete" :disabled="deleting">Cancel</v-btn>
          <v-btn color="red" variant="flat" @click="performDelete" :loading="deleting">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="2200">
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
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
  { title: 'Actions', key: 'actions', sortable: false },
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
