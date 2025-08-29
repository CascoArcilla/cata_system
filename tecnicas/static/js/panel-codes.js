let inWords = document
  .getElementsByClassName("ct-codes-form")[0]
  .getElementsByClassName("ct-code");
let codes = [];
let numCata = document.getElementsByClassName("ct-num-cata")[0].value;

let sortData;

initIU();

function submitData(e) {
  const codesInput = document.createElement("input");
  codesInput.type = "hidden";
  codesInput.name = "sort_codes";
  codesInput.value = JSON.stringify(sortData);
  this.appendChild(codesInput);
}

function initIU() {
  setCodes();
  definePermutations();
  addIUPermutations();

  const formWords = document.getElementsByClassName("ct-codes-form")[0];
  formWords.addEventListener("submit", submitData);
}

function setCodes() {
  if (codes) {
    codes = [];
  }
  for (let i = 0; i < inWords.length; i++) {
    codes.push(inWords.item(i).value.toUpperCase());
  }
}

function setPermutations() {
  definePermutations();
  addIUPermutations();
}

function definePermutations() {
  setCodes();
  const permutations = generatePermutations(codes);
  const newPer = shuffle(permutations);

  const usePermutations = [];
  let index = 0;

  while (true) {
    if (usePermutations.length == numCata) {
      break;
    } else if (index < newPer.length) {
      usePermutations.push(newPer[index]);
      index++;
    } else if (index >= newPer.length) {
      index = 0;
    }
  }

  const permutationsSort = [];

  usePermutations.forEach((permutation) => {
    let newValue = [];
    let index = 1;

    permutation.forEach((cod) => {
      newValue.push({
        code: cod,
        position: index,
      });

      index++;
    });

    permutationsSort.push(newValue);
  });

  sortData = permutationsSort.slice();
}

function generatePermutations(objetos) {
  var result = [];

  var backtrack = (index, objetos) => {
    if (index === objetos.length) {
      result.push(objetos.slice());
      return;
    }

    for (let j = index; j < objetos.length; j++) {
      [objetos[index], objetos[j]] = [objetos[j], objetos[index]];
      backtrack(index + 1, objetos);
      [objetos[index], objetos[j]] = [objetos[j], objetos[index]];
    }
  };

  backtrack(0, objetos);
  return result;
}

function shuffle(arr) {
  const arrSuffle = arr.slice();

  for (let i = arrSuffle.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arrSuffle[i], arrSuffle[j]] = [arrSuffle[j], arrSuffle[i]];
  }

  return arrSuffle;
}

function addIUPermutations() {
  const container = document.getElementsByClassName("ct-orden-list")[0];
  const itemsChild = [];
  container.replaceChildren();

  let index = 1;

  sortData.forEach((permuta) => {
    const paragraph = document.createElement("p");
    paragraph.classList.add("px-3", "font-bold", "text-xl", "text-black");
    paragraph.textContent = `orden ${index}`;

    const unlist = document.createElement("ul");
    unlist.classList.add(
      "flex",
      "flex-wrap",
      "gap-3",
      "px-3",
      "py-1",
      "text-white"
    );

    permuta.forEach((obj) => {
      const itemList = document.createElement("li");
      itemList.classList.add(
        "px-2",
        "bg-gray-600",
        "font-bold",
        "tracking-wide"
      );
      itemList.textContent = `${obj.position}: ${obj.code}`;
      unlist.appendChild(itemList);
    });

    const section = document.createElement("section");
    section.classList.add("bg-gray-400", "py-2");

    section.appendChild(paragraph);
    section.appendChild(unlist);

    container.appendChild(section);
    index++;
  });
}
