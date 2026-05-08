<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const heroVisible = ref(false)

onMounted(() => {
  setTimeout(() => { heroVisible.value = true }, 100)
})

const features = [
  { icon: '🛠️', title: 'Service Requests', desc: 'Raise and track service tickets for your equipment in real time.' },
  { icon: '🏢', title: 'Multi-Department Routing', desc: 'Requests routed to the right vendor department automatically.' },
  { icon: '👨‍🔧', title: 'Expert Technicians', desc: 'Certified technicians handle every repair with precision.' },
  { icon: '📊', title: 'Live Tracking', desc: 'Monitor status from open to resolved with full transparency.' },
  { icon: '🔔', title: 'Instant Alerts', desc: 'Get notified via SMS and email at every milestone.' },
  { icon: '🔒', title: 'Secure & Verified', desc: 'OTP-based authentication for both customers and vendors.' }
]

const stats = [
  { value: '12K+', label: 'Customers Served' },
  { value: '400+', label: 'Vendor Partners' },
  { value: '98%', label: 'Resolution Rate' },
  { value: '24/7', label: 'Support Available' }
]
</script>

<template>
  <div class="landing">
    <!-- NAVBAR -->
    <nav class="navbar">
      <div class="nav-inner">
        <div class="brand">
          <span class="brand-icon">⚡</span>
          <span class="brand-name">Smart<span class="accent">Market</span></span>
        </div>
        <div class="nav-links">
          <a href="#features" class="nav-link">Features</a>
          <a href="#how" class="nav-link">How it Works</a>
          <a href="#stats" class="nav-link">Stats</a>
        </div>
        <div class="nav-actions">
          <button class="btn-outline" @click="router.push('/signin')">Sign In</button>
          <button class="btn-primary" @click="router.push('/signup')">Get Started</button>
        </div>
      </div>
    </nav>

    <!-- HERO -->
    <section class="hero" :class="{ visible: heroVisible }">
      <div class="hero-bg">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
        <div class="grid-overlay"></div>
      </div>
      <div class="hero-content">
        <div class="hero-badge">🚀 Next-Gen Service Platform</div>
        <h1 class="hero-title">
          Your Machine,<br/>
          <span class="gradient-text">Our Expertise</span>
        </h1>
        <p class="hero-desc">
          Connect customers with certified technicians through Smart Market —
          the intelligent service management platform built for modern businesses.
        </p>
        <div class="hero-ctas">
          <button class="cta-primary" @click="router.push('/signup')">
            <span>Create Account</span>
            <span class="cta-arrow">→</span>
          </button>
          <button class="cta-secondary" @click="router.push('/signin')">
            Sign In to Dashboard
          </button>
        </div>
        <div class="hero-trust">
          <span class="trust-item">✓ Free to join</span>
          <span class="trust-item">✓ OTP verified</span>
          <span class="trust-item">✓ Instant access</span>
        </div>
      </div>
      <div class="hero-visual">
        <div class="dashboard-mock">
          <div class="mock-header">
            <div class="mock-dot red"></div>
            <div class="mock-dot yellow"></div>
            <div class="mock-dot green"></div>
            <span class="mock-title">Service Dashboard</span>
          </div>
          <div class="mock-body">
            <div class="mock-stat-row">
              <div class="mock-stat"><span class="ms-val">42</span><span class="ms-lbl">Open</span></div>
              <div class="mock-stat accent-bg"><span class="ms-val">18</span><span class="ms-lbl">In Progress</span></div>
              <div class="mock-stat success-bg"><span class="ms-val">213</span><span class="ms-lbl">Resolved</span></div>
            </div>
            <div class="mock-ticket" v-for="(label, i) in ['Open','In Progress','Resolved']" :key="i">
              <div class="mock-ticket-left">
                <div class="mock-avatar"></div>
                <div class="mock-info">
                  <div class="mock-line thick"></div>
                  <div class="mock-line thin"></div>
                </div>
              </div>
              <div class="mock-badge" :class="['open','progress','done'][i]">{{ label }}</div>
            </div>
            <div class="mock-bar-section">
              <div class="mock-bar-label">Weekly Resolution</div>
              <div class="mock-bars">
                <div class="mock-bar" v-for="h in [60,85,45,90,70,100,55]" :key="h" :style="{height: h+'%'}"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- STATS -->
    <section class="stats-section" id="stats">
      <div class="stats-inner">
        <div class="stat-card" v-for="s in stats" :key="s.label">
          <div class="stat-value">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
      </div>
    </section>

    <!-- HOW IT WORKS -->
    <section class="how-section" id="how">
      <div class="section-header">
        <div class="section-badge">Simple Process</div>
        <h2 class="section-title">How It Works</h2>
        <p class="section-desc">Three steps to get your service request resolved</p>
      </div>
      <div class="steps-row">
        <div class="step-card">
          <div class="step-num">01</div>
          <div class="step-icon">📝</div>
          <h3>Sign Up & Verify</h3>
          <p>Create your account as a Customer or Vendor. Verify your identity via OTP.</p>
        </div>
        <div class="step-connector"></div>
        <div class="step-card">
          <div class="step-num">02</div>
          <div class="step-icon">🎫</div>
          <h3>Raise a Ticket</h3>
          <p>Submit your service request with machine details and issue description.</p>
        </div>
        <div class="step-connector"></div>
        <div class="step-card">
          <div class="step-num">03</div>
          <div class="step-icon">✅</div>
          <h3>Get it Resolved</h3>
          <p>Our expert technicians fix your issue. Track progress every step of the way.</p>
        </div>
      </div>
    </section>

    <!-- FEATURES -->
    <section class="features-section" id="features">
      <div class="section-header">
        <div class="section-badge">Why Smart Market</div>
        <h2 class="section-title">Everything You Need</h2>
        <p class="section-desc">A complete platform for service management at scale</p>
      </div>
      <div class="features-grid">
        <div class="feature-card" v-for="f in features" :key="f.title">
          <div class="feature-icon">{{ f.icon }}</div>
          <h3 class="feature-title">{{ f.title }}</h3>
          <p class="feature-desc">{{ f.desc }}</p>
        </div>
      </div>
    </section>

    <!-- CTA BANNER -->
    <section class="cta-banner">
      <div class="cta-banner-inner">
        <h2>Ready to get started?</h2>
        <p>Join thousands of customers and vendors already on Smart Market</p>
        <div class="cta-banner-btns">
          <button class="cta-primary" @click="router.push('/signup')">Sign Up as Customer</button>
          <button class="cta-vendor" @click="router.push('/signup')">Join as Vendor</button>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="footer-inner">
        <div class="brand">
          <span class="brand-icon">⚡</span>
          <span class="brand-name">Smart<span class="accent">Market</span></span>
        </div>
        <p class="footer-copy">© 2025 SmartMarket. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
