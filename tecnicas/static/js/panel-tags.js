const itemsSelects = document.getElementsByClassName("ct-select-op");
const options = itemsSelects.item(0).getElementsByTagName("option");
const values = [];

const formNewTag = document.getElementsByClassName("ct-form-new-tag")[0];
if (formNewTag) {
  formNewTag.addEventListener("submit", postNewTag);
}

async function postNewTag(e) {
  e.preventDefault();

  const dataForm = new FormData(this);
  const url = "/cata/presenter/api/nueva-etiqueta";

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
      spanNotifaction(jsonResponse.error)
      return;
    }

    const inputTag = document.getElementsByName("nueva_etiqueta")[0];
    inputTag.value = "";

    const newTag = jsonResponse["new_tag"];
    addNewOptionToSelect(newTag);
    spanNotifaction("Etiqueta agregada correctamente", false)
  } catch (error) {
    spanNotifaction("Error en proceso de creación de etiqueta")
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
