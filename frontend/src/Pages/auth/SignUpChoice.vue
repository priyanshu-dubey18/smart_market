<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="auth-page">
    <div class="auth-bg">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="grid-overlay"></div>
    </div>

    <div class="auth-container">
      <!-- Back -->
      <button class="back-btn" @click="router.push('/')">← Back to Home</button>

      <div class="auth-card">
        <div class="auth-logo">
          <span class="logo-icon">⚡</span>
          <span class="logo-text">Smart<span class="accent">Market</span></span>
        </div>

        <div class="auth-header">
          <h1>Create an Account</h1>
          <p>Choose how you'd like to join Smart Market</p>
        </div>

        <div class="choice-cards">
          <!-- Customer -->
          <button class="choice-card customer-card" @click="router.push('/signup/customer')">
            <div class="choice-icon-wrap customer-icon">
              <span class="choice-icon">👤</span>
            </div>
            <div class="choice-info">
              <h3>Customer</h3>
              <p>Raise service requests for your equipment and track repairs in real time.</p>
            </div>
            <div class="choice-features">
              <span class="cf-item">✓ Submit service tickets</span>
              <span class="cf-item">✓ Track repair progress</span>
              <span class="cf-item">✓ Get SMS & email alerts</span>
            </div>
            <div class="choice-arrow">→</div>
          </button>

          <!-- Vendor -->
          <button class="choice-card vendor-card" @click="router.push('/signup/vendor')">
            <div class="choice-icon-wrap vendor-icon">
              <span class="choice-icon">🏢</span>
            </div>
            <div class="choice-info">
              <h3>Vendor / Technician</h3>
              <p>Join as a service provider. Manage departments and resolve customer tickets.</p>
            </div>
            <div class="choice-features">
              <span class="cf-item">✓ Manage service tickets</span>
              <span class="cf-item">✓ Multi-department support</span>
              <span class="cf-item">✓ Assign technicians</span>
            </div>
            <div class="choice-arrow">→</div>
          </button>
        </div>

        <p class="auth-footer-text">
          Already have an account?
          <button class="link-btn" @click="router.push('/signin')">Sign In</button>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
* { box-sizing: border-box; margin: 0; padding: 0; }
.auth-page {
  min-height: 100vh;
  background: #080d1a;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  position: relative;
}
.auth-bg { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.orb { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.12; }
.orb-1 { width: 500px; height: 500px; background: #6366f1; top: -100px; left: -100px; animation: orbFloat 8s ease-in-out infinite; }
.orb-2 { width: 400px; height: 400px; background: #06b6d4; bottom: -50px; right: 5%; animation: orbFloat 10s ease-in-out infinite reverse; }
.grid-overlay {
  position: absolute; inset: 0;
  background-image: linear-gradient(rgba(99,102,241,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(99,102,241,0.03) 1px,transparent 1px);
  background-size: 50px 50px;
}
@keyframes orbFloat { 0%,100%{transform:translate(0,0)} 50%{transform:translate(20px,-20px)} }

.auth-container { position: relative; z-index: 1; width: 100%; max-width: 680px; }

.back-btn {
  background: none; border: none; color: #64748b;
  font-size: 0.9rem; cursor: pointer; margin-bottom: 1.5rem;
  display: flex; align-items: center; gap: 0.3rem;
  transition: color 0.2s; padding: 0;
}
.back-btn:hover { color: #a5b4fc; }

.auth-card {
  background: rgba(15,23,42,0.9);
  border: 1px solid rgba(99,102,241,0.15);
  border-radius: 24px;
  padding: 2.5rem;
  backdrop-filter: blur(20px);
  box-shadow: 0 25px 50px rgba(0,0,0,0.4);
}
.auth-logo { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 2rem; justify-content: center; }
.logo-icon { font-size: 1.5rem; }
.logo-text { font-size: 1.25rem; font-weight: 800; color: #f1f5f9; }
.accent { color: #6366f1; }
.auth-header { text-align: center; margin-bottom: 2rem; }
.auth-header h1 { font-size: 1.75rem; font-weight: 800; color: #f1f5f9; margin-bottom: 0.5rem; letter-spacing: -0.5px; }
.auth-header p { color: #64748b; font-size: 0.95rem; }

.choice-cards { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 2rem; }

.choice-card {
  display: flex; flex-direction: column; gap: 0.75rem;
  width: 100%; text-align: left;
  padding: 1.5rem; border-radius: 16px;
  border: 2px solid transparent;
  cursor: pointer; transition: all 0.3s;
  position: relative; overflow: hidden;
  background: rgba(255,255,255,0.03);
}
.choice-card::before {
  content: ''; position: absolute; inset: 0;
  opacity: 0; transition: opacity 0.3s;
}
.customer-card::before { background: linear-gradient(135deg,rgba(99,102,241,0.05),rgba(99,102,241,0.02)); }
.vendor-card::before { background: linear-gradient(135deg,rgba(6,182,212,0.05),rgba(6,182,212,0.02)); }
.customer-card { border-color: rgba(99,102,241,0.2); }
.vendor-card { border-color: rgba(6,182,212,0.2); }
.customer-card:hover { border-color: #6366f1; transform: translateY(-2px); box-shadow: 0 12px 30px rgba(99,102,241,0.15); }
.vendor-card:hover { border-color: #06b6d4; transform: translateY(-2px); box-shadow: 0 12px 30px rgba(6,182,212,0.15); }
.choice-card:hover::before { opacity: 1; }

.choice-icon-wrap {
  width: 52px; height: 52px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
}
.customer-icon { background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.3); }
.vendor-icon { background: rgba(6,182,212,0.15); border: 1px solid rgba(6,182,212,0.3); }
.choice-icon { font-size: 1.5rem; }
.choice-info { }
.choice-info h3 { font-size: 1.1rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.3rem; }
.choice-info p { font-size: 0.85rem; color: #64748b; line-height: 1.5; }
.choice-features { display: flex; flex-direction: column; gap: 0.3rem; }
.cf-item { font-size: 0.8rem; color: #475569; }
.customer-card:hover .cf-item { color: #a5b4fc; }
.vendor-card:hover .cf-item { color: #67e8f9; }
.choice-arrow {
  position: absolute; right: 1.5rem; top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem; color: #334155; transition: all 0.3s;
}
.customer-card:hover .choice-arrow { color: #6366f1; transform: translateY(-50%) translateX(4px); }
.vendor-card:hover .choice-arrow { color: #06b6d4; transform: translateY(-50%) translateX(4px); }

.auth-footer-text { text-align: center; font-size: 0.9rem; color: #475569; }
.link-btn { background: none; border: none; color: #6366f1; font-weight: 600; cursor: pointer; font-size: 0.9rem; transition: color 0.2s; }
.link-btn:hover { color: #a5b4fc; }

@media (max-width: 560px) {
  .auth-card { padding: 1.5rem; }
}
</style>
