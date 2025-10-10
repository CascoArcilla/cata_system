function startTest() {
  const actionForms = document.querySelector(".ct-action-form");
  actionForms.submit();
}

function closeSession() {
  const actionForms = document.querySelector(".ct-action-form");
  actionForms.querySelector(".action-option").value = "close_session"
  actionForms.submit();
}
