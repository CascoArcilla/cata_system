const notifiactions = document.getElementsByClassName("ct-notificacion");
const inputs = document.getElementsByClassName("ct-inputs-pos-cata");

for (let index = 0; index < inputs.length; index++) {
  inputs.item(index).addEventListener("change", hiddenErrorAndMessages);
}

function hiddenErrorAndMessages(e) {
  for (let index = 0; index < notifiactions.length; index++) {
    console.log("Oculto");
    notifiactions.item(index).classList.add("hidden");
  }
}
