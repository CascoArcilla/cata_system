const descriptons = {
  atributos:
    "Tiene la finalidad de agregar atributos sensoriales que seran evaluadas para el producto de interes",
  vocabulario:
    "Los vocabularios se refieren a Emociones y Recuerdos. También puedes elejir los que hayas creado",
};

const helpStyleWords = document.querySelector(".cts-help-style-words");
let radiosStyleWords;

function initRadiosStyleWords() {
  radiosStyleWords = document.getElementsByName("estilo_palabras");
  console.log(radiosStyleWords);

  for (let index = 0; index < radiosStyleWords.length; index++) {
    const radio = radiosStyleWords[index];

    if (radio.checked) {
      const radioOption = radio.parentElement.textContent.trim();
      const textHelp = descriptons[radioOption];
      helpStyleWords.textContent = textHelp;
    }

    radio.parentElement.addEventListener("click", (e) => {
      const radioOption = radio.parentElement.textContent.trim();
      const textHelp = descriptons[radioOption];
      helpStyleWords.textContent = textHelp;
    });
  }
}

initRadiosStyleWords();
