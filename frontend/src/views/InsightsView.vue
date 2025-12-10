<template>
  <div class="insights-view">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-8 flex-wrap gap-3">
      <div>
        <h1 class="text-h5 font-weight-bold" style="color: white;">Pricing Insights</h1>
        <p class="text-body-2 mt-2" style="color: #8b8b8b;">Analyze trends and optimize pricing strategy</p>
      </div>
      <v-btn 
        icon="mdi-refresh" 
        variant="text" 
        :loading="loadingInsights" 
        @click="refresh"
        style="color: #3b82f6;"
      ></v-btn>
    </div>

    <!-- Property Selector -->
    <v-card 
      class="mb-8" 
      elevation="0"
      style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
    >
      <v-card-text class="py-6">
        <v-row align="center">
          <v-col cols="12" md="6">
            <v-select
              v-model="selectedUnit"
              :items="properties"
              item-title="label"
              item-value="unit_id"
              label="Select Property"
              :loading="loadingProps"
              return-object
              clearable
              variant="outlined"
              density="compact"
              @update:modelValue="handleSelect"
              style="--v-field-background-color: #1a1a1a;"
            ></v-select>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-alert 
      v-if="error" 
      type="error" 
      class="mb-4" 
      closable
      style="background: rgba(239, 68, 68, 0.1); border-left-color: #ef4444; color: #fca5a5;"
    >
      {{ error }}
    </v-alert>

    <div v-if="!insights" class="text-center py-16">
      <v-icon size="64" class="mb-4" style="color: #505050;">mdi-chart-line</v-icon>
      <div class="text-h6" style="color: #606060;">Select a property to view insights</div>
    </div>

    <template v-else>
      <!-- Summary Stats -->
      <v-row class="mb-8">
        <!-- Our Avg Price -->
        <v-col cols="12" sm="6" md="3">
          <v-card 
            elevation="0" 
            class="h-100"
            style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
          >
            <v-card-text class="d-flex align-center justify-space-between py-6">
              <div>
                <div class="text-caption" style="color: #8b8b8b;">Our Avg Price</div>
                <div class="text-h4 font-weight-bold mt-3" style="color: #3b82f6;">₱{{ insights.avg_our_price }}</div>
              </div>
              <div style="background: rgba(59, 130, 246, 0.15); padding: 12px; border-radius: 12px;">
                <v-icon size="32" color="#3b82f6">mdi-currency-php</v-icon>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Comp Avg Price -->
        <v-col cols="12" sm="6" md="3">
          <v-card 
            elevation="0" 
            class="h-100"
            style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
          >
            <v-card-text class="d-flex align-center justify-space-between py-6">
              <div>
                <div class="text-caption" style="color: #8b8b8b;">Comp Avg Price</div>
                <div class="text-h4 font-weight-bold mt-3" style="color: #ef4444;">₱{{ insights.avg_comp_price }}</div>
              </div>
              <div style="background: rgba(239, 68, 68, 0.15); padding: 12px; border-radius: 12px;">
                <v-icon size="32" color="#ef4444">mdi-trending-up</v-icon>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Booking Rate -->
        <v-col cols="12" sm="6" md="3">
          <v-card 
            elevation="0" 
            class="h-100"
            style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
          >
            <v-card-text class="d-flex align-center justify-space-between py-6">
              <div>
                <div class="text-caption" style="color: #8b8b8b;">Booking Rate</div>
                <div class="text-h4 font-weight-bold mt-3" style="color: #22c55e;">{{ insights.booking_rate }}%</div>
              </div>
              <div style="background: rgba(34, 197, 94, 0.15); padding: 12px; border-radius: 12px;">
                <v-icon size="32" color="#22c55e">mdi-percent</v-icon>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Best Day Rate -->
        <v-col cols="12" sm="6" md="3">
          <v-card 
            elevation="0" 
            class="h-100"
            style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
          >
            <v-card-text class="d-flex align-center justify-space-between py-6">
              <div>
                <div class="text-caption" style="color: #8b8b8b;">By Day (Best)</div>
                <div class="text-h4 font-weight-bold mt-3" style="color: #fbbf24;">{{ maxDayRate }}%</div>
              </div>
              <div style="background: rgba(251, 191, 36, 0.15); padding: 12px; border-radius: 12px;">
                <v-icon size="32" color="#fbbf24">mdi-chart-box</v-icon>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Charts Row -->
      <v-row class="mb-8">
        <!-- Price Comparison Chart -->
        <v-col cols="12" lg="6">
          <v-card 
            elevation="0"
            style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
            class="h-100"
          >
            <v-card-title class="text-subtitle-1" style="color: white;">Price Comparison Trend</v-card-title>
            <v-divider style="border-color: rgba(255,255,255,0.1);"></v-divider>
            <v-card-text class="py-6">
              <div class="chart-wrapper">
                <canvas ref="priceChartEl"></canvas>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Booking Rate Chart -->
        <v-col cols="12" lg="6">
          <v-card 
            elevation="0"
            style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
            class="h-100"
          >
            <v-card-title class="text-subtitle-1" style="color: white;">Booking Rate by Day</v-card-title>
            <v-divider style="border-color: rgba(255,255,255,0.1);"></v-divider>
            <v-card-text class="py-6">
              <div class="chart-wrapper">
                <canvas ref="bookingChartEl"></canvas>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Booking Rates Table -->
      <v-card 
        elevation="0"
        style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
        class="mb-8"
      >
        <v-card-title style="color: white;">Booking Rates by Day of Week</v-card-title>
        <v-divider style="border-color: rgba(255,255,255,0.1);"></v-divider>
        <v-card-text class="py-6">
          <v-table v-if="insights.booking_rate_by_day" density="compact" style="background: transparent;">
            <thead>
              <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <th style="color: #8b8b8b;">Day of Week</th>
                <th style="color: #8b8b8b; text-align: right;">Booking Rate</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="day in daysOfWeek" :key="day" style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <td style="color: white;">{{ day }}</td>
                <td style="text-align: right;">
                  <div style="display: flex; align-items: center; justify-content: flex-end; gap: 8px;">
                    <div 
                      :style="{
                        width: (insights.booking_rate_by_day[day] || 0) + '%',
                        height: '8px',
                        background: 'linear-gradient(90deg, #3b82f6, #a855f7)',
                        borderRadius: '4px',
                        maxWidth: '100px'
                      }"
                    ></div>
                    <span style="color: #22c55e; font-weight: 600; min-width: 50px;">{{ formattedRate(day) }}%</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card>

      <!-- Missed Opportunities -->
      <v-card 
        elevation="0"
        style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
      >
        <v-card-title style="color: white;" class="text-subtitle-1">Missed Opportunities</v-card-title>
        <v-divider style="border-color: rgba(255,255,255,0.1);"></v-divider>
        <v-card-text class="py-6">
          <v-table v-if="insights.missed_opportunities?.length" density="compact" style="background: transparent;">
            <thead>
              <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <th style="color: #8b8b8b;">Date</th>
                <th style="color: #8b8b8b;">Unit</th>
                <th style="color: #8b8b8b;">Our Price</th>
                <th style="color: #8b8b8b;">Comp Avg</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in insights.missed_opportunities" :key="row.date + row.unit_id" style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td class="text-caption" style="color: #b0b0b0;">{{ row.date }}</td>
                <td style="color: white; font-weight: 600;">{{ row.unit_id }}</td>
                <td style="color: #ef4444;">₱{{ row.our_price }}</td>
                <td style="color: #22c55e;">₱{{ row.comp_avg_price }}</td>
              </tr>
            </tbody>
          </v-table>
          <div v-else class="text-center py-8" style="color: #606060; font-size: 14px;">No missed opportunities detected.</div>
        </v-card-text>
      </v-card>
    </template>
  </div>
