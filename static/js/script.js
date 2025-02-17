function validateForm() {
    const questions = document.querySelectorAll('input[type="radio"]');
    let filled = true;
    const formData = {};

    questions.forEach(question => {
        formData[question.name] = formData[question.name] || [];
        if (question.checked) {
            formData[question.name].push(question.value);
        }
    });

    for (const key in formData) {
        if (formData[key].length === 0) {
            filled = false;
        }
    }

    if (!filled) {
        alert("Vennligst fyll ut alle punktene før du sender inn skjemaet.");
    }

    return filled;
}
