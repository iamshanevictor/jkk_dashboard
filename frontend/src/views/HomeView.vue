<template>
  <v-container class="py-10">
    <div class="text-center mb-10">
      <h1 class="text-h4 font-weight-bold mb-2">Rentalytics</h1>
      <p class="text-subtitle-1 text-grey-darken-1">
        Optimize your vacation rental pricing with data-driven insights
      </p>
    </div>

    <v-row class="mb-8" align="stretch">
      <v-col
        v-for="card in cards"
        :key="card.title"
        cols="12"
        sm="6"
        md="3"
      >
        <v-card :to="card.to" class="h-100" hover>
          <v-card-text class="text-center">
            <v-icon :color="card.color" size="40" class="mb-3">{{ card.icon }}</v-icon>
            <div class="text-h6 font-weight-medium mb-1">{{ card.title }}</div>
            <div class="text-body-2 text-grey-darken-1">{{ card.subtitle }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-sheet color="grey-lighten-4" class="py-8 px-6 text-center rounded">
      <h2 class="text-h5 font-weight-semibold mb-2">Get Started</h2>
      <p class="text-body-1 text-grey-darken-1 mb-4">Start optimizing your pricing strategy today.</p>
      <v-btn color="primary" :to="'/data-entry'" prepend-icon="mdi-pencil" size="large">
        Log Your First Price Entry
      </v-btn>
    </v-sheet>
  </v-container>
</template>

<script setup>
const cards = [
  {
    title: 'Log Prices',
    subtitle: 'Record daily pricing decisions and booking outcomes',
    icon: 'mdi-notebook-edit-outline',
    to: '/data-entry',
    color: 'primary',
  },
  {
    title: 'Analytics',
    subtitle: 'View booking rates, pricing trends, and missed opportunities',
    icon: 'mdi-chart-line',
    to: '/insights',
    color: 'deep-purple',
  },
  {
    title: 'Dashboard',
    subtitle: 'Summary statistics and recent pricing entries',
    icon: 'mdi-view-dashboard-outline',
    to: '/dashboard',
    color: 'green-darken-1',
  },
  {
    title: 'Settings',
    subtitle: 'Configure property clusters and manage units',
    icon: 'mdi-cog-outline',
    to: '/manage',
    color: 'orange-darken-1',
  },
]
</script>
