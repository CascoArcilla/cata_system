const descriptons = {
  estructurada: ["Establece número de segmentos:", "Puede ser 5, 7 o 9"],
  continua: ["Establece la longitud de la escala:", "Puede ser 9, 12 o 15"],
};

let labels;

let pSize;
let iSize;

initPanel();

function initPanel() {
  initRadios();
}

function initRadios() {
  labels = document.getElementsByClassName("ct-radio-escala");
  pSize = document
    .getElementsByClassName("ct-size-scale")
    .item(0)
    .getElementsByTagName("p")[0];
  iSize = document
    .getElementsByClassName("ct-size-scale")
    .item(0)
    .getElementsByTagName("input")[0];

  pSize.textContent = descriptons["estructurada"][0];
  iSize.placeholder = descriptons["estructurada"][1];

  for (let i = 0; i < labels.length; i++) {
    labels
      .item(i)
      .getElementsByTagName("input")[0]
      .addEventListener("change", () => {
        showDescriptionTamanoScale(labels.item(i));
      });
  }
}

function showDescriptionTamanoScale(label) {
  const text = label.textContent.trim();
  pSize.textContent = descriptons[text][0];
  iSize.placeholder = descriptons[text][1];
}