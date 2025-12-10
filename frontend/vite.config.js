import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'

export default defineConfig({
  plugins: [vue(), vuetify({ autoImport: true })],
  build: {
    outDir: '../app/static/dist',
    emptyOutDir: true
  },
  server: {
    port: 5173,
    strictPort: true
  }
})
