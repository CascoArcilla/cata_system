let dragged = null;

const productsPlaceHolder = `
    <p class="text-products text-center text-lg font-medium">
        Agrupación de productos
    </p>`;

const wordsPlaceHolder = `
    <p class="text-words text-center text-lg font-medium">
        Lista de atributos
    </p>`;

const products = document.querySelectorAll(".draggable");
const zonesDrop = document.querySelectorAll(".dropzone");

const DATA_GRUPS = {};

products.forEach(manageDragables);
zonesDrop.forEach(manageDropZone);


/*
////
//////
//////// Add new grups
//////
////
*/

function addNewGrup() {
    const container = document.getElementById("containers");
    const newGrup = document.createElement("section");
    const styles = "w-fit space-y-4 border rounded p-2 bg-surface-ligt";
    newGrup.classList.add(...styles.split(" "));

    const formWord = document.getElementById("form-word");
    const formWordClone = formWord.cloneNode(true);
    formWordClone.classList.remove("hidden");

    newGrup.innerHTML = `
        <div class="dropzone w-64 min-h-16 bg-surface-sweet rounded p-2 flex items-center justify-center flex-wrap gap-2">
            ${productsPlaceHolder}
        </div>
        ${formWordClone.outerHTML}
        <div
            class="words-container w-64 min-h-16 bg-surface-sweet rounded p-2 flex items-center justify-center flex-wrap gap-2">
            ${wordsPlaceHolder}
        </div>
        <div class="cts-container-question flex items-center justify-around gap-2">
            <button class="cts-question cts-btn-general-compress flex-1 cts-btn-fifthy btn-push">
                ¿Remover este grupo?
            </button>
            <button class="cts-remove cts-btn-general-compress flex-1 cts-btn-primary btn-push hidden">
                Remover
            </button>
            <button class="cts-no-remove cts-btn-general-compress flex-1 cts-btn-fourthy btn-push hidden">
                Conservar
            </button>
        </div>`;

    manageDropZone(newGrup.querySelector(".dropzone"));
    container.appendChild(newGrup);
}


/*
////
//////
//////// Manage products' drags and remove drags
//////
////
*/

/**
 * 
 * @param {HTMLElement} zone 
 */
function manageDropZone(zone) {
    /*
    ////
    ////// Trash Zone product
    ////
    */
    if (zone.classList.contains("trash-products")) {
        zone.addEventListener("dragover", (e) => e.preventDefault());

        zone.addEventListener("drop", (event) => {
            const codeDrag = dragged.dataset.code
            const oldParent = dragged.parentNode;
            const oldCodeZone = oldParent.getAttribute("id")

            if (oldParent.classList.contains("original-products")) {
                spanNotifaction("No puedes borrar este producto");
                return
            }

            dragged.remove()
            removeProduct(codeDrag, oldCodeZone)

            spanNotifaction("Producto removido del grupo", false);
            dragged = null

            if (oldParent.classList.contains("dropzone") && oldParent.children.length === 0) {
                oldParent.innerHTML = productsPlaceHolder;
            }
        })
        return
    }

    /*
    ////
    ////// Identificate grups and creata dinamic data
    ////
    */

    // Create id for grup
    const idZone = generateSimpleID()

    // Add products if there en the page
    const products = []
    const productsElements = zone.querySelectorAll(".draggable") || None;

    if (productsElements) {
        productsElements.forEach((proEle) => {
            products.push({
                id: proEle.dataset.idProduct,
                code: proEle.dataset.code
            })
        })
    }

    const parentZone = zone.parentNode;
    const wordsInGrup = parentZone.querySelectorAll(".item-word") || None

    // Add words if there en the page
    const words = []
    if (wordsInGrup) {
        wordsInGrup.forEach((wordElement) => {
            words.push(wordElement.textContent)
        })
    }

    DATA_GRUPS[idZone] = {
        products: products,
        words: words
    }

    /*
    ////
    ////// Drop Zone product
    ////
    */

    zone.setAttribute("id", idZone)
    zone.addEventListener("dragover", (e) => e.preventDefault());

    zone.addEventListener("drop", () => {
        const codeDrag = dragged.dataset.code
        const zoneCode = zone.getAttribute("id")

        // Check that new produck is not in currents products of the group
        const obj = DATA_GRUPS[zoneCode].products.find((product) => product.code == codeDrag)
        if (obj) {
            spanNotifaction("Ese producto ya está en el grupo");
            return
        }

        DATA_GRUPS[zoneCode].products.push({
            id: dragged.dataset.idProduct,
            code: dragged.dataset.code
        })

        const oldParent = dragged.parentNode;

        const p = zone.querySelector("p");
        if (p) {
            p.remove();
        }

        // Move original or clone product in zone
        if (oldParent.classList.contains("dropzone")) {
            zone.appendChild(dragged);
        } else {
            const clone = dragged.cloneNode(true);
            clone.classList.remove("opacity-50");
            manageDragables(clone);
            zone.appendChild(clone);
        }

        if (oldParent.classList.contains("dropzone")) {
            if (oldParent.children.length === 0) oldParent.innerHTML = productsPlaceHolder;
            const zoneCodeOld = oldParent.getAttribute("id")
            removeProduct(codeDrag, zoneCodeOld)
        }
    });

    // Add listeners to elements options and WordForm for the list words
    addListenersButtonQuestionGrup(zone.parentNode)
    manageFormWord(parentZone.querySelector("form"), parentZone.querySelector(".words-container"), idZone)

    if (DATA_GRUPS[idZone].words.length) {
        parentZone.querySelector(".words-container").innerHTML = "";
        DATA_GRUPS[idZone].words.forEach((word) => {
            const itemWord = getItemWord(word, idZone);
            parentZone.querySelector(".words-container").appendChild(itemWord);
        })
    }
}

