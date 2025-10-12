function finishSession() {
  const form = document.querySelector(".action-form");
  form.querySelector("input").value = "finish_session";
  form.submit();
}
