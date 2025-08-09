const inputs = document.getElementsByClassName("ct-inputs-pos-cata");
disableInputs();
setTimeout(() => {
  const notifications = document.getElementsByClassName("ct-notifica");
  for (let index = 0; index < notifications.length; index++) {
    notifications.item(index).classList.add("hidden");
  }
}, 1800);

function disableInputs() {
  for (let index = 0; index < inputs.length; index++) {
    inputs.item(index).disabled = true;
  }
}

function enableInputs() {
  for (let index = 0; index < inputs.length; index++) {
    inputs.item(index).disabled = false;
  }
  changeButtons();
}

function changeButtons(callBack = function () {}) {
  const btnUpdate = document.getElementsByClassName("ct-btn-actualizar")[0];
  const btnSave = document.getElementsByClassName("ct-btn-guardar")[0];
  const btnCancel = document.getElementsByClassName("ct-btn-cancel")[0];

  if (btnUpdate.classList.contains("hidden")) {
    btnUpdate.classList.remove("hidden");
    btnSave.classList.add("hidden");
    btnCancel.classList.add("hidden");
  } else {
    btnUpdate.classList.add("hidden");
    btnSave.classList.remove("hidden");
    btnCancel.classList.remove("hidden");
  }

  callBack();
}
