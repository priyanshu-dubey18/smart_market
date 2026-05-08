<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../composables/useAuthStore.js'

const router = useRouter()
const { setSignupData } = useAuthStore()

const identifier = ref('')   // email or username
const password = ref('')
const showPass = ref(false)
const loading = ref(false)
const error = ref('')
const showSuccess = ref(false)
const loggedUser = ref(null)

async function handleLogin() {
  error.value = ''
  if (!identifier.value.trim()) { error.value = 'Email or username is required.'; return }
  if (!password.value) { error.value = 'Password is required.'; return }

  loading.value = true
  try {
    const res = await fetch('/api/method/smart_market.api.auth.login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': 'fetch' },
      body: JSON.stringify({ identifier: identifier.value.trim(), password: password.value })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.message || 'Invalid credentials. Please try again.')

    loggedUser.value = data.message
    showSuccess.value = true
  } catch (e) {
    error.value = e.message || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}

function goToDashboard() {
  showSuccess.value = false
  router.push('/service-request')
}

function goResetEmail() {
  setSignupData({ otpFlow: 'reset-email', otpMedium: 'phone' })
  router.push('/auth/reset-email')
}
function goResetPassword() {
  setSignupData({ otpFlow: 'reset-password', otpMedium: 'email' })
  router.push('/auth/reset-password')
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
      <button class="back-btn" @click="router.push('/')">← Back to Home</button>

      <div class="auth-card">
        <div class="auth-logo">
          <span class="logo-icon">⚡</span>
          <span class="logo-text">Smart<span class="accent">Market</span></span>
        </div>

        <div class="card-top">
          <h1>Welcome Back</h1>
          <p>Sign in to your Smart Market account</p>
        </div>

        <!-- User type tabs -->
        <div class="user-tabs">
          <div class="tab-info">Sign in as Customer or Vendor — same form, backend identifies your role.</div>
        </div>

        <form @submit.prevent="handleLogin" class="auth-form">

          <div class="field-group">
            <label>Email or Username</label>
            <div class="input-wrap">
              <span class="input-icon">👤</span>
              <input v-model="identifier" type="text" placeholder="Enter email or username" autocomplete="username" />
            </div>
          </div>

          <div class="field-group">
            <label>Password</label>
            <div class="input-wrap">
              <span class="input-icon">🔒</span>
              <input v-model="password" :type="showPass ? 'text' : 'password'" placeholder="Your password" autocomplete="current-password" />
              <button type="button" class="toggle-pass" @click="showPass = !showPass">{{ showPass ? '🙈' : '👁️' }}</button>
            </div>
          </div>

          <div v-if="error" class="error-box">⚠️ {{ error }}</div>

          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading">Sign In →</span>
            <span v-else class="spinner"></span>
          </button>
        </form>

        <!-- Forgot links -->
        <div class="forgot-section">
          <p class="forgot-title">Forgot your credentials?</p>
          <div class="forgot-btns">
            <button class="forgot-btn email-reset" @click="goResetEmail">
              <span class="fb-icon">✉️</span>
              <div>
                <div class="fb-title">Reset Email / Username</div>
                <div class="fb-desc">OTP sent to your phone</div>
              </div>
            </button>
            <button class="forgot-btn pass-reset" @click="goResetPassword">
              <span class="fb-icon">🔑</span>
              <div>
                <div class="fb-title">Reset Password</div>
                <div class="fb-desc">OTP sent to your email</div>
              </div>
            </button>
          </div>
        </div>

        <p class="auth-footer-text">
          Don't have an account?
          <button class="link-btn" @click="router.push('/signup')">Create Account</button>
        </p>
      </div>
    </div>

    <!-- SUCCESS MODAL -->
    <Transition name="modal">
      <div v-if="showSuccess" class="modal-overlay" @click.self="goToDashboard">
        <div class="modal">
          <div class="modal-icon">🎊</div>
          <h2>Login Successful!</h2>
          <p>
            Welcome back, <strong>{{ loggedUser?.full_name || identifier }}</strong>!<br/>
            Redirecting you to the dashboard.
          </p>
          <div class="modal-user-info" v-if="loggedUser">
            <div class="info-row">
              <span class="info-key">Role</span>
              <span class="info-val capitalize">{{ loggedUser.user_type || 'User' }}</span>
            </div>
            <div class="info-row">
              <span class="info-key">Email</span>
              <span class="info-val">{{ loggedUser.email || identifier }}</span>
            </div>
          </div>
          <button class="modal-btn" @click="goToDashboard">Go to Service Request →</button>
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
.orb-1 { width: 500px; height: 500px; background: #6366f1; top: -150px; left: -100px; animation: orbFloat 8s ease-in-out infinite; }
.orb-2 { width: 350px; height: 350px; background: #f59e0b; bottom: -50px; right: 5%; animation: orbFloat 12s ease-in-out infinite reverse; }
.grid-overlay {
  position: absolute; inset: 0;
  background-image: linear-gradient(rgba(99,102,241,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(99,102,241,0.03) 1px,transparent 1px);
  background-size: 50px 50px;
}
@keyframes orbFloat { 0%,100%{transform:translate(0,0)} 50%{transform:translate(20px,-20px)} }

.auth-container { position: relative; z-index: 1; width: 100%; max-width: 480px; }
.back-btn { background: none; border: none; color: #64748b; font-size: 0.9rem; cursor: pointer; margin-bottom: 1.5rem; transition: color 0.2s; padding: 0; display: block; }
.back-btn:hover { color: #a5b4fc; }
.auth-card {
  background: rgba(15,23,42,0.92); border: 1px solid rgba(99,102,241,0.15);
  border-radius: 24px; padding: 2.5rem;
  backdrop-filter: blur(20px); box-shadow: 0 25px 50px rgba(0,0,0,0.5);
  display: flex; flex-direction: column; gap: 1.5rem;
}
.auth-logo { display: flex; align-items: center; gap: 0.5rem; justify-content: center; }
.logo-icon { font-size: 1.3rem; }
.logo-text { font-size: 1.1rem; font-weight: 800; color: #f1f5f9; }
.accent { color: #6366f1; }
.card-top { text-align: center; }
.card-top h1 { font-size: 1.75rem; font-weight: 800; color: #f1f5f9; margin-bottom: 0.4rem; letter-spacing: -0.5px; }
.card-top p { font-size: 0.9rem; color: #64748b; }

.user-tabs { }
.tab-info {
  padding: 0.6rem 0.85rem; background: rgba(99,102,241,0.06);
  border: 1px solid rgba(99,102,241,0.15); border-radius: 10px;
  font-size: 0.8rem; color: #64748b; text-align: center;
}

.auth-form { display: flex; flex-direction: column; gap: 1.25rem; }
.field-group { display: flex; flex-direction: column; gap: 0.4rem; }
label { font-size: 0.85rem; font-weight: 600; color: #94a3b8; }
.input-wrap {
  display: flex; align-items: center;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px; padding: 0 1rem; transition: all 0.2s;
}
.input-wrap:focus-within { border-color: #6366f1; background: rgba(99,102,241,0.05); box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }
.input-icon { font-size: 1rem; margin-right: 0.5rem; opacity: 0.6; flex-shrink: 0; }
.input-wrap input { flex: 1; background: none; border: none; outline: none; color: #f1f5f9; font-size: 0.95rem; padding: 0.85rem 0; font-family: inherit; }
.input-wrap input::placeholder { color: #334155; }
.toggle-pass { background: none; border: none; cursor: pointer; font-size: 1rem; padding: 0; opacity: 0.6; }

.error-box { padding: 0.75rem 1rem; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 10px; color: #fca5a5; font-size: 0.85rem; }

.submit-btn {
  width: 100%; padding: 0.9rem; border: none; border-radius: 12px;
  background: linear-gradient(135deg,#6366f1,#4f46e5);
  color: white; font-size: 1rem; font-weight: 700; cursor: pointer; transition: all 0.2s;
  box-shadow: 0 0 20px rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; min-height: 50px;
}
.submit-btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 0 35px rgba(99,102,241,0.5); }
.submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }
.spinner { width: 22px; height: 22px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.forgot-section { }
.forgot-title { font-size: 0.8rem; color: #475569; margin-bottom: 0.75rem; font-weight: 600; }
.forgot-btns { display: flex; gap: 0.75rem; }
.forgot-btn {
  flex: 1; display: flex; align-items: center; gap: 0.6rem;
  padding: 0.75rem; border-radius: 12px; cursor: pointer; transition: all 0.2s;
  text-align: left; border: 1px solid rgba(255,255,255,0.06);
  background: rgba(255,255,255,0.03);
}
.email-reset:hover { border-color: rgba(99,102,241,0.4); background: rgba(99,102,241,0.05); }
.pass-reset:hover { border-color: rgba(245,158,11,0.4); background: rgba(245,158,11,0.05); }
.fb-icon { font-size: 1.2rem; flex-shrink: 0; }
.fb-title { font-size: 0.8rem; font-weight: 700; color: #94a3b8; }
.fb-desc { font-size: 0.7rem; color: #475569; margin-top: 2px; }
.email-reset:hover .fb-title { color: #a5b4fc; }
.pass-reset:hover .fb-title { color: #fbbf24; }

.auth-footer-text { text-align: center; font-size: 0.9rem; color: #475569; }
.link-btn { background: none; border: none; color: #6366f1; font-weight: 600; cursor: pointer; font-size: 0.9rem; transition: color 0.2s; }
.link-btn:hover { color: #a5b4fc; }

/* SUCCESS MODAL */
.modal-overlay {
  position: fixed; inset: 0; z-index: 1000;
  background: rgba(0,0,0,0.7); backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center; padding: 2rem;
}
.modal {
  background: rgba(15,23,42,0.98); border: 1px solid rgba(99,102,241,0.3);
  border-radius: 24px; padding: 2.5rem; max-width: 400px; width: 100%;
  text-align: center; box-shadow: 0 30px 60px rgba(0,0,0,0.6);
  display: flex; flex-direction: column; gap: 1.25rem; align-items: center;
}
.modal-icon { font-size: 3.5rem; animation: pop 0.5s ease; }
@keyframes pop { 0%{transform:scale(0)} 80%{transform:scale(1.1)} 100%{transform:scale(1)} }
.modal h2 { font-size: 1.75rem; font-weight: 800; color: #f1f5f9; }
.modal p { font-size: 0.9rem; color: #64748b; line-height: 1.6; }
.modal-user-info { width: 100%; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; overflow: hidden; }
.info-row { display: flex; justify-content: space-between; padding: 0.65rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.04); }
.info-row:last-child { border-bottom: none; }
.info-key { font-size: 0.8rem; color: #475569; }
.info-val { font-size: 0.8rem; color: #a5b4fc; font-weight: 600; }
.capitalize { text-transform: capitalize; }
.modal-btn {
  width: 100%; padding: 0.85rem; border: none; border-radius: 12px;
  background: linear-gradient(135deg,#6366f1,#4f46e5);
  color: white; font-size: 1rem; font-weight: 700; cursor: pointer; transition: all 0.2s;
  box-shadow: 0 0 20px rgba(99,102,241,0.3);
}
.modal-btn:hover { transform: translateY(-1px); }
.modal-enter-active,.modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from,.modal-leave-to { opacity: 0; transform: scale(0.9); }
@media (max-width: 560px) { .auth-card { padding: 1.5rem; } .forgot-btns { flex-direction: column; } }
</style>
