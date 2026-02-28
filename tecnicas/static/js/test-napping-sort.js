// Napping Sort Mode - Three Phase Implementation
// Phase 1: Place products on plane
// Phase 2: Create groups by selecting points
// Phase 3: Describe groups with words

// Store groups: { "group-1": ["CODE1", "CODE2"], "group-2": ["CODE3"] }
const productGroups = {};

// Store group words: { "group-1": ["word1", "word2"], "group-2": ["word3"] }
const groupWords = {};

// Track which group each product belongs to: { "CODE1": "group-1", "CODE2": "group-1" }
const productToGroup = {};

// Selected points for creating a group
let selectedPoints = [];

// Current group counter for generating IDs
let groupCounter = 1;

// Current phase (1, 2, or 3)
let currentPhase = 1;

// Current group being described
let currentGroupId = null;

// Only initialize if in sort mode
const modeElementSort = document.querySelector('[data-mode]');
const isSortMode = modeElementSort && modeElementSort.dataset.mode.toLowerCase() === 'sorting';

if (isSortMode) {
    initSortMode();
}

function loadExistingGroups() {
    const dataGroupContainer = document.querySelector('.data-group-products');
    if (!dataGroupContainer) return { hasGroups: false, hasWords: false };

    const groupElements = dataGroupContainer.querySelectorAll('.item-group');
    let hasGroups = false;
    let hasWords = false;

    groupElements.forEach((groupEl, index) => {
        const groupId = `group-${groupCounter++}`;
        const products = [];
        const words = groupEl.dataset.words ? groupEl.dataset.words.split(',').map(w => w.trim()).filter(w => w) : [];

        // Get products in this group
        groupEl.querySelectorAll('.item-group-product').forEach(productEl => {
            const code = productEl.dataset.code;
            products.push(code);
            productToGroup[code] = groupId;
        });

        if (products.length > 0) {
            hasGroups = true;
            productGroups[groupId] = products;
            groupWords[groupId] = words;

            if (words.length > 0) {
                hasWords = true;
            }
        }
    });

    return { hasGroups, hasWords };
}

