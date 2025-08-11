const descriptons = {
  estructurada: ["Establece número de segmentos:", "Puede ser 5, 7 o 9"],
  continua: ["Establece la longitud de la escala:", "Puede ser 9, 12 o 15"],
  atributos:
    "Con el estilo atributos elijes las palabras para evaluar los productos",
  vocabulario:
    "Los vocabularios son un conjunto de palabras especificas para evaluar aspectos de un producto.",
};

let inputsScale;
let inputTamano;

let inputsStyle;
let helpStyle;

initPanel();

function initPanel() {
  initRadios();
}

function initRadios() {
  inputsScale = document.getElementsByName("tipo_escala");
  inputTamano = document.getElementsByName("tamano_escala").item(0);

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

function showDescriptionStyle(label) {
  const text = label.textContent.trim();
  helpStyle.textContent = descriptons[text];
}

function showDescriptionTamanoScale(label) {
  const text = label.textContent.trim();
  let parent = inputTamano.parentElement;
  parent.getElementsByTagName("p").textContent = descriptons[text][0];
  inputTamano.placeholder = descriptons[text][1];
}