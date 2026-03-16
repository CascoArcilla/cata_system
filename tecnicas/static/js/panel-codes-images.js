const codeInputs = document.querySelectorAll('input[name^="producto_"]');
const imageInputs = document.querySelectorAll('input[type="file"][name^="imagen_"]');

codeInputs.forEach((codeInput, index) => {
    const imageInput = imageInputs[index];
    const labelContainer = imageInput.closest('label');
    const labelTextElement = labelContainer ? labelContainer.querySelector('p') : null;

    codeInput.addEventListener('input', (event) => {
        const newCode = event.target.value.trim().toUpperCase();

        if (newCode) {
            const newName = `imagen_${newCode}`;
            const newId = `id_imagen_${newCode}`;

            imageInput.name = newName;
            imageInput.id = newId;

            if (labelContainer) {
                labelContainer.setAttribute('for', newId);
            }
            if (labelTextElement) {
                labelTextElement.textContent = `Producto ${newCode}`;
            }
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    imageInputs.forEach((imageInput, index) => {
        const nameBase = "imagen_"
        const newCode = imageInput.name.slice(nameBase.length);
        codeInputs[index].value = newCode;
    });
});