/*
////
//////
//////// Management Drags and FormWord
//////
////
*/

/**
 * 
 * @param {HTMLElement} el 
 */
function manageDragables(el) {
    el.addEventListener("dragstart", () => {
        dragged = el;
        setTimeout(() => el.classList.add("opacity-50"), 0);
    });

    el.addEventListener("dragend", () => {
        dragged = null;
        el.classList.remove("opacity-50");
    });
}

/**
 * 
 * @param {HTMLFormElementt} form 
 * @param {HTMLElement} containerWords
 */
function manageFormWord(form, containerWords, codeGrup) {
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        if (!form.reportValidity()) {
            return;
        }

        const input = form.querySelector('input[type="text"]');

        if (!input) return;

        const name = input.value.trim().toLowerCase().replace(/\s+/g, '');
        if (!name) return;

        if (DATA_GRUPS[codeGrup].words.includes(name)) {
            input.value = "";
            input.focus();
            spanNotifaction("Esa palabra ya está en la lista");
            return;
        }

        DATA_GRUPS[codeGrup].words.push(name)
        const wordItem = getItemWord(name, codeGrup)

        const p = containerWords.querySelector("p");
        if (p) {
            p.remove();
        }

        containerWords.appendChild(wordItem)

        input.value = "";
        input.focus();
    });
}

/*
////
//////
//////// Management Drags and FormWord
//////
////
*/

/**
 * 
 * @param {HTMLElement} grup 
 */
function removeGrup(grup) {
    delete DATA_GRUPS[grup.querySelector(".dropzone").getAttribute("id")]
    grup.remove()
}

function removeWord(code, wordName) {
    const newWords = DATA_GRUPS[code].words.filter(word => word != wordName)
    DATA_GRUPS[code].words = newWords
    if (!newWords.length) {
        const containerWords = document.getElementById(code).parentNode.querySelector(".words-container")
        containerWords.innerHTML = wordsPlaceHolder;
    }
}

function removeProduct(codeProduct, codeZone) {
    const newProducts = DATA_GRUPS[codeZone].products.filter((product) => product.code != codeProduct)
    DATA_GRUPS[codeZone].products = newProducts
}

function getItemWord(wordName, code) {
    const STYLES_DIV = "cts-item-words bg-surface-ligt text-black rounded font-bold text-lg p-1 flex flex-wrap flex-row flex-1 min-w-fit justify-center items-center gap-3";
    const STYLES_BTN = "cts-remove-word cts-btn-general-compress px-2 cts-btn-fourthy"

    const btn = document.createElement("button");
    btn.setAttribute("data-code", code);
    btn.setAttribute("data-word", wordName);
    btn.classList.add(...STYLES_BTN.split(" "));
    btn.textContent = "➖";

    const span = document.createElement("span");
    span.classList.add("item-word");
    span.textContent = wordName;

    const div = document.createElement("div");
    div.setAttribute("id", `word-${code}-${wordName}`);
    div.classList.add(...STYLES_DIV.split(" "));

    div.appendChild(span);
    div.appendChild(btn);

    btn.addEventListener("click", (e) => {
        removeWord(code, wordName)
        div.remove()
    })

    return div;
};

/**
 * 
 * @param {HTMLElement} grupContainer 
 */
