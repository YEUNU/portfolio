import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import api from './services/api' // Axios 인스턴스 import

// Pinia 인스턴스 생성
const pinia = createPinia()

// Vue 앱 인스턴스 생성
const app = createApp(App)

// Axios 인스턴스를 전역 속성으로 설정
// 이렇게 하면 모든 컴포넌트에서 this.$api 로 접근 가능합니다.
app.config.globalProperties.$api = api

// Pinia와 Vue Router를 앱에 등록
app.use(pinia)
app.use(router)

// 앱을 #app 엘리먼트에 마운트
app.mount('#app')