</template>

<script setup>
import { Chart, registerables } from 'chart.js'
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'

Chart.register(...registerables)

const apiBase = import.meta.env.DEV ? 'http://localhost:5000' : ''
const properties = ref([])
const selectedUnit = ref(null)
const insights = ref(null)
const loadingProps = ref(false)
const loadingInsights = ref(false)
const error = ref('')
const priceChartEl = ref(null)
const bookingChartEl = ref(null)
let priceChart
let bookingChart

const maxDayRate = computed(() => {
  if (!insights.value?.booking_rate_by_day) return '0'
  const rates = Object.values(insights.value.booking_rate_by_day)
  return rates.length ? Math.max(...rates).toFixed(2) : '0'
})

async function fetchProperties() {
  loadingProps.value = true
  try {
    const res = await fetch(`${apiBase}/api/properties/all`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    properties.value = data.map(p => ({ ...p, label: `${p.property_name} (${p.unit_id})` }))
    if (data.length) {
      selectedUnit.value = properties.value[0]
      await fetchInsights()
    }
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load properties'
  } finally {
    loadingProps.value = false
  }
}

async function fetchInsights() {
  if (!selectedUnit.value?.unit_id) {
    insights.value = null
    return
  }
  loadingInsights.value = true
  error.value = ''
  try {
    const res = await fetch(`${apiBase}/api/insights/${selectedUnit.value.unit_id}`)
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`)
    if (!data.insights || Object.keys(data.insights).length === 0) {
      insights.value = null
      error.value = 'No price logs found for this property.'
      destroyCharts()
      return
    }
    insights.value = data.insights
    await nextTick()
    renderCharts()
  } catch (err) {
    console.error(err)
    insights.value = null
    error.value = err.message || 'Failed to load insights'
    destroyCharts()
  } finally {
    loadingInsights.value = false
  }
}

function handleSelect() {
  fetchInsights()
}

function refresh() {
  fetchInsights()
}

function renderCharts() {
  if (!insights.value) return

  const labels = insights.value.chart_data?.map(item => item.date) || []
  const ourPrices = insights.value.chart_data?.map(item => item.our_price) || []
  const compPrices = insights.value.chart_data?.map(item => item.comp_price) || []

  if (priceChart) priceChart.destroy()
  priceChart = new Chart(priceChartEl.value, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Our Listed Price',
          data: ourPrices,
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59,130,246,0.1)',
          tension: 0.4,
          fill: true,
          borderWidth: 2,
        },
        {
          label: 'Competitor Avg',
          data: compPrices,
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239,68,68,0.1)',
          tension: 0.4,
          fill: true,
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom' },
      },
      scales: {
        y: { beginAtZero: true },
      },
    },
  })

  const bookingLabels = Object.keys(insights.value.booking_rate_by_day || {})
  const bookingValues = Object.values(insights.value.booking_rate_by_day || {})

  if (bookingChart) bookingChart.destroy()
  bookingChart = new Chart(bookingChartEl.value, {
    type: 'bar',
    data: {
      labels: bookingLabels,
      datasets: [
        {
          label: 'Booking Rate %',
          data: bookingValues,
          backgroundColor: '#10b981',
          borderColor: '#059669',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
      },
      scales: {
        x: { beginAtZero: true, max: 100 },
      },
    },
  })
}

function destroyCharts() {
  if (priceChart) {
    priceChart.destroy()
    priceChart = null
  }
  if (bookingChart) {
    bookingChart.destroy()
    bookingChart = null
  }
}

onMounted(fetchProperties)
onBeforeUnmount(destroyCharts)
</script>

<style scoped>
.chart-wrapper {
  position: relative;
  height: 300px;
}
</style>
import { Chart, registerables } from 'chart.js'
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'

Chart.register(...registerables)

const apiBase = import.meta.env.DEV ? 'http://localhost:5000' : ''
const properties = ref([])
const selectedUnit = ref(null)
const insights = ref(null)
const loadingProps = ref(false)
const loadingInsights = ref(false)
const error = ref('')
const priceChartEl = ref(null)
const bookingChartEl = ref(null)
let priceChart
let bookingChart

const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

function formattedRate(day) {
  const rate = insights.value?.booking_rate_by_day?.[day]
  return rate !== undefined ? rate.toFixed(2) : '0.00'
}

async function fetchProperties() {
  loadingProps.value = true
  try {
    const res = await fetch(`${apiBase}/api/properties/all`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    properties.value = data.map(p => ({ ...p, label: `${p.property_name} (${p.unit_id})` }))
    if (data.length) {
      selectedUnit.value = properties.value[0]
      await fetchInsights()
    }
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load properties'
  } finally {
    loadingProps.value = false
  }
}

async function fetchInsights() {
  if (!selectedUnit.value?.unit_id) {
    insights.value = null
    return
  }
  loadingInsights.value = true
  error.value = ''
  try {
    const res = await fetch(`${apiBase}/api/insights/${selectedUnit.value.unit_id}`)
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`)
    if (!data.insights || Object.keys(data.insights).length === 0) {
      insights.value = null
      error.value = 'No price logs found for this property.'
      destroyCharts()
      return
    }
    insights.value = data.insights
    await nextTick()
    renderCharts()
  } catch (err) {
    console.error(err)
    insights.value = null
    error.value = err.message || 'Failed to load insights'
    destroyCharts()
  } finally {
    loadingInsights.value = false
  }
}

