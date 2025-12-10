import { createApp } from 'vue'
import App from './App.vue'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

// Register all Vuetify components/directives so v-app/v-col/etc resolve
const vuetify = createVuetify({
	components,
	directives,
})

createApp(App).use(vuetify).mount('#app')
