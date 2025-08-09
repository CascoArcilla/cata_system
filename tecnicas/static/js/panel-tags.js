const itemsSelects = document.getElementsByClassName("ct-select-op");
const options = itemsSelects.item(0).getElementsByTagName("option");
const values = [];

const extraPanel = document.getElementsByClassName("ct-new-tags")[0];
function showHiddeExtraTags() {
  if (extraPanel.classList.contains("hidden")) {
    extraPanel.classList.remove("hidden");
  } else {
    extraPanel.classList.add("hidden");
  }
}

const formNewTag = document.getElementsByClassName("ct-form-new-tag")[0];
if (formNewTag) {
  formNewTag.addEventListener("submit", postNewTag);
}

async function postNewTag(e) {
  e.preventDefault();

  const dataForm = new FormData(this);
  const url = "/cata/nueva-etiqueta";

  try {
    const respone = await fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": dataForm.get("csrfmiddlewaretoken"),
      },
      body: dataForm,
    });

    const jsonResponse = await respone.json();

    if (jsonResponse.error) {
      const errorp = document.getElementsByClassName("ct-error-tag")[0];
      errorp.textContent = `error: ${jsonResponse.error}`;
      errorp.classList.remove("hidden");
      return;
    }

    const inputTag = document.getElementsByName("nueva_etiqueta")[0];
    inputTag.value = "";
    showHiddeExtraTags();

    const newTag = jsonResponse["new_tag"];
    addNewOptionToSelect(newTag);
  } catch (error) {
    console.log("Error:", error);
  }
}

function createOptionSelect(value = 0, text = "define texto") {
  const option = document.createElement("option");
  option.value = value;
  option.textContent = text;
  return option;
}

function addNewOptionToSelect(newValues) {
  for (let i = 0; i < itemsSelects.length; i++) {
    const newOption = createOptionSelect(newValues.id, newValues.valor);
    itemsSelects.item(i).appendChild(newOption);
  }
}
