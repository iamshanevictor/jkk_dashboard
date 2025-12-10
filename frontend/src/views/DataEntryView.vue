<template>
  <div class="data-entry-view">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-8 flex-wrap gap-3">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: white;">Booking Calendar</h1>
        <p class="text-body-2 mt-2" style="color: #8b8b8b;">Record pricing and booking information by date</p>
      </div>
    </div>

    <!-- Property Selection -->
    <v-row class="mb-8">
      <v-col
        v-for="unit in units"
        :key="unit.unit_id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card
          elevation="0"
          class="property-card cursor-pointer transition-all h-100"
          :style="{
            background: selectedUnit?.unit_id === unit.unit_id ? 'rgba(59, 130, 246, 0.2)' : '#2a2a2a',
            border: selectedUnit?.unit_id === unit.unit_id 
              ? '2px solid #3b82f6' 
              : '1px solid rgba(255,255,255,0.1)',
          }"
          @click="selectUnit(unit)"
        >
          <v-card-text class="text-center py-6">
            <v-icon 
              size="40" 
              class="mb-2"
              :color="selectedUnit?.unit_id === unit.unit_id ? '#3b82f6' : '#606060'"
            >
              mdi-home
            </v-icon>
            <div class="text-subtitle-2 font-weight-bold" style="color: white;">{{ unit.property_name }}</div>
            <div class="text-caption mt-1" style="color: #8b8b8b;">{{ unit.unit_id }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-alert 
      v-if="!units.length" 
      type="info" 
      border="start" 
      color="primary" 
      class="mb-8"
      style="background: rgba(59, 130, 246, 0.1); border-left-color: #3b82f6; color: #93c5fd;"
    >
      No properties found. Add properties in the <strong>Manage</strong> section.
    </v-alert>

    <!-- Calendar Section -->
    <v-card 
      v-if="selectedUnit" 
      elevation="0" 
      class="mb-8"
      style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
    >
      <v-card-text class="py-6">
        <!-- Calendar Header -->
        <div class="d-flex align-center justify-space-between mb-6">
          <v-btn icon="mdi-chevron-left" variant="text" @click="changeMonth(-1)" style="color: #3b82f6;"></v-btn>
          <div class="text-h6 font-weight-bold" style="min-width: 200px; text-align: center; color: white;">
            {{ monthYearLabel }}
          </div>
          <v-btn icon="mdi-chevron-right" variant="text" @click="changeMonth(1)" style="color: #3b82f6;"></v-btn>
        </div>

        <!-- Legend -->
        <div class="d-flex flex-wrap gap-4 mb-8 justify-center">
          <div class="d-flex align-center gap-2">
            <div style="width: 16px; height: 16px; background: #3b82f6; border-radius: 4px;"></div>
            <span class="text-caption" style="color: #b0b0b0;">Selected</span>
          </div>
          <div class="d-flex align-center gap-2">
            <div style="width: 16px; height: 16px; background: #ef4444; border-radius: 4px;"></div>
            <span class="text-caption" style="color: #b0b0b0;">Booked</span>
          </div>
          <div class="d-flex align-center gap-2">
            <div style="width: 16px; height: 16px; background: #505050; border-radius: 4px;"></div>
            <span class="text-caption" style="color: #b0b0b0;">Available</span>
          </div>
          <div class="d-flex align-center gap-2">
            <div style="width: 16px; height: 16px; background: #3a3a3a; border-radius: 4px;"></div>
            <span class="text-caption" style="color: #b0b0b0;">Past</span>
          </div>
        </div>

        <!-- Calendar Grid -->
        <div style="overflow-x: auto;">
          <div style="display: grid; grid-template-columns: repeat(7, minmax(100px, 1fr)); gap: 8px;">
            <!-- Day Headers -->
            <div
              v-for="day in days"
              :key="day"
              style="font-weight: 600; text-align: center; padding: 8px; color: #606060; font-size: 12px;"
            >
              {{ day }}
            </div>

            <!-- Calendar Days -->
            <div
              v-for="calDay in calendarDays"
              :key="calDay.key"
              class="calendar-cell"
              :style="getCellStyle(calDay)"
              @click="toggleDay(calDay)"
            >
              <div style="font-weight: 600; font-size: 14px; margin-bottom: 4px;">{{ calDay.label }}</div>
              <div v-if="calDay.price" style="font-size: 11px; color: #aaa;">₱{{ calDay.price }}</div>
            </div>
          </div>
        </div>

        <!-- Selection Summary -->
        <div v-if="selectionRanges.length" class="mt-8">
          <div class="text-caption" style="color: #8b8b8b;">Selected Dates:</div>
          <div class="d-flex flex-wrap gap-2 mt-2">
            <v-chip 
              v-for="range in selectionRanges" 
              :key="`${range.start}-${range.end}`"
              size="small"
              style="background: rgba(59, 130, 246, 0.2); color: #93c5fd;"
            >
              {{ formatRange(range) }}
            </v-chip>
          </div>
          <v-btn 
            class="mt-4"
            @click="showDialog = true"
            prepend-icon="mdi-content-save"
            variant="flat"
            style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white;"
          >
            Save {{ selectedDates.size }} Entries
          </v-btn>
        </div>
      </v-card-text>
    </v-card>

    <!-- Bulk Entry Dialog -->
    <v-dialog v-model="showDialog" max-width="480">
      <v-card elevation="0" style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);">
        <v-card-title class="text-subtitle-1 font-weight-bold" style="color: white;">Bulk Entry</v-card-title>
        <v-divider style="border-color: rgba(255,255,255,0.1);"></v-divider>
        <v-card-text class="py-6">
          <v-form @submit.prevent="saveEntries">
            <v-text-field
              v-model.number="bulkPrice"
              label="Listed Price"
              type="number"
              prefix="₱"
              min="0"
              step="0.01"
              variant="outlined"
              density="compact"
              required
              class="mb-4"
              style="--v-field-background-color: #1a1a1a;"
            ></v-text-field>
            <div class="text-body-2 font-weight-medium mb-3" style="color: white;">Booking Status</div>
            <v-radio-group v-model="bulkBooking" inline>
              <v-radio label="Booked" value="booked" style="color: white;"></v-radio>
              <v-radio label="Available" value="available" style="color: white;"></v-radio>
            </v-radio-group>
          </v-form>
        </v-card-text>
        <v-divider style="border-color: rgba(255,255,255,0.1);"></v-divider>
        <v-card-actions class="justify-end pa-4">
          <v-btn variant="text" @click="showDialog = false" style="color: #606060;">Cancel</v-btn>
          <v-btn 
            variant="flat" 
            :loading="saving" 
            @click="saveEntries"
            style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white;"
          >
            Save
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
    <v-dialog v-model="showDialog" max-width="480">
      <v-card elevation="1">
        <v-card-title class="text-subtitle-1 font-weight-bold">Bulk Entry</v-card-title>
        <v-divider></v-divider>
        <v-card-text class="py-6">
          <v-form @submit.prevent="saveEntries">
            <v-text-field
              v-model.number="bulkPrice"
              label="Listed Price"
              type="number"
              prefix="₱"
              min="0"
              step="0.01"
              variant="outlined"
              density="compact"
              required
              class="mb-4"
            ></v-text-field>
            <div class="text-body-2 font-weight-medium mb-2">Booking Status</div>
            <v-radio-group v-model="bulkBooking" inline>
              <v-radio label="Booked" value="booked"></v-radio>
              <v-radio label="Available" value="available"></v-radio>
            </v-radio-group>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="justify-end pa-4">
          <v-btn variant="text" @click="showDialog = false">Cancel</v-btn>
          <v-btn color="primary" variant="flat" :loading="saving" @click="saveEntries">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="2200">
      {{ snackbar.message }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

const apiBase = import.meta.env.DEV ? 'http://localhost:5000' : ''
const units = ref([])
const selectedUnit = ref(null)
const currentDate = ref(new Date())
const existingBookings = ref(new Map())
const selectedDates = ref(new Set())
const showDialog = ref(false)
const bulkPrice = ref(null)
const bulkBooking = ref('booked')
const saving = ref(false)
const snackbar = reactive({ show: false, message: '', color: 'success' })
const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const monthYearLabel = computed(() => {
  const date = currentDate.value
  return date.toLocaleString('en-US', { month: 'long', year: 'numeric' })
})

const calendarDays = computed(() => {
  const date = currentDate.value
  const year = date.getFullYear()
  const month = date.getMonth()
  const firstDay = new Date(year, month, 1)
  const startOffset = firstDay.getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const todayStr = formatDate(new Date())

  const cells = []

  // Previous month fillers
  for (let i = 0; i < startOffset; i++) {
    const d = new Date(year, month, i - startOffset + 1)
    cells.push({
      key: `prev-${i}`,
      label: d.getDate(),
      isOtherMonth: true,
    })
  }

  // Current month days
  for (let day = 1; day <= daysInMonth; day++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    const isPast = dateStr < todayStr
    const booking = existingBookings.value.get(dateStr)
    const isBooked = booking?.was_booked === 'Y'
    const isSelected = selectedDates.value.has(dateStr)
    const isToday = dateStr === todayStr

    cells.push({
      key: dateStr,
      label: day,
      dateStr,
      price: booking?.our_listed_price,
      isPast,
      isBooked,
      isSelected,
      isToday,
      disabled: isPast || isBooked,
      isOtherMonth: false,
    })
  }

  // Next month fillers
  while (cells.length < 42) {
    const idx = cells.length - daysInMonth - startOffset + 1
    cells.push({ key: `next-${idx}`, label: idx, isOtherMonth: true })
  }

  return cells
})

const selectionRanges = computed(() => buildRanges([...selectedDates.value].sort()))

function getCellStyle(day) {
  if (day.isOtherMonth) {
    return {
      backgroundColor: '#1a1a1a',
      color: '#505050',
      cursor: 'default',
      borderRadius: '8px',
      padding: '12px',
      minHeight: '70px',
      display: 'flex',
      alignItems: 'flex-start',
      flexDirection: 'column',
      justifyContent: 'flex-start',
      border: '1px solid rgba(255,255,255,0.05)',
    }
  }
  if (day.isPast) {
    return {
      backgroundColor: '#1a1a1a',
      color: '#505050',
      cursor: 'not-allowed',
      opacity: '0.5',
      borderRadius: '8px',
      padding: '12px',
      minHeight: '70px',
      display: 'flex',
      alignItems: 'flex-start',
      flexDirection: 'column',
      justifyContent: 'flex-start',
      border: '1px solid rgba(255,255,255,0.05)',
    }
  }
  if (day.isBooked) {
    return {
      backgroundColor: '#ef4444',
      color: 'white',
      cursor: 'not-allowed',
      borderRadius: '8px',
      padding: '12px',
      minHeight: '70px',
      display: 'flex',
      alignItems: 'flex-start',
      flexDirection: 'column',
      justifyContent: 'flex-start',
      border: day.isToday ? '2px solid #b91c1c' : '1px solid rgba(255,255,255,0.1)',
    }
  }
  if (day.isSelected) {
    return {
      backgroundColor: '#3b82f6',
      color: 'white',
      cursor: 'pointer',
      borderRadius: '8px',
      padding: '12px',
      minHeight: '70px',
      display: 'flex',
      alignItems: 'flex-start',
      flexDirection: 'column',
      justifyContent: 'flex-start',
      border: '2px solid #1d4ed8',
    }
  }
  return {
    backgroundColor: '#3a3a3a',
    color: '#b0b0b0',
    cursor: 'pointer',
    borderRadius: '8px',
    padding: '12px',
    minHeight: '70px',
    display: 'flex',
    alignItems: 'flex-start',
    flexDirection: 'column',
    justifyContent: 'flex-start',
    transition: 'transform 0.12s ease, box-shadow 0.12s ease',
    border: day.isToday ? '2px solid #3b82f6' : '1px solid rgba(255,255,255,0.1)',
  }
}

function toast(message, color = 'success') {
  snackbar.message = message
  snackbar.color = color
  snackbar.show = true
}

function formatDate(date) {
  return new Date(date).toISOString().split('T')[0]
}

function selectUnit(unit) {
  selectedUnit.value = unit
  selectedDates.value = new Set()
  loadBookings()
}

function changeMonth(delta) {
  const d = new Date(currentDate.value)
  d.setMonth(d.getMonth() + delta)
  currentDate.value = d
}

function toggleDay(day) {
  if (!day.dateStr || day.disabled) return
  const next = new Set(selectedDates.value)
  if (next.has(day.dateStr)) next.delete(day.dateStr)
  else next.add(day.dateStr)
  selectedDates.value = next
}

function buildRanges(dates) {
  if (!dates.length) return []
  const ranges = []
  let start = dates[0]
  let end = dates[0]

  for (let i = 1; i < dates.length; i++) {
    const cur = dates[i]
    const prev = dates[i - 1]
    const nextDay = new Date(prev)
    nextDay.setDate(nextDay.getDate() + 1)
    const nextStr = formatDate(nextDay)
    if (cur === nextStr) {
      end = cur
    } else {
      ranges.push({ start, end })
      start = cur
      end = cur
    }
  }
  ranges.push({ start, end })
  return ranges
}

function formatRange(range) {
  if (range.start === range.end) return new Date(range.start).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  const startStr = new Date(range.start).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  const endStr = new Date(range.end).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  return `${startStr} - ${endStr}`
}

async function fetchUnits() {
  try {
    const res = await fetch(`${apiBase}/api/properties`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    units.value = data
    if (data.length) selectUnit(data[0])
  } catch (err) {
    console.error(err)
    toast('Failed to load properties', 'error')
  }
}

async function loadBookings() {
  if (!selectedUnit.value) return
  try {
    const res = await fetch(`${apiBase}/api/unit-bookings/${selectedUnit.value.unit_id}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const bookings = await res.json()
    const map = new Map()
    bookings.forEach(b => map.set(b.date, b))
    existingBookings.value = map
  } catch (err) {
    console.error(err)
    toast('Failed to load bookings', 'error')
  }
}

async function saveEntries() {
  if (!selectedUnit.value || !selectedDates.value.size) return
  if (!bulkPrice.value || bulkPrice.value <= 0) {
    toast('Enter a valid price', 'error')
    return
  }
  saving.value = true
  try {
    for (const date of selectedDates.value) {
      const payload = {
        unit_id: selectedUnit.value.unit_id,
        date,
        listed_price: Number(bulkPrice.value),
        was_booked: bulkBooking.value === 'booked' ? 'Y' : 'N',
      }
      const res = await fetch(`${apiBase}/log_entry`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      if (!res.ok) {
        const detail = await res.json().catch(() => ({}))
        throw new Error(detail.error || `Failed to save entry for ${date}`)
      }
    }
    toast(`Saved ${selectedDates.value.size} price entries`)
    showDialog.value = false
    selectedDates.value = new Set()
    bulkPrice.value = null
    await loadBookings()
  } catch (err) {
    console.error(err)
    toast(err.message || 'Failed to save entries', 'error')
  } finally {
    saving.value = false
  }
}

onMounted(fetchUnits)
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}

.transition-all {
  transition: all 0.2s ease;
}

.border-thick {
  border: 3px solid !important;
}

.border-primary {
  border-color: #3b82f6 !important;
}

.calendar-cell {
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}

.calendar-cell:hover:not([style*="not-allowed"]) {
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(59, 130, 246, 0.12);
}
</style>
