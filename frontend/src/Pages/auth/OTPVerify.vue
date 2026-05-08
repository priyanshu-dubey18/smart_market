<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../composables/useAuthStore.js'

const router = useRouter()
const { state, setSignupData } = useAuthStore()

// 6-digit OTP boxes
const otpDigits = ref(['', '', '', '', '', ''])
const otpRefs = ref([])
const loading = ref(false)
const error = ref('')
const resendTimer = ref(30)
const canResend = ref(false)

let timerInterval = null

onMounted(() => {
  if (!state.otpContact) {
    router.push('/signup')
    return
  }
  startTimer()
  // focus first input
  setTimeout(() => { otpRefs.value[0]?.focus() }, 100)
})
onUnmounted(() => clearInterval(timerInterval))

function startTimer() {
  resendTimer.value = 30
  canResend.value = false
  clearInterval(timerInterval)
  timerInterval = setInterval(() => {
    resendTimer.value--
    if (resendTimer.value <= 0) {
      clearInterval(timerInterval)
      canResend.value = true
    }
  }, 1000)
}

function onDigitInput(index, event) {
  const val = event.target.value.replace(/\D/g, '')
  otpDigits.value[index] = val.slice(-1)
  if (val && index < 5) {
    otpRefs.value[index + 1]?.focus()
  }
}
function onKeyDown(index, event) {
  if (event.key === 'Backspace' && !otpDigits.value[index] && index > 0) {
    otpRefs.value[index - 1]?.focus()
  }
}
function onPaste(event) {
  const pasted = event.clipboardData.getData('text').replace(/\D/g,'').slice(0, 6)
  pasted.split('').forEach((d, i) => { if (i < 6) otpDigits.value[i] = d })
  const nextEmpty = pasted.length < 6 ? pasted.length : 5
  otpRefs.value[nextEmpty]?.focus()
  event.preventDefault()
}

const otpCode = computed(() => otpDigits.value.join(''))
const isComplete = computed(() => otpCode.value.length === 6)

const maskedContact = computed(() => {
  if (!state.otpContact) return ''
  if (state.otpMedium === 'email') {
    const [u, d] = state.otpContact.split('@')
    return u.slice(0,2) + '***@' + d
  }
  return state.otpContact.slice(0,3) + '****' + state.otpContact.slice(-3)
})

async function verifyOTP() {
  if (!isComplete.value) { error.value = 'Please enter the complete 6-digit OTP.'; return }
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('/api/method/smart_market.api.auth.verify_otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': 'fetch' },
      body: JSON.stringify({ contact: state.otpContact, otp: otpCode.value, purpose: state.otpFlow })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.message || 'Invalid OTP. Please try again.')

    setSignupData({ verifiedOtp: true })

    if (state.otpFlow === 'signup') {
      router.push('/auth/credentials')
    } else if (state.otpFlow === 'reset-email') {
      router.push('/auth/reset-email-set')
    } else if (state.otpFlow === 'reset-password') {
      router.push('/auth/reset-password-set')
    }
  } catch (e) {
    error.value = e.message || 'Invalid OTP. Please try again.'
    otpDigits.value = ['','','','','','']
    setTimeout(() => otpRefs.value[0]?.focus(), 50)
  } finally {
    loading.value = false
  }
}