function handleSelect() {
  fetchInsights()
}

function refresh() {
  fetchInsights()
}

function renderCharts() {
  if (!insights.value) return

  const labels = insights.value.chart_data?.map(item => item.date) || []
  const ourPrices = insights.value.chart_data?.map(item => item.our_price) || []
  const compPrices = insights.value.chart_data?.map(item => item.comp_price) || []

  if (priceChart) priceChart.destroy()
  priceChart = new Chart(priceChartEl.value, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Our Listed Price',
          data: ourPrices,
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59,130,246,0.15)',
          tension: 0.3,
          fill: true,
          borderWidth: 2,
          pointBackgroundColor: '#3b82f6',
          pointBorderColor: '#1e3a8a',
          pointRadius: 4,
          pointHoverRadius: 6,
        },
        {
          label: 'Competitor Avg Price',
          data: compPrices,
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239,68,68,0.15)',
          tension: 0.3,
          fill: true,
          borderWidth: 2,
          pointBackgroundColor: '#ef4444',
          pointBorderColor: '#7f1d1d',
          pointRadius: 4,
          pointHoverRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { 
          position: 'bottom',
          labels: {
            color: '#b0b0b0',
            boxWidth: 12,
            padding: 16,
            font: { size: 12 }
          }
        },
        filler: { propagate: false },
      },
      scales: {
        y: { 
          beginAtZero: true,
          ticks: { color: '#8b8b8b' },
          grid: { color: 'rgba(255,255,255,0.05)' },
          border: { display: false }
        },
        x: { 
          ticks: { color: '#8b8b8b' },
          grid: { color: 'rgba(255,255,255,0.05)' },
          border: { display: false }
        }
      },
    },
  })

  const bookingLabels = Object.keys(insights.value.booking_rate_by_day || {})
  const bookingValues = Object.values(insights.value.booking_rate_by_day || {})

  if (bookingChart) bookingChart.destroy()
  bookingChart = new Chart(bookingChartEl.value, {
    type: 'bar',
    data: {
      labels: bookingLabels,
      datasets: [
        {
          label: 'Booking Rate %',
          data: bookingValues,
          backgroundColor: 'rgba(168, 85, 247, 0.8)',
          borderColor: '#a855f7',
          borderWidth: 1,
          borderRadius: 6,
        },
      ],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
      },
      scales: {
        x: { 
          beginAtZero: true, 
          max: 100,
          ticks: { color: '#8b8b8b' },
          grid: { color: 'rgba(255,255,255,0.05)' },
          border: { display: false }
        },
        y: { 
          ticks: { color: '#8b8b8b' },
          grid: { display: false },
          border: { display: false }
        }
      },
    },
  })
}

function destroyCharts() {
  if (priceChart) {
    priceChart.destroy()
    priceChart = null
  }
  if (bookingChart) {
    bookingChart.destroy()
    bookingChart = null
  }
}

onMounted(fetchProperties)
onBeforeUnmount(destroyCharts)
</script>

<style scoped>
.chart-wrapper {
  position: relative;
  height: 320px;
}
</style>
