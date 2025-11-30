const actionForm = document.querySelector(".form-action-session");
const notificationError = document.querySelector(".ct-notification-error");

if (notificationError) {
  setTimeout(function () {
    notificationError.classList.add("hidden");
  }, 3000);
}

function startRepetition() {
  const input = actionForm.querySelector(".action-option")
  input.value = "start_session";
  actionForm.submit();
}

function deleteSession() {
  const input = actionForm.querySelector(".action-option")
  input.value = "delete_session";
  actionForm.submit();
}

function startSession(nameMode) {
  const nameUnderscort = nameMode.replaceAll(" ", "_");
  console.log(nameUnderscort);
  const input = actionForm.querySelector(".action-option")
  input.value = `start_${nameUnderscort}`;
  actionForm.submit();
}
