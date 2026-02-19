function toggleMobileMenu() {
  const mobileMenu = document.getElementById("mobile-menu")
  const menuIcon = document.getElementById("menu-icon")
  const closeIcon = document.getElementById("close-icon")

  mobileMenu.classList.toggle("active")

  if (mobileMenu.classList.contains("active")) {
    menuIcon.style.display = "none"
    closeIcon.style.display = "block"
  } else {
    menuIcon.style.display = "block"
    closeIcon.style.display = "none"
  }
}
