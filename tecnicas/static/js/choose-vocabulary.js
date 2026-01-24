document.addEventListener("DOMContentLoaded", () => {
  const vocabSelect = document.getElementById("vocabulario");
  const wordsList = document.getElementById("palabras-lista");
  const formNextStep = document.getElementById("cts-create-session");
  let vocabularyId = "";

  vocabSelect.addEventListener("change", async (e) => {
    const vocabId = e.target.value;
    vocabularyId = vocabId;

    wordsList.innerHTML = `
    <li
        class="text-center font-bold tracking-wide text-xl bg-surface-card px-3 py-3 pb-4 rounded w-full">
        Cargando...
    </li>`;

    if (!vocabId) {
      wordsList.innerHTML = `
      <li
        class="text-center font-bold tracking-wide text-xl bg-surface-card px-3 py-3 pb-4 rounded w-full">
        Selecciona un vocabulario para ver sus palabras
      </li>`
      return;
    }

    url_fetch = `api/vocabulario/${vocabId}/palabras`;

    try {
      const response = await fetch(url_fetch, { method: "GET" });
      if (!response.ok) throw new Error("Error en la petición");
      const json_response = await response.json();

      words = json_response.data.words;

      if (words === 0) {
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

  formNextStep.addEventListener("submit", (e) => {
    if (!vocabularyId) {
      e.preventDefault();
      wordsList.innerHTML = `
      <li
        class="text-center font-bold tracking-wide text-xl bg-surface-card px-3 py-3 pb-4 rounded w-full">
        Selecciona un vocabulario para ver sus palabras
      </li>`
      return;
    }

    const useVocabulary = document.createElement("input");
    useVocabulary.type = "hidden";
    useVocabulary.name = "vocabulario";
    useVocabulary.value = vocabularyId;

    formNextStep.appendChild(useVocabulary);
  });
});
