<template>
  <div class="home-view">
    <!-- Header with Welcome Message -->
    <div class="d-flex justify-space-between align-center mb-10 flex-wrap gap-3">
      <div>
        <h1 class="text-h4 font-weight-bold mb-2" style="color: white; letter-spacing: -0.5px;">Welcome back John Doe!</h1>
        <p class="text-body-2" style="color: #a0a0a0;">Here's your property performance overview</p>
      </div>
      <v-btn 
        @click="$router.push('/manage')" 
        prepend-icon="mdi-plus"
        color="primary"
        variant="flat"
        class="px-6"
      >
        Add Property
      </v-btn>
    </div>

    <!-- Stat Cards Grid -->
    <v-row class="mb-10">
      <!-- Total Properties -->
      <v-col cols="12" sm="6" md="3">
        <v-card 
          elevation="0" 
          class="stat-card h-100 pa-6"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; transition: all 0.3s ease;"
        >
          <div class="d-flex justify-space-between align-start mb-4">
            <div class="flex-grow-1">
              <div class="text-caption font-weight-medium" style="color: #a0a0a0; text-transform: uppercase; letter-spacing: 0.5px;">Active Contracts</div>
              <div class="text-h3 font-weight-bold mt-3" style="color: white; font-size: 2.5rem;">{{ stats.totalProperties }}</div>
            </div>
            <div style="background: rgba(59, 130, 246, 0.15); padding: 12px; border-radius: 10px; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center;">
              <v-icon size="28" color="#3b82f6">mdi-home-group</v-icon>
            </div>
          </div>
        </v-card>
      </v-col>

      <!-- Total Entries -->
      <v-col cols="12" sm="6" md="3">
        <v-card 
          elevation="0" 
          class="stat-card h-100 pa-6"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; transition: all 0.3s ease;"
        >
          <div class="d-flex justify-space-between align-start mb-4">
            <div class="flex-grow-1">
              <div class="text-caption font-weight-medium" style="color: #a0a0a0; text-transform: uppercase; letter-spacing: 0.5px;">Pending Signatures</div>
              <div class="text-h3 font-weight-bold mt-3" style="color: white; font-size: 2.5rem;">{{ stats.totalEntries }}</div>
            </div>
            <div style="background: rgba(34, 197, 94, 0.15); padding: 12px; border-radius: 10px; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center;">
              <v-icon size="28" color="#22c55e">mdi-file-document-multiple</v-icon>
            </div>
          </div>
        </v-card>
      </v-col>

      <!-- Booking Rate -->
      <v-col cols="12" sm="6" md="3">
        <v-card 
          elevation="0" 
          class="stat-card h-100 pa-6"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; transition: all 0.3s ease;"
        >
          <div class="d-flex justify-space-between align-start mb-4">
            <div class="flex-grow-1">
              <div class="text-caption font-weight-medium" style="color: #a0a0a0; text-transform: uppercase; letter-spacing: 0.5px;">Total Contracts</div>
              <div class="text-h3 font-weight-bold mt-3" style="color: white; font-size: 2.5rem;">{{ stats.bookingRate }}</div>
            </div>
            <div style="background: rgba(251, 191, 36, 0.15); padding: 12px; border-radius: 10px; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center;">
              <v-icon size="28" color="#fbbf24">mdi-percent</v-icon>
            </div>
          </div>
        </v-card>
      </v-col>

      <!-- Avg Price -->
      <v-col cols="12" sm="6" md="3">
        <v-card 
          elevation="0" 
          class="stat-card h-100 pa-6"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; transition: all 0.3s ease;"
        >
          <div class="d-flex justify-space-between align-start mb-4">
            <div class="flex-grow-1">
              <div class="text-caption font-weight-medium" style="color: #a0a0a0; text-transform: uppercase; letter-spacing: 0.5px;">Expiring Soon</div>
              <div class="text-h3 font-weight-bold mt-3" style="color: white; font-size: 2.5rem;">{{ stats.expiringSoon }}</div>
            </div>
            <div style="background: rgba(168, 85, 247, 0.15); padding: 12px; border-radius: 10px; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center;">
              <v-icon size="28" color="#a855f7">mdi-clock-outline</v-icon>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Main Content Row: Chart + Recent Contracts -->
    <v-row class="mb-10">
      <!-- Signed over Time Chart -->
      <v-col cols="12" lg="8">
        <v-card 
          elevation="0" 
          class="h-100"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px;"
        >
          <div class="pa-6 pb-0 d-flex justify-space-between align-center border-b" style="border-color: rgba(255,255,255,0.1);">
            <div>
              <div class="text-caption font-weight-medium" style="color: #a0a0a0; text-transform: uppercase; letter-spacing: 0.5px;">Total Shipments</div>
              <h3 class="text-h6 mt-2" style="color: white; font-weight: 600;">Signed over time</h3>
            </div>
            <div style="display: flex; gap: 8px;">
              <v-btn size="sm" variant="text" style="color: rgba(255,255,255,0.5); font-size: 12px;">Jan - Jun</v-btn>
            </div>
          </div>
          <v-card-text class="pa-6" style="height: 300px; display: flex; align-items: center; justify-content: center; color: #606060;">
            <div style="text-align: center;">
              <v-icon size="48" style="color: rgba(255,255,255,0.2);">mdi-chart-line</v-icon>
              <p class="mt-3">Chart will display here</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Recent Contracts -->
      <v-col cols="12" lg="4">
        <v-card 
          elevation="0"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px;"
        >
          <div class="pa-6 pb-0 border-b" style="border-color: rgba(255,255,255,0.1);">
            <div class="text-caption font-weight-medium" style="color: #a0a0a0; text-transform: uppercase; letter-spacing: 0.5px;">Latest</div>
            <h3 class="text-h6 mt-2" style="color: white; font-weight: 600;">Recent contracts</h3>
          </div>
          <v-card-text class="pa-6">
            <div class="mb-4 pb-4 d-flex align-start gap-3" style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <v-icon color="#3b82f6" size="24">mdi-checkbox-marked-circle</v-icon>
              <div>
                <div style="color: white; font-weight: 500;">Growth Plan</div>
                <div style="color: #a0a0a0; font-size: 12px; margin-top: 2px;">James Walker</div>
              </div>
            </div>
            <div class="mb-4 pb-4 d-flex align-start gap-3" style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <v-icon color="#22c55e" size="24">mdi-checkbox-marked-circle</v-icon>
              <div>
                <div style="color: white; font-weight: 500;">Marketing Strategy</div>
                <div style="color: #a0a0a0; font-size: 12px; margin-top: 2px;">Sarah Chen</div>
              </div>
            </div>
            <div class="mb-4 pb-4 d-flex align-start gap-3" style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <v-icon color="#fbbf24" size="24">mdi-checkbox-marked-circle</v-icon>
              <div>
                <div style="color: white; font-weight: 500;">Product Launch</div>
                <div style="color: #a0a0a0; font-size: 12px; margin-top: 2px;">Michael Johnson</div>
              </div>
            </div>
            <div class="d-flex align-start gap-3">
              <v-icon color="#a855f7" size="24">mdi-checkbox-marked-circle</v-icon>
              <div>
                <div style="color: white; font-weight: 500;">Budget Review</div>
                <div style="color: #a0a0a0; font-size: 12px; margin-top: 2px;">David Lee</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Your Contacts Section -->
    <div class="mb-6">
      <div class="d-flex justify-space-between align-center mb-6">
        <h3 class="text-h6 font-weight-bold" style="color: white;">Your Contacts</h3>
        <v-btn size="sm" variant="text" style="color: #3b82f6;">See all</v-btn>
      </div>
      <v-row>
        <v-col cols="12" sm="6" lg="3" v-for="i in 4" :key="i">
          <v-card 
            elevation="0" 
            class="pa-6 h-100"
            style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; text-align: center;"
          >
            <div class="d-flex justify-center gap-2 mb-4">
              <v-avatar size="28" style="background: rgba(59, 130, 246, 0.2);"><span style="color: #3b82f6; font-weight: 600;">J</span></v-avatar>
              <v-avatar size="28" style="background: rgba(34, 197, 94, 0.2);"><span style="color: #22c55e; font-weight: 600;">A</span></v-avatar>
              <v-avatar size="28" style="background: rgba(168, 85, 247, 0.2);"><span style="color: #a855f7; font-weight: 600;">M</span></v-avatar>
            </div>
            <div style="color: #a0a0a0; font-size: 12px; margin-bottom: 8px;">280+</div>
            <h4 style="color: white; font-weight: 600; margin-bottom: 8px;">NDA Agreement</h4>
            <p style="color: #808080; font-size: 12px; line-height: 1.5;">To make sure our data is secure when we build</p>
            <div class="d-flex justify-center gap-2 mt-6">
              <v-btn size="sm" variant="text" prepend-icon="mdi-share-variant" style="color: #3b82f6; text-transform: none; font-size: 12px;">Share</v-btn>
              <v-btn size="sm" variant="text" prepend-icon="mdi-pencil" style="color: #3b82f6; text-transform: none; font-size: 12px;">Edit</v-btn>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const apiBase = import.meta.env.DEV ? 'http://localhost:5000' : ''
