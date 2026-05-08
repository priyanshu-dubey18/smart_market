import { reactive } from 'vue'

const state = reactive({
  userType: '',       // 'customer' | 'vendor'
  fullName: '',
  email: '',
  phone: '',
  password: '',
  otpFlow: '',        // 'signup' | 'reset-email' | 'reset-password'
  otpContact: '',     // email or phone shown in OTP screen
  otpMedium: '',      // 'phone' | 'email'
  verifiedOtp: false,
  loggedInUser: null,
})

function setSignupData(data) {
  Object.assign(state, data)
}

function clearAuth() {
  state.userType = ''
  state.fullName = ''
  state.email = ''
  state.phone = ''
  state.password = ''
  state.otpFlow = ''
  state.otpContact = ''
  state.otpMedium = ''
  state.verifiedOtp = false
}

export function useAuthStore() {
  return { state, setSignupData, clearAuth }
}
