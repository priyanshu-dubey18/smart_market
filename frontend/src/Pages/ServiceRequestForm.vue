<script setup>
import { ref } from 'vue'

// Form field values
const customer = ref('')
const machine = ref('')
const issueDescription = ref('')

// Messages shown to the user
const errorMessage = ref('')
const successMessage = ref('')
const isSubmitting = ref(false)

// Reset all form fields after a successful submit
function clearForm() {
  customer.value = ''
  machine.value = ''
  issueDescription.value = ''
}

// Submit the service request to the Frappe backend
async function submitServiceRequest() {
  errorMessage.value = ''
  successMessage.value = ''

  // Basic validation: all fields are required
  if (!customer.value || !machine.value || !issueDescription.value) {
    errorMessage.value = 'All fields are required'
    return
  }

  isSubmitting.value = true

  try {
    const response = await fetch('/api/method/smart_market.api.create_service_ticket', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        customer_name: customer.value,
        machine_name: machine.value,
        issue_description: issueDescription.value,
      }),
    })

    const result = await response.json()

    if (!response.ok || !result.message.success) {
      throw new Error(result.message.message || 'Failed to submit service request')
    }

    successMessage.value = 'Service Request Submitted Successfully! Ticket ID: ' + result.message.ticket_id
    clearForm()
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    isSubmitting.value = false
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
</style>