function initSortMode() {
    const continueGroupingBtn = document.getElementById('continue-grouping');
    const continueDescriptionBtn = document.getElementById('continue-description');
    const createGroupBtn = document.getElementById('create-group-btn');
    const dissolveGroupBtn = document.getElementById('dissolve-group-btn');
    const groupControls = document.getElementById('group-controls');
    const questionSaveBtn = document.getElementById('question-save');

    const groupWordDialog = document.getElementById('group-word-dialog');
    const groupWordForm = document.getElementById('group-word-form');
    const groupWordInput = document.getElementsByName('nombre_palabra')[0];
    groupWordInput.value = "";
    const groupWordList = document.getElementById('group-word-list');
    const dialogGroupId = document.getElementById('dialog-group-id');

    // Hide question save button initially
    questionSaveBtn.classList.add('hidden');

    // Load existing groups from backend and determine initial phase
    const { hasGroups, hasWords } = loadExistingGroups();

    setTimeout(() => {
        // Determine initial phase based on existing data
        if (hasGroups && hasWords) {
            // Skip to Phase 3 (Description) if groups have words
            currentPhase = 3;
            window.isPlacementActive = false;
            groupControls.classList.remove('hidden');
            continueDescriptionBtn.classList.remove('hidden');

            renderExistingGroups();
            startDescriptionPhase();
        } else if (hasGroups) {
            // Skip to Phase 2 (Grouping) if groups exist but no words
            currentPhase = 2;
            renderExistingGroups();
            window.isPlacementActive = false;
            groupControls.classList.remove('hidden');
            continueDescriptionBtn.classList.remove('hidden');

            const plane = document.getElementById('napping-plane');
            plane.classList.remove('cursor-crosshair');
            plane.classList.add('cursor-default');

            enablePointSelection();
            spanNotifaction("Continúa agrupando productos o pasa a la descripción.", false);
        } else {
            // Start in Phase 1 (Placement)
            currentPhase = 1;
        }
    }, 200);

    // Phase 1: Product Placement
    // Show continue to grouping button when all products are placed
    setInterval(() => {
        if (currentPhase === 1) {
            const placedCount = Object.keys(window.placedPoints).length;
            const totalProducts = document.querySelectorAll('.item-product').length;

            if (placedCount === totalProducts && placedCount > 0) {
                continueGroupingBtn.classList.remove('hidden');
            } else {
                continueGroupingBtn.classList.add('hidden');
            }
        }
    }, 500);

    // Transition to Phase 2: Grouping
    continueGroupingBtn.addEventListener('click', () => {
        const placedCount = Object.keys(window.placedPoints).length;
        const totalProducts = document.querySelectorAll('.item-product').length;

        if (placedCount !== totalProducts) {
            spanNotifaction("Por favor, coloca todos los productos antes de continuar.");
            return;
        }

        startGroupingPhase();
    });

    function startGroupingPhase() {
        currentPhase = 2;
        window.isPlacementActive = false;
        continueGroupingBtn.classList.add('hidden');
        groupControls.classList.remove('hidden');
        continueDescriptionBtn.classList.remove('hidden');

        const plane = document.getElementById('napping-plane');
        plane.classList.remove('cursor-crosshair');
        plane.classList.add('cursor-default');

        // Remove selection from products
        document.querySelectorAll('.item-product').forEach(p => {
            p.classList.remove('ring-4', 'ring-primary');
        });

        spanNotifaction("Fase de agrupación: Selecciona puntos y crea grupos.", false);

        // Auto-save points when transitioning to Phase 2
        sortModeSaveData(false);

        // Enable point selection
        enablePointSelection();
    }

    function enablePointSelection() {
        // Add click handler to points for selection
        document.getElementById('napping-plane').addEventListener('click', (e) => {
            if (currentPhase !== 2) return;

            const point = e.target.closest('.data-point');
            if (point) {
                e.stopPropagation();
                togglePointSelection(point.dataset.code);
            }
        });
    }

    function togglePointSelection(code) {
        // Check if point is already in a group
        if (productToGroup[code]) {
            spanNotifaction(`El producto ${code} ya pertenece al grupo ${productToGroup[code]}`);
            return;
        }

        const point = document.getElementById(`point-${code}`);
        const index = selectedPoints.indexOf(code);

        if (index > -1) {
            // Deselect
            selectedPoints.splice(index, 1);
            point.classList.remove('ring-4', 'ring-blue-500');
            point.classList.add('bg-red-600');
            point.classList.remove('bg-blue-600');
        } else {
            // Select
            selectedPoints.push(code);
            point.classList.add('ring-4', 'ring-blue-500');
            point.classList.remove('bg-red-600');
            point.classList.add('bg-blue-600');
        }
    }

    // Create Group
    createGroupBtn.addEventListener('click', () => {
        if (selectedPoints.length === 0) {
            spanNotifaction("Selecciona al menos un punto para crear un grupo");
            return;
        }

        const groupId = `group-${groupCounter++}`;
        productGroups[groupId] = [...selectedPoints];
        groupWords[groupId] = [];

        // Update product to group mapping
        selectedPoints.forEach(code => {
            productToGroup[code] = groupId;
        });

        // Visual update: change color of grouped points
        const colors = ['bg-green-600', 'bg-purple-600', 'bg-yellow-600', 'bg-pink-600', 'bg-indigo-600'];
        const colorIndex = (groupCounter - 2) % colors.length;

        selectedPoints.forEach(code => {
            const point = document.getElementById(`point-${code}`);
            point.classList.remove('bg-blue-600', 'ring-4', 'ring-blue-500');
            point.classList.add(colors[colorIndex]);
        });

        // Add group to display
        addGroupToDisplay(groupId, selectedPoints, colors[colorIndex]);

        // Clear selection
        selectedPoints = [];

        spanNotifaction(`Grupo "${groupId}" creado con éxito`, false);
    });

    function addGroupToDisplay(groupId, products, colorClass) {
        const groupsDisplay = document.getElementById('groups-display');

        const groupBadge = document.createElement('div');
        groupBadge.id = `display-${groupId}`;
        groupBadge.className = `badge badge-lg gap-2 p-4 ${colorClass} text-white cursor-pointer font-semibold`;
        groupBadge.innerHTML = `
            [ ${products.join(', ')} ]
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-4 h-4 stroke-current dissolve-group-icon" data-group-id="${groupId}">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        `;

        groupsDisplay.appendChild(groupBadge);

        // Add dissolve handler
        groupBadge.querySelector('.dissolve-group-icon').addEventListener('click', (e) => {
            e.stopPropagation();
            dissolveGroup(groupId);
        });

        // Add click handler for Phase 3 (describe group)
        groupBadge.addEventListener('click', () => {
            if (currentPhase === 3) {
                openGroupWordDialog(groupId);
            }
        });
    }

    function dissolveGroup(groupId) {
        if (currentPhase === 3) {
            spanNotifaction("No puedes disolver un grupo en la fase de descripción");
            return;
        }

        if (groupWords[groupId] && groupWords[groupId].length > 0) {
            spanNotifaction("No puedes disolver un grupo que ya tiene palabras descriptivas");
            return;
        }

        // Remove from product to group mapping
        productGroups[groupId].forEach(code => {
            delete productToGroup[code];
            const point = document.getElementById(`point-${code}`);
            point.classList.remove('bg-green-600', 'bg-purple-600', 'bg-yellow-600', 'bg-pink-600', 'bg-indigo-600');
            point.classList.add('bg-red-600');
        });

        // Remove group
        delete productGroups[groupId];
        delete groupWords[groupId];

        // Remove from display
        const displayElement = document.getElementById(`display-${groupId}`);
        if (displayElement) {
            displayElement.remove();
        }

        spanNotifaction(`Grupo "${groupId}" disuelto`, false);
    }

    // Dissolve Group button (dissolves last created group or selected group)
    dissolveGroupBtn.addEventListener('click', () => {
        const groupIds = Object.keys(productGroups);
        if (groupIds.length === 0) {
            spanNotifaction("No hay grupos para disolver");
            return;
        }

        // Dissolve the last group
        const lastGroupId = groupIds[groupIds.length - 1];
        dissolveGroup(lastGroupId);
    });

    // Transition to Phase 3: Description
    continueDescriptionBtn.addEventListener('click', () => {
        const groupIds = Object.keys(productGroups);
        if (groupIds.length === 0) {
            spanNotifaction("Crea al menos un grupo para continuar");
            return;
        }

        // Check all products are in groups
        const totalProducts = document.querySelectorAll('.item-product').length;
        const groupedProducts = Object.keys(productToGroup).length;

        if (groupedProducts !== totalProducts) {
            spanNotifaction("Todos los productos deben estar asignados a un grupo");
            return;
        }

        startDescriptionPhase();
    });

    function startDescriptionPhase() {
        currentPhase = 3;
        continueDescriptionBtn.classList.add('hidden');

        createGroupBtn.classList.add('hidden');
        dissolveGroupBtn.classList.add('hidden');

        questionSaveBtn.classList.remove('hidden');

        const iconsDisolveGroup = document.querySelectorAll('.dissolve-group-icon');
        for (let index = 0; index < iconsDisolveGroup.length; index++) {
            const icon = iconsDisolveGroup.item(index);
            icon.remove();
        }

        spanNotifaction("Fase de descripción: Haz clic en un grupo para agregar palabras.", false);

        // Auto-save groups when transitioning to Phase 3
        sortModeSaveData(false);
    }

    // Group Word Dialog Functions
    function openGroupWordDialog(groupId) {
        currentGroupId = groupId;
        dialogGroupId.innerText = groupId;
        renderGroupWordList();
        groupWordDialog.showModal();
    }

    function renderGroupWordList() {
        groupWordList.innerHTML = '';
        const words = groupWords[currentGroupId] || [];

        words.forEach((word, index) => {
            const badge = document.createElement('div');
            badge.className = 'badge badge-secondary gap-2 p-3';
            badge.innerHTML = `
                ${word}
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-4 h-4 stroke-current cursor-pointer remove-word" data-index="${index}"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            `;

            badge.querySelector('.remove-word').addEventListener('click', () => {
                removeGroupWord(index);
            });

            groupWordList.appendChild(badge);

        });

        // Update group display with word count
        updateGroupDisplayWithWords(currentGroupId);
    }

    function addGroupWord(word) {
        if (!groupWords[currentGroupId]) {
            groupWords[currentGroupId] = [];
        }

        if (groupWords[currentGroupId].includes(word)) {
            spanNotifaction("Palabra duplicada");
            return;
        }

        groupWords[currentGroupId].push(word);
        renderGroupWordList();
    }

    function removeGroupWord(index) {
        if (groupWords[currentGroupId]) {
            groupWords[currentGroupId].splice(index, 1);
            renderGroupWordList();
        }
    }

    groupWordForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const word = groupWordInput.value.trim();
        if (word) {
            addGroupWord(word);
            groupWordInput.value = '';
            groupWordInput.focus();
        }
    });

    function updateGroupDisplayWithWords(groupId) {
        const displayElement = document.getElementById(`display-${groupId}`);
        if (!displayElement) return;

        const words = groupWords[groupId] || [];
        const products = productGroups[groupId] || [];

        // Add tooltip with words on hover
        if (words.length > 0) {
            let tooltip = displayElement.querySelector('.group-tooltip');
            if (!tooltip) {
                tooltip = document.createElement('div');
                tooltip.className = 'group-tooltip absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-800 text-white text-xs rounded z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none hidden';
                displayElement.classList.add('group', 'relative');
                displayElement.appendChild(tooltip);
            }

            const wordBadges = words.map(w => `<span class="inline-block px-2 py-1 bg-yellow-600 text-white rounded text-xs">${w}</span>`).join('');
            tooltip.innerHTML = `
                <strong>${groupId}</strong>
                <div class="mt-2 pt-2 border-t border-gray-600" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; max-width: 300px;">
                    ${wordBadges}
                </div>
            `;
            tooltip.style.maxWidth = '320px';
            tooltip.style.whiteSpace = 'normal';
            tooltip.classList.remove('hidden');
        } else {
            let tooltip = displayElement.querySelector('.group-tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        }
    }

    function renderExistingGroups() {
        const colors = ['bg-green-600', 'bg-purple-600', 'bg-yellow-600', 'bg-pink-600', 'bg-indigo-600'];
        let colorIndex = 0;

        for (const [groupId, products] of Object.entries(productGroups)) {
            const color = colors[colorIndex % colors.length];
            colorIndex++;

            // Update point colors
            products.forEach(code => {
                const point = document.getElementById(`point-${code}`);

                if (point) {
                    point.classList.remove('bg-red-600');
                    point.classList.add(color);
                }
            });

            // Add group to display
            addGroupToDisplay(groupId, products, color);

            // Update display with words if they exist
            if (groupWords[groupId] && groupWords[groupId].length > 0) {
                updateGroupDisplayWithWords(groupId);
            }
        }
    }

    // Set up callbacks to extend the base saveData function
    window.beforeSaveData = function (isFinishSession = false) {
        if (isFinishSession) {
            // Validate all products are placed
            const totalProducts = document.querySelectorAll('.item-product').length;
            const placedCount = Object.keys(window.placedPoints).length;

            if (placedCount !== totalProducts) {
                spanNotifaction("Por favor, coloca todos los productos antes de finalizar la sesión");
                return false;
            }

            // Validate all products are in groups
            const groupedProducts = Object.keys(productToGroup).length;
            if (groupedProducts !== totalProducts) {
                spanNotifaction("Todos los productos deben estar asignados a un grupo");
                return false;
            }

            // Validate each group has at least one product (already guaranteed by creation logic)
            const groupIds = Object.keys(productGroups);
            if (groupIds.length === 0) {
                spanNotifaction("Debe existir al menos un grupo");
                return false;
            }

            // Validate each group has at least one word
            for (const groupId of groupIds) {
                const words = groupWords[groupId] || [];
                if (words.length < 1) {
                    spanNotifaction(`El grupo ${groupId} debe tener al menos una palabra descriptiva`);
                    return false;
                }
            }
        }
        return true;
    };

    // Override save-progress button to use sort mode save function
    const saveProgressBtn = document.getElementById('save-progress');
    // Remove existing event listener by cloning and replacing
    const newSaveProgressBtn = saveProgressBtn.cloneNode(true);
    newSaveProgressBtn.textContent = 'Guardar Progreso Sort';
    saveProgressBtn.parentNode.replaceChild(newSaveProgressBtn, saveProgressBtn);

    newSaveProgressBtn.addEventListener('click', async () => {
        await sortModeSaveData(false);
    });

    // Override finish-session button to use sort mode save function
    document.getElementById('finish-session').addEventListener('click', async (e) => {
        e.preventDefault();
        e.stopPropagation();
        const success = await sortModeSaveData(true);
        if (success) {
            const formFinish = document.getElementById("form-finish-session");
            formFinish.action = "";
            formFinish.submit();
        }
    });

    // Sort mode specific save function
    async function sortModeSaveData(isFinishSession = false) {
        // Run validation callback if it exists
        if (window.beforeSaveData && typeof window.beforeSaveData === 'function') {
            const validationResult = window.beforeSaveData(isFinishSession);
            if (validationResult === false) {
                return false;
            }
        }

        // Build products array with basic position info and group assignment
        const products = [];
        for (const [code, point] of Object.entries(window.placedPoints)) {
            const groupId = productToGroup[code];
            products.push({
                code: code,
                x: point.x,
                y: point.y,
                idProduct: point.id,
                group: groupId || "" // Empty string if no group assigned
            });
        }

        // Build groups object with word arrays
        const groups = {};
        const groupIds = Object.keys(productGroups);

        // Only include groups if they exist
        if (groupIds.length > 0) {
            for (const groupId of groupIds) {
                groups[groupId] = groupWords[groupId] || [];
            }
        }

        // Build the data structure
        const data = { products: products };

        // Only add groups if they exist
        if (Object.keys(groups).length > 0) {
            data.groups = groups;
        }

        const URL = "/sensorial/testers/api/rating-napping";
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch(URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                spanNotifaction("Error en la respuesta del servidor");
                return false;
            }

            const result = await response.json();

            if (result.error) {
                spanNotifaction(result.error);
                return false;
            } else {
                spanNotifaction(result.message, false);
                return true;
            }
        } catch (error) {
            spanNotifaction("Error en proceso de guardar los datos");
            return false;
        }
    }
}
