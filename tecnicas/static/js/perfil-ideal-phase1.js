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

// Actualizar valores mostrados en tiempo real
document.addEventListener('DOMContentLoaded', function() {
  const intensityScales = document.querySelectorAll('input[name="rating-intensity"]');
  const idealScales = document.querySelectorAll('input[name="rating-ideal"]');
  
  intensityScales.forEach(scale => {
    const word = scale.dataset.word;
    const valueDisplay = document.querySelector(`.intensity-value-${word}`);
    
    scale.addEventListener('input', function() {
      valueDisplay.textContent = this.value;
    });
  });
  
  idealScales.forEach(scale => {
    const word = scale.dataset.word;
    const valueDisplay = document.querySelector(`.ideal-value-${word}`);
    
    scale.addEventListener('input', function() {
      valueDisplay.textContent = this.value;
    });
  });
});

function checkSendRatingDual(word) {
  const btnCheck = document.querySelector(`.ct-btn-check-${word}`);
  const btnSend = document.querySelector(`.ct-btn-submit-${word}`);
  const btnCancel = document.querySelector(`.ct-btn-cancel-${word}`);

  btnCheck.classList.add("hidden");
  btnSend.classList.remove("hidden");
  btnCancel.classList.remove("hidden");
}

function cancelSendRatingDual(word) {
  const btnCheck = document.querySelector(`.ct-btn-check-${word}`);
  const btnSend = document.querySelector(`.ct-btn-submit-${word}`);
  const btnCancel = document.querySelector(`.ct-btn-cancel-${word}`);

  btnCheck.classList.remove("hidden");
  btnSend.classList.add("hidden");
  btnCancel.classList.add("hidden");
}

async function sendRatingDual(word) {
  const containerBtn = document.querySelector(`.actions-${word}`);
  addOrRemoveWaitSpin(containerBtn);

  const formRatingWord = document.querySelector(`.form-rating-${word}`);
  const dataForm = new FormData(formRatingWord);
  const url = "/sensorial/testers/api/ratingword/perfil-ideal/fase1";

  const codeProduct = document
    .querySelector(".ct-product-rating")
    .querySelector(".code-product").textContent;
  const idProduct = document
    .querySelector(".ct-product-rating")
    .querySelector(".id-product").textContent;

  const idWord = formRatingWord.querySelector(".id-word").textContent;
  const idTechnique = document.querySelector(".ct-input-id-tech").value;

  // Obtener valores de ambas escalas
  const intensityValue = formRatingWord.querySelector('input[name="rating-intensity"]').value;
  const idealValue = formRatingWord.querySelector('input[name="rating-ideal"]').value;

  dataForm.set("code-product", codeProduct);
  dataForm.set("id-product", idProduct);
  dataForm.set("name-word", word);
  dataForm.set("id-word", idWord);
  dataForm.set("id-technique", idTechnique);
  dataForm.set("rating-intensity", intensityValue);
  dataForm.set("rating-ideal", idealValue);

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

    remplaceForm(formRatingWord, jsonResponse.message);
    if (isEndedRatingWords()) {
      addBtnNextWord();
    }
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
    "Palabra calificada,<br>gracias por la participación";
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

function addBtnNextWord() {
  const thankYouMessage = document.createElement("p");
  thankYouMessage.textContent = "Has finalizado con este producto";
  thankYouMessage.classList.add("text-2xl", "font-bold", "mb-3");

  const btnNextWord = document.createElement("button");
  btnNextWord.classList.add(...BTN_CLASS_STYLE, "ct-btn-next-word");
  btnNextWord.textContent = "Siguiente producto";
  btnNextWord.addEventListener("click", nextWord);

  const articleContainer = document.createElement("article");
  articleContainer.classList.add(
    "bg-gray-200",
    "p-6",
    "rounded-lg",
    "mb-3",
    "text-center"
  );

  articleContainer.appendChild(thankYouMessage);
  articleContainer.appendChild(btnNextWord);

  const scalesContainer = document.querySelector(".scales-container");
  scalesContainer.innerHTML = "";
  scalesContainer.appendChild(articleContainer);
}

function isEndedRatingWords() {
  const currentNumerWords = document.querySelectorAll(
    'form[class*="form-rating-"]'
  ).length;

  return !currentNumerWords;
}

function nextWord(e) {
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
