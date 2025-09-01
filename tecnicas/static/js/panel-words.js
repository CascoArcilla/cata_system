// **************************************
// Logic for get to words and render UI
// **************************************
const imgList = document.querySelector(".ct-img-list");

const listWordsSelect = [];
const wordsSelectContainer = document.querySelector(".ct-palabras-usadas");

const errorp = document.getElementsByClassName("ct-error-words")[0];
const foundWordsContainer = document.getElementsByClassName(
  "ct-palabras-encontradas"
)[0];

const formSearch = document.getElementsByClassName("ct-serach-words")[0];
formSearch.addEventListener("submit", getWordsByName);

async function getWordsByName(e) {
  e.preventDefault();
  errorp.classList.add("hidden");
  foundWordsContainer.innerHTML = "";

  let words = [];

  const dataForm = new FormData(this);
  const params = new URLSearchParams({
    palabra: dataForm.get("search").trim(),
  });

  const url = `api/palabras?${params}`;

  try {
    const respone = await fetch(url, {
      method: "GET",
      headers: {
        "X-CSRFToken": dataForm.get("csrfmiddlewaretoken"),
      },
    });

    const jsonResponse = await respone.json();

    if (jsonResponse.error) {
      errorp.textContent = `Error: ${jsonResponse.error}`;
      errorp.classList.remove("hidden");
      return;
    }

    words = jsonResponse["data"];
  } catch (error) {
    console.log("Error:", error);
  }

  showWordsFound(words);
}

function createWordElement({ word, add = true, callback = null }) {
  const li = document.createElement("li");
  li.classList.add(
    add ? "bg-gray-600" : "bg-gray-400",
    add ? "text-white" : "text-black",
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
    "gap-3"
  );

  const pName = document.createElement("p");
  pName.textContent = word.nombre_palabra;
  pName.id = word.id;

  let callButton;

  if (callback) {
    callButton = () => callback(word);
  }

  li.appendChild(pName);
  li.appendChild(createButton(add, callButton));

  return li;
}

function createButton(add = true, callback = null) {
  const button = document.createElement("button");
  button.textContent = add ? "➕" : "➖";
  button.classList.add(
    "px-4",
    "border-b-2",
    "active:border-b-0",
    "active:border-t-2",
    "transition-all",
    "rounded-xl",
    "font-black",
    "w-fit",
    "capitalize"
  );

  button.classList.add(
    add ? "active:border-green-500" : "active:border-red-500",
    add ? "border-green-800" : "border-red-800",
    add ? "bg-green-500" : "bg-red-500"
  );

  if (callback) {
    button.addEventListener("click", callback);
  }

  return button;
}

function swtichGridSearch(change = true) {
  change
    ? foundWordsContainer.classList.add("grid")
    : foundWordsContainer.classList.remove("grid");
}

function showWordsFound(words) {
  foundWordsContainer.innerHTML = "";
  swtichGridSearch();

  words.forEach((word) => {
    const elemtnLi = createWordElement({ word: word, callback: addWordToUse });
    foundWordsContainer.appendChild(elemtnLi);
  });
}

function addWordToUse(word) {
  if (listWordsSelect.find((w) => w.id === word.id)) {
    spanNotificationRed(
      `La palabra "${word.nombre_palabra}" ya fue seleccionada`
    );

    return;
  }

  listWordsSelect.push(word);
  updatelistWordsSelect();
}

function spanNotificationRed(errorMessage) {
  const noti = document.querySelector(".ct-notification-red");
  noti.textContent = errorMessage;
  noti.classList.remove("hidden");

  setTimeout(() => {
    noti.classList.add("hidden");
  }, 2500);
}

function spanNotificationGreen(message) {
  const noti = document.querySelector(".ct-notification-green");
  noti.textContent = message;
  noti.classList.remove("hidden");

  setTimeout(() => {
    noti.classList.add("hidden");
  }, 3000);
}

function removeWordToUse(word) {
  const index = listWordsSelect.findIndex((w) => w.id === word.id);
  if (index > -1) {
    listWordsSelect.splice(index, 1);
    updatelistWordsSelect();
  }
}

function updatelistWordsSelect() {
  wordsSelectContainer.innerHTML = "";
  listWordsSelect.forEach((word) => {
    const elemtnLi = createWordElement({
      word: word,
      add: false,
      callback: removeWordToUse,
    });
    wordsSelectContainer.appendChild(elemtnLi);
  });

  if (listWordsSelect.length === 0) {
    wordsSelectContainer.appendChild(imgList);
  }
}

// **************************************
// Logic for post new Word
// **************************************
const formNewWord = document.querySelector(".ct-form-new-word");
formNewWord.addEventListener("submit", postNewWord);

async function postNewWord(e) {
  e.preventDefault();

  const dataForm = new FormData(this);
  const url = "api/palabras";

  dataForm.set(
    "nombre_palabra",
    dataForm.get("nombre_palabra").trim().toLowerCase()
  );

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
      spanNotificationRed(`Error: ${jsonResponse.error}`);
      return;
    }

    const word = jsonResponse["data"];
    addWordToUse(word);
    spanNotificationGreen(jsonResponse["message"]);

    formNewWord.reset();
  } catch (error) {
    spanNotificationRed(`Error: ${error}`);
  }
}
