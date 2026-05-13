<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const customer = ref('')
const machine = ref('')
const serialNumber = ref('')
const issueDescription = ref('')

const isSubmitting = ref(false)
const showModal = ref(false)
const modalType = ref('')
const modalMessage = ref('')
const ticketId = ref('')

function clearForm() {
  customer.value = ''
  machine.value = ''
  serialNumber.value = ''
  issueDescription.value = ''
}

function closeModal() {
  showModal.value = false
  modalType.value = ''
  modalMessage.value = ''
  ticketId.value = ''
}

async function submitServiceRequest() {
  if (!customer.value || !machine.value || !serialNumber.value || !issueDescription.value) {
    showModal.value = true
    modalType.value = 'error'
    modalMessage.value = 'All fields are required.'
    return
  }

  isSubmitting.value = true
  try {
    const response = await fetch('/api/method/smart_market.api.create_service_ticket', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': 'fetch' },
      body: JSON.stringify({
        customer_name: customer.value,
        machine_name: machine.value,
        serial_number: serialNumber.value,
        issue_description: issueDescription.value,
      }),
    })

    const data = await response.json()
    const result = data.message || data

    if (!response.ok || !result.success) {
      throw new Error(result.message || data.exception || 'Failed to submit service request')
    }

    ticketId.value = result.ticket_id || ''
    showModal.value = true
    modalType.value = 'success'
    modalMessage.value = 'Your service request has been submitted successfully!'
    clearForm()
  } catch (error) {
    showModal.value = true
    modalType.value = 'error'
    modalMessage.value = error.message || 'An unexpected error occurred'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <!-- Full-page dark background with ambient orbs -->
  <div class="relative min-h-screen bg-[#080d1a] flex items-center justify-center px-4 py-12 font-sans">

    <!-- Background orbs -->
    <div class="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      <div class="absolute w-[500px] h-[500px] rounded-full bg-indigo-500 opacity-10 blur-[90px] -top-40 -left-40 animate-float"></div>
      <div class="absolute w-[350px] h-[350px] rounded-full bg-cyan-400 opacity-10 blur-[80px] bottom-0 right-0 animate-float-reverse"></div>
      <!-- Grid overlay -->
      <div class="absolute inset-0" style="background-image: linear-gradient(rgba(99,102,241,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(99,102,241,0.03) 1px, transparent 1px); background-size: 50px 50px;"></div>
    </div>

    <!-- Card -->
    <div class="relative z-10 w-full max-w-lg">

      <!-- Back to home -->
      <button
        class="mb-5 text-slate-500 text-sm hover:text-indigo-400 transition-colors flex items-center gap-1"
        @click="router.push('/')"
      >
        ← Back to Home
      </button>

      <div class="bg-slate-900/90 border border-indigo-500/15 rounded-3xl p-8 backdrop-blur-xl shadow-[0_25px_50px_rgba(0,0,0,0.5)]">

        <!-- Logo -->
        <div class="flex items-center justify-center gap-2 mb-6">
          <span class="text-xl">⚡</span>
          <span class="text-lg font-extrabold text-slate-100">Smart<span class="text-indigo-400">Market</span></span>
        </div>

        <!-- Header -->
        <div class="mb-7">
          <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/15 border border-indigo-500/30 text-indigo-300 text-xs font-bold mb-3">
            🛠️ Service Request
          </div>
          <h1 class="text-2xl font-extrabold text-slate-100 tracking-tight mb-1">Submit a Service Request</h1>
          <p class="text-sm text-slate-500 leading-relaxed">Describe your issue and our team will get back to you promptly.</p>
        </div>

        <!-- Form -->
        <form class="flex flex-col gap-5" @submit.prevent="submitServiceRequest">

          <!-- Customer Name -->
          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-semibold text-slate-400 uppercase tracking-wide">Customer Name</label>
            <div class="flex items-center bg-white/5 border border-white/10 rounded-xl px-4 transition-all focus-within:border-indigo-500 focus-within:bg-indigo-500/5 focus-within:shadow-[0_0_0_3px_rgba(99,102,241,0.1)]">
              <span class="mr-3 text-base opacity-60 flex-shrink-0">👤</span>
              <input
                v-model.trim="customer"
                type="text"
                placeholder="Enter your full name"
                class="flex-1 bg-transparent border-none outline-none text-slate-100 text-sm py-3.5 placeholder-slate-600 font-normal"
              />
            </div>
          </div>

          <!-- Machine Name -->
          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-semibold text-slate-400 uppercase tracking-wide">Machine Name</label>
            <div class="flex items-center bg-white/5 border border-white/10 rounded-xl px-4 transition-all focus-within:border-indigo-500 focus-within:bg-indigo-500/5 focus-within:shadow-[0_0_0_3px_rgba(99,102,241,0.1)]">
              <span class="mr-3 text-base opacity-60 flex-shrink-0">⚙️</span>
              <input
                v-model.trim="machine"
                type="text"
                placeholder="Enter machine name or model"
                class="flex-1 bg-transparent border-none outline-none text-slate-100 text-sm py-3.5 placeholder-slate-600 font-normal"
              />
            </div>
          </div>

          <!-- Serial Number -->
          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-semibold text-slate-400 uppercase tracking-wide">Serial Number</label>
            <div class="flex items-center bg-white/5 border border-white/10 rounded-xl px-4 transition-all focus-within:border-indigo-500 focus-within:bg-indigo-500/5 focus-within:shadow-[0_0_0_3px_rgba(99,102,241,0.1)]">
              <span class="mr-3 text-base opacity-60 flex-shrink-0">🔖</span>
              <input
                v-model.trim="serialNumber"
                type="text"
                placeholder="e.g. SN-2024-XXXX"
                class="flex-1 bg-transparent border-none outline-none text-slate-100 text-sm py-3.5 placeholder-slate-600 font-normal"
              />
            </div>
          </div>

          <!-- Issue Description -->
          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-semibold text-slate-400 uppercase tracking-wide">Problem Description</label>
            <div class="bg-white/5 border border-white/10 rounded-xl px-4 pt-3 pb-1 transition-all focus-within:border-indigo-500 focus-within:bg-indigo-500/5 focus-within:shadow-[0_0_0_3px_rgba(99,102,241,0.1)]">
              <textarea
                v-model.trim="issueDescription"
                rows="4"
                placeholder="Describe the problem in detail..."
                class="w-full bg-transparent border-none outline-none text-slate-100 text-sm resize-none placeholder-slate-600 font-normal leading-relaxed pb-2"
              ></textarea>
            </div>
            <span class="text-xs text-slate-600">Be as specific as possible to help us resolve faster.</span>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full py-3.5 rounded-xl font-bold text-base text-white bg-gradient-to-r from-indigo-600 to-indigo-500 shadow-[0_0_20px_rgba(99,102,241,0.3)] transition-all hover:-translate-y-0.5 hover:shadow-[0_0_35px_rgba(99,102,241,0.5)] disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2 min-h-[52px]"
          >
            <span v-if="!isSubmitting">Submit Service Request →</span>
            <span v-else class="flex items-center gap-2">
              <svg class="animate-spin w-5 h-5" viewBox="0 0 24 24" fill="none">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
              </svg>
              Submitting...
            </span>
          </button>
        </form>

        <!-- Footer note -->
        <p class="text-center text-xs text-slate-600 mt-5">
          Need help? <button class="text-indigo-400 font-semibold hover:text-indigo-300 transition-colors" @click="router.push('/signin')">Sign in</button> to track your tickets.
        </p>
      </div>
    </div>

    <!-- Modal -->
    <Transition name="modal">
      <div
        v-if="showModal"
        class="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/70 backdrop-blur-sm"
        @click.self="closeModal"
      >
        <div class="bg-slate-900 border rounded-2xl p-8 max-w-sm w-full text-center shadow-2xl flex flex-col items-center gap-4"
             :class="modalType === 'success' ? 'border-emerald-500/30' : 'border-red-500/30'"
        >
          <!-- Icon -->
          <div class="text-5xl animate-pop">
            {{ modalType === 'success' ? '🎉' : '⚠️' }}
          </div>

          <!-- Title -->
          <h3 class="text-xl font-extrabold text-slate-100">
            {{ modalType === 'success' ? 'Request Submitted!' : 'Something went wrong' }}
          </h3>

          <!-- Message -->
          <p class="text-sm text-slate-400 leading-relaxed">{{ modalMessage }}</p>

          <!-- Ticket ID badge -->
          <div v-if="ticketId" class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 flex justify-between items-center">
            <span class="text-xs text-slate-500">Ticket ID</span>
            <span class="text-sm font-bold text-indigo-300">{{ ticketId }}</span>
          </div>

          <!-- Close button -->
          <button
            class="w-full py-3 rounded-xl font-bold text-sm text-white transition-all hover:-translate-y-0.5"
            :class="modalType === 'success' ? 'bg-gradient-to-r from-emerald-600 to-emerald-500 shadow-[0_0_20px_rgba(16,185,129,0.3)] hover:shadow-[0_0_35px_rgba(16,185,129,0.5)]' : 'bg-gradient-to-r from-slate-700 to-slate-600'"
            @click="closeModal"
          >
            {{ modalType === 'success' ? 'Submit Another Request' : 'Try Again' }}
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(20px, -20px); }
}
@keyframes float-reverse {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-20px, 20px); }
}
@keyframes pop {
  0% { transform: scale(0); }
  80% { transform: scale(1.1); }
  100% { transform: scale(1); }
}
.animate-float { animation: float 8s ease-in-out infinite; }
.animate-float-reverse { animation: float-reverse 10s ease-in-out infinite; }
.animate-pop { animation: pop 0.5s ease forwards; }

.modal-enter-active, .modal-leave-active { transition: all 0.25s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; transform: scale(0.95); }
</style>
