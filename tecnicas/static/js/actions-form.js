function exit_sesion(styleClass) {
  const form = document.querySelector(`.${styleClass}`);
  const action = form.querySelector(".action-input");
  action.value = "exit_session";
  form.submit();
}

function finishSession(styleClass) {
  const form = document.querySelector(`.${styleClass}`);
  const action = form.querySelector(".action-input");
  action.value = "finish_session";
  form.submit();
}
