import { createRouter, createWebHistory } from 'vue-router'

import Home from '../Pages/Home.vue'
import About from '../Pages/About.vue'
import ServiceRequestForm from '../Pages/ServiceRequestForm.vue'
import CustomerDashboard from '../Pages/CustomerDashboard.vue'
import TechnicianDashboard from '../Pages/TechnicianDashboard.vue'
import SignUpChoice from '../Pages/auth/SignUpChoice.vue'
import CustomerSignUp from '../Pages/auth/CustomerSignUp.vue'
import VendorSignUp from '../Pages/auth/VendorSignUp.vue'
import OTPVerify from '../Pages/auth/OTPVerify.vue'
import SetCredentials from '../Pages/auth/SetCredentials.vue'
import SignIn from '../Pages/auth/SignIn.vue'
import ResetEmail from '../Pages/auth/ResetEmail.vue'
import ResetEmailSet from '../Pages/auth/ResetEmailSet.vue'
import ResetPassword from '../Pages/auth/ResetPassword.vue'
import ResetPasswordSet from '../Pages/auth/ResetPasswordSet.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/about', name: 'About', component: About },
  { path: '/service-request', name: 'ServiceRequest', component: ServiceRequestForm },
  { path: '/dashboard/customer', name: 'CustomerDashboard', component: CustomerDashboard },
  { path: '/dashboard/technician', name: 'TechnicianDashboard', component: TechnicianDashboard },

  // Auth — Sign Up
  { path: '/signup', name: 'SignUpChoice', component: SignUpChoice },
  { path: '/signup/customer', name: 'CustomerSignUp', component: CustomerSignUp },
  { path: '/signup/vendor', name: 'VendorSignUp', component: VendorSignUp },

  // Auth — OTP + Credentials
  { path: '/auth/otp', name: 'OTPVerify', component: OTPVerify },
  { path: '/auth/credentials', name: 'SetCredentials', component: SetCredentials },

  // Auth — Sign In
  { path: '/signin', name: 'SignIn', component: SignIn },

  // Auth — Reset
  { path: '/auth/reset-email', name: 'ResetEmail', component: ResetEmail },
  { path: '/auth/reset-email-set', name: 'ResetEmailSet', component: ResetEmailSet },
  { path: '/auth/reset-password', name: 'ResetPassword', component: ResetPassword },
  { path: '/auth/reset-password-set', name: 'ResetPasswordSet', component: ResetPasswordSet },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
