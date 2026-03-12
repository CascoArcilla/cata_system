// **************************************
// Create Vocabulary
// **************************************
async function submitSelectWords(classNanmeForm) {
  const form = document.querySelector(`.${classNanmeForm}`);

  const name_vocabulary = form.querySelector(".cts-name-voca").value;
  if (!name_vocabulary || name_vocabulary == "") {
    spanNotifaction("Se requiere el nombre del vocabulario", true);
    return;
  }

  if (listWordsSelect.length === 0) {
    spanNotifaction("Debe seleccionar al menos un atributo", true);
    return;
  }

  const wordsInput = document.createElement("input");
  wordsInput.type = "hidden";
  wordsInput.name = "words";
  wordsInput.value = JSON.stringify(listWordsSelect);

  form.appendChild(wordsInput);

  form.submit();
}
