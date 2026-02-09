function switchToSignup() {
  document.getElementById("login-form").classList.remove("active")
  document.getElementById("signup-form").classList.add("active")
}

function switchToLogin() {
  document.getElementById("signup-form").classList.remove("active")
  document.getElementById("login-form").classList.add("active")
}

function loginWithGoogle() {
  if (typeof googleLoginUrl !== "undefined" && googleLoginUrl) {
    window.location.href = googleLoginUrl
  } else {
    console.error("Google login URL is not defined")
  }
}
