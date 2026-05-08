<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../composables/useAuthStore.js'

const router = useRouter()
const { state, clearAuth } = useAuthStore()

const username = ref('')
const password = ref('')
const confirmPass = ref('')
const showPass = ref(false)
const showConfirm = ref(false)
const loading = ref(false)
const error = ref('')
const showSuccess = ref(false)

if (!state.verifiedOtp) {
  router.push('/signup')
}

const passMatch = computed(() => password.value && confirmPass.value && password.value === confirmPass.value)
const passStrength = computed(() => {
  const p = password.value
  if (p.length < 4) return 1
  if (p.length < 8) return 2
  if (p.length >= 8 && /[!@#$%^&*]/.test(p)) return 4
  return 3
})

function validate() {
  if (!username.value.trim() || username.value.length < 3) return 'Username must be at least 3 characters.'
  if (!/^[a-zA-Z0-9_]+$/.test(username.value)) return 'Username can only contain letters, numbers and underscores.'
  if (password.value.length < 8) return 'Password must be at least 8 characters.'
  if (password.value !== confirmPass.value) return 'Passwords do not match.'
  return null
}

async function handleSave() {
  error.value = validate()
  if (error.value) return

  loading.value = true
  try {
    const endpoint = state.userType === 'vendor'
      ? '/api/method/smart_market.api.auth.vendor_signup'
      : '/api/method/smart_market.api.auth.customer_signup'

    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': 'fetch' },
      body: JSON.stringify({
        full_name: state.fullName,
        email: state.email,
        phone: state.phone,
        username: username.value,
        password: password.value,
        user_type: state.userType
      })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.message || 'Account creation failed.')

    showSuccess.value = true
  } catch (e) {
    error.value = e.message || 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}

function goToDashboard() {
  clearAuth()
  router.push('/service-request')
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

        <div class="card-top">
          <div class="user-badge" :class="state.userType === 'vendor' ? 'vendor-badge' : 'customer-badge'">
            {{ state.userType === 'vendor' ? '🏢 Vendor' : '👤 Customer' }}
          </div>
          <h1>Set Your Credentials</h1>
          <p>Choose a username and a strong password to secure your account.</p>
        </div>

        <form @submit.prevent="handleSave" class="auth-form">

          <div class="field-group">
            <label>Username</label>
            <div class="input-wrap">
              <span class="input-icon">@</span>
              <input v-model="username" type="text" placeholder="e.g. john_doe123" autocomplete="username" />
            </div>
            <span class="field-hint">Only letters, numbers, underscores. Min 3 chars.</span>
          </div>

          <div class="field-group">
            <label>New Password</label>
            <div class="input-wrap">
              <span class="input-icon">🔒</span>
              <input v-model="password" :type="showPass ? 'text' : 'password'" placeholder="Min. 8 characters" autocomplete="new-password" />
              <button type="button" class="toggle-pass" @click="showPass = !showPass">{{ showPass ? '🙈' : '👁️' }}</button>
            </div>
          </div>

          <!-- Strength bar -->
          <div class="pass-strength" v-if="password.length > 0">
            <div class="strength-bars">
              <div class="sbar" :class="{ w: passStrength >= 1, weak: passStrength === 1 }"></div>
              <div class="sbar" :class="{ w: passStrength >= 2, medium: passStrength === 2 }"></div>
              <div class="sbar" :class="{ w: passStrength >= 3, good: passStrength === 3 }"></div>
              <div class="sbar" :class="{ w: passStrength >= 4, strong: passStrength === 4 }"></div>
            </div>
            <span class="strength-label" :class="['','weak-text','medium-text','good-text','strong-text'][passStrength]">
              {{ ['','Weak','Fair','Good','Strong'][passStrength] }}
            </span>
          </div>

          <div class="field-group">
            <label>Re-enter Password</label>
            <div class="input-wrap" :class="{ match: passMatch, mismatch: confirmPass && !passMatch }">
              <span class="input-icon">🔑</span>
              <input v-model="confirmPass" :type="showConfirm ? 'text' : 'password'" placeholder="Repeat your password" autocomplete="new-password" />
              <button type="button" class="toggle-pass" @click="showConfirm = !showConfirm">{{ showConfirm ? '🙈' : '👁️' }}</button>
              <span class="match-icon" v-if="confirmPass">{{ passMatch ? '✅' : '❌' }}</span>
            </div>
          </div>

          <div v-if="error" class="error-box">⚠️ {{ error }}</div>

          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading">Save & Create Account →</span>
            <span v-else class="spinner"></span>
          </button>
        </form>

        <!-- Steps -->
        <div class="steps-indicator">
          <div class="step done"><div class="step-dot done-dot">✓</div><span>Details</span></div>
          <div class="step-line"></div>
          <div class="step done"><div class="step-dot done-dot">✓</div><span>Verified</span></div>
          <div class="step-line"></div>
          <div class="step active"><div class="step-dot active-dot">3</div><span>Credentials</span></div>
        </div>
      </div>
    </div>

    <!-- SUCCESS MODAL -->
    <Transition name="modal">
      <div v-if="showSuccess" class="modal-overlay" @click.self="goToDashboard">
        <div class="modal">
          <div class="modal-icon">🎉</div>
          <h2>Sign Up Successful!</h2>
          <p>
            Welcome to Smart Market, <strong>{{ state.fullName }}</strong>!<br/>
            Your {{ state.userType }} account has been created.
          </p>
          <div class="modal-user-info">
            <div class="info-row">
              <span class="info-key">Username</span>
              <span class="info-val">{{ username }}</span>
            </div>
            <div class="info-row">
              <span class="info-key">Email</span>
              <span class="info-val">{{ state.email }}</span>
            </div>
            <div class="info-row">
              <span class="info-key">Type</span>
              <span class="info-val capitalize">{{ state.userType }}</span>
            </div>
          </div>
          <button class="modal-btn" @click="goToDashboard">
            Go to Service Request →
          </button>
        </div>
      </div>
    </Transition>
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
.orb-1 { width: 450px; height: 450px; background: #10b981; top: -100px; right: -100px; animation: orbFloat 8s ease-in-out infinite; }
.orb-2 { width: 350px; height: 350px; background: #6366f1; bottom: -50px; left: 5%; animation: orbFloat 10s ease-in-out infinite reverse; }
.grid-overlay {
  position: absolute; inset: 0;
  background-image: linear-gradient(rgba(16,185,129,0.02) 1px,transparent 1px),linear-gradient(90deg,rgba(16,185,129,0.02) 1px,transparent 1px);
  background-size: 50px 50px;
}
@keyframes orbFloat { 0%,100%{transform:translate(0,0)} 50%{transform:translate(20px,-20px)} }

.auth-container { position: relative; z-index: 1; width: 100%; max-width: 520px; }
.auth-card {
  background: rgba(15,23,42,0.92); border: 1px solid rgba(16,185,129,0.15);
  border-radius: 24px; padding: 2.5rem;
  backdrop-filter: blur(20px); box-shadow: 0 25px 50px rgba(0,0,0,0.5);
  display: flex; flex-direction: column; gap: 1.5rem;
}
.auth-logo { display: flex; align-items: center; gap: 0.5rem; justify-content: center; }
.logo-icon { font-size: 1.3rem; }
.logo-text { font-size: 1.1rem; font-weight: 800; color: #f1f5f9; }
.accent { color: #6366f1; }
.card-top { }
.user-badge { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.35rem 0.85rem; border-radius: 100px; font-size: 0.8rem; font-weight: 700; margin-bottom: 0.75rem; }
.customer-badge { background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.3); color: #a5b4fc; }
.vendor-badge { background: rgba(6,182,212,0.15); border: 1px solid rgba(6,182,212,0.3); color: #67e8f9; }
.card-top h1 { font-size: 1.6rem; font-weight: 800; color: #f1f5f9; margin-bottom: 0.4rem; letter-spacing: -0.5px; }
.card-top p { font-size: 0.85rem; color: #64748b; }
.auth-form { display: flex; flex-direction: column; gap: 1.25rem; }
.field-group { display: flex; flex-direction: column; gap: 0.4rem; }
label { font-size: 0.85rem; font-weight: 600; color: #94a3b8; }
.input-wrap {
  display: flex; align-items: center;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px; padding: 0 1rem; transition: all 0.2s;
}
.input-wrap:focus-within { border-color: #10b981; background: rgba(16,185,129,0.05); box-shadow: 0 0 0 3px rgba(16,185,129,0.1); }
.input-wrap.match { border-color: rgba(16,185,129,0.5); }
.input-wrap.mismatch { border-color: rgba(239,68,68,0.4); }
.input-icon { font-size: 1rem; margin-right: 0.5rem; opacity: 0.6; flex-shrink: 0; font-style: normal; font-weight: 700; color: #64748b; }
.input-wrap input { flex: 1; background: none; border: none; outline: none; color: #f1f5f9; font-size: 0.95rem; padding: 0.85rem 0; font-family: inherit; }
.input-wrap input::placeholder { color: #334155; }
.toggle-pass { background: none; border: none; cursor: pointer; font-size: 1rem; padding: 0; opacity: 0.6; }
.match-icon { font-size: 0.9rem; margin-left: 0.25rem; }
.field-hint { font-size: 0.75rem; color: #475569; }

.pass-strength { display: flex; align-items: center; gap: 0.75rem; }
.strength-bars { display: flex; gap: 4px; flex: 1; }
.sbar { flex: 1; height: 4px; border-radius: 2px; background: rgba(255,255,255,0.08); transition: all 0.3s; }
.sbar.w { background: #ef4444; }
.sbar.w.medium { background: #f59e0b; }
.sbar.w.good { background: #22c55e; }
.sbar.w.strong { background: #10b981; }
.strength-label { font-size: 0.75rem; white-space: nowrap; }
.weak-text { color: #ef4444; } .medium-text { color: #f59e0b; } .good-text { color: #22c55e; } .strong-text { color: #10b981; }

.error-box { padding: 0.75rem 1rem; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 10px; color: #fca5a5; font-size: 0.85rem; }
.submit-btn {
  width: 100%; padding: 0.9rem; border: none; border-radius: 12px;
  background: linear-gradient(135deg,#10b981,#059669);
  color: white; font-size: 1rem; font-weight: 700; cursor: pointer; transition: all 0.2s;
  box-shadow: 0 0 20px rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; min-height: 50px;
}
.submit-btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 0 35px rgba(16,185,129,0.5); }
.submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }
.spinner { width: 22px; height: 22px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.steps-indicator { display: flex; align-items: center; gap: 0.5rem; justify-content: center; }
.step { display: flex; flex-direction: column; align-items: center; gap: 0.3rem; }
.step span { font-size: 0.7rem; color: #334155; white-space: nowrap; }
.step.active span { color: #34d399; }
.step.done span { color: #10b981; }
.step-dot { width: 28px; height: 28px; border-radius: 50%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; color: #334155; }
.active-dot { background: rgba(16,185,129,0.2); border-color: #10b981; color: #34d399; font-weight: 700; }
.done-dot { background: rgba(16,185,129,0.15); border-color: #10b981; color: #10b981; }
.step-line { flex: 1; height: 1px; background: rgba(255,255,255,0.07); min-width: 30px; }

/* SUCCESS MODAL */
.modal-overlay {
  position: fixed; inset: 0; z-index: 1000;
  background: rgba(0,0,0,0.7); backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center; padding: 2rem;
}
.modal {
  background: rgba(15,23,42,0.98); border: 1px solid rgba(16,185,129,0.3);
  border-radius: 24px; padding: 2.5rem; max-width: 420px; width: 100%;
  text-align: center; box-shadow: 0 30px 60px rgba(0,0,0,0.6), 0 0 50px rgba(16,185,129,0.1);
  display: flex; flex-direction: column; gap: 1.25rem; align-items: center;
}
.modal-icon { font-size: 3.5rem; animation: pop 0.5s ease; }
@keyframes pop { 0%{transform:scale(0)} 80%{transform:scale(1.1)} 100%{transform:scale(1)} }
.modal h2 { font-size: 1.75rem; font-weight: 800; color: #f1f5f9; letter-spacing: -0.5px; }
.modal p { font-size: 0.9rem; color: #64748b; line-height: 1.6; }
.modal-user-info { width: 100%; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; overflow: hidden; }
.info-row { display: flex; justify-content: space-between; padding: 0.65rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.04); }
.info-row:last-child { border-bottom: none; }
.info-key { font-size: 0.8rem; color: #475569; }
.info-val { font-size: 0.8rem; color: #a5b4fc; font-weight: 600; }
.capitalize { text-transform: capitalize; }
.modal-btn {
  width: 100%; padding: 0.85rem; border: none; border-radius: 12px;
  background: linear-gradient(135deg,#10b981,#059669);
  color: white; font-size: 1rem; font-weight: 700; cursor: pointer; transition: all 0.2s;
  box-shadow: 0 0 20px rgba(16,185,129,0.3);
}
.modal-btn:hover { transform: translateY(-1px); box-shadow: 0 0 35px rgba(16,185,129,0.5); }
.modal-enter-active,.modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from,.modal-leave-to { opacity: 0; transform: scale(0.9); }

@media (max-width: 560px) { .auth-card { padding: 1.5rem; } }
</style>
