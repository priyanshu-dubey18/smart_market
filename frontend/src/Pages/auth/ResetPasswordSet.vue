<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../composables/useAuthStore.js'

const router = useRouter()
const { state, clearAuth } = useAuthStore()

if (!state.verifiedOtp) router.push('/signin')

const password = ref('')
const confirmPass = ref('')
const showPass = ref(false)
const showConfirm = ref(false)
const loading = ref(false)
const error = ref('')
const showSuccess = ref(false)

const passMatch = computed(() => password.value && confirmPass.value && password.value === confirmPass.value)

async function handleSave() {
  error.value = ''
  if (password.value.length < 8) { error.value = 'Password must be at least 8 characters.'; return }
  if (password.value !== confirmPass.value) { error.value = 'Passwords do not match.'; return }

  loading.value = true
  try {
    const res = await fetch('/api/method/smart_market.api.auth.reset_password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': 'fetch' },
      body: JSON.stringify({ email: state.email, new_password: password.value })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.message || 'Password reset failed.')
    showSuccess.value = true
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
function goSignIn() { clearAuth(); router.push('/signin') }
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
        <div class="reset-icon">🔒</div>
        <div class="card-top">
          <h1>Set New Password</h1>
          <p>OTP verified! Enter and confirm your new password.</p>
        </div>
        <form @submit.prevent="handleSave" class="auth-form">
          <div class="field-group">
            <label>New Password</label>
            <div class="input-wrap">
              <span class="input-icon">🔒</span>
              <input v-model="password" :type="showPass ? 'text' : 'password'" placeholder="Min. 8 characters" autocomplete="new-password" />
              <button type="button" class="toggle-pass" @click="showPass = !showPass">{{ showPass ? '🙈' : '👁️' }}</button>
            </div>
          </div>
          <div class="field-group">
            <label>Confirm New Password</label>
            <div class="input-wrap" :class="{ match: passMatch, mismatch: confirmPass && !passMatch }">
              <span class="input-icon">🔑</span>
              <input v-model="confirmPass" :type="showConfirm ? 'text' : 'password'" placeholder="Repeat new password" autocomplete="new-password" />
              <button type="button" class="toggle-pass" @click="showConfirm = !showConfirm">{{ showConfirm ? '🙈' : '👁️' }}</button>
              <span v-if="confirmPass" class="match-icon">{{ passMatch ? '✅' : '❌' }}</span>
            </div>
          </div>
          <div v-if="error" class="error-box">⚠️ {{ error }}</div>
          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading">Save New Password →</span>
            <span v-else class="spinner"></span>
          </button>
        </form>
      </div>
    </div>
    <Transition name="modal">
      <div v-if="showSuccess" class="modal-overlay">
        <div class="modal">
          <div class="modal-icon">🔐</div>
          <h2>Password Reset!</h2>
          <p>Your password has been updated successfully. Please sign in with your new password.</p>
          <button class="modal-btn" @click="goSignIn">Go to Sign In →</button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
* { box-sizing: border-box; margin: 0; padding: 0; }
.auth-page { min-height: 100vh; background: #080d1a; display: flex; align-items: center; justify-content: center; padding: 2rem; font-family: 'Inter',-apple-system,BlinkMacSystemFont,sans-serif; position: relative; }
.auth-bg { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.orb { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.12; }
.orb-1 { width: 400px; height: 400px; background: #f59e0b; top: -100px; right: -100px; animation: orbFloat 8s ease-in-out infinite; }
.orb-2 { width: 300px; height: 300px; background: #6366f1; bottom: -50px; left: 5%; animation: orbFloat 10s ease-in-out infinite reverse; }
.grid-overlay { position: absolute; inset: 0; background-image: linear-gradient(rgba(245,158,11,0.02) 1px,transparent 1px),linear-gradient(90deg,rgba(245,158,11,0.02) 1px,transparent 1px); background-size: 50px 50px; }
@keyframes orbFloat { 0%,100%{transform:translate(0,0)} 50%{transform:translate(20px,-20px)} }
.auth-container { position: relative; z-index: 1; width: 100%; max-width: 460px; }
.auth-card { background: rgba(15,23,42,0.92); border: 1px solid rgba(245,158,11,0.15); border-radius: 24px; padding: 2.5rem; backdrop-filter: blur(20px); box-shadow: 0 25px 50px rgba(0,0,0,0.5); display: flex; flex-direction: column; align-items: center; gap: 1.5rem; text-align: center; }
.auth-logo { display: flex; align-items: center; gap: 0.5rem; }
.logo-icon { font-size: 1.3rem; }
.logo-text { font-size: 1.1rem; font-weight: 800; color: #f1f5f9; }
.accent { color: #6366f1; }
.reset-icon { width: 70px; height: 70px; border-radius: 20px; font-size: 2rem; background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.25); display: flex; align-items: center; justify-content: center; }
.card-top h1 { font-size: 1.5rem; font-weight: 800; color: #f1f5f9; margin-bottom: 0.5rem; }
.card-top p { font-size: 0.85rem; color: #64748b; line-height: 1.6; }
.auth-form { width: 100%; display: flex; flex-direction: column; gap: 1.25rem; }
.field-group { display: flex; flex-direction: column; gap: 0.4rem; text-align: left; }
label { font-size: 0.85rem; font-weight: 600; color: #94a3b8; }
.input-wrap { display: flex; align-items: center; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 0 1rem; transition: all 0.2s; }
.input-wrap:focus-within { border-color: #f59e0b; box-shadow: 0 0 0 3px rgba(245,158,11,0.1); }
.input-wrap.match { border-color: rgba(16,185,129,0.5); }
.input-wrap.mismatch { border-color: rgba(239,68,68,0.4); }
.input-icon { font-size: 1rem; margin-right: 0.5rem; opacity: 0.6; }
.input-wrap input { flex: 1; background: none; border: none; outline: none; color: #f1f5f9; font-size: 0.95rem; padding: 0.85rem 0; font-family: inherit; }
.input-wrap input::placeholder { color: #334155; }
.toggle-pass { background: none; border: none; cursor: pointer; font-size: 1rem; padding: 0; opacity: 0.6; }
.match-icon { font-size: 0.9rem; margin-left: 0.25rem; }
.error-box { width: 100%; padding: 0.75rem 1rem; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 10px; color: #fca5a5; font-size: 0.85rem; text-align: left; }
.submit-btn { width: 100%; padding: 0.9rem; border: none; border-radius: 12px; background: linear-gradient(135deg,#f59e0b,#d97706); color: white; font-size: 1rem; font-weight: 700; cursor: pointer; transition: all 0.2s; box-shadow: 0 0 20px rgba(245,158,11,0.3); display: flex; align-items: center; justify-content: center; min-height: 50px; }
.submit-btn:hover:not(:disabled) { transform: translateY(-1px); }
.submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }
.spinner { width: 22px; height: 22px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.modal-overlay { position: fixed; inset: 0; z-index: 1000; background: rgba(0,0,0,0.7); backdrop-filter: blur(8px); display: flex; align-items: center; justify-content: center; padding: 2rem; }
.modal { background: rgba(15,23,42,0.98); border: 1px solid rgba(245,158,11,0.3); border-radius: 24px; padding: 2.5rem; max-width: 380px; width: 100%; text-align: center; display: flex; flex-direction: column; gap: 1.25rem; align-items: center; }
.modal-icon { font-size: 3rem; animation: pop 0.5s ease; }
@keyframes pop { 0%{transform:scale(0)} 80%{transform:scale(1.1)} 100%{transform:scale(1)} }
.modal h2 { font-size: 1.5rem; font-weight: 800; color: #f1f5f9; }
.modal p { font-size: 0.9rem; color: #64748b; line-height: 1.6; }
.modal-btn { width: 100%; padding: 0.85rem; border: none; border-radius: 12px; background: linear-gradient(135deg,#f59e0b,#d97706); color: white; font-size: 1rem; font-weight: 700; cursor: pointer; }
.modal-enter-active,.modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from,.modal-leave-to { opacity: 0; transform: scale(0.9); }
</style>
