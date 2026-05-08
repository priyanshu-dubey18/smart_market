<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../composables/useAuthStore.js'

const router = useRouter()
const { state, clearAuth } = useAuthStore()

if (!state.verifiedOtp) router.push('/signin')

const newEmail = ref('')
const newUsername = ref('')
const loading = ref(false)
const error = ref('')
const showSuccess = ref(false)

async function handleSave() {
  error.value = ''
  if (!newEmail.value.trim() && !newUsername.value.trim()) {
    error.value = 'Please enter at least a new email or username.'
    return
  }
  if (newEmail.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newEmail.value)) {
    error.value = 'Invalid email format.'
    return
  }
  loading.value = true
  try {
    const res = await fetch('/api/method/smart_market.api.auth.reset_email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': 'fetch' },
      body: JSON.stringify({ phone: state.phone, new_email: newEmail.value, new_username: newUsername.value })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.message || 'Update failed.')
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
        <div class="reset-icon">✏️</div>
        <div class="card-top">
          <h1>Update Email / Username</h1>
          <p>OTP verified! Enter your new email and/or username below.</p>
        </div>
        <form @submit.prevent="handleSave" class="auth-form">
          <div class="field-group">
            <label>New Email Address <span class="optional">(optional)</span></label>
            <div class="input-wrap">
              <span class="input-icon">✉️</span>
              <input v-model="newEmail" type="email" placeholder="new.email@example.com" />
            </div>
          </div>
          <div class="field-group">
            <label>New Username <span class="optional">(optional)</span></label>
            <div class="input-wrap">
              <span class="input-icon">@</span>
              <input v-model="newUsername" type="text" placeholder="new_username" />
            </div>
          </div>
          <div v-if="error" class="error-box">⚠️ {{ error }}</div>
          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading">Save Changes →</span>
            <span v-else class="spinner"></span>
          </button>
        </form>
      </div>
    </div>
    <Transition name="modal">
      <div v-if="showSuccess" class="modal-overlay">
        <div class="modal">
          <div class="modal-icon">✅</div>
          <h2>Updated Successfully!</h2>
          <p>Your email / username has been updated. Please sign in with your new credentials.</p>
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
.orb-1 { width: 400px; height: 400px; background: #6366f1; top: -100px; left: -100px; animation: orbFloat 8s ease-in-out infinite; }
.orb-2 { width: 300px; height: 300px; background: #10b981; bottom: -50px; right: 10%; animation: orbFloat 10s ease-in-out infinite reverse; }
.grid-overlay { position: absolute; inset: 0; background-image: linear-gradient(rgba(99,102,241,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(99,102,241,0.03) 1px,transparent 1px); background-size: 50px 50px; }
@keyframes orbFloat { 0%,100%{transform:translate(0,0)} 50%{transform:translate(20px,-20px)} }
.auth-container { position: relative; z-index: 1; width: 100%; max-width: 460px; }
.auth-card { background: rgba(15,23,42,0.92); border: 1px solid rgba(99,102,241,0.15); border-radius: 24px; padding: 2.5rem; backdrop-filter: blur(20px); box-shadow: 0 25px 50px rgba(0,0,0,0.5); display: flex; flex-direction: column; align-items: center; gap: 1.5rem; text-align: center; }
.auth-logo { display: flex; align-items: center; gap: 0.5rem; }
.logo-icon { font-size: 1.3rem; }
.logo-text { font-size: 1.1rem; font-weight: 800; color: #f1f5f9; }
.accent { color: #6366f1; }
.reset-icon { width: 70px; height: 70px; border-radius: 20px; font-size: 2rem; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.25); display: flex; align-items: center; justify-content: center; }
.card-top h1 { font-size: 1.5rem; font-weight: 800; color: #f1f5f9; margin-bottom: 0.5rem; }
.card-top p { font-size: 0.85rem; color: #64748b; line-height: 1.6; }
.auth-form { width: 100%; display: flex; flex-direction: column; gap: 1.25rem; }
.field-group { display: flex; flex-direction: column; gap: 0.4rem; text-align: left; }
.optional { color: #475569; font-weight: 400; font-size: 0.75rem; }
label { font-size: 0.85rem; font-weight: 600; color: #94a3b8; }
.input-wrap { display: flex; align-items: center; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 0 1rem; transition: all 0.2s; }
.input-wrap:focus-within { border-color: #10b981; box-shadow: 0 0 0 3px rgba(16,185,129,0.1); }
.input-icon { font-size: 1rem; margin-right: 0.5rem; opacity: 0.6; font-style: normal; font-weight: 700; color: #64748b; }
.input-wrap input { flex: 1; background: none; border: none; outline: none; color: #f1f5f9; font-size: 0.95rem; padding: 0.85rem 0; font-family: inherit; }
.input-wrap input::placeholder { color: #334155; }
.error-box { width: 100%; padding: 0.75rem 1rem; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 10px; color: #fca5a5; font-size: 0.85rem; text-align: left; }
.submit-btn { width: 100%; padding: 0.9rem; border: none; border-radius: 12px; background: linear-gradient(135deg,#10b981,#059669); color: white; font-size: 1rem; font-weight: 700; cursor: pointer; transition: all 0.2s; box-shadow: 0 0 20px rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; min-height: 50px; }
.submit-btn:hover:not(:disabled) { transform: translateY(-1px); }
.submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }
.spinner { width: 22px; height: 22px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.modal-overlay { position: fixed; inset: 0; z-index: 1000; background: rgba(0,0,0,0.7); backdrop-filter: blur(8px); display: flex; align-items: center; justify-content: center; padding: 2rem; }
.modal { background: rgba(15,23,42,0.98); border: 1px solid rgba(16,185,129,0.3); border-radius: 24px; padding: 2.5rem; max-width: 380px; width: 100%; text-align: center; display: flex; flex-direction: column; gap: 1.25rem; align-items: center; }
.modal-icon { font-size: 3rem; animation: pop 0.5s ease; }
@keyframes pop { 0%{transform:scale(0)} 80%{transform:scale(1.1)} 100%{transform:scale(1)} }
.modal h2 { font-size: 1.5rem; font-weight: 800; color: #f1f5f9; }
.modal p { font-size: 0.9rem; color: #64748b; line-height: 1.6; }
.modal-btn { width: 100%; padding: 0.85rem; border: none; border-radius: 12px; background: linear-gradient(135deg,#10b981,#059669); color: white; font-size: 1rem; font-weight: 700; cursor: pointer; }
.modal-enter-active,.modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from,.modal-leave-to { opacity: 0; transform: scale(0.9); }
</style>
