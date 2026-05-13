<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ─── State ───────────────────────────────────────────────────────────────────
const pageVisible  = ref(false)
const isLoading    = ref(false)   // API fetch spinner example
const customerName = ref('Rahul Sharma')

// ─── Summary Cards Data ───────────────────────────────────────────────────────
const summaryCards = ref([
  {
    icon: '🏭',
    title: 'My Machines',
    count: '000003',
    subtitle: 'Registered machines',
    accent: 'indigo',
    glow: 'rgba(99,102,241,0.25)',
  },
  {
    icon: '🎫',
    title: 'Service Tickets',
    count: 5,
    subtitle: '2 open · 3 resolved',
    accent: 'cyan',
    glow: 'rgba(6,182,212,0.25)',
  },
  {
    icon: '🧾',
    title: 'My Invoices',
    count: 3,
    subtitle: '1 pending payment',
    accent: 'violet',
    glow: 'rgba(139,92,246,0.25)',
  },
])

// ─── Recent Service Tickets ───────────────────────────────────────────────────
const tickets = ref([
  { id: 'TKT-0001', machine: 'CNC Machine X200',   status: 'Open',        date: '2025-05-10' },
  { id: 'TKT-0002', machine: 'Hydraulic Press HP5', status: 'In Progress', date: '2025-05-08' },
  { id: 'TKT-0003', machine: 'Lathe Machine LM3',   status: 'Completed',   date: '2025-05-05' },
  { id: 'TKT-0004', machine: 'Drill Machine DM7',   status: 'Open',        date: '2025-05-03' },
  { id: 'TKT-0005', machine: 'Compressor CP-200',   status: 'Completed',   date: '2025-04-29' },
])

// ─── Status badge styling ─────────────────────────────────────────────────────
const statusConfig = {
  'Open':        { cls: 'badge-yellow', icon: '🟡' },
  'In Progress': { cls: 'badge-blue',   icon: '🔵' },
  'Completed':   { cls: 'badge-green',  icon: '🟢' },
}

// ─── Accent color map ─────────────────────────────────────────────────────────
const accentBorder = {
  indigo: 'rgba(99,102,241,0.35)',
  cyan:   'rgba(6,182,212,0.35)',
  violet: 'rgba(139,92,246,0.35)',
}

// ─── Lifecycle ────────────────────────────────────────────────────────────────
onMounted(() => {
  setTimeout(() => { pageVisible.value = true }, 80)
})

// ─── Methods ──────────────────────────────────────────────────────────────────
function createServiceRequest() {
  router.push('/service-request')
}

/* ─────────────────────────────────────────────────────────────────────────────
   API EXAMPLE — कैसे service tickets fetch करें
   GET /api/resource/Service Ticket

   async function fetchTickets() {
     isLoading.value = true
     try {
       const res = await fetch(
         '/api/resource/Service%20Ticket?filters=[["customer","=","CUST-001"]]&fields=["name","machine","status","creation"]',
         {
           headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': 'fetch' }
         }
       )
       const data = await res.json()
       tickets.value = data.data.map(t => ({
         id:      t.name,
         machine: t.machine,
         status:  t.status,
         date:    t.creation?.slice(0, 10),
       }))
     } catch (err) {
       console.error('Tickets fetch failed:', err)
     } finally {
       isLoading.value = false
     }
   }
───────────────────────────────────────────────────────────────────────────── */
</script>

