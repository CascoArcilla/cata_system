// Store words: { "CODE": ["word1", "word2"] }
const productWords = {};

// Only initialize ultra flash if the mode is active
if (window.isUltraFlash) {
    initUltraFlash();
}

function initUltraFlash() {
    const continueBtn = document.getElementById('continue-description');
    const questionSaveBtn = document.getElementById('question-save');
    const dialog = document.getElementById('word-dialog');
    const wordForm = document.getElementById('word-form');
    const wordInput = document.querySelector('.cts-input-list-word');
    const wordList = document.getElementById('word-list');
    const dialogProductCode = document.getElementById('dialog-product-code');

    let isDescriptionPhase = false;
    let currentProductCode = null;

    const points = document.querySelectorAll('.data-point');
    let hasExistingWords = false;

    wordInput.value = '';

    // Check if there are existing words from backend
    points.forEach(point => {
        const code = point.dataset.code;
        const wordsAttr = point.dataset.words;

        if (wordsAttr && wordsAttr.trim() !== '') {
            productWords[code] = wordsAttr.split(',').filter(w => w.trim() !== '');
            
            if (productWords[code].length >= 1) {
                hasExistingWords = true;
            }
        }
    });

    setTimeout(() => {
        if (hasExistingWords) {
            startDescriptionPhase();
            // Update all point labels to show existing words
            points.forEach(point => {
                const code = point.dataset.code;
                if (productWords[code] && productWords[code].length > 0) {
                    updatePointLabel(code);
                }
            });
        } else {
            // No existing words, show continue button for phase 1
            continueBtn.classList.remove('hidden');
        }
    }, 100);

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
        questionSaveBtn.classList.remove("hidden");
        spanNotifaction("Fase de descripción: Haz clic en un punto para agregar palabras.", false);

        const plane = document.getElementById('napping-plane');
        plane.classList.remove('cursor-crosshair');
        plane.classList.add('cursor-default');
        document.querySelectorAll('.item-product').forEach(p => {
            p.classList.remove('ring-4', 'ring-primary');
        });
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

        // No maximum limit on words

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

        const words = productWords[code] || [];

        // Remove existing tooltip if present
        let tooltip = point.querySelector('.cts-tooltip');

        if (tooltip) {
            tooltip.remove();
        }

        // Only create tooltip in description phase and if there are words
        if (isDescriptionPhase && words.length > 0) {
            tooltip = document.createElement('div');
            tooltip.className = 'cts-tooltip absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-800 text-white text-xs rounded z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none';

            // Display words in a 3-column grid (no coordinates)
            const wordBadges = words.map(w => `<span class="inline-block px-2 py-1 bg-yellow-600 text-white rounded text-xs">${w}</span>`).join('');
            tooltip.innerHTML = `
                <strong>${code}</strong>
                <div class="mt-2 pt-2 border-t border-gray-600" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; max-width: 300px;">
                    ${wordBadges}
                </div>
            `;

            // Add max-width to tooltip
            tooltip.style.maxWidth = '320px';
            tooltip.style.whiteSpace = 'normal';
            point.appendChild(tooltip);
        }
    }

    // Set up callbacks to extend the base saveData function
    // Validation callback - runs before saving
    window.beforeSaveData = function () {
        // If in description phase, validate words (minimum 1 per product)
        if (isDescriptionPhase) {
            const codeProducts = Object.keys(window.placedPoints);
            for (const code of codeProducts) {
                const words = productWords[code] || [];
                if (words.length < 1) {
                    spanNotifaction(`El producto ${code} debe tener al menos 1 palabra.`);
                    return false;
                }
            }
        }
        return true;
    };

    // Data extension callback - adds words to each product's data
    window.getExtraDataForSave = function (code) {
        const words = productWords[code] || [];
        console.log(`Getting words for ${code}:`, words);
        return {
            words: words
        };
    };
}
