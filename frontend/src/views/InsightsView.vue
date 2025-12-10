<template>
  <v-container class="py-8">
    <div class="d-flex flex-wrap align-center justify-space-between mb-6 gap-3">
      <div>
        <h2 class="text-h5 font-weight-bold mb-1">Weekly Pricing Insight Report</h2>
        <p class="text-body-2 text-grey-darken-1">Select a property to view analytics and insights.</p>
      </div>
      <v-btn icon="mdi-refresh" variant="text" :loading="loadingInsights" @click="refresh"></v-btn>
    </div>

    <v-row class="mb-6" align="center" justify="center">
      <v-col cols="12" md="6">
        <v-select
          v-model="selectedUnit"
          :items="properties"
          item-title="label"
          item-value="unit_id"
          label="Select Property Unit"
          :loading="loadingProps"
          return-object
          clearable
          @update:modelValue="handleSelect"
        ></v-select>
      </v-col>
    </v-row>

    <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

    <div v-if="!insights" class="text-center py-10 text-grey">
      <v-icon size="48" class="mb-3">mdi-chart-timeline-variant</v-icon>
      <div class="text-subtitle-1">Select a property to view insights.</div>
    </div>

    <template v-else>
      <v-row class="mb-6">
        <v-col cols="12" md="4">
          <v-card color="blue-lighten-5" class="h-100">
            <v-card-text>
              <div class="text-subtitle-2 text-blue-darken-2">Average Prices</div>
              <div class="text-h5 font-weight-bold text-blue-darken-3">₱{{ insights.avg_our_price }} | ₱{{ insights.avg_comp_price }}</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card color="purple-lighten-5" class="h-100">
            <v-card-text>
              <div class="text-subtitle-2 text-purple-darken-2">Booking Rate</div>
              <div class="text-h4 font-weight-bold text-purple-darken-3">{{ insights.booking_rate }}%</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card color="green-lighten-5" class="h-100">
            <v-card-text>
              <div class="text-subtitle-2 text-green-darken-2">Booking Rate by Day</div>
              <ul class="pl-4 text-body-2 text-green-darken-3">
                <li v-for="day in daysOfWeek" :key="day">{{ day }}: {{ formattedRate(day) }}%</li>
              </ul>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mb-6">
        <v-col cols="12" lg="6">
          <v-card class="h-100">
            <v-card-title>Price Comparison Trend</v-card-title>
            <v-card-text>
              <div class="chart-wrapper">
                <canvas ref="priceChartEl"></canvas>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" lg="6">
          <v-card class="h-100">
            <v-card-title>Booking Rate by Day of Week</v-card-title>
            <v-card-text>
              <div class="chart-wrapper">
                <canvas ref="bookingChartEl"></canvas>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-card>
        <v-card-title>Missed Opportunities</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-table v-if="insights.missed_opportunities?.length">
            <thead>
              <tr>
                <th>Date</th>
                <th>Unit ID</th>
                <th>Our Price</th>
                <th>Comp Avg Price</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in insights.missed_opportunities" :key="row.date + row.unit_id">
                <td>{{ row.date }}</td>
                <td>{{ row.unit_id }}</td>
                <td>₱{{ row.our_price }}</td>
                <td>₱{{ row.comp_avg_price }}</td>
              </tr>
            </tbody>
          </v-table>
          <div v-else class="text-center py-6 text-grey">No missed opportunities detected.</div>
        </v-card-text>
      </v-card>
    </template>
  </v-container>
</template>

<script setup>
import { Chart, registerables } from 'chart.js'
import { onBeforeUnmount, onMounted, ref } from 'vue'

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
          borderColor: 'rgba(59,130,246,1)',
          backgroundColor: 'rgba(59,130,246,0.2)',
          tension: 0.3,
          fill: false,
        },
        {
          label: 'Competitor Avg Price',
          data: compPrices,
          borderColor: 'rgba(239,68,68,1)',
          backgroundColor: 'rgba(239,68,68,0.2)',
          tension: 0.3,
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, title: { display: true, text: 'Price' } },
        x: { title: { display: true, text: 'Date' } },
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
          backgroundColor: 'rgba(168,85,247,0.6)',
          borderColor: 'rgba(168,85,247,1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, max: 100, title: { display: true, text: 'Booking Rate %' } },
        x: { title: { display: true, text: 'Day of Week' } },
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
