<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// Auth pages and Home handle their own navbar — no global nav needed
const hideNav = computed(() => {
  const noNavRoutes = ['Home', 'SignUpChoice', 'CustomerSignUp', 'VendorSignUp',
    'OTPVerify', 'SetCredentials', 'SignIn',
    'ResetEmail', 'ResetEmailSet', 'ResetPassword', 'ResetPasswordSet']
  return noNavRoutes.includes(route.name)
})
</script>

<template>
  <div>
    <nav v-if="!hideNav" class="global-nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/service-request">Service Request</router-link> |
      <router-link to="/about">About</router-link>
    </nav>
    <router-view />
  </div>
</template>

<style scoped>
.global-nav {
  background: rgba(15,23,42,0.95);
  padding: 0.75rem 1.5rem;
  border-bottom: 1px solid rgba(99,102,241,0.15);
  font-family: 'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
  font-size: 0.9rem;
}
.global-nav a {
  color: #94a3b8;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}
.global-nav a:hover,
.global-nav a.router-link-active { color: #a5b4fc; }
</style>
