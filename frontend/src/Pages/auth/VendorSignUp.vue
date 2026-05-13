<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../composables/useAuthStore.js'

const router = useRouter()
const { setSignupData } = useAuthStore()

const fullName = ref('')
const email = ref('')
const phone = ref('')
const password = ref('')
const showPass = ref(false)
const loading = ref(false)
const error = ref('')

function validate() {
  if (!fullName.value.trim()) return 'Full name is required.'
  if (!email.value.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) return 'Valid email is required.'
  if (!phone.value.trim() || !/^\d{10}$/.test(phone.value.replace(/\s/g,''))) return 'Valid 10-digit phone number is required.'
  if (password.value.length < 8) return 'Password must be at least 8 characters.'
  return null
}

async function handleSubmit() {
  error.value = validate()
  if (error.value) return

  loading.value = true
  try {
    // Backend verifies if this email/user exists as an Employee or User
    const checkRes = await fetch('/api/method/smart_market.api.auth.check_vendor_eligibility', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': 'fetch' },
      body: JSON.stringify({ email: email.value, full_name: fullName.value })
    })
    const checkData = await checkRes.json()
    if (!checkRes.ok) throw new Error(checkData.message || 'Vendor verification failed. Contact your administrator.')
    if (!checkData.message?.eligible) throw new Error('Your email is not registered in the system. Please contact the administrator.')

    // Send OTP to registered email
    const otpRes = await fetch('/api/method/smart_market.api.auth.send_otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': 'fetch' },
      body: JSON.stringify({ medium: 'email', contact: email.value, purpose: 'vendor_signup' })
    })
    const otpData = await otpRes.json()
    if (!otpRes.ok) throw new Error(otpData.message || 'Failed to send OTP')

    setSignupData({
      userType: 'vendor',
      devOtp: otpData.dev_otp || '',
      fullName: fullName.value,
      email: email.value,
      phone: phone.value,
      password: password.value,
      otpFlow: 'signup',
      otpContact: email.value,
      otpMedium: 'email'
    })
    router.push('/auth/otp')
  } catch (e) {
    error.value = e.message || 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-bg">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="grid-overlay"></div>
    </div>

    <div class="auth-container">
      <button class="back-btn" @click="router.push('/signup')">← Back</button>

      <div class="auth-card">
        <div class="auth-logo">
          <span class="logo-icon">⚡</span>
          <span class="logo-text">Smart<span class="accent">Market</span></span>
        </div>

        <div class="card-top">
          <div class="user-badge vendor-badge">
            <span>🏢</span> Vendor Registration
          </div>
          <h1>Join as Vendor</h1>
          <p>Your email must be pre-registered by the administrator as an Employee or User in the system.</p>
        </div>

        <div class="info-box">
          <span class="info-icon">ℹ️</span>
          <p>Vendor registration requires prior authorization. Only pre-approved employees or users can sign up as vendors.</p>
        </div>

        <form @submit.prevent="handleSubmit" class="auth-form">

          <div class="field-group">
            <label>Full Name</label>
            <div class="input-wrap">
              <span class="input-icon">👤</span>
              <input v-model="fullName" type="text" placeholder="Enter your full name" autocomplete="name" />
            </div>
          </div>

          <div class="field-group">
            <label>Work Email Address</label>
            <div class="input-wrap">
              <span class="input-icon">✉️</span>
              <input v-model="email" type="email" placeholder="your.work@email.com" autocomplete="email" />
            </div>
            <span class="field-hint">Must match the email registered in the system</span>
          </div>

          <div class="field-group">
            <label>Phone Number</label>
            <div class="input-wrap">
              <span class="input-icon">📱</span>
              <input v-model="phone" type="tel" placeholder="10-digit mobile number" maxlength="10" />
            </div>
            <span class="field-hint">Phone used for account identification only</span>
          </div>

          <div class="field-group">
            <label>Password</label>
            <div class="input-wrap">
              <span class="input-icon">🔒</span>
              <input v-model="password" :type="showPass ? 'text' : 'password'" placeholder="Min. 8 characters" autocomplete="new-password" />
              <button type="button" class="toggle-pass" @click="showPass = !showPass">{{ showPass ? '🙈' : '👁️' }}</button>
            </div>
          </div>

          <div class="pass-strength" v-if="password.length > 0">
            <div class="strength-bars">
              <div class="sbar" :class="{ active: password.length >= 1 }"></div>
              <div class="sbar" :class="{ active: password.length >= 4, medium: password.length >= 4 && password.length < 8 }"></div>
              <div class="sbar" :class="{ active: password.length >= 8, strong: password.length >= 8 }"></div>
              <div class="sbar" :class="{ active: password.length >= 12 && /[!@#$%^&*]/.test(password), strong: true }"></div>
            </div>
            <span class="strength-label">
              {{ password.length < 4 ? 'Weak' : password.length < 8 ? 'Fair' : password.length < 12 ? 'Good' : 'Strong' }}
            </span>
          </div>

          <div v-if="error" class="error-box">⚠️ {{ error }}</div>

          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading">Verify & Send OTP →</span>
            <span v-else class="spinner"></span>
          </button>
        </form>

        <p class="auth-footer-text">
          Already registered?
          <button class="link-btn" @click="router.push('/signin')">Sign In</button>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
* { box-sizing: border-box; margin: 0; padding: 0; }
.auth-page {
  min-height: 100vh; background: #080d1a;
  display: flex; align-items: center; justify-content: center;
  padding: 2rem; font-family: 'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
  position: relative;
}
.auth-bg { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.orb { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.12; }
.orb-1 { width: 500px; height: 500px; background: #06b6d4; top: -150px; right: -150px; animation: orbFloat 8s ease-in-out infinite; }
.orb-2 { width: 350px; height: 350px; background: #6366f1; bottom: -50px; left: 5%; animation: orbFloat 10s ease-in-out infinite reverse; }
.grid-overlay {
  position: absolute; inset: 0;
  background-image: linear-gradient(rgba(6,182,212,0.02) 1px,transparent 1px),linear-gradient(90deg,rgba(6,182,212,0.02) 1px,transparent 1px);
  background-size: 50px 50px;
}
@keyframes orbFloat { 0%,100%{transform:translate(0,0)} 50%{transform:translate(20px,-20px)} }

.auth-container { position: relative; z-index: 1; width: 100%; max-width: 520px; }
.back-btn { background: none; border: none; color: #64748b; font-size: 0.9rem; cursor: pointer; margin-bottom: 1.5rem; transition: color 0.2s; padding: 0; display: block; }
.back-btn:hover { color: #67e8f9; }
.auth-card {
  background: rgba(15,23,42,0.92); border: 1px solid rgba(6,182,212,0.15);
  border-radius: 24px; padding: 2.5rem;
  backdrop-filter: blur(20px); box-shadow: 0 25px 50px rgba(0,0,0,0.5);
}
.auth-logo { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1.5rem; justify-content: center; }
.logo-icon { font-size: 1.3rem; }
.logo-text { font-size: 1.1rem; font-weight: 800; color: #f1f5f9; }
.accent { color: #6366f1; }
.card-top { margin-bottom: 1.25rem; }
.user-badge { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.35rem 0.85rem; border-radius: 100px; font-size: 0.8rem; font-weight: 700; margin-bottom: 1rem; }
.vendor-badge { background: rgba(6,182,212,0.15); border: 1px solid rgba(6,182,212,0.3); color: #67e8f9; }
.card-top h1 { font-size: 1.6rem; font-weight: 800; color: #f1f5f9; margin-bottom: 0.5rem; letter-spacing: -0.5px; }
.card-top p { font-size: 0.85rem; color: #64748b; line-height: 1.5; }

.info-box {
  display: flex; gap: 0.75rem; align-items: flex-start;
  padding: 0.85rem 1rem; margin-bottom: 1.5rem;
  background: rgba(6,182,212,0.08); border: 1px solid rgba(6,182,212,0.2); border-radius: 12px;
}
.info-icon { font-size: 1rem; flex-shrink: 0; margin-top: 1px; }
.info-box p { font-size: 0.8rem; color: #67e8f9; line-height: 1.5; }

.auth-form { display: flex; flex-direction: column; gap: 1.25rem; }
.field-group { display: flex; flex-direction: column; gap: 0.4rem; }
label { font-size: 0.85rem; font-weight: 600; color: #94a3b8; }
.input-wrap {
  display: flex; align-items: center;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px; padding: 0 1rem; transition: all 0.2s;
}
.input-wrap:focus-within { border-color: #06b6d4; background: rgba(6,182,212,0.05); box-shadow: 0 0 0 3px rgba(6,182,212,0.1); }
.input-icon { font-size: 1rem; margin-right: 0.5rem; opacity: 0.6; flex-shrink: 0; }
.input-wrap input { flex: 1; background: none; border: none; outline: none; color: #f1f5f9; font-size: 0.95rem; padding: 0.85rem 0; font-family: inherit; }
.input-wrap input::placeholder { color: #334155; }
.toggle-pass { background: none; border: none; cursor: pointer; font-size: 1rem; padding: 0; opacity: 0.6; transition: opacity 0.2s; }
.toggle-pass:hover { opacity: 1; }
.field-hint { font-size: 0.75rem; color: #475569; }

.pass-strength { display: flex; align-items: center; gap: 0.75rem; }
.strength-bars { display: flex; gap: 4px; flex: 1; }
.sbar { flex: 1; height: 4px; border-radius: 2px; background: rgba(255,255,255,0.08); transition: all 0.3s; }
.sbar.active { background: #ef4444; }
.sbar.active.medium { background: #f59e0b; }
.sbar.active.strong { background: #10b981; }
.strength-label { font-size: 0.75rem; color: #64748b; white-space: nowrap; }

.error-box { padding: 0.75rem 1rem; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 10px; color: #fca5a5; font-size: 0.85rem; }
.submit-btn {
  width: 100%; padding: 0.9rem; border: none; border-radius: 12px;
  background: linear-gradient(135deg,#06b6d4,#0891b2);
  color: white; font-size: 1rem; font-weight: 700; cursor: pointer; transition: all 0.2s;
  box-shadow: 0 0 20px rgba(6,182,212,0.3); display: flex; align-items: center; justify-content: center; min-height: 50px;
}
.submit-btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 0 35px rgba(6,182,212,0.5); }
.submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }
.spinner { width: 22px; height: 22px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.auth-footer-text { text-align: center; font-size: 0.9rem; color: #475569; margin-top: 1.5rem; }
.link-btn { background: none; border: none; color: #06b6d4; font-weight: 600; cursor: pointer; font-size: 0.9rem; transition: color 0.2s; }
.link-btn:hover { color: #67e8f9; }
@media (max-width: 560px) { .auth-card { padding: 1.5rem; } }
</style>
