const descriptons = {
  atributos:
    "Con el estilo atributos elijes las palabras para evaluar los productos",
  vocabulario:
    "Los vocabularios son un conjunto de palabras específicas para evaluar aspectos de un producto",
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