async function resendOTP() {
  if (!canResend.value) return
  loading.value = true
  error.value = ''
  try {
    await fetch('/api/method/smart_market.api.auth.send_otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': 'fetch' },
      body: JSON.stringify({ medium: state.otpMedium, contact: state.otpContact, purpose: state.otpFlow })
    })
    startTimer()
    otpDigits.value = ['','','','','','']
    otpRefs.value[0]?.focus()
  } catch {
    error.value = 'Failed to resend OTP.'
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
      <div class="auth-card">
        <div class="auth-logo">
          <span class="logo-icon">⚡</span>
          <span class="logo-text">Smart<span class="accent">Market</span></span>
        </div>

        <div class="otp-icon-wrap">
          <div class="otp-icon">
            <span>{{ state.otpMedium === 'email' ? '📧' : '📱' }}</span>
          </div>
        </div>

        <div class="card-top">
          <h1>Verify Your {{ state.otpMedium === 'email' ? 'Email' : 'Phone' }}</h1>
          <p>
            We've sent a 6-digit verification code to<br/>
            <strong class="contact-highlight">{{ maskedContact }}</strong>
          </p>
        </div>

        <!-- OTP Boxes -->
        <div class="otp-boxes" @paste="onPaste">
          <input
            v-for="(_, i) in otpDigits"
            :key="i"
            :ref="el => otpRefs[i] = el"
            class="otp-box"
            :class="{ filled: otpDigits[i], error: error }"
            type="text"
            inputmode="numeric"
            maxlength="1"
            :value="otpDigits[i]"
            @input="onDigitInput(i, $event)"
            @keydown="onKeyDown(i, $event)"
          />
        </div>

        <div v-if="error" class="error-box">⚠️ {{ error }}</div>

        <button
          class="submit-btn"
          :class="{ ready: isComplete }"
          :disabled="loading || !isComplete"
          @click="verifyOTP"
        >
          <span v-if="!loading">Verify OTP →</span>
          <span v-else class="spinner"></span>
        </button>

        <!-- Resend -->
        <div class="resend-row">
          <span class="resend-text">Didn't receive the code?</span>
          <button
            class="resend-btn"
            :class="{ active: canResend }"
            :disabled="!canResend"
            @click="resendOTP"
          >
            {{ canResend ? 'Resend OTP' : `Resend in ${resendTimer}s` }}
          </button>
        </div>

        <div class="steps-indicator">
          <div class="step done">
            <div class="step-dot done-dot">✓</div>
            <span>Details</span>
          </div>
          <div class="step-line"></div>
          <div class="step active">
            <div class="step-dot active-dot">2</div>
            <span>Verify OTP</span>
          </div>
          <div class="step-line"></div>
          <div class="step">
            <div class="step-dot">3</div>
            <span>Set Credentials</span>
          </div>
        </div>
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
.orb-1 { width: 400px; height: 400px; background: #6366f1; top: -100px; left: -100px; animation: orbFloat 8s ease-in-out infinite; }
.orb-2 { width: 300px; height: 300px; background: #10b981; bottom: -50px; right: 10%; animation: orbFloat 10s ease-in-out infinite reverse; }
.grid-overlay {
  position: absolute; inset: 0;
  background-image: linear-gradient(rgba(99,102,241,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(99,102,241,0.03) 1px,transparent 1px);
  background-size: 50px 50px;
}
@keyframes orbFloat { 0%,100%{transform:translate(0,0)} 50%{transform:translate(20px,-20px)} }

.auth-container { position: relative; z-index: 1; width: 100%; max-width: 460px; }
.auth-card {
  background: rgba(15,23,42,0.92); border: 1px solid rgba(99,102,241,0.15);
  border-radius: 24px; padding: 2.5rem;
  backdrop-filter: blur(20px); box-shadow: 0 25px 50px rgba(0,0,0,0.5);
  display: flex; flex-direction: column; align-items: center; gap: 1.5rem;
  text-align: center;
}
.auth-logo { display: flex; align-items: center; gap: 0.5rem; }
.logo-icon { font-size: 1.3rem; }
.logo-text { font-size: 1.1rem; font-weight: 800; color: #f1f5f9; }
.accent { color: #6366f1; }

.otp-icon-wrap { }
.otp-icon {
  width: 72px; height: 72px; border-radius: 20px;
  background: linear-gradient(135deg,rgba(99,102,241,0.2),rgba(99,102,241,0.05));
  border: 1px solid rgba(99,102,241,0.3);
  display: flex; align-items: center; justify-content: center; font-size: 2rem;
}

.card-top { }
.card-top h1 { font-size: 1.6rem; font-weight: 800; color: #f1f5f9; margin-bottom: 0.5rem; letter-spacing: -0.5px; }
.card-top p { font-size: 0.9rem; color: #64748b; line-height: 1.6; }
.contact-highlight { color: #a5b4fc; font-weight: 700; }

/* OTP BOXES */
.otp-boxes { display: flex; gap: 0.6rem; }
.otp-box {
  width: 52px; height: 60px;
  background: rgba(255,255,255,0.04);
  border: 2px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  font-size: 1.5rem; font-weight: 800; color: #f1f5f9;
  text-align: center; outline: none;
  transition: all 0.2s; font-family: inherit;
  caret-color: #6366f1;
}
.otp-box:focus { border-color: #6366f1; background: rgba(99,102,241,0.08); box-shadow: 0 0 0 3px rgba(99,102,241,0.15); }
.otp-box.filled { border-color: rgba(99,102,241,0.5); background: rgba(99,102,241,0.05); }
.otp-box.error { border-color: rgba(239,68,68,0.5); animation: shake 0.3s ease; }
@keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-4px)} 75%{transform:translateX(4px)} }

.error-box { width: 100%; padding: 0.75rem 1rem; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 10px; color: #fca5a5; font-size: 0.85rem; }

.submit-btn {
  width: 100%; padding: 0.9rem; border: none; border-radius: 12px;
  background: rgba(99,102,241,0.2); border: 1px solid rgba(99,102,241,0.3);
  color: #64748b; font-size: 1rem; font-weight: 700; cursor: not-allowed;
  transition: all 0.3s; min-height: 50px; display: flex; align-items: center; justify-content: center;
}
.submit-btn.ready {
  background: linear-gradient(135deg,#6366f1,#4f46e5);
  border-color: transparent; color: white; cursor: pointer;
  box-shadow: 0 0 20px rgba(99,102,241,0.3);
}
.submit-btn.ready:hover { transform: translateY(-1px); box-shadow: 0 0 35px rgba(99,102,241,0.5); }
.spinner { width: 22px; height: 22px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.resend-row { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; justify-content: center; }
.resend-text { font-size: 0.85rem; color: #475569; }
.resend-btn { background: none; border: none; font-size: 0.85rem; font-weight: 600; color: #334155; cursor: not-allowed; transition: color 0.2s; }
.resend-btn.active { color: #6366f1; cursor: pointer; }
.resend-btn.active:hover { color: #a5b4fc; }

/* STEPS */
.steps-indicator { display: flex; align-items: center; gap: 0.5rem; }
.step { display: flex; flex-direction: column; align-items: center; gap: 0.3rem; }
.step span { font-size: 0.7rem; color: #334155; white-space: nowrap; }
.step.active span { color: #a5b4fc; }
.step.done span { color: #10b981; }
.step-dot {
  width: 28px; height: 28px; border-radius: 50%;
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; color: #334155;
}
.active-dot { background: rgba(99,102,241,0.2); border-color: #6366f1; color: #a5b4fc; font-weight: 700; }
.done-dot { background: rgba(16,185,129,0.15); border-color: #10b981; color: #10b981; }
.step-line { flex: 1; height: 1px; background: rgba(255,255,255,0.07); min-width: 30px; }

@media (max-width: 480px) {
  .otp-box { width: 42px; height: 52px; font-size: 1.2rem; }
  .otp-boxes { gap: 0.4rem; }
  .auth-card { padding: 1.5rem; }
}
</style>