function addListenersButtonQuestionGrup(grupContainer) {
    // Function hidden question
    grupContainer.querySelector(".cts-question").addEventListener("click", (event) => {
        hiddenQuestionRemoveGroup(grupContainer)
    })

    // Function cancel remove
    grupContainer.querySelector(".cts-no-remove").addEventListener("click", (event) => {
        hiddenQuestionRemoveGroup(grupContainer, false)
    })

    // Function remove grup
    grupContainer.querySelector(".cts-remove").addEventListener("click", (event) => {
        removeGrup(grupContainer)
    })
}

/*
////
//////
//////// Management Options Save and remove groups
//////
////
*/

/**
 * 
 * @param {HTMLDivElement} container 
 * @param {boolean} hiddenQuestion 
 */
function hiddenQuestionRemoveGroup(container, hiddenQuestion = true) {
    const question = container.querySelector(".cts-question")
    const remove = container.querySelector(".cts-remove")
    const noRemove = container.querySelector(".cts-no-remove")


    if (hiddenQuestion) {
        question.classList.add("hidden")
        remove.classList.remove("hidden")
        noRemove.classList.remove("hidden")
    } else {
        question.classList.remove("hidden")
        remove.classList.add("hidden")
        noRemove.classList.add("hidden")
    }
}

function generateSimpleID() {
    const first = Date.now().toString(35);
    const second = Math.random().toString(36).slice(2);
    return first + second;
}

function showOptionsSave() {
    document.getElementById("question-save").classList.add("hidden");
    document.getElementById("finish-session").classList.remove("hidden");
    document.getElementById("cancel-save").classList.remove("hidden");
}

function showQuestionSave() {
    document.getElementById("question-save").classList.remove("hidden");
    document.getElementById("finish-session").classList.add("hidden");
    document.getElementById("cancel-save").classList.add("hidden");
}

document
    .getElementById("question-save")
    .addEventListener("click", showOptionsSave);

document
    .getElementById("cancel-save")
    .addEventListener("click", showQuestionSave);

/*
////
//////
//////// Save data
//////
////
*/

async function saveData() {
    const keysDataGrups = Object.keys(DATA_GRUPS);
    const allCodesProducts = new Set()

    products.forEach((productElement) => {
        allCodesProducts.add(productElement.getAttribute("data-code"))
    })

    if (keysDataGrups.length === 0) {
        spanNotifaction("No hay grupos para guardar")
        return false;
    }

    const data = []
    let thereError = false;
    const codesProducts = []

    keysDataGrups.forEach((key) => {
        if (thereError) return

        const dataGrup = DATA_GRUPS[key];
        if (!dataGrup) {
            spanNotifaction("No hay datos para guardar")
            thereError = true;
            return
        }

        if (dataGrup.products.length === 0) {
            spanNotifaction("Los grupos deben tener por lo menos un producto para guardar")
            thereError = true;
            return
        }

        if (dataGrup.words.length === 0) {
            spanNotifaction("Los grupos deben tener por lo menos una palabra para guardar")
            thereError = true;
            return
        }

        const words = dataGrup.words;
        const products = dataGrup.products;

        codesProducts.push(...products.map((product) => product.code))

        data.push({
            words,
            products
        })
    })

    if (thereError) return false;

    const currentCodesProducts = new Set(codesProducts)
    const difference = symmetricDifference(currentCodesProducts, allCodesProducts)

    if (difference.size > 0) {
        spanNotifaction("Falta un producto que debe ser ordenado")
        return false
    }

    const URL = "/sensorial/testers/api/rating-sort"
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        const response = await fetch(URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify(data),
        })

        if (!response.ok) {
            spanNotifaction("Error en la respuesta del servidor")
            return false;
        }

        const result = await response.json()

        if (result.error) {
            spanNotifaction(result.error)
            return false
        } else {
            spanNotifaction(result.message, false)
            return true
        }
    } catch (error) {
        spanNotifaction("Error en proceso de guardar los datos")
        return false
    }
}

const buttonSaveData = document.getElementById("save-progress")
buttonSaveData.addEventListener("click", saveData)

function symmetricDifference(setA, setB) {
    let _difference = new Set(setA);
    for (let elem of setB) {
        if (_difference.has(elem)) {
            _difference.delete(elem);
        } else {
            _difference.add(elem);
        }
    }
    return _difference;
}

/*
////
//////
//////// Finish session
//////
////
*/

document
    .getElementById("finish-session")
    .addEventListener("click", finishSession);

async function finishSession() {
    const save = await saveData();
    if (!save) {
        spanNotifaction("Error al guardar los datos")
        return
    };

    const FORM_ACTION = document.querySelector(".form-actions")

    const inputAction = FORM_ACTION.querySelector(".action-input");
    FORM_ACTION.action = "";
    inputAction.value = "finish_session";
    FORM_ACTION.submit();
}