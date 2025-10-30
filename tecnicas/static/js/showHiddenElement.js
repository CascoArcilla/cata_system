function hiddenWarningDialog(styleClass) {
  const element = document.querySelector(`.${styleClass}`)
  element.classList.add("hidden")
}

function showWarningDialog(styleClass) {
  const element = document.querySelector(`.${styleClass}`)
  element.classList.remove("hidden")
}