* { box-sizing: border-box; margin: 0; padding: 0; }
.landing {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #080d1a;
  color: #f1f5f9;
  min-height: 100vh;
  overflow-x: hidden;
}

/* NAVBAR */
.navbar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  backdrop-filter: blur(20px);
  background: rgba(8,13,26,0.85);
  border-bottom: 1px solid rgba(99,102,241,0.15);
}
.nav-inner {
  max-width: 1200px; margin: 0 auto;
  padding: 1rem 2rem;
  display: flex; align-items: center; gap: 2rem;
}
.brand { display: flex; align-items: center; gap: 0.5rem; margin-right: auto; }
.brand-icon { font-size: 1.5rem; }
.brand-name { font-size: 1.25rem; font-weight: 800; letter-spacing: -0.5px; }
.accent { color: #6366f1; }
.nav-links { display: flex; gap: 2rem; }
.nav-link { color: #94a3b8; text-decoration: none; font-size: 0.9rem; font-weight: 500; transition: color 0.2s; }
.nav-link:hover { color: #f1f5f9; }
.nav-actions { display: flex; gap: 0.75rem; }
.btn-outline {
  padding: 0.5rem 1.25rem; border: 1px solid rgba(99,102,241,0.5);
  border-radius: 8px; background: transparent; color: #a5b4fc;
  font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
}
.btn-outline:hover { background: rgba(99,102,241,0.1); border-color: #6366f1; }
.btn-primary {
  padding: 0.5rem 1.25rem; border: none; border-radius: 8px;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white; font-size: 0.9rem; font-weight: 600; cursor: pointer;
  box-shadow: 0 0 20px rgba(99,102,241,0.3); transition: all 0.2s;
}
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 0 30px rgba(99,102,241,0.5); }

/* HERO */
.hero {
  position: relative; min-height: 100vh;
  display: flex; align-items: center;
  padding: 8rem 2rem 4rem;
  max-width: 1200px; margin: 0 auto; gap: 4rem;
  opacity: 0; transform: translateY(30px); transition: all 0.8s ease;
}
.hero.visible { opacity: 1; transform: translateY(0); }
.hero-bg { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.orb {
  position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.15;
  animation: orbFloat 8s ease-in-out infinite;
}
.orb-1 { width: 600px; height: 600px; background: #6366f1; top: -200px; left: -200px; }
.orb-2 { width: 400px; height: 400px; background: #06b6d4; bottom: -100px; right: 10%; animation-duration: 10s; animation-direction: reverse; }
.orb-3 { width: 300px; height: 300px; background: #8b5cf6; top: 40%; left: 50%; animation-duration: 12s; }
@keyframes orbFloat {
  0%,100% { transform: translate(0,0); }
  50% { transform: translate(30px,-30px); }
}
.grid-overlay {
  position: absolute; inset: 0;
  background-image: linear-gradient(rgba(99,102,241,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(99,102,241,0.03) 1px,transparent 1px);
  background-size: 50px 50px;
}
.hero-content { position: relative; z-index: 1; flex: 1; max-width: 560px; }
.hero-badge {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.4rem 1rem; border-radius: 100px;
  background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.3);
  color: #a5b4fc; font-size: 0.85rem; font-weight: 600; margin-bottom: 1.5rem;
}
.hero-title { font-size: 3.5rem; font-weight: 900; line-height: 1.1; letter-spacing: -2px; margin-bottom: 1.5rem; }
.gradient-text {
  background: linear-gradient(135deg, #6366f1, #06b6d4);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-desc { font-size: 1.1rem; color: #94a3b8; line-height: 1.7; margin-bottom: 2rem; }
.hero-ctas { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
.cta-primary {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.85rem 1.75rem; border: none; border-radius: 12px;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white; font-size: 1rem; font-weight: 700; cursor: pointer;
  transition: all 0.2s; box-shadow: 0 0 30px rgba(99,102,241,0.4);
}
.cta-primary:hover { transform: translateY(-2px); box-shadow: 0 0 50px rgba(99,102,241,0.6); }
.cta-arrow { transition: transform 0.2s; }
.cta-primary:hover .cta-arrow { transform: translateX(4px); }
.cta-secondary {
  padding: 0.85rem 1.75rem; border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px; background: rgba(255,255,255,0.05);
  color: #e2e8f0; font-size: 1rem; font-weight: 600; cursor: pointer;
  transition: all 0.2s; backdrop-filter: blur(10px);
}
.cta-secondary:hover { background: rgba(255,255,255,0.1); }
.hero-trust { display: flex; gap: 1.5rem; flex-wrap: wrap; }
.trust-item { font-size: 0.85rem; color: #10b981; font-weight: 500; }

/* HERO VISUAL */
.hero-visual { position: relative; z-index: 1; flex: 1; display: flex; justify-content: center; }
.dashboard-mock {
  background: rgba(15,23,42,0.8); border: 1px solid rgba(99,102,241,0.2);
  border-radius: 16px; width: 100%; max-width: 400px;
  backdrop-filter: blur(20px);
  box-shadow: 0 25px 50px rgba(0,0,0,0.5),0 0 0 1px rgba(99,102,241,0.1);
  overflow: hidden;
}
.mock-header {
  display: flex; align-items: center; gap: 0.4rem;
  padding: 0.75rem 1rem;
  background: rgba(99,102,241,0.08);
  border-bottom: 1px solid rgba(99,102,241,0.1);
}
.mock-dot { width: 10px; height: 10px; border-radius: 50%; }
.mock-dot.red { background: #ef4444; }
.mock-dot.yellow { background: #f59e0b; }
.mock-dot.green { background: #10b981; }
.mock-title { margin-left: auto; font-size: 0.8rem; color: #64748b; font-weight: 600; }
.mock-body { padding: 1rem; display: flex; flex-direction: column; gap: 1rem; }
.mock-stat-row { display: flex; gap: 0.5rem; }
.mock-stat {
  flex: 1; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.06);
  border-radius: 8px; padding: 0.6rem; text-align: center;
}
.mock-stat.accent-bg { background: rgba(99,102,241,0.12); border-color: rgba(99,102,241,0.2); }
.mock-stat.success-bg { background: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.2); }
.ms-val { display: block; font-size: 1.2rem; font-weight: 700; color: #e2e8f0; }
.ms-lbl { display: block; font-size: 0.65rem; color: #64748b; margin-top: 2px; }
.mock-ticket {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.6rem 0.75rem;
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px;
}
.mock-ticket-left { display: flex; align-items: center; gap: 0.5rem; }
.mock-avatar { width: 28px; height: 28px; border-radius: 50%; background: linear-gradient(135deg,#6366f1,#06b6d4); }
.mock-info { display: flex; flex-direction: column; gap: 3px; }
.mock-line { height: 6px; border-radius: 3px; background: rgba(255,255,255,0.1); }
.mock-line.thick { width: 80px; }
.mock-line.thin { width: 50px; background: rgba(255,255,255,0.05); }
.mock-badge { font-size: 0.65rem; font-weight: 700; padding: 0.2rem 0.5rem; border-radius: 100px; }
.mock-badge.open { background: rgba(239,68,68,0.15); color: #f87171; }
.mock-badge.progress { background: rgba(245,158,11,0.15); color: #fbbf24; }
.mock-badge.done { background: rgba(16,185,129,0.15); color: #34d399; }
.mock-bar-label { font-size: 0.7rem; color: #64748b; margin-bottom: 0.4rem; }
.mock-bars { display: flex; align-items: flex-end; gap: 4px; height: 50px; }
.mock-bar { flex: 1; background: linear-gradient(to top,#6366f1,rgba(99,102,241,0.3)); border-radius: 3px 3px 0 0; min-height: 4px; }

/* STATS */
.stats-section {
  position: relative; z-index: 1;
  padding: 3rem 2rem;
  background: rgba(99,102,241,0.05);
  border-top: 1px solid rgba(99,102,241,0.1);
  border-bottom: 1px solid rgba(99,102,241,0.1);
}
.stats-inner { max-width: 900px; margin: 0 auto; display: grid; grid-template-columns: repeat(4,1fr); gap: 2rem; text-align: center; }
.stat-value {
  font-size: 2.5rem; font-weight: 900;
  background: linear-gradient(135deg,#6366f1,#06b6d4);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.stat-label { font-size: 0.9rem; color: #64748b; margin-top: 0.3rem; font-weight: 500; }

/* HOW IT WORKS */
.how-section { position: relative; z-index: 1; padding: 6rem 2rem; max-width: 1000px; margin: 0 auto; }
.section-header { text-align: center; margin-bottom: 4rem; }
.section-badge {
  display: inline-block; padding: 0.3rem 1rem; border-radius: 100px;
  background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.2);
  color: #a5b4fc; font-size: 0.8rem; font-weight: 600; margin-bottom: 1rem;
}
.section-title { font-size: 2.5rem; font-weight: 800; letter-spacing: -1px; margin-bottom: 0.75rem; }
.section-desc { font-size: 1rem; color: #64748b; }
.steps-row { display: flex; align-items: center; gap: 1rem; }
.step-card {
  flex: 1; background: rgba(15,23,42,0.8);
  border: 1px solid rgba(99,102,241,0.15); border-radius: 16px;
  padding: 2rem; text-align: center; transition: all 0.3s;
}
.step-card:hover { border-color: rgba(99,102,241,0.4); transform: translateY(-4px); box-shadow: 0 20px 40px rgba(99,102,241,0.1); }
.step-num { font-size: 0.75rem; font-weight: 800; color: #6366f1; letter-spacing: 2px; margin-bottom: 0.75rem; }
.step-icon { font-size: 2rem; margin-bottom: 0.75rem; }
.step-card h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem; }
.step-card p { font-size: 0.85rem; color: #64748b; line-height: 1.6; }
.step-connector { width: 60px; height: 2px; background: linear-gradient(90deg,#6366f1,rgba(99,102,241,0.2)); flex-shrink: 0; }

/* FEATURES */
.features-section { position: relative; z-index: 1; padding: 6rem 2rem; max-width: 1200px; margin: 0 auto; }
.features-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.5rem; }
.feature-card {
  background: rgba(15,23,42,0.6); border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px; padding: 1.75rem; transition: all 0.3s;
}
.feature-card:hover { border-color: rgba(99,102,241,0.3); background: rgba(99,102,241,0.05); transform: translateY(-2px); }
.feature-icon { font-size: 2rem; margin-bottom: 1rem; }
.feature-title { font-size: 1rem; font-weight: 700; margin-bottom: 0.5rem; }
.feature-desc { font-size: 0.85rem; color: #64748b; line-height: 1.6; }

/* CTA BANNER */
.cta-banner {
  position: relative; z-index: 1;
  margin: 2rem; border-radius: 24px;
  background: linear-gradient(135deg,rgba(99,102,241,0.2),rgba(6,182,212,0.1));
  border: 1px solid rgba(99,102,241,0.2);
}
.cta-banner-inner { padding: 4rem 3rem; text-align: center; }
.cta-banner h2 { font-size: 2rem; font-weight: 800; margin-bottom: 0.75rem; }
.cta-banner p { color: #94a3b8; margin-bottom: 2rem; }
.cta-banner-btns { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
.cta-vendor {
  padding: 0.85rem 1.75rem; border: 1px solid rgba(6,182,212,0.4);
  border-radius: 12px; background: rgba(6,182,212,0.1);
  color: #67e8f9; font-size: 1rem; font-weight: 700; cursor: pointer; transition: all 0.2s;
}
.cta-vendor:hover { background: rgba(6,182,212,0.2); transform: translateY(-2px); }

/* FOOTER */
.footer { position: relative; z-index: 1; padding: 2rem; border-top: 1px solid rgba(255,255,255,0.05); }
.footer-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; }
.footer-copy { font-size: 0.85rem; color: #334155; }

/* RESPONSIVE */
@media (max-width: 900px) {
  .hero { flex-direction: column; padding-top: 7rem; }
  .hero-visual { display: none; }
  .hero-title { font-size: 2.5rem; }
  .stats-inner { grid-template-columns: repeat(2,1fr); }
  .features-grid { grid-template-columns: repeat(2,1fr); }
  .steps-row { flex-direction: column; }
  .step-connector { width: 2px; height: 40px; background: linear-gradient(180deg,#6366f1,rgba(99,102,241,0.2)); }
  .nav-links { display: none; }
}
@media (max-width: 560px) {
  .features-grid { grid-template-columns: 1fr; }
  .hero-title { font-size: 2rem; }
}
</style>
