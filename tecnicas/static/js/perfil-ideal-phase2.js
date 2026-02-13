const BTN_CLASS_STYLE = [
  "text-lg",
  "tracking-wider",
  "font-medium",
  "p-2",
  "px-4",
  "border-b-2",
  "active:border-b-0",
  "active:border-t-2",
  "active:border-blue-500",
  "border-blue-800",
  "transition-all",
  "rounded-xl",
  "bg-blue-500",
  "text-white",
  "w-fit",
  "disabled:bg-amber-600",
];

function checkSendRatingHedonic() {
  const btnCheck = document.querySelector(".ct-btn-check-hedonic");
  const btnSend = document.querySelector(".ct-btn-submit-hedonic");
  const btnCancel = document.querySelector(".ct-btn-cancel-hedonic");

  btnCheck.classList.add("hidden");
  btnSend.classList.remove("hidden");
  btnCancel.classList.remove("hidden");
}

function cancelSendRatingHedonic() {
  const btnCheck = document.querySelector(".ct-btn-check-hedonic");
  const btnSend = document.querySelector(".ct-btn-submit-hedonic");
  const btnCancel = document.querySelector(".ct-btn-cancel-hedonic");

  btnCheck.classList.remove("hidden");
  btnSend.classList.add("hidden");
  btnCancel.classList.add("hidden");
}

async function sendRatingHedonic() {
  const containerBtn = document.querySelector(".actions-hedonic");
  addOrRemoveWaitSpin(containerBtn);

  const formRatingHedonic = document.querySelector(".form-rating-hedonic");
  const dataForm = new FormData(formRatingHedonic);
  const url = "/cata/testers/api/ratingword/perfil-ideal/fase2";

  const codeProduct = document
    .querySelector(".ct-product-rating")
    .querySelector(".code-product").textContent;
  const idProduct = document
    .querySelector(".ct-product-rating")
    .querySelector(".id-product").textContent;

  const idTechnique = document.querySelector(".ct-input-id-tech").value;

  // Obtener valor de la escala hedónica
  const hedonicValue = formRatingHedonic.querySelector('input[name="rating-hedonic"]').value;

  dataForm.set("code-product", codeProduct);
  dataForm.set("id-product", idProduct);
  dataForm.set("id-technique", idTechnique);
  dataForm.set("rating-hedonic", hedonicValue);

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": dataForm.get("csrfmiddlewaretoken"),
      },
      body: dataForm,
    });

    const jsonResponse = await response.json();

    if (jsonResponse.error) {
      addOrRemoveWaitSpin(containerBtn, false, jsonResponse.error);
      return;
    }

    remplaceForm(formRatingHedonic, jsonResponse.message);
    addBtnNextProduct();
  } catch (error) {
    addOrRemoveWaitSpin(containerBtn, false, "La sesión ha caducado");
    console.log("Error:", error);
  }
}

function remplaceForm(oldForm, message) {
  const articleContainer = document.createElement("article");
  const thankYouMessage = document.createElement("p");
  const messageResponse = document.createElement("p");

  thankYouMessage.innerHTML =
    "Producto calificado,<br>gracias por la participación";
  messageResponse.textContent = message;

  articleContainer.classList.add(
    "bg-gray-200",
    "p-6",
    "rounded-lg",
    "mb-3",
    "text-center"
  );
  thankYouMessage.classList.add("text-2xl", "font-bold");
  messageResponse.classList.add("text-lg");

  articleContainer.appendChild(thankYouMessage);
  articleContainer.appendChild(messageResponse);
  oldForm.replaceWith(articleContainer);
}

function addBtnNextProduct() {
  const thankYouMessage = document.createElement("p");
  thankYouMessage.textContent = "Producto evaluado exitosamente";
  thankYouMessage.classList.add("text-2xl", "font-bold", "mb-3");

  const btnNextProduct = document.createElement("button");
  btnNextProduct.classList.add(...BTN_CLASS_STYLE, "ct-btn-next-product");
  btnNextProduct.textContent = "Siguiente producto";
  btnNextProduct.addEventListener("click", nextProduct);

  const articleContainer = document.createElement("article");
  articleContainer.classList.add(
    "bg-gray-200",
    "p-6",
    "rounded-lg",
    "mb-3",
    "text-center"
  );

  articleContainer.appendChild(thankYouMessage);
  articleContainer.appendChild(btnNextProduct);

  const scalesContainer = document.querySelector(".scales-container");
  scalesContainer.innerHTML = "";
  scalesContainer.appendChild(articleContainer);
}

function nextProduct(e) {
  location.reload();
}

function createSpinCharge() {
  const divSpin = document.createElement("div");

  divSpin.classList.add(
    "w-10",
    "h-10",
    "rounded-full",
    "border-4",
    "border-t-4",
    "border-gray-200",
    "border-t-blue-600",
    "animate-spin"
  );

  return divSpin;
}

function addOrRemoveWaitSpin(containerBtn, render = true, error = false) {
  const actions = containerBtn.querySelector(`.btns-container`);

  if (render) {
    containerBtn.innerHTML = "";
    const spin = createSpinCharge();
    actions.classList.add("hidden");
    containerBtn.appendChild(spin);
    containerBtn.appendChild(actions);
    containerBtn.classList.remove("items-end");
    containerBtn.classList.add("items-center");
  }

  if (!render) {
    containerBtn.innerHTML = "";

    if (error) {
      containerBtn.appendChild(createErrorSubmit(error));
    }

    containerBtn.append(actions);
    actions.classList.remove("hidden");
    containerBtn.classList.remove("items-center");
    containerBtn.classList.add("items-end");
  }
}

function createErrorSubmit(errorMessage) {
  const containerError = document.createElement("div");
  containerError.classList.add(
    "w-full",
    "p-2",
    "bg-red-400",
    "font-bold",
    "text-center",
    "rounded-lg"
  );

  const errorP = document.createElement("p");
  errorP.textContent = errorMessage;

  containerError.appendChild(errorP);
  return containerError;
}
