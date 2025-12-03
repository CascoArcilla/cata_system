// Store words: { "CODE": ["word1", "word2"] }
const productWords = {};
if (window.isUltraFlash) {
    initUltraFlash(productWords);
}

function initUltraFlash(productWords) {
    const continueBtn = document.getElementById('continue-description');
    const questionSaveBtn = document.getElementById('question-save');
    const saveProgressBtn = document.getElementById('save-progress');
    const dialog = document.getElementById('word-dialog');
    const wordForm = document.getElementById('word-form');
    const wordInput = document.getElementById('word-input');
    const wordList = document.getElementById('word-list');
    const dialogProductCode = document.getElementById('dialog-product-code');

    let isDescriptionPhase = false;
    let currentProductCode = null;

    const points = document.querySelectorAll('.data-point');
    let hasExistingWords = false;

    // Check if there are existing words
    points.forEach(point => {
        const code = point.dataset.code;
        const wordsAttr = point.dataset.words;

        if (wordsAttr) {
            productWords[code] = wordsAttr.split(',').filter(w => w);
            hasExistingWords = true;
        }
    });

    if (hasExistingWords) {
        startDescriptionPhase();
        points.forEach(point => {
            const code = point.dataset.code;
            updatePointLabel(code);
            console.log(productWords[code]);
        });
    } else {
        continueBtn.classList.remove('hidden');
    }

    // Check if all products are placed
    continueBtn.addEventListener('click', () => {
        const placedCount = Object.keys(window.placedPoints).length;
        const totalProducts = document.querySelectorAll('.item-product').length;

        if (placedCount !== totalProducts) {
            spanNotifaction("Por favor, coloca todos los productos antes de continuar.");
            return;
        }

        startDescriptionPhase();
    });

    function startDescriptionPhase() {
        isDescriptionPhase = true;
        window.isPlacementActive = false;
        continueBtn.classList.add('hidden');
        document.getElementById("question-save").classList.remove("hidden");

        spanNotifaction("Fase de descripción: Haz clic en un punto para agregar palabras.", false);

        document.getElementById('napping-plane').classList.remove('cursor-crosshair');
        document.getElementById('napping-plane').classList.add('cursor-default');
        document.querySelectorAll('.item-product').forEach(p => p.classList.remove('ring-4', 'ring-primary'))
    }

    // Handle Point Click for Description
    // We need to attach this to the plane or points.
    // Since points are re-rendered, delegating to plane is better, or hooking into renderPoint.
    // But renderPoint is in the other file.
    // Let's use event delegation on the plane, but we need to catch the click on the point.

    document.getElementById('napping-plane').addEventListener('click', (e) => {
        if (!isDescriptionPhase) return;

        const point = e.target.closest('.data-point');

        if (point) {
            e.stopPropagation();
            openWordDialog(point.dataset.code);
        }
    });

    function openWordDialog(code) {
        currentProductCode = code;
        dialogProductCode.innerText = code;
        renderWordListInDialog();
        dialog.showModal();
    }

    function renderWordListInDialog() {
        wordList.innerHTML = '';
        const words = productWords[currentProductCode] || [];

        words.forEach((word, index) => {
            const badge = document.createElement('div');
            badge.className = 'badge badge-secondary gap-2 p-3';
            badge.innerHTML = `
                ${word}
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-4 h-4 stroke-current cursor-pointer remove-word" data-index="${index}"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            `;

            badge.querySelector('.remove-word').addEventListener('click', () => {
                removeWord(index);
            });

            wordList.appendChild(badge);
        });

        // Update visualization on the plane
        updatePointLabel(currentProductCode);
    }

    function addWord(word) {
        if (!productWords[currentProductCode]) {
            productWords[currentProductCode] = [];
        }

        if (productWords[currentProductCode].length >= 5) {
            spanNotifaction("Máximo 5 palabras por producto.");
            return;
        }

        if (productWords[currentProductCode].includes(word)) {
            spanNotifaction("Palabra duplicada");
            return;
        }

        productWords[currentProductCode].push(word);
        renderWordListInDialog();
    }

    function removeWord(index) {
        if (productWords[currentProductCode]) {
            productWords[currentProductCode].splice(index, 1);
            renderWordListInDialog();
        }
    }

    wordForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const word = wordInput.value.trim();
        if (word) {
            addWord(word);
            wordInput.value = '';
            wordInput.focus();
        }
    });

    function updatePointLabel(code) {
        const point = document.getElementById(`point-${code}`);
        if (!point) return;

        // Find or create the words container below the point
        const tooltip = point.querySelector('.group-hover\\:block');
        if (tooltip) {
            // Rebuild tooltip content
            const xVal = parseFloat(point.dataset.px).toFixed(1);
            const yVal = parseFloat(point.dataset.py).toFixed(1);
            const words = productWords[code] || [];

            let wordsHtml = '';
            if (words.length > 0) {
                wordsHtml = `<div class="mt-1 pt-1 border-t border-gray-600 text-yellow-300 italic">${words.join(', ')}</div>`;
            }

            tooltip.innerHTML = `
                <strong>${code}</strong><br>
                X: ${xVal}<br>
                Y: ${yVal}
                ${wordsHtml}
            `;
        }
    }

    // Override saveData to include words
    // We need to hook into the existing saveData or replace it.
    // Since we made saveData global, we can wrap it.

    const originalSaveData = window.saveData;

    window.saveData = async function () {
        // If in description phase, validate words
        if (isDescriptionPhase) {
            const codes = Object.keys(window.placedPoints);
            for (const code of codes) {
                const words = productWords[code] || [];
                if (words.length < 3) {
                    spanNotifaction(`El producto ${code} debe tener al menos 3 palabras.`);
                    return false;
                }
            }
        }

        // Prepare data
        const codeProducts = Object.keys(window.placedPoints);
        const data = [];

        if (document.querySelectorAll('.item-product').length != codeProducts.length) {
            spanNotifaction("Por favor, coloca todos los puntos")
            return false;
        }

        codeProducts.forEach((code) => {
            const point = window.placedPoints[code];
            const words = productWords[code] || [];

            const objData = {
                code: code,
                x: point.x,
                y: point.y,
                idProduct: point.id,
                words: words // Add words here
            };

            data.push(objData);
        })

        // We can reuse the rest of the logic, but we need to send the data.
        // The original function constructs data inside it. We can't easily inject data into it unless we rewrite it.
        // So I will rewrite the fetch part here.

        const URL = "/cata/testers/api/rating-napping/no-mode"
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
}
