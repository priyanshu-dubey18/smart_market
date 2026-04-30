import { createRouter, createWebHistory } from 'vue-router'

import Home from '../Pages/Home.vue'
import About from '../Pages/About.vue'
import ServiceRequestForm from '../Pages/ServiceRequestForm.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/service-request',
    name: 'ServiceRequest',
    component: ServiceRequestForm
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
