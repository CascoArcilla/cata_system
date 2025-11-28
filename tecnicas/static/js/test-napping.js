
const planeContainer = document.getElementById('napping-plane');
const productsContainer = document.getElementById('items');
const products = document.querySelectorAll('.item-product');

// Configuration for the physical dimensions of the tablecloth (in cm)
const PHYSICAL_WIDTH = 60;
const PHYSICAL_HEIGHT = 40;

let selectedProductCode = null;
let selectedProductId = null;

// Object to store coordinates: { "CODE": { x: 10.5, y: 20.1, id: 123 } }
const placedPoints = {};

// 1. Handle Product Selection
products.forEach(product => {
    product.addEventListener('click', () => {
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
    placedPoints[selectedProductCode] = {
        x: parseFloat(xCoord.toFixed(2)),
        y: parseFloat(yCoord.toFixed(2)),
        id: selectedProductId
    };

    // Render Point
    renderPoint(selectedProductCode, xPixel, yPixel, xCoord, yCoord);
});

function renderPoint(code, xPx, yPx, xVal, yVal) {
    // Remove existing point for this product if it exists
    const existingPoint = document.getElementById(`point-${code}`);
    if (existingPoint) {
        existingPoint.remove();
    }

    const point = document.createElement('div');
    point.id = `point-${code}`;
    point.className = 'absolute w-4 h-4 bg-red-600 rounded-full transform -translate-x-1/2 -translate-y-1/2 cursor-pointer border-2 border-white shadow-md group';
    point.style.left = `${xPx}px`;
    point.style.top = `${yPx}px`;

    // Tooltip/Label
    const label = document.createElement('div');
    label.className = 'absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-gray-800 text-white text-xs rounded whitespace-nowrap z-10 hidden group-hover:block';
    label.innerHTML = `
            <strong>${code}</strong><br>
            X: ${xVal.toFixed(1)}<br>
            Y: ${yVal.toFixed(1)}
        `;

    point.appendChild(label);
    planeContainer.appendChild(point);

    // Also show a permanent label next to the point if desired, 
    // or just rely on the hover. For now, let's add a small text label below it.
    const textLabel = document.createElement('span');
    textLabel.className = 'absolute top-4 left-1/2 transform -translate-x-1/2 text-xs font-bold text-gray-700 pointer-events-none';
    textLabel.innerText = code;
    point.appendChild(textLabel);
}

