<script setup>
import { ref } from 'vue'

// Form field values
const customer = ref('')
const machine = ref('')
const serialNumber = ref('')
const issueDescription = ref('')

// Messages shown to the user
const errorMessage = ref('')
const successMessage = ref('')
const isSubmitting = ref(false)
const showModal = ref(false)
const modalType = ref('') // 'success' or 'error'
const modalMessage = ref('')

// Reset all form fields after a successful submit
function clearForm() {
  customer.value = ''
  machine.value = ''
  serialNumber.value = ''
  issueDescription.value = ''
}

// Close the modal
function closeModal() {
  showModal.value = false
  modalType.value = ''
  modalMessage.value = ''
}

// Submit the service request to the Frappe backend
async function submitServiceRequest() {
  isSubmitting.value = true

  try {
    // First, ensure customer exists
    let customerName = await ensureCustomerExists(customer.value)
    
    // Then, ensure machine exists
    let machineName = await ensureMachineExists(machine.value, serialNumber.value, customerName)
    
    // Finally, create the service ticket
    const ticketResponse = await fetch('/api/resource/Service Ticket', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        customer: customerName,
        machine: machineName,
        issue_description: issueDescription.value,
        status: 'Open',
        priority: 'Medium'
      }),
    })

    if (!ticketResponse.ok) {
      const errorData = await ticketResponse.json()
      throw new Error(errorData.exception || `Failed to create ticket: ${ticketResponse.status}`)
    }

    const ticketData = await ticketResponse.json()
    showModal.value = true
    modalType.value = 'success'
    modalMessage.value = `Service Request Submitted Successfully! Ticket ID: ${ticketData.data.name}`
    clearForm()
  } catch (error) {
    showModal.value = true
    modalType.value = 'error'
    modalMessage.value = error.message || 'An unexpected error occurred'
    console.error('Service Request Error:', error)
  } finally {
    isSubmitting.value = false
  }
}

// Helper function to ensure customer exists
async function ensureCustomerExists(customerName) {
  try {
    // Check if customer exists
    const checkResponse = await fetch(`/api/resource/Customer?filters=[["customer_name","=","${customerName}"]]`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (checkResponse.ok) {
      const checkData = await checkResponse.json()
      if (checkData.data && checkData.data.length > 0) {
        return checkData.data[0].name
      }
    }
    
    // Create new customer
    const createResponse = await fetch('/api/resource/Customer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        customer_name: customerName,
        customer_type: 'Individual'
      }),
    })
    
    if (!createResponse.ok) {
      throw new Error('Failed to create customer')
    }
    
    const createData = await createResponse.json()
    return createData.data.name
  } catch (error) {
    console.error('Customer creation error:', error)
    return customerName // Fallback
  }
}

// Helper function to ensure machine exists
async function ensureMachineExists(machineName, serialNumber, customerName) {
  try {
    // Check if machine exists by serial number
    const checkResponse = await fetch(`/api/resource/Machine?filters=[["serial__number","=","${serialNumber}"]]`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (checkResponse.ok) {
      const checkData = await checkResponse.json()
      if (checkData.data && checkData.data.length > 0) {
        return checkData.data[0].name
      }
    }
    
    // Create new machine
    const createResponse = await fetch('/api/resource/Machine', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        machine_name: machineName,
        serial__number: serialNumber,
        customer: customerName,
        status: 'Active'
      }),
    })
    
    if (!createResponse.ok) {
      throw new Error('Failed to create machine')
    }
    
    const createData = await createResponse.json()
    return createData.data.name
  } catch (error) {
    console.error('Machine creation error:', error)
    return serialNumber // Fallback
  }
}
</script>

<template>
  <main class="service-request-page">
    <h1>Service Request Form</h1>

    <form class="service-request-form" @submit.prevent="submitServiceRequest">
      <div class="form-group">
        <label for="customer">Customer Name</label>
        <input
          id="customer"
          v-model.trim="customer"
          type="text"
          placeholder="Enter customer name"
        />
      </div>

      <div class="form-group">
        <label for="machine">Machine</label>
        <input
          id="machine"
          v-model.trim="machine"
          type="text"
          placeholder="Enter machine name"
        />
      </div>

      <div class="form-group">
        <label for="serial-number">Serial Number</label>
        <input
          id="serial-number"
          v-model.trim="serialNumber"
          type="text"
          placeholder="Enter machine serial number"
        />
      </div>

      <div class="form-group">
        <label for="issue-description">Problem Description</label>
        <textarea
          id="issue-description"
          v-model.trim="issueDescription"
          rows="5"
          placeholder="Describe the problem"
        ></textarea>
      </div>

      <p v-if="errorMessage" class="message error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="message success">{{ successMessage }}</p>

      <button type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Submitting...' : 'Submit Request' }}
      </button>
    </form>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3 :class="modalType === 'success' ? 'success-title' : 'error-title'">
            {{ modalType === 'success' ? 'Success!' : 'Error!' }}
          </h3>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <p>{{ modalMessage }}</p>
        </div>
        <div class="modal-footer">
          <button class="modal-btn" @click="closeModal">OK</button>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.service-request-page {
  max-width: 520px;
  margin: 0 auto;
  padding: 2rem;
}

.service-request-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

label {
  font-weight: 600;
}

input,
textarea {
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font: inherit;
}

textarea {
  resize: vertical;
}

button {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 4px;
  background: #2563eb;
  color: white;
  font: inherit;
  cursor: pointer;
}

button:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.message {
  margin: 0;
  font-weight: 600;
}

.success {
  color: #15803d;
}

.error {
  color: #b91c1c;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.success-title {
  color: #15803d;
  margin: 0;
}

.error-title {
  color: #b91c1c;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
}

.close-btn:hover {
  color: #374151;
}

.modal-body {
  padding: 1rem;
}

.modal-body p {
  margin: 0;
  line-height: 1.5;
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
  text-align: right;
}

.modal-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  background: #2563eb;
  color: white;
  cursor: pointer;
  font: inherit;
}

.modal-btn:hover {
  background: #1d4ed8;
}
</style>
