document.addEventListener("DOMContentLoaded", () => {
  const vocabSelect = document.getElementById("vocabulario");
  const wordsList = document.getElementById("palabras-lista");
  const formNextStep = document.querySelector(".cts-create-session");

  const resetToDefault = () => {
    if (vocabSelect) {
      vocabSelect.value = "";
    }
    if (wordsList) {
      wordsList.innerHTML = `
        <li class="text-center font-bold tracking-wide text-xl bg-surface-card px-3 py-3 pb-4 rounded w-full">
            Selecciona un vocabulario para ver sus palabras
        </li>`;
    }
    const descContainer = document.getElementById("vocabulario-descripcion-container");
    if (descContainer) {
        descContainer.classList.add("hidden");
        document.getElementById("vocabulario-descripcion").textContent = "";
    }
  };

  window.addEventListener("pageshow", () => {
    resetToDefault();
  });

  resetToDefault();

  if (vocabSelect) {
    vocabSelect.addEventListener("change", async (e) => {
      const vocabularyId = e.target.value;

      wordsList.innerHTML = `
      <li class="text-center font-bold tracking-wide text-xl bg-surface-card px-3 py-3 pb-4 rounded w-full">
          Cargando...
      </li>`;

          
      const descContainer = document.getElementById("vocabulario-descripcion-container");
      const descText = document.getElementById("vocabulario-descripcion");

      if (!vocabularyId) {
        resetToDefault();
        if (descContainer) descContainer.classList.add("hidden");
        return;
      }

      const url_fetch = `api/vocabulario/${vocabularyId}/palabras`;

      try {
        const response = await fetch(url_fetch, { method: "GET" });
        if (!response.ok) throw new Error("Error en la petición");
        const json_response = await response.json();

        const data = json_response.data;
        const words = data.words;
        const description = data.descripcion;

        if (descContainer && descText) {
             descText.textContent = description || "Sin descripción disponible";
             descContainer.classList.remove("hidden");
        }

        if (words.length === 0) {
          wordsList.innerHTML =
            "<li class='text-center font-bold tracking-wide text-xl bg-surface-card px-3 py-3 pb-4 rounded w-full'>No hay palabras asociadas</li>";
          return;
        }

        wordsList.innerHTML = "";
        words.forEach((p) => {
          const li = document.createElement("li");
          li.textContent = p.nombre_palabra;
          li.className =
            "bg-surface-card text-black rounded font-bold text-lg px-4 py-3 capitalize";
          wordsList.appendChild(li);
        });
      } catch (err) {
        wordsList.innerHTML =
          "<li class='text-red-500 text-center text-lg'>Error al cargar las palabras</li>";
        console.error(err);
      }
    });
  }

  if (formNextStep) {
    formNextStep.addEventListener("submit", (e) => {
      const currentVocabularyId = vocabSelect ? vocabSelect.value : null;

      if (!currentVocabularyId) {
        e.preventDefault();
        wordsList.innerHTML = `
        <li class="text-center font-bold tracking-wide text-xl bg-surface-card px-3 py-3 pb-4 rounded w-full">
          Selecciona un vocabulario para ver sus palabras
        </li>`;
        return;
      }

      const existingInput = formNextStep.querySelector('input[name="vocabulario"]');
      if (existingInput) {
        existingInput.remove();
      }

      const useVocabulary = document.createElement("input");
      useVocabulary.type = "hidden";
      useVocabulary.name = "vocabulario";
      useVocabulary.value = currentVocabularyId;

      formNextStep.appendChild(useVocabulary);
    });
  }
});
