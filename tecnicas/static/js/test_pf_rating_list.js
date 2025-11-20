let dragged = null;
const nextProduct = `
<h2 class="text-2xl font-bold text-center">Éxito al guardar los datos</h2>
<div class="flex justify-center">
  <button class="cts-btn-general cts-btn-primary btn-push" onclick="window.location.reload()">
      Evaluar siguiente atributo
  </button>
</div>`;

document.querySelectorAll(".draggable").forEach((el) => {
  el.addEventListener("dragstart", () => {
    dragged = el;
    setTimeout(() => el.classList.add("opacity-50"), 0);
  });

  el.addEventListener("dragend", () => {
    dragged = null;
    el.classList.remove("opacity-50");
  });
});

document.querySelectorAll(".dropzone").forEach((zone) => {
  zone.addEventListener("dragover", (e) => e.preventDefault());

  zone.addEventListener("drop", () => {
    zone.appendChild(dragged);
  });
});

document
  .getElementById("question-save")
  .addEventListener("click", showOptionsSave);

document
  .getElementById("cancel-save")
  .addEventListener("click", showQuestionSave);

document.getElementById("save-data").addEventListener("click", async () => {
  showLoading();
  const currentDataRatend = [];

  document.querySelectorAll(".dropzone").forEach((zone) => {
    const index = parseInt(zone.dataset.index);
    const children = zone.querySelectorAll(".draggable");

    children.forEach((el) => {
      currentDataRatend.push({
        name: el.dataset.code,
        container: index,
      });
    });
  });

  if (!currentDataRatend.length) {
    cancelLoading();
    spanNotifaction("No has ordenado los productos");
  } else if (
    currentDataRatend.length != document.querySelectorAll(".draggable").length
  ) {
    cancelLoading();
    spanNotifaction("Faltan productos por calificar");
  } else {
    saveData(currentDataRatend);
  }
});

async function saveData(dataToSend = []) {
  const URL = "/cata/testers/api/ratingword/pf/list";

  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  const requestData = {
    phase: parseInt(document.querySelector(".cts-phase-pf").dataset.phase),
    word: document.querySelector(".cts-phase-pf").dataset.nameWord,
    data: dataToSend,
  };

  console.log(requestData);

  try {
    // const response = await fetch(URL, {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //     "X-CSRFToken": csrfToken,
    //     "X-Requested-With": "XMLHttpRequest",
    //   },
    //   body: JSON.stringify(requestData),
    // });

    // if (!response.ok) {
    //   spanNotifaction("Fallo con la respuesta recibida");
    //   cancelLoading();
    //   return false;
    // }

    // const result = await response.json();

    // const messError = result.error;

    // if (messError) {
    //   spanNotifaction(messError);
    //   cancelLoading();
    //   return false;
    // }

    // spanNotifaction(result.message, false);
    const containerRatings = document.querySelector(".container-rating-word");
    containerRatings.innerHTML = "";
    containerRatings.innerHTML = nextProduct;
    cancelLoading();
    return true;
  } catch (error) {
    console.log(error);
    cancelLoading();
    spanNotifaction("¡Oh! Ocurrió un error al tratar de guardar los datos");
    return false;
  }
}

function showLoading() {
  document.getElementById("save-data").classList.add("hidden");
  document.getElementById("cancel-save").classList.add("hidden");
  document.getElementById("loading-data-save").classList.remove("hidden");
}

function cancelLoading() {
  document.getElementById("loading-data-save").classList.add("hidden");
  document.getElementById("question-save").classList.remove("hidden");
}

function showOptionsSave() {
  document.getElementById("question-save").classList.add("hidden");
  document.getElementById("save-data").classList.remove("hidden");
  document.getElementById("cancel-save").classList.remove("hidden");
}

function showQuestionSave() {
  document.getElementById("question-save").classList.remove("hidden");
  document.getElementById("save-data").classList.add("hidden");
  document.getElementById("cancel-save").classList.add("hidden");
}
