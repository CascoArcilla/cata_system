async function getListWordsTesters() {
  const URL = "/sensorial/testers/api/ratingword/pf/list";
  try {
    const response = await fetch(URL, {
      method: "GET",
    });

    if (!response.ok) {
      spanNotifaction("Fallo con la respuesta recibida");
      return false;
    }

    const result = await response.json();
    const messError = result.error;
    if (messError) {
      spanNotifaction(messError);
      const containerWords = document.querySelector(".cts-content-list-words");
      containerWords.innerHTML = `
            <p class="bg-surface-sweet font-bold text-center text-lg px-4 pt-2 pb-3 rounded w-full max-sm:mx-2">
                ${messError}
            </p>`;
      return false;
    }
    spanNotifaction(result.message, false);
    const containerWords = document.querySelector(".cts-content-list-words");
    containerWords.innerHTML = "";

    const listWordsTesters = result.lists_words;

    listWordsTesters.forEach((listTester) => {
      const username = listTester.username;
      const words = listTester.words;
      const status = listTester.status;
      const listDiv = createListWords(username, words, status);
      containerWords.appendChild(listDiv);
    });

    return true;
  } catch (error) {
    console.error(error);
    spanNotifaction("Error del servidor con la API");
    return false;
  }
}

function createListWords(username, words, status = "indefinido") {
  const div = document.createElement("div");
  const paragraph = document.createElement("p");
  const paragraphStatus = document.createElement("p");
  const ul = document.createElement("ul");

  div.classList.add(
    "cts-item-list-tester",
    "bg-surface-sweet",
    "px-4",
    "pt-2",
    "pb-3",
    "rounded",
    "shrink-0",
    "w-64",
    "space-y-2"
  );

  paragraph.classList.add(
    "bg-surface-card",
    "text-lg",
    "font-semibold",
    "text-center",
    "rounded"
  );

  paragraphStatus.classList.add(
    "bg-surface-card",
    "text-lg",
    "font-semibold",
    "text-center",
    "rounded"
  );

  paragraph.textContent = username;
  paragraphStatus.textContent = status;

  ul.classList.add("text-center", "grid", "grid-cols-2", "gap-2", "w-full");

  words.forEach((word) => {
    const li = document.createElement("li");
    li.classList.add(
      "bg-surface-ligt",
      "rounded",
      "font-bold",
      "py-1",
      "px-2",
      "break-words"
    );
    li.textContent = word.nombre_palabra;
    ul.appendChild(li);
  });

  div.appendChild(paragraph);
  div.appendChild(paragraphStatus);
  div.appendChild(ul);
  return div;
}
