const selectWordsContainer = document.querySelector(".ct-words-select");
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
