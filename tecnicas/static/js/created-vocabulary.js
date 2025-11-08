// **************************************
// Create Vocabulary
// **************************************
async function submitSelectWords(classNanmeForm, update = false) {
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

  const [isUpdata, orinalName] = inputIsUpdateVocabulary(update);

  form.appendChild(wordsInput);
  form.appendChild(isUpdata);
  if (orinalName) form.appendChild(orinalName);

  form.submit();
}

function inputIsUpdateVocabulary(is_update = false) {
  const isUpdata = document.createElement("input");
  isUpdata.type = "hidden";
  isUpdata.name = "is_update";
  isUpdata.value = is_update;

  if (is_update) {
    const orinalName = document.querySelector(".cts-original-name").textContent;
    const inputName = document.createElement("input");
    inputName.type = "hidden";
    inputName.name = "original_name";
    inputName.value = orinalName;
    return [isUpdata, inputName];
  }

  return [isUpdata, is_update];
}
