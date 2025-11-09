document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("wordsForm");

  form.addEventListener("submit", (e) => {
    e.preventDefault(); // prevenimos envío por defecto
    const checkboxes = form.querySelectorAll('input[type="checkbox"]');
    const unchecked = Array.from(checkboxes).filter((cb) => !cb.checked);

    if (unchecked.length > 0) {
      const confirmLeaveBlank = confirm(
        "Algunas palabras no han sido marcadas. ¿Deseas continuar dejando esas casillas en blanco?"
      );

      if (!confirmLeaveBlank) {
        return;
      }
    }

    // form.submit();
  });
});
