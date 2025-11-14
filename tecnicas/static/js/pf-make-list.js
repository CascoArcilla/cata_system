const FORM_DESCRIBE = document.querySelector(".cts-form-pf-word");
const BOX_WORDS = document.querySelector(".cts-box-words");
const IMG_LIST = document.querySelector(".cts-img-list");
const ERROR_INPUT_WORD = document.querySelector(".error-input-word");

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
      notifactionError("Esa palabra ya está en la lista");
      return;
    }

    WORDS.push(value);
    renderWords();

    input.value = "";
    input.focus();
  });
}

function notifactionError(messageError) {
  ERROR_INPUT_WORD.textContent = messageError;
  ERROR_INPUT_WORD.classList.remove("hidden");
  setTimeout(() => {
    ERROR_INPUT_WORD.textContent = "";
    ERROR_INPUT_WORD.classList.add("hidden");
  }, 3000);
}

window.addEventListener("DOMContentLoaded", () => {
  initWordsFromBox();
  setupDescribeFormToAddWord();
});
