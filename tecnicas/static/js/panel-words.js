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
    const noti = document.querySelector(".ct-notification-red");
    noti.textContent = `La palabra "${word.nombre_palabra}" ya fue seleccionada`;
    noti.classList.remove("hidden");

    setTimeout(() => {
      noti.classList.add("hidden");
    }, 1800);
    
    return;
  }

  listWordsSelect.push(word);
  updatelistWordsSelect();
}

function spanNotificationRed(params) {}

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

/*const selectWordsContainer = document.querySelector(".ct-words-select");
const tagsWords = document.querySelectorAll(".word");
let numberWords = 3;
const allWords = [];

for (let i = 0; i < tagsWords.length; i++) {
  let atributes = tagsWords.item(i).children;
  allWords.push({
    id: atributes[1].innerText,
    name: atributes[0].innerText,
    selected: false,
  });
}

for (let i = 1; i <= numberWords; i++) {
  const select = creadSelect(i);
  selectWordsContainer.appendChild(select);
}

function creadSelect(index) {
  const label = document.createElement("label");
  label.attributes["form"] = `palabra-${index}`;
  label.classList.add(
    "font-medium",
    "py-2",
    "px-3",
    "bg-gray-200",
    "capitalize",
    "rounded",
    "text-center"
  );

  const p = document.createElement("p");
  p.innerText = `Palabra ${index}`;

  const select = document.createElement("select");
  select.attributes["id"] = `palabra-${index}`;
  select.name = `palabra-${index}`;
  select.required = true;
  select.classList.add(
    "ct-select-op",
    "p-1",
    "rounded",
    "bg-gray-500",
    "[*]:capitalize",
    "[*]:text-white"
  );

  const emtpyOption = document.createElement("option");
  emtpyOption.value = "";
  emtpyOption.innerText = "Seleccione palabra";
  emtpyOption.attributes["selected"] = true;
  emtpyOption.attributes["disabled"] = true;

  select.appendChild(emtpyOption);

  allWords.forEach((dataWord, i) => {
    const option = document.createElement("option");
    option.value = dataWord.id;
    option.innerText = dataWord.name;
    select.appendChild(option);
  });

  label.appendChild(p);
  label.appendChild(select);

  return label;
}
*/
