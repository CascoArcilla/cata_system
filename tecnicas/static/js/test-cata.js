document.addEventListener("DOMContentLoaded", () => {
  const containFormData = document.querySelector(".words-check-container");

  const form = document.getElementById("wordsForm");
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const message = document.getElementById("response-message");

  const modalContent = document.getElementById("confirmModalContent");
  const confirmBtn = document.getElementById("confirmBtn");

  const URL = "/sensorial/testers/api/ratingword/cata";

  const checkboxes = form.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach((cb) => (cb.checked = false));

  let wordsData = [];

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const checkboxes = form.querySelectorAll('input[type="checkbox"]');
    wordsData = Array.from(checkboxes).map((cb) => ({
      id: parseInt(cb.dataset.wordId),
      word: cb.dataset.wordName,
      is_check: cb.checked,
    }));

    showModal(wordsData);
  });

  function showModal(words) {
    const checkedWords = words.filter((w) => w.is_check);
    const uncheckedWords = words.filter((w) => !w.is_check);

    modalContent.innerHTML = `
            <div class="bg-surface-general p-4 rounded-lg space-y-2">
                <p class="font-semibold text-green-600">Palabras seleccionadas:</p>
                <ul class="flex flex-wrap gap-2">
                    ${
                      checkedWords.length > 0
                        ? checkedWords
                            .map(
                              (w) =>
                                `<li class="bg-surface-sweet font-bold rounded p-2">${w.word}</li>`
                            )
                            .join("")
                        : '<li class="bg-surface-sweet font-bold rounded p-2 w-full text-center">Ninguna seleccionada</li>'
                    }
                </ul>
            </div>
            <div class="bg-surface-general p-4 rounded-lg space-y-2">
                <p class="font-semibold text-red-600">Palabras no seleccionadas:</p>
                <ul class="flex flex-wrap gap-2">
                    ${
                      uncheckedWords.length > 0
                        ? uncheckedWords
                            .map(
                              (w) =>
                                `<li class="bg-surface-sweet font-bold rounded p-2">${w.word}</li>`
                            )
                            .join("")
                        : '<li class="bg-surface-sweet font-bold rounded p-2 w-full text-center">Todas seleccionadas</li>'
                    }
                </ul>
            </div>
        `;
  }

  confirmBtn.addEventListener("click", async () => {
    const dataProduct = {
      id: parseInt(document.querySelector(".id-product").textContent),
      code: document.querySelector(".code-product").textContent,
    };

    try {
      const response = await fetch(URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
          "X-Requested-With": "XMLHttpRequest",
        },
        body: JSON.stringify({ words: wordsData, product: dataProduct }),
      });

      if (!response.ok) {
        message.textContent = "Error en la respuesta del servidor";
        message.classList.remove("hidden");
      }

      const result = await response.json();
      const messError = result.error;

      if (messError) {
        message.textContent = messError;
        return;
      }
      containFormData.innerHTML = `
            <section class="space-y-4">
                <h3 class="text-xl font-bold">
                    Exito al guardar
                </h3>
                <p class="text-sm italic">
                    ${result.message}
                </p>
                <button type="button" class="cts-btn-general cts-btn-primary btn-push" onclick="window.location.reload();">
                    Siguiente Producto
                </button>
            </section>
      `;
    } catch (err) {
      console.error(err);
      message.textContent = "Error en la respuesta del servidor";
      message.classList.remove("hidden");
    }
  });
});
