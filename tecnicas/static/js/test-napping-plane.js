const planeContainer = document.getElementById('napping-plane');
const productsContainer = document.getElementById('items');
const products = document.querySelectorAll('.item-product');

// Configuration for the physical dimensions of the tablecloth (in cm)
const PHYSICAL_WIDTH = 60;
const PHYSICAL_HEIGHT = 40;

let selectedProductCode = null;
let selectedProductId = null;

// Object to store coordinates: { "CODE": { x: 10.5, y: 20.1, id: 123 } }
window.placedPoints = {};

const modeElement = document.querySelector('[data-mode]');
window.isUltraFlash = modeElement && modeElement.dataset.mode.toLowerCase().includes('ultra flash');

// For ultra flash mode, it starts active but will be controlled by ultra-flash.js
if (window.isUltraFlash) {
  document.getElementById("question-save").classList.add("hidden");
  window.isPlacementActive = true;
} else {
  // Normal mode: placement is always active
  window.isPlacementActive = true;
}

// 1. Handle Product Selection
products.forEach(product => {
  product.addEventListener('click', () => {
    if (!window.isPlacementActive) return;

    // Remove selection from others
    products.forEach(p => p.classList.remove('ring-4', 'ring-primary'));

    // Select current
    product.classList.add('ring-4', 'ring-primary');
    selectedProductCode = product.dataset.code;
    selectedProductId = product.dataset.idProduct;
  });
});

// 2. Handle Plane Click (Placing Points)
planeContainer.addEventListener('click', (e) => {
  if (!window.isPlacementActive) return;

  if (!selectedProductCode) {
    spanNotifaction("Por favor, selecciona un producto primero")
    return;
  }

  const rect = planeContainer.getBoundingClientRect();

  // Calculate click position relative to the container (in pixels)
  const xPixel = e.clientX - rect.left;
  const yPixel = e.clientY - rect.top;

  // Calculate scaled coordinates (0 to PHYSICAL_DIMENSIONS)
  // X axis: 0 on left, 60 on right
  const xCoord = (xPixel / rect.width) * PHYSICAL_WIDTH;

  // Y axis: 0 on bottom, 40 on top (Invert Y because DOM Y is 0 at top)
  const yCoord = PHYSICAL_HEIGHT - ((yPixel / rect.height) * PHYSICAL_HEIGHT);

  // Update Data Object
  window.placedPoints[selectedProductCode] = {
    x: parseFloat(xCoord.toFixed(2)),
    y: parseFloat(yCoord.toFixed(2)),
    id: selectedProductId
  };

  // Render Point
  window.renderPoint(selectedProductCode, xPixel, yPixel, xCoord, yCoord);
});

// Make renderPoint global
window.renderPoint = function (code, xPx, yPx, xVal, yVal) {
  // Remove existing point for this product if it exists
  const existingPoint = document.getElementById(`point-${code}`);
  if (existingPoint) {
    existingPoint.remove();
  }

  const point = document.createElement('div');
  point.id = `point-${code}`;
  point.className = 'data-point absolute w-4 h-4 bg-red-600 rounded-full transform -translate-x-1/2 -translate-y-1/2 cursor-pointer border-2 border-white shadow-md group';
  point.dataset.code = code;
  point.dataset.px = xVal;
  point.dataset.py = yVal;
  point.dataset.idProduct = window.placedPoints[code]?.id;

  point.style.left = `${xPx}px`;
  point.style.top = `${yPx}px`;

  planeContainer.appendChild(point);

  const textLabel = document.createElement('span');
  textLabel.className = 'absolute top-4 left-1/2 transform -translate-x-1/2 text-xs font-bold text-gray-700 pointer-events-none';
  textLabel.innerText = code;
  point.appendChild(textLabel);
}

function checkPoints() {
  const points = document.querySelectorAll('.data-point');

  points.forEach(point => {
    const code = point.dataset.code;

    const xVal = parseFloat(point.dataset.px);
    const yVal = parseFloat(point.dataset.py);

    const rect = planeContainer.getBoundingClientRect();

    const px = (xVal / PHYSICAL_WIDTH) * rect.width;
    const py = ((PHYSICAL_HEIGHT - yVal) / PHYSICAL_HEIGHT) * rect.height;

    window.placedPoints[code] = {
      x: xVal.toFixed(2),
      y: yVal.toFixed(2),
      id: point.dataset.idProduct
    };

    window.renderPoint(code, px, py, xVal, yVal);
  });
}

setTimeout(checkPoints, 100);

/*
////
//////
//////// Question to finish session
//////
////
*/

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
//////// Save data and finish session
//////
////
*/

// Callback for additional validation before saving
window.beforeSaveData = null;

// Function to get extra data for each product
window.getExtraDataForSave = null;

window.saveData = async function (isFinishSession = false) {
  const codeProducts = Object.keys(window.placedPoints);
  const data = [];

  // Only validate all products placed if finishing session
  if (isFinishSession && products.length != codeProducts.length) {
    spanNotifaction("Por favor, coloca todos los puntos antes de finalizar la sesión")
    return false;
  }

  // Call beforeSaveData callback if it exists (for ultra flash validation)
  if (window.beforeSaveData && typeof window.beforeSaveData === 'function') {
    const validationResult = window.beforeSaveData(isFinishSession);
    if (validationResult === false) {
      return false;
    }
  }

  codeProducts.forEach((code) => {
    const point = window.placedPoints[code];

    const objData = {
      code: code,
      x: point.x,
      y: point.y,
      idProduct: point.id
    };

    // Get extra data if callback exists (for ultra flash words)
    if (window.getExtraDataForSave && typeof window.getExtraDataForSave === 'function') {
      const extraData = window.getExtraDataForSave(code);
      Object.assign(objData, extraData);
    }

    data.push(objData);
  })

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

// Function to finish session with validation
window.finishSession = async function () {
  const success = await window.saveData(true);
  if (success) {
    // Submit the form to finish session
    const formFinish = document.getElementById("form-finish-session")
    formFinish.action = ""
    formFinish.submit();
  }
}

document
  .getElementById("save-progress")
  .addEventListener("click", () => window.saveData(false));