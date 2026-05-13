<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ─── State ───────────────────────────────────────────────────────────────────
const pageVisible     = ref(false)
const isLoading       = ref(false)
const technicianName  = ref('Arjun Mehta')
const selectedTicket  = ref(null)   // currently selected ticket for action

// ─── Summary Cards ────────────────────────────────────────────────────────────
const summaryCards = ref([
  {
    icon: '📋',
    title: 'Assigned Tickets',
    count: 8,
    subtitle: 'Total assigned to you',
    glow: 'rgba(99,102,241,0.25)',
    border: 'rgba(99,102,241,0.35)',
  },
  {
    icon: '⚙️',
    title: 'In Progress',
    count: 3,
    subtitle: 'Currently being worked on',
    glow: 'rgba(245,158,11,0.25)',
    border: 'rgba(245,158,11,0.35)',
  },
  {
    icon: '✅',
    title: 'Completed Today',
    count: 2,
    subtitle: 'Resolved on 2025-05-13',
    glow: 'rgba(16,185,129,0.25)',
    border: 'rgba(16,185,129,0.35)',
  },
])

// ─── Assigned Tickets ─────────────────────────────────────────────────────────
const tickets = ref([
  { id: 'TKT-0001', customer: 'Rahul Sharma',  machine: 'CNC Machine X200',    status: 'Open',        priority: 'High',   date: '2025-05-13' },
  { id: 'TKT-0002', customer: 'Priya Verma',   machine: 'Hydraulic Press HP5', status: 'In Progress', priority: 'Medium', date: '2025-05-12' },
  { id: 'TKT-0003', customer: 'Amit Joshi',    machine: 'Lathe Machine LM3',   status: 'Completed',   priority: 'Low',    date: '2025-05-11' },
  { id: 'TKT-0004', customer: 'Sonia Patel',   machine: 'Drill Machine DM7',   status: 'Open',        priority: 'High',   date: '2025-05-10' },
  { id: 'TKT-0005', customer: 'Vikram Singh',  machine: 'Compressor CP-200',   status: 'In Progress', priority: 'Medium', date: '2025-05-09' },
])

// ─── Used Parts ───────────────────────────────────────────────────────────────
const usedParts = ref([
  { name: 'Hydraulic Seal Kit',  qty: 2, price: 1200 },
  { name: 'Ball Bearing 6205',   qty: 4, price:  350 },
  { name: 'V-Belt A42',          qty: 1, price:  180 },
])
const totalPartsValue = computed(() => usedParts.value.reduce((s, p) => s + p.qty * p.price, 0))

// ─── Badge config ─────────────────────────────────────────────────────────────
const statusConfig = {
  'Open':        { cls: 'badge-yellow', icon: '🟡' },
  'In Progress': { cls: 'badge-blue',   icon: '🔵' },
  'Completed':   { cls: 'badge-green',  icon: '🟢' },
}
const priorityConfig = {
  'High':   { cls: 'pri-red',    icon: '🔴' },
  'Medium': { cls: 'pri-orange', icon: '🟠' },
  'Low':    { cls: 'pri-green',  icon: '🟢' },
}

// ─── Action handlers ─────────────────────────────────────────────────────────
function startWork(ticket) {
  ticket.status = 'In Progress'
}
function completeTicket(ticket) {
  ticket.status = 'Completed'
}
function addPart() {
  usedParts.value.push({ name: 'New Part', qty: 1, price: 0 })
}

// ─── Lifecycle ────────────────────────────────────────────────────────────────
onMounted(() => {
  setTimeout(() => { pageVisible.value = true }, 80)
})

/* ─────────────────────────────────────────────────────────────────────────────
   API EXAMPLE — assigned tickets fetch करने का तरीका
   GET /api/resource/Service Ticket

   async function fetchAssignedTickets() {
     isLoading.value = true
     try {
       const res = await fetch(
         '/api/resource/Service%20Ticket' +
         '?filters=[["assigned_technician","=","TECH-001"]]' +
         '&fields=["name","customer","machine","status","priority","creation"]',
         { headers: { 'X-Frappe-CSRF-Token': 'fetch' } }
       )
       const { data } = await res.json()
       tickets.value = data.map(t => ({
         id:       t.name,
         customer: t.customer,
         machine:  t.machine,
         status:   t.status,
         priority: t.priority,
         date:     t.creation?.slice(0, 10),
       }))
     } catch (err) {
       console.error('Fetch failed:', err)
     } finally {
       isLoading.value = false
     }
   }
───────────────────────────────────────────────────────────────────────────── */
</script>

