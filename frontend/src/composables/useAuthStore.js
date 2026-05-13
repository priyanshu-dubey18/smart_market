import { reactive } from 'vue'

const state = reactive({
  userType: '',
  fullName: '',
  email: '',
  phone: '',
  password: '',
  otpFlow: '',
  otpContact: '',
  otpMedium: '',
  verifiedOtp: false,
  loggedInUser: null,
  devOtp: '',
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
