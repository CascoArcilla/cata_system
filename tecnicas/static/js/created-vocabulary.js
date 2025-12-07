// **************************************
// Create Vocabulary
// **************************************
async function submitSelectWords(classNanmeForm) {
  const form = document.querySelector(`.${classNanmeForm}`);

  const name_vocabulary = form.querySelector(".cts-name-voca").value;
  if (!name_vocabulary || name_vocabulary == "") {
    spanNotificationRed("Se requiere el nombre del vocabulario");
    return;
  }

  if (listWordsSelect.length === 0) {
    spanNotificationRed("Debe seleccionar al menos una palabra");
    return;
  }

  const wordsInput = document.createElement("input");
  wordsInput.type = "hidden";
  wordsInput.name = "words";
  wordsInput.value = JSON.stringify(listWordsSelect);

  form.appendChild(wordsInput);

  form.submit();
}