<template>
  <div class="dash" :class="{ visible: pageVisible }">

    <!-- ── Ambient BG (same family as Home.vue) ── -->
    <div class="bg-layer" aria-hidden="true">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
      <div class="grid-overlay"></div>
    </div>

    <div class="dash-inner">

      <!-- ── TOPBAR ── -->
      <nav class="topbar">
        <div class="brand">
          <span class="brand-icon">⚡</span>
          <span class="brand-name">Smart<span class="accent">Market</span></span>
          <span class="role-chip">Technician</span>
        </div>
        <div class="topbar-right">
          <span class="user-chip">🔧 {{ technicianName }}</span>
          <button class="btn-outline" @click="router.push('/')">← Home</button>
          <button class="btn-danger-sm">Sign Out</button>
        </div>
      </nav>

      <!-- ── WELCOME ── -->
      <section class="welcome-section">
        <div class="welcome-badge">🔧 Technician Portal</div>
        <h1 class="welcome-title">
          Welcome, <span class="gradient-text">{{ technicianName }}</span>
        </h1>
        <p class="welcome-sub">
          Manage assigned service tickets and machine repairs — all in one place.
        </p>
      </section>

      <!-- ── SUMMARY CARDS ── -->
      <section class="cards-section">
        <div
          v-for="card in summaryCards"
          :key="card.title"
          class="summary-card"
          :style="{ '--glow': card.glow, '--border': card.border }"
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

      <!-- ── TWO-COLUMN LAYOUT (table + parts) ── -->
      <div class="main-grid">

        <!-- ── ASSIGNED TICKETS ── -->
        <section class="panel tickets-panel">
          <div class="panel-head">
            <div>
              <h2 class="panel-title">Assigned Tickets</h2>
              <p class="panel-desc">Tap a row to select · Use action buttons below</p>
            </div>
            <span class="ticket-count-chip">{{ tickets.length }} total</span>
          </div>

          <!-- Loading state -->
          <div v-if="isLoading" class="spinner-wrap">
            <div class="spinner"></div>
            <p class="spinner-text">Loading tickets…</p>
          </div>

          <!-- Table -->
          <div v-else class="table-wrap">
            <table class="tbl">
              <thead>
                <tr>
                  <th>Ticket ID</th>
                  <th>Customer</th>
                  <th>Machine</th>
                  <th>Status</th>
                  <th>Priority</th>
                  <th>Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="ticket in tickets"
                  :key="ticket.id"
                  class="tbl-row"
                  :class="{ selected: selectedTicket?.id === ticket.id }"
                  @click="selectedTicket = ticket"
                >
                  <td class="ticket-id">{{ ticket.id }}</td>
                  <td class="customer-name">{{ ticket.customer }}</td>
                  <td class="machine-name">{{ ticket.machine }}</td>
                  <td>
                    <span class="badge" :class="statusConfig[ticket.status]?.cls">
                      {{ statusConfig[ticket.status]?.icon }} {{ ticket.status }}
                    </span>
                  </td>
                  <td>
                    <span class="badge" :class="priorityConfig[ticket.priority]?.cls">
                      {{ priorityConfig[ticket.priority]?.icon }} {{ ticket.priority }}
                    </span>
                  </td>
                  <td class="date-cell">{{ ticket.date }}</td>
                  <td class="action-cell">
                    <button
                      v-if="ticket.status === 'Open'"
                      class="act-btn act-start"
                      @click.stop="startWork(ticket)"
                    >▶ Start</button>
                    <button
                      v-if="ticket.status === 'In Progress'"
                      class="act-btn act-done"
                      @click.stop="completeTicket(ticket)"
                    >✓ Done</button>
                    <span v-if="ticket.status === 'Completed'" class="done-label">Closed</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- ── RIGHT COLUMN ── -->
        <aside class="right-col">

          <!-- Selected ticket quick-actions -->
          <section class="panel quick-actions">
            <h2 class="panel-title">Quick Actions</h2>
            <p class="panel-desc mb-1">
              {{ selectedTicket ? `Selected: ${selectedTicket.id}` : 'Select a ticket from the table' }}
            </p>
            <div class="action-btns">
              <button
                class="action-btn action-start"
                :disabled="!selectedTicket || selectedTicket.status !== 'Open'"
                @click="selectedTicket && startWork(selectedTicket)"
              >
                <span>▶</span> Start Work
              </button>
              <button
                class="action-btn action-complete"
                :disabled="!selectedTicket || selectedTicket.status !== 'In Progress'"
                @click="selectedTicket && completeTicket(selectedTicket)"
              >
                <span>✓</span> Complete Ticket
              </button>
              <button class="action-btn action-parts" @click="addPart">
                <span>＋</span> Add Used Parts
              </button>
            </div>
          </section>

          <!-- Used Parts -->
          <section class="panel parts-panel">
            <div class="panel-head">
              <div>
                <h2 class="panel-title">Used Parts</h2>
                <p class="panel-desc">Parts consumed for repairs</p>
              </div>
              <button class="add-part-btn" @click="addPart">＋</button>
            </div>

            <!-- Parts list -->
            <div class="parts-list">
              <div
                v-for="(part, i) in usedParts"
                :key="i"
                class="part-row"
              >
                <div class="part-info">
                  <span class="part-icon">🔩</span>
                  <div>
                    <p class="part-name">{{ part.name }}</p>
                    <p class="part-qty">Qty: {{ part.qty }}</p>
                  </div>
                </div>
                <span class="part-price">₹{{ (part.qty * part.price).toLocaleString() }}</span>
              </div>
            </div>

            <!-- Total -->
            <div class="parts-total">
              <span>Total Value</span>
              <span class="total-val">₹{{ totalPartsValue.toLocaleString() }}</span>
            </div>
          </section>

        </aside>
      </div><!-- /main-grid -->

    </div><!-- /dash-inner -->
  </div><!-- /dash -->