const stats = ref({
  totalProperties: 150,
  totalEntries: 267,
  bookingRate: 680,
  expiringSoon: 22,
})

async function loadStats() {
  try {
    const [propsRes, dashRes] = await Promise.all([
      fetch(`${apiBase}/api/properties/all`),
      fetch(`${apiBase}/api/dashboard`),
    ])

    if (propsRes.ok) {
      const properties = await propsRes.json()
      stats.value.totalProperties = properties.length
    }

    if (dashRes.ok) {
      const dashboard = await dashRes.json()
      stats.value.totalEntries = dashboard.summary_stats?.total_entries || 0
      if (dashboard.summary_stats?.booked_entries && dashboard.summary_stats?.total_entries) {
        stats.value.bookingRate = Math.round((dashboard.summary_stats.booked_entries / dashboard.summary_stats.total_entries) * 100)
      }
    }
  } catch (err) {
    console.error('Failed to load stats:', err)
  }
}

onMounted(loadStats)
</script>

<style scoped>
.home-view {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-card:hover {
  border-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}
</style>
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-8">
      <div>
        <h1 class="text-h4 font-weight-bold mb-2" style="color: white;">Dashboard</h1>
        <p class="text-body-2" style="color: #b0b0b0;">Manage your vacation rental pricing with data-driven insights</p>
      </div>
      <v-btn 
        @click="$router.push('/manage')" 
        prepend-icon="mdi-plus"
        style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white;"
        flat
      >
        Add Property
      </v-btn>
    </div>

    <!-- Quick Stats -->
    <v-row class="mb-8">
      <!-- Total Properties -->
      <v-col cols="12" sm="6" md="3">
        <v-card 
          elevation="0" 
          class="stat-card h-100"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
        >
          <v-card-text class="d-flex align-center justify-space-between py-6">
            <div>
              <div class="text-caption" style="color: #8b8b8b;">Total Properties</div>
              <div class="text-h4 font-weight-bold mt-3" style="color: white;">{{ stats.totalProperties }}</div>
            </div>
            <div style="background: rgba(59, 130, 246, 0.15); padding: 12px; border-radius: 12px;">
              <v-icon size="32" color="#3b82f6">mdi-home-group</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Total Entries -->
      <v-col cols="12" sm="6" md="3">
        <v-card 
          elevation="0" 
          class="stat-card h-100"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
        >
          <v-card-text class="d-flex align-center justify-space-between py-6">
            <div>
              <div class="text-caption" style="color: #8b8b8b;">Total Entries</div>
              <div class="text-h4 font-weight-bold mt-3" style="color: white;">{{ stats.totalEntries }}</div>
            </div>
            <div style="background: rgba(34, 197, 94, 0.15); padding: 12px; border-radius: 12px;">
              <v-icon size="32" color="#22c55e">mdi-file-document-multiple</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Booking Rate -->
      <v-col cols="12" sm="6" md="3">
        <v-card 
          elevation="0" 
          class="stat-card h-100"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
        >
          <v-card-text class="d-flex align-center justify-space-between py-6">
            <div>
              <div class="text-caption" style="color: #8b8b8b;">Booking Rate</div>
              <div class="text-h4 font-weight-bold mt-3" style="color: white;">{{ stats.bookingRate }}%</div>
            </div>
            <div style="background: rgba(251, 191, 36, 0.15); padding: 12px; border-radius: 12px;">
              <v-icon size="32" color="#fbbf24">mdi-percent</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Avg Price -->
      <v-col cols="12" sm="6" md="3">
        <v-card 
          elevation="0" 
          class="stat-card h-100"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
        >
          <v-card-text class="d-flex align-center justify-space-between py-6">
            <div>
              <div class="text-caption" style="color: #8b8b8b;">Avg Price</div>
              <div class="text-h4 font-weight-bold mt-3" style="color: white;">₱{{ stats.avgPrice }}</div>
            </div>
            <div style="background: rgba(168, 85, 247, 0.15); padding: 12px; border-radius: 12px;">
              <v-icon size="32" color="#a855f7">mdi-currency-php</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Quick Actions & Getting Started -->
    <v-row>
      <!-- Quick Actions -->
      <v-col cols="12" md="6">
        <v-card 
          elevation="0" 
          class="h-100"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
        >
          <v-card-title style="color: white; padding-top: 20px;">Quick Actions</v-card-title>
          <v-divider style="border-color: rgba(255,255,255,0.1);"></v-divider>
          <v-card-text class="py-6">
            <div class="d-flex flex-column gap-3">
              <v-btn 
                @click="$router.push('/data-entry')" 
                block 
                variant="flat"
                prepend-icon="mdi-calendar-edit"
                style="background: rgba(59, 130, 246, 0.2); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3);"
              >
                Log Price Entry
              </v-btn>
              <v-btn 
                @click="$router.push('/dashboard')" 
                block 
                variant="flat"
                prepend-icon="mdi-view-dashboard"
                style="background: rgba(34, 197, 94, 0.2); color: #22c55e; border: 1px solid rgba(34, 197, 94, 0.3);"
              >
                View Dashboard
              </v-btn>
              <v-btn 
                @click="$router.push('/insights')" 
                block 
                variant="flat"
                prepend-icon="mdi-chart-line"
                style="background: rgba(168, 85, 247, 0.2); color: #a855f7; border: 1px solid rgba(168, 85, 247, 0.3);"
              >
                View Insights
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Getting Started Checklist -->
      <v-col cols="12" md="6">
        <v-card 
          elevation="0" 
          class="h-100"
          style="background: #2a2a2a; border: 1px solid rgba(255,255,255,0.1);"
        >
          <v-card-title style="color: white; padding-top: 20px;">Getting Started</v-card-title>
          <v-divider style="border-color: rgba(255,255,255,0.1);"></v-divider>
          <v-card-text class="py-6">
            <div class="text-body-2" style="color: #b0b0b0; line-height: 1.8;">
              <div class="mb-4 d-flex align-start gap-3">
                <v-icon color="#10b981" size="24">mdi-check-circle</v-icon>
                <div>
                  <div style="color: white; font-weight: 600;">Add Properties</div>
                  <div style="color: #808080; font-size: 12px;">Start by adding your vacation rental units</div>
                </div>
              </div>
              <div class="mb-4 d-flex align-start gap-3">
                <v-icon color="#3b82f6" size="24">mdi-check-circle</v-icon>
                <div>
                  <div style="color: white; font-weight: 600;">Log Entries</div>
                  <div style="color: #808080; font-size: 12px;">Record daily pricing and booking data</div>
                </div>
              </div>
              <div class="mb-4 d-flex align-start gap-3">
                <v-icon color="#fbbf24" size="24">mdi-check-circle</v-icon>
                <div>
                  <div style="color: white; font-weight: 600;">Review Insights</div>
                  <div style="color: #808080; font-size: 12px;">Analyze trends and optimize pricing</div>
                </div>
              </div>
              <div class="d-flex align-start gap-3">
                <v-icon color="#a855f7" size="24">mdi-check-circle</v-icon>
                <div>
                  <div style="color: white; font-weight: 600;">Track Performance</div>
                  <div style="color: #808080; font-size: 12px;">Monitor booking rates and revenue</div>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const apiBase = import.meta.env.DEV ? 'http://localhost:5000' : ''
const stats = ref({
  totalProperties: 0,
  totalEntries: 0,
  bookingRate: 0,
  avgPrice: 0,
})

async function loadStats() {
  try {
    const [propsRes, dashRes] = await Promise.all([
      fetch(`${apiBase}/api/properties/all`),
      fetch(`${apiBase}/api/dashboard`),
    ])

    const properties = await propsRes.json()
    const dashboard = await dashRes.json()

    stats.value = {
      totalProperties: properties.length,
      totalEntries: dashboard.summary_stats?.total_entries || 0,
      bookingRate: dashboard.summary_stats?.booked_entries && dashboard.summary_stats?.total_entries
        ? Math.round((dashboard.summary_stats.booked_entries / dashboard.summary_stats.total_entries) * 100)
        : 0,
      avgPrice: dashboard.summary_stats?.avg_listed_price || 0,
    }
  } catch (err) {
    console.error('Failed to load stats:', err)
  }
}

onMounted(loadStats)
</script>
