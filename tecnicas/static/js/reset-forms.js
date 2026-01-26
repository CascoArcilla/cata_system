window.addEventListener('pageshow', (event) => {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.reset();
    });
});