<template>
  <!-- Page wrapper — same dark background as Home.vue -->
  <div class="dash" :class="{ visible: pageVisible }">

    <!-- Ambient background orbs (matches Home.vue style) -->
    <div class="bg-layer" aria-hidden="true">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
      <div class="grid-overlay"></div>
    </div>

    <!-- ── MAIN CONTENT ── -->
    <div class="dash-inner">

      <!-- ── NAVBAR ── -->
      <nav class="topbar">
        <div class="brand">
          <span class="brand-icon">⚡</span>
          <span class="brand-name">Smart<span class="accent">Market</span></span>
        </div>
        <div class="topbar-right">
          <span class="user-chip">👤 {{ customerName }}</span>
          <button class="btn-outline" @click="router.push('/')">← Home</button>
          <button class="btn-danger-sm">Sign Out</button>
        </div>
      </nav>

      <!-- ── WELCOME SECTION ── -->
      <section class="welcome-section">
        <div class="welcome-badge">🏠 Customer Portal</div>
        <h1 class="welcome-title">
          Welcome, <span class="gradient-text">{{ customerName }}</span>
        </h1>
        <p class="welcome-sub">
          Manage your machines, service requests and invoices — all in one place.
        </p>
      </section>

      <!-- ── SUMMARY CARDS ── -->
      <section class="cards-section">
        <div
          v-for="card in summaryCards"
          :key="card.title"
          class="summary-card"
          :style="{ '--glow': card.glow, '--border': accentBorder[card.accent] }"
        >
          <div class="card-icon-wrap">
            <span class="card-icon">{{ card.icon }}</span>
          </div>
          <div class="card-body">
            <p class="card-title">{{ card.title }}</p>
            <p class="card-count">{{ card.count }}</p>
            <p class="card-sub">{{ card.subtitle }}</p>
          </div>
          <div class="card-glow-dot"></div>
        </div>
      </section>

      <!-- ── RECENT TICKETS TABLE ── -->
      <section class="table-section">
        <div class="section-head">
          <div>
            <h2 class="section-title">Recent Service Tickets</h2>
            <p class="section-desc">Latest updates on your service requests</p>
          </div>
          <!-- Create Service Request Button -->
          <button class="cta-btn" @click="createServiceRequest">
            <span class="cta-icon">＋</span>
            Create Service Request
          </button>
        </div>

        <!-- Loading spinner example -->
        <div v-if="isLoading" class="spinner-wrap">
          <div class="spinner"></div>
          <p class="spinner-text">Fetching tickets…</p>
        </div>

        <!-- Empty state -->
        <div v-else-if="tickets.length === 0" class="empty-state">
          <div class="empty-icon">📭</div>
          <p class="empty-title">No tickets yet</p>
          <p class="empty-sub">Create your first service request to get started.</p>
        </div>

        <!-- Table -->
        <div v-else class="table-wrap">
          <table class="tbl">
            <thead>
              <tr>
                <th>Ticket ID</th>
                <th>Machine</th>
                <th>Status</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="ticket in tickets" :key="ticket.id" class="tbl-row">
                <td class="ticket-id">{{ ticket.id }}</td>
                <td class="machine-name">{{ ticket.machine }}</td>
                <td>
                  <span class="badge" :class="statusConfig[ticket.status]?.cls">
                    {{ statusConfig[ticket.status]?.icon }} {{ ticket.status }}
                  </span>
                </td>
                <td class="date-cell">{{ ticket.date }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

    </div><!-- /dash-inner -->
  </div><!-- /dash -->
</template>

<style scoped>
/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.dash {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #080d1a;
  color: #f1f5f9;
  min-height: 100vh;
  overflow-x: hidden;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.dash.visible { opacity: 1; transform: translateY(0); }

/* ── Ambient background (same as Home.vue) ── */
.bg-layer { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.orb {
  position: absolute; border-radius: 50%;
  filter: blur(90px); opacity: 0.12;
  animation: orbFloat 9s ease-in-out infinite;
}
.orb-1 { width: 600px; height: 600px; background: #6366f1; top: -180px; left: -180px; }
.orb-2 { width: 350px; height: 350px; background: #06b6d4; bottom: 0; right: 5%; animation-duration: 11s; animation-direction: reverse; }
.orb-3 { width: 280px; height: 280px; background: #8b5cf6; top: 45%; left: 55%; animation-duration: 13s; }
@keyframes orbFloat {
  0%,100% { transform: translate(0,0); }
  50%      { transform: translate(25px,-25px); }
}
.grid-overlay {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(99,102,241,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(99,102,241,0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

/* ── Layout ── */
.dash-inner {
  position: relative; z-index: 1;
  max-width: 1200px; margin: 0 auto;
  padding: 0 1.5rem 4rem;
}

/* ── Navbar ── */
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.25rem 0;
  border-bottom: 1px solid rgba(99,102,241,0.12);
  margin-bottom: 2.5rem;
}
.brand { display: flex; align-items: center; gap: 0.5rem; }
.brand-icon { font-size: 1.4rem; }
.brand-name { font-size: 1.2rem; font-weight: 800; letter-spacing: -0.5px; }
.accent { color: #6366f1; }
.topbar-right { display: flex; align-items: center; gap: 0.75rem; }
.user-chip {
  padding: 0.4rem 0.9rem; border-radius: 100px;
  background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.25);
  color: #a5b4fc; font-size: 0.82rem; font-weight: 600;
}
.btn-outline {
  padding: 0.4rem 1rem; border: 1px solid rgba(99,102,241,0.4);
  border-radius: 8px; background: transparent; color: #a5b4fc;
  font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
}
.btn-outline:hover { background: rgba(99,102,241,0.1); }
.btn-danger-sm {
  padding: 0.4rem 1rem; border: 1px solid rgba(239,68,68,0.3);
  border-radius: 8px; background: rgba(239,68,68,0.08);
  color: #fca5a5; font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
}
.btn-danger-sm:hover { background: rgba(239,68,68,0.16); }

/* ── Welcome section ── */
.welcome-section { margin-bottom: 2.5rem; }
.welcome-badge {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.35rem 1rem; border-radius: 100px;
  background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.25);
  color: #a5b4fc; font-size: 0.8rem; font-weight: 600;
  margin-bottom: 1rem;
}
.welcome-title {
  font-size: 2.4rem; font-weight: 900;
  letter-spacing: -1.5px; line-height: 1.1;
  margin-bottom: 0.6rem;
}
.gradient-text {
  background: linear-gradient(135deg, #6366f1, #06b6d4);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.welcome-sub { font-size: 1rem; color: #64748b; }

/* ── Summary cards ── */
.cards-section {
  display: grid; grid-template-columns: repeat(3,1fr);
  gap: 1.25rem; margin-bottom: 2.5rem;
}
.summary-card {
  position: relative; overflow: hidden;
  background: rgba(15,23,42,0.75);
  border: 1px solid var(--border, rgba(99,102,241,0.2));
  border-radius: 18px; padding: 1.6rem 1.5rem;
  display: flex; align-items: center; gap: 1.25rem;
  backdrop-filter: blur(16px);
  box-shadow: 0 4px 30px rgba(0,0,0,0.3);
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
  cursor: default;
}
.summary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 16px 48px var(--glow, rgba(99,102,241,0.2));
  border-color: var(--border);
}
.card-glow-dot {
  position: absolute; top: -30px; right: -30px;
  width: 100px; height: 100px; border-radius: 50%;
  background: var(--glow, rgba(99,102,241,0.15));
  filter: blur(30px); pointer-events: none;
}
.card-icon-wrap {
  width: 52px; height: 52px; border-radius: 14px; flex-shrink: 0;
  background: rgba(99,102,241,0.1);
  border: 1px solid rgba(99,102,241,0.2);
  display: flex; align-items: center; justify-content: center;
}
.card-icon { font-size: 1.5rem; }
.card-body { display: flex; flex-direction: column; gap: 0.1rem; }
.card-title { font-size: 0.78rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.card-count { font-size: 1.9rem; font-weight: 900; letter-spacing: -1px; color: #e2e8f0; }
.card-sub { font-size: 0.75rem; color: #475569; margin-top: 0.1rem; }

/* ── Section header row ── */
.table-section {
  background: rgba(15,23,42,0.6);
  border: 1px solid rgba(99,102,241,0.12);
  border-radius: 20px; padding: 2rem;
  backdrop-filter: blur(16px);
}
.section-head {
  display: flex; align-items: flex-start; justify-content: space-between;
  margin-bottom: 1.75rem; gap: 1rem; flex-wrap: wrap;
}
.section-title { font-size: 1.2rem; font-weight: 800; color: #e2e8f0; margin-bottom: 0.25rem; }
.section-desc { font-size: 0.8rem; color: #475569; }

/* ── Create Service Request Button ── */
.cta-btn {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.7rem 1.4rem;
  border: none; border-radius: 12px;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white; font-size: 0.9rem; font-weight: 700; cursor: pointer;
  box-shadow: 0 0 24px rgba(99,102,241,0.35);
  transition: all 0.2s ease; white-space: nowrap;
}
.cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 40px rgba(99,102,241,0.55);
}
.cta-icon { font-size: 1.1rem; font-weight: 900; }

/* ── Table ── */
.table-wrap { overflow-x: auto; border-radius: 12px; }
.tbl {
  width: 100%; border-collapse: collapse;
  font-size: 0.88rem;
}
.tbl thead tr {
  border-bottom: 1px solid rgba(99,102,241,0.12);
}
.tbl th {
  text-align: left; padding: 0.75rem 1rem;
  color: #475569; font-size: 0.75rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.6px;
}
.tbl-row {
  border-bottom: 1px solid rgba(255,255,255,0.04);
  transition: background 0.15s ease;
}
.tbl-row:last-child { border-bottom: none; }
.tbl-row:hover { background: rgba(99,102,241,0.05); }
.tbl td { padding: 0.9rem 1rem; vertical-align: middle; }
.ticket-id { color: #a5b4fc; font-weight: 700; font-family: monospace; }
.machine-name { color: #cbd5e1; font-weight: 500; }
.date-cell { color: #475569; font-size: 0.82rem; }

/* ── Status badges ── */
.badge {
  display: inline-flex; align-items: center; gap: 0.3rem;
  padding: 0.3rem 0.75rem; border-radius: 100px;
  font-size: 0.75rem; font-weight: 700;
}
.badge-yellow { background: rgba(234,179,8,0.12);  border: 1px solid rgba(234,179,8,0.3);  color: #fde047; }
.badge-blue   { background: rgba(59,130,246,0.12); border: 1px solid rgba(59,130,246,0.3); color: #93c5fd; }
.badge-green  { background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.3); color: #34d399; }

/* ── Spinner ── */
.spinner-wrap { display: flex; flex-direction: column; align-items: center; padding: 3rem; gap: 1rem; }
.spinner {
  width: 40px; height: 40px; border-radius: 50%;
  border: 3px solid rgba(99,102,241,0.2);
  border-top-color: #6366f1;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.spinner-text { color: #475569; font-size: 0.85rem; }

/* ── Empty state ── */
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-title { font-size: 1.1rem; font-weight: 700; color: #e2e8f0; margin-bottom: 0.5rem; }
.empty-sub { font-size: 0.85rem; color: #475569; }

/* ── Responsive ── */
@media (max-width: 768px) {
  .cards-section { grid-template-columns: 1fr; }
  .welcome-title { font-size: 1.8rem; }
  .topbar { flex-wrap: wrap; gap: 0.75rem; }
}
@media (max-width: 480px) {
  .section-head { flex-direction: column; }
  .cta-btn { width: 100%; justify-content: center; }
}
</style>
