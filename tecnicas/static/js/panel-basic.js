const descriptons = {
  estructurada: "Establece número de segmentos:",
  continua: "Establece la longitud de la escala:",
  atributos:
    "Con el estilo atributos elijes las palabras para evaluar los productos",
  vocabulario:
    "Los vocabularios son un conjunto de palabras específicas para evaluar aspectos de un producto",
};

let inputsScale;
let inputTamano;

let inputsStyle;
let helpStyle;
let sizeOptionsContainer;
const SIZE_OPTIONS = {
  estructurada: [5, 7, 9],
  continua: [9, 13, 15],
};

initPanel();

function initPanel() {
  initRadios();
  initSizeOptions();
}

function initRadios() {
  inputTamano = document.getElementsByName("tamano_escala").item(0);
  inputsScale = document.getElementsByName("tipo_escala");
  inputsScale.item(0).checked = true;

  for (let index = 0; index < inputsScale.length; index++) {
    let parent = inputsScale.item(index).parentElement;
    parent.addEventListener("click", () => {
      showDescriptionTamanoScale(parent);
    });
    if (inputsScale.item(index).checked) {
      showDescriptionTamanoScale(parent);
    }
  }

  labelsStyle = document.getElementsByClassName("ct-radio-estilo");
  helpStyle = document.getElementsByClassName("ct-ayuda-estilo")[0];
  inputsStyle = document.getElementsByName("estilo_palabras");

  for (let index = 0; index < inputsStyle.length; index++) {
    let parent = inputsStyle.item(index).parentElement;
    parent.addEventListener("click", () => {
      showDescriptionStyle(parent);
    });
    if (inputsStyle.item(index).checked) {
      showDescriptionStyle(parent);
    }
  }
}

function initSizeOptions() {
  sizeOptionsContainer = document.getElementsByClassName(
    "cts-options-size-scale"
  )[0];

  for (let i = 0; i < inputsScale.length; i++) {
    const radio = inputsScale.item(i);
    radio.addEventListener("change", () => {
      const tag = getTagFromLabel(radio);
      populateSizeOptions(tag);
    });
    if (radio.checked) {
      const tag = getTagFromLabel(radio);
      populateSizeOptions(tag);
    }
  }

  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    const chosen = document.querySelector(
      'input[name="option_size_scale"]:checked'
    );
    if (chosen && inputTamano) {
      inputTamano.value = chosen.value;
    }

    if (sizeOptionsContainer) {
      const toRemove = sizeOptionsContainer.querySelectorAll(
        'input[name="option_size_scale"]'
      );
      toRemove.forEach((el) => el.remove());
    }
  });
}

function getTagFromLabel(radio) {
  try {
    const parent = radio.parentElement;
    if (!parent) return "";
    const text = parent.textContent || "";
    return text.trim().split(/\s+/)[0].toLowerCase();
  } catch (err) {
    return "";
  }
}

function populateSizeOptions(tag) {
  const options = SIZE_OPTIONS[tag] || SIZE_OPTIONS["estructurada"];
  if (!sizeOptionsContainer) return;
  sizeOptionsContainer.innerHTML = "";

  options.forEach((val) => {
    const label = document.createElement("label");
    label.className = "flex flex-col items-center cursor-pointer";

    const input = document.createElement("input");
    input.type = "radio";
    input.name = "option_size_scale";
    input.value = String(val);
    input.className = "radio radio-lg checked:bg-pink-500";

    const span = document.createElement("span");
    span.className = "mt-2 text-xl text-gray-700 font-medium";
    span.textContent = String(val);

    label.appendChild(input);
    label.appendChild(span);
    sizeOptionsContainer.appendChild(label);
  });

  const firstRadioSize = document
    .getElementsByName("option_size_scale")
    .item(0);
  firstRadioSize.checked = true;
}

function showDescriptionStyle(label) {
  const text = label.textContent.trim();
  helpStyle.textContent = descriptons[text];
}

function showDescriptionTamanoScale(label) {
  const text = label.textContent.trim();
  let parent = inputTamano.parentElement;
  parent.getElementsByTagName("p")[0].textContent = descriptons[text];
}
