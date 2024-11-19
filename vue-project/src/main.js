// import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useKakao } from 'vue3-kakao-maps/@utils'

import App from './App.vue'
import router from './router'

useKakao(import.meta.env.VITE_KAKAO_MAP_API_KEY)

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
