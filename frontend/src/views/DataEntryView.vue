<template>
  <v-container class="py-8">
    <div class="text-center mb-6">
      <h2 class="text-h5 font-weight-bold mb-2">Booking Calendar</h2>
      <p class="text-body-2 text-grey-darken-1">Select dates to record pricing and booking information.</p>
    </div>

    <v-row class="mb-6" v-if="units.length">
      <v-col
        v-for="unit in units"
        :key="unit.unit_id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card
          class="unit-card"
          :elevation="selectedUnit?.unit_id === unit.unit_id ? 6 : 1"
          :class="{ 'selected-unit': selectedUnit?.unit_id === unit.unit_id }"
          role="button"
          @click="selectUnit(unit)"
        >
          <v-card-text class="text-center">
            <v-icon size="32" class="mb-2" color="primary">mdi-home-analytics</v-icon>
            <div class="text-subtitle-1 font-weight-bold">{{ unit.property_name }}</div>
            <div class="text-body-2 text-grey">{{ unit.unit_id }}</div>
            <div class="text-caption text-grey-darken-1">Click to manage</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-alert v-else type="info" border="start" color="primary" class="mb-6">
      No properties found. Add properties in Manage.
    </v-alert>

    <div v-if="selectedUnit">
      <div class="calendar-header">
        <v-btn icon variant="text" @click="changeMonth(-1)"><v-icon>mdi-chevron-left</v-icon></v-btn>
        <div class="text-h6 font-weight-semibold">{{ monthYearLabel }}</div>
        <v-btn icon variant="text" @click="changeMonth(1)"><v-icon>mdi-chevron-right</v-icon></v-btn>
      </div>

      <div class="legend">
        <div><span class="swatch selected"></span>Selected</div>
        <div><span class="swatch booked"></span>Booked</div>
        <div><span class="swatch available"></span>Available</div>
        <div><span class="swatch past"></span>Past</div>
      </div>

      <div class="calendar-wrapper">
        <div class="day-headers">
          <div v-for="d in days" :key="d" class="day-header">{{ d }}</div>
        </div>
        <div class="calendar-grid">
          <div
            v-for="day in calendarDays"
            :key="day.key"
            class="calendar-day"
            :class="day.classes"
            @click="toggleDay(day)"
          >
            <div class="day-number">{{ day.label }}</div>
            <div v-if="day.price" class="price-indicator">₱{{ day.price }}</div>
          </div>
        </div>
      </div>

      <div v-if="selectionRanges.length" class="selection-summary">
        <div class="text-subtitle-2 font-weight-semibold mb-2">Selected Dates</div>
        <div class="chips">
          <v-chip
            v-for="range in selectionRanges"
            :key="range.start + range.end"
            color="primary"
            variant="tonal"
            class="mr-2 mb-2"
            label
          >
            {{ formatRange(range) }}
          </v-chip>
        </div>
        <v-btn color="primary" prepend-icon="mdi-pencil" @click="showDialog = true">
          Set Pricing & Booking Info
        </v-btn>
      </div>
    </div>

    <v-dialog v-model="showDialog" max-width="480">
      <v-card>
        <v-card-title class="text-h6">Bulk Entry for Selected Dates</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveEntries">
            <v-text-field
              v-model.number="bulkPrice"
              label="Listed Price (₱)"
              type="number"
              min="0"
              step="0.01"
              required
            ></v-text-field>
            <v-radio-group v-model="bulkBooking" label="Booking Status" inline>
              <v-radio label="All dates are booked" value="booked"></v-radio>
              <v-radio label="All dates are available" value="available"></v-radio>
            </v-radio-group>
          </v-form>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn variant="text" @click="showDialog = false">Cancel</v-btn>
          <v-btn color="primary" variant="flat" :loading="saving" @click="saveEntries">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="2200">
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
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
      classes: ['other-month'],
      disabled: true,
    })
  }

  // Current month days
  for (let day = 1; day <= daysInMonth; day++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    const isPast = dateStr < todayStr
    const booking = existingBookings.value.get(dateStr)
    const isBooked = booking?.was_booked
    const isSelected = selectedDates.value.has(dateStr)

    const classes = ['in-month']
    if (isPast) classes.push('past')
    if (isBooked) classes.push('booked')
    if (!isPast && !isBooked) classes.push('available')
    if (isSelected && !isPast && !isBooked) classes.push('selected')
    if (dateStr === todayStr) classes.push('today')

    cells.push({
      key: dateStr,
      label: day,
      dateStr,
      price: booking?.our_listed_price,
      isPast,
      isBooked,
      isSelected,
      disabled: isPast || isBooked,
      classes,
    })
  }

  // Next month fillers
  while (cells.length < 42) {
    const idx = cells.length - daysInMonth - startOffset + 1
    cells.push({ key: `next-${idx}`, label: idx, classes: ['other-month'], disabled: true })
  }

  return cells
})

const selectionRanges = computed(() => buildRanges([...selectedDates.value].sort()))

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
.calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 480px;
  margin: 0 auto 12px;
}

.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  margin-bottom: 12px;
  font-size: 14px;
}

.legend .swatch {
  display: inline-block;
  width: 12px;
  height: 12px;
  margin-right: 6px;
  border-radius: 3px;
  border: 1px solid #ccc;
}

.legend .selected { background: #3b82f6; }
.legend .booked { background: #ef4444; }
.legend .available { background: #e5e7eb; }
.legend .past { background: #f3f4f6; }

.calendar-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  padding: 12px;
  max-width: 900px;
  margin: 0 auto;
}

.day-headers {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  font-weight: 600;
  color: #4b5563;
  padding-bottom: 8px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.calendar-day {
  position: relative;
  min-height: 74px;
  border-radius: 10px;
  padding: 6px;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  transition: transform 0.12s ease, box-shadow 0.12s ease;
  cursor: pointer;
  background: #f3f4f6;
}

.calendar-day.in-month.available:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(59, 130, 246, 0.12);
}

.calendar-day.other-month {
  background: #fafafa;
  color: #9ca3af;
  cursor: default;
}

.calendar-day.past {
  background: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
  opacity: 0.7;
}

.calendar-day.booked {
  background: #ef4444;
  color: white;
  cursor: not-allowed;
}

.calendar-day.selected {
  background: #3b82f6;
  color: white;
  font-weight: 700;
}

.calendar-day.today {
  border: 2px solid #3b82f6;
}

.day-number {
  font-weight: 600;
  font-size: 16px;
}

.price-indicator {
  position: absolute;
  bottom: 6px;
  right: 6px;
  font-size: 12px;
  background-color: rgba(0,0,0,0.7);
  color: white;
  padding: 2px 6px;
  border-radius: 6px;
}

.selection-summary {
  margin: 18px auto 0;
  background: #e8f1ff;
  border: 1px solid #cbdffb;
  border-radius: 12px;
  padding: 16px;
  max-width: 900px;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.unit-card.selected-unit {
  border: 2px solid #3b82f6;
}
</style>
