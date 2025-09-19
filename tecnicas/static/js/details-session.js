const actionForm = document.querySelector(".form-action-session");
const notificationError = document.querySelector(".ct-notification-error");

if (notificationError) {
  setTimeout(function () {
    notificationError.classList.add("hidden");
  }, 2000);
}

function startRepetition() {
  const inputAction = document.createElement("input");
  inputAction.type = "hidden";
  inputAction.name = "action";
  inputAction.value = "start_session";

  const inputUser = document.createElement("input");
  inputUser.type = "hidden";
  inputUser.name = "username";
  inputUser.value = "aguBido";

  actionForm.appendChild(inputAction);
  actionForm.appendChild(inputUser);

  actionForm.classList.remove("hidden");
  actionForm.submit();
}
