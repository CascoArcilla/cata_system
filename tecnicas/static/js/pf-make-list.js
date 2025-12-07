const FORM_DESCRIBE = document.querySelector(".cts-form-pf-word");
const BOX_WORDS = document.querySelector(".cts-box-words");
const IMG_LIST = document.querySelector(".cts-img-list");
const ERROR_INPUT_WORD = document.querySelector(".error-input-word");
const FORM_ACTION = document.querySelector(".form-actions");

const WORDS = [];
const STYLES_LI = [
  "cts-item-words",
  "bg-gray-400",
  "text-black",
  "rounded",
  "font-bold",
  "text-lg",
  "px-4",
  "py-3",
  "flex",
  "flex-wrap",
  "flex-row",
  "flex-1",
  "min-w-fit",
  "justify-center",
  "items-center",
  "gap-3",
];

const STYLES_BTN = [
  "cts-remove-word",
  "px-4",
  "border-b-2",
  "active:border-b-0",
  "active:border-t-2",
  "transition-all",
  "rounded-xl",
  "font-black",
  "w-fit",
  "capitalize",
  "active:border-red-500",
  "border-red-800",
  "bg-red-500",
];

const itemWord = (wordName, index) => {
  const btn = document.createElement("button");
  btn.setAttribute("data-index", index);
  btn.classList.add(...STYLES_BTN);
  btn.textContent = "➖";

  const ph = document.createElement("p");
  ph.classList.add("ct-word-received");
  ph.textContent = wordName;

  const li = document.createElement("li");
  li.setAttribute("id", `word-${index}`);
  li.classList.add(...STYLES_LI);

  li.appendChild(ph);
  li.appendChild(btn);

  return li;
};

function initWordsFromBox() {
  if (!BOX_WORDS) return;
  const current_words = BOX_WORDS.querySelectorAll(".cts-item-words");
  if (!current_words.length) return;

  WORDS.length = 0;
  current_words.forEach((li) => {
    const p = li.querySelector(".ct-word-received");
    const text = p ? p.textContent.trim() : li.textContent.trim();
    if (text) WORDS.push(text);
  });
  renderWords();
}

function renderWords() {
  if (!BOX_WORDS) return;
  if (!WORDS.length) {
    BOX_WORDS.innerHTML = "";
    IMG_LIST.classList.remove("hidden");
    BOX_WORDS.appendChild(IMG_LIST);
    return;
  }

  BOX_WORDS.innerHTML = "";
  WORDS.forEach((word, index) => {
    let liElement = itemWord(word, index);
    BOX_WORDS.appendChild(liElement);
  });

  const removeButtons = BOX_WORDS.querySelectorAll("button.cts-remove-word");
  removeButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const idx = parseInt(btn.dataset.index);
      if (!Number.isNaN(idx)) {
        WORDS.splice(idx, 1);
        renderWords();
      }
    });
  });
}

function setupDescribeFormToAddWord() {
  if (!FORM_DESCRIBE) return;
  FORM_DESCRIBE.addEventListener("submit", (e) => {
    e.preventDefault();

    if (!FORM_DESCRIBE.reportValidity()) {
      return;
    }

    const input = FORM_DESCRIBE.querySelector('input[type="text"]');
    if (!input) return;

    const value = input.value.trim();
    if (!value) return;

    if (WORDS.includes(value)) {
      spanNotifaction("Esa palabra ya está en la lista");
      return;
    }

    WORDS.push(value);
    renderWords();

    input.value = "";
    input.focus();
  });
}

function spanNotifaction(messageError, isError = true) {
  const span = document.createElement("span");
  span.textContent = messageError;

  const div = document.createElement("div");
  div.classList.add("alert", isError ? "alert-error" : "alert-success");
  div.appendChild(span);

  ERROR_INPUT_WORD.append(div);

  setTimeout(() => {
    ERROR_INPUT_WORD.removeChild(div);
  }, 3000);
}

async function sendWordsToSave() {
  if (!WORDS.length) {
    spanNotifaction("Debe existir al menos una palabra en la lista");
    return false;
  }

  const currentPhase = parseInt(
    document.querySelector(".cts-phase-pf").dataset.phase
  );

  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  const requestData = {
    phase: currentPhase,
    words: WORDS,
  };

  const URL = "/cata/testers/api/ratingword/pf/list";

  try {
    const response = await fetch(URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify(requestData),
    });

    if (!response.ok) {
      spanNotifaction("Fallo con la respuesta recibida");
      return false;
    }

    const result = await response.json();

    const messError = result.error;

    if (messError) {
      spanNotifaction(messError);
      return false;
    }

    spanNotifaction(result.message, false);
    const addedWords = result.words;
    WORDS.length = 0;
    addedWords.forEach((word) => WORDS.push(word));
    renderWords();
    return true;
  } catch (err) {
    console.error(err);
    spanNotifaction("Error en la respuesta del servidor");
    return false;
  }
}

async function setUpFormAction() {
  const saveWords = await sendWordsToSave();
  if (!saveWords) {
    return false;
  }

  const input = FORM_ACTION.querySelector(".action-input");
  FORM_ACTION.action = "";
  input.value = "finish_session";
  FORM_ACTION.submit();
}

window.addEventListener("DOMContentLoaded", async () => {
  initWordsFromBox();
  setupDescribeFormToAddWord();

  const currentPhase = parseInt(
    document.querySelector(".cts-phase-pf").dataset.phase
  );

  if (currentPhase == 2) await sendWordsToSave();
  if (document.querySelector(".cts-content-list-words"))
    await getListWordsTesters();
});