</template>

<style scoped>
/* ── Reset ── */
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

/* ── Background orbs ── */
.bg-layer { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.orb {
  position: absolute; border-radius: 50%;
  filter: blur(90px); opacity: 0.11;
  animation: orbFloat 9s ease-in-out infinite;
}
.orb-1 { width: 550px; height: 550px; background: #6366f1; top: -150px; right: -150px; }
.orb-2 { width: 350px; height: 350px; background: #f59e0b; bottom: 5%; left: 5%; animation-duration: 12s; animation-direction: reverse; }
.orb-3 { width: 280px; height: 280px; background: #10b981; top: 50%; left: 40%; animation-duration: 15s; }
@keyframes orbFloat {
  0%,100% { transform: translate(0,0); }
  50%      { transform: translate(20px,-20px); }
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
  max-width: 1300px; margin: 0 auto;
  padding: 0 1.5rem 4rem;
}

/* ── Topbar ── */
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.25rem 0;
  border-bottom: 1px solid rgba(99,102,241,0.12);
  margin-bottom: 2.5rem; flex-wrap: wrap; gap: 0.75rem;
}
.brand { display: flex; align-items: center; gap: 0.5rem; }
.brand-icon { font-size: 1.4rem; }
.brand-name { font-size: 1.2rem; font-weight: 800; letter-spacing: -0.5px; }
.accent { color: #6366f1; }
.role-chip {
  padding: 0.2rem 0.65rem; border-radius: 100px;
  background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.3);
  color: #fbbf24; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
}
.topbar-right { display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; }
.user-chip {
  padding: 0.4rem 0.9rem; border-radius: 100px;
  background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.25);
  color: #fcd34d; font-size: 0.82rem; font-weight: 600;
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

/* ── Welcome ── */
.welcome-section { margin-bottom: 2.5rem; }
.welcome-badge {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.35rem 1rem; border-radius: 100px;
  background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.25);
  color: #fcd34d; font-size: 0.8rem; font-weight: 600;
  margin-bottom: 1rem;
}
.welcome-title {
  font-size: 2.4rem; font-weight: 900;
  letter-spacing: -1.5px; line-height: 1.1; margin-bottom: 0.6rem;
}
.gradient-text {
  background: linear-gradient(135deg, #f59e0b, #ef4444);
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
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  cursor: default;
}
.summary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 16px 48px var(--glow, rgba(99,102,241,0.2));
}
.card-glow-dot {
  position: absolute; top: -30px; right: -30px;
  width: 100px; height: 100px; border-radius: 50%;
  background: var(--glow, rgba(99,102,241,0.15));
  filter: blur(30px); pointer-events: none;
}
.card-icon-wrap {
  width: 52px; height: 52px; border-radius: 14px; flex-shrink: 0;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  display: flex; align-items: center; justify-content: center;
}
.card-icon { font-size: 1.5rem; }
.card-body { display: flex; flex-direction: column; gap: 0.1rem; }
.card-title { font-size: 0.78rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.card-count { font-size: 1.9rem; font-weight: 900; letter-spacing: -1px; color: #e2e8f0; }
.card-sub { font-size: 0.75rem; color: #475569; margin-top: 0.1rem; }

/* ── Main grid ── */
.main-grid {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 1.5rem;
  align-items: start;
}

/* ── Panel base ── */
.panel {
  background: rgba(15,23,42,0.7);
  border: 1px solid rgba(99,102,241,0.12);
  border-radius: 18px; padding: 1.75rem;
  backdrop-filter: blur(16px);
}
.panel-head {
  display: flex; align-items: flex-start; justify-content: space-between;
  margin-bottom: 1.5rem; gap: 1rem;
}
.panel-title { font-size: 1.1rem; font-weight: 800; color: #e2e8f0; margin-bottom: 0.2rem; }
.panel-desc { font-size: 0.78rem; color: #475569; }
.mb-1 { margin-bottom: 1rem; }
.ticket-count-chip {
  padding: 0.3rem 0.75rem; border-radius: 100px;
  background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.2);
  color: #a5b4fc; font-size: 0.75rem; font-weight: 700; white-space: nowrap;
}

/* ── Table ── */
.table-wrap { overflow-x: auto; border-radius: 10px; }
.tbl { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.tbl thead tr { border-bottom: 1px solid rgba(99,102,241,0.12); }
.tbl th {
  text-align: left; padding: 0.7rem 0.85rem;
  color: #475569; font-size: 0.72rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap;
}
.tbl-row {
  border-bottom: 1px solid rgba(255,255,255,0.04);
  transition: background 0.15s ease; cursor: pointer;
}
.tbl-row:last-child { border-bottom: none; }
.tbl-row:hover { background: rgba(99,102,241,0.05); }
.tbl-row.selected { background: rgba(99,102,241,0.08); border-left: 3px solid #6366f1; }
.tbl td { padding: 0.8rem 0.85rem; vertical-align: middle; }
.ticket-id { color: #a5b4fc; font-weight: 700; font-family: monospace; font-size: 0.8rem; }
.customer-name { color: #e2e8f0; font-weight: 600; }
.machine-name { color: #94a3b8; font-size: 0.8rem; }
.date-cell { color: #475569; font-size: 0.78rem; white-space: nowrap; }
.action-cell { white-space: nowrap; }

/* ── Inline action buttons ── */
.act-btn {
  padding: 0.3rem 0.7rem; border-radius: 7px;
  font-size: 0.75rem; font-weight: 700; cursor: pointer; border: none;
  transition: all 0.2s;
}
.act-start { background: rgba(59,130,246,0.15); color: #93c5fd; border: 1px solid rgba(59,130,246,0.3); }
.act-start:hover { background: rgba(59,130,246,0.25); }
.act-done { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
.act-done:hover { background: rgba(16,185,129,0.25); }
.done-label { font-size: 0.72rem; color: #334155; font-weight: 600; }

/* ── Status / priority badges ── */
.badge {
  display: inline-flex; align-items: center; gap: 0.25rem;
  padding: 0.25rem 0.6rem; border-radius: 100px;
  font-size: 0.72rem; font-weight: 700; white-space: nowrap;
}
.badge-yellow { background: rgba(234,179,8,0.12);  border: 1px solid rgba(234,179,8,0.3);  color: #fde047; }
.badge-blue   { background: rgba(59,130,246,0.12); border: 1px solid rgba(59,130,246,0.3); color: #93c5fd; }
.badge-green  { background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.3); color: #34d399; }
.pri-red    { background: rgba(239,68,68,0.12);  border: 1px solid rgba(239,68,68,0.3);  color: #fca5a5; }
.pri-orange { background: rgba(249,115,22,0.12); border: 1px solid rgba(249,115,22,0.3); color: #fdba74; }
.pri-green  { background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.3); color: #34d399; }

/* ── Right column ── */
.right-col { display: flex; flex-direction: column; gap: 1.25rem; }

/* ── Quick Actions ── */
.quick-actions { }
.action-btns { display: flex; flex-direction: column; gap: 0.6rem; }
.action-btn {
  display: flex; align-items: center; gap: 0.6rem;
  padding: 0.7rem 1rem; border-radius: 10px;
  font-size: 0.85rem; font-weight: 700; cursor: pointer;
  border: 1px solid transparent; transition: all 0.2s;
  text-align: left;
}
.action-btn:disabled { opacity: 0.35; cursor: not-allowed; }
.action-start {
  background: rgba(59,130,246,0.1); border-color: rgba(59,130,246,0.3); color: #93c5fd;
}
.action-start:not(:disabled):hover { background: rgba(59,130,246,0.2); transform: translateX(3px); }
.action-complete {
  background: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.3); color: #34d399;
}
.action-complete:not(:disabled):hover { background: rgba(16,185,129,0.2); transform: translateX(3px); }
.action-parts {
  background: rgba(139,92,246,0.1); border-color: rgba(139,92,246,0.3); color: #c4b5fd;
}
.action-parts:hover { background: rgba(139,92,246,0.2); transform: translateX(3px); }

/* ── Parts panel ── */
.parts-panel { }
.add-part-btn {
  width: 30px; height: 30px; border-radius: 8px;
  background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.3);
  color: #a5b4fc; font-size: 1.2rem; cursor: pointer; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s; flex-shrink: 0;
}
.add-part-btn:hover { background: rgba(99,102,241,0.22); }
.parts-list { display: flex; flex-direction: column; gap: 0.6rem; margin-bottom: 1rem; }
.part-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.65rem 0.75rem;
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05);
  border-radius: 10px; gap: 0.75rem;
}
.part-info { display: flex; align-items: center; gap: 0.6rem; }
.part-icon { font-size: 1.1rem; }
.part-name { font-size: 0.8rem; font-weight: 600; color: #cbd5e1; }
.part-qty { font-size: 0.7rem; color: #475569; margin-top: 1px; }
.part-price { font-size: 0.82rem; font-weight: 700; color: #34d399; white-space: nowrap; }
.parts-total {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.6rem 0.75rem;
  border-top: 1px solid rgba(255,255,255,0.06);
  font-size: 0.82rem; color: #64748b; font-weight: 600;
}
.total-val { font-size: 1rem; font-weight: 800; color: #e2e8f0; }

/* ── Spinner ── */
.spinner-wrap { display: flex; flex-direction: column; align-items: center; padding: 3rem; gap: 1rem; }
.spinner {
  width: 36px; height: 36px; border-radius: 50%;
  border: 3px solid rgba(99,102,241,0.2); border-top-color: #6366f1;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.spinner-text { color: #475569; font-size: 0.82rem; }

/* ── Responsive ── */
@media (max-width: 1024px) {
  .main-grid { grid-template-columns: 1fr; }
  .right-col { flex-direction: row; flex-wrap: wrap; }
  .quick-actions, .parts-panel { flex: 1; min-width: 260px; }
}
@media (max-width: 768px) {
  .cards-section { grid-template-columns: 1fr; }
  .welcome-title { font-size: 1.8rem; }
  .right-col { flex-direction: column; }
}
</style>
