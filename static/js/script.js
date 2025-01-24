function validateDomain(currentDomain) {
    const inputs = document.querySelectorAll(`#domain${currentDomain} input[type="number"]`);
    console.log(`Validating domain ${currentDomain} with ${inputs.length} inputs.`);
    for (let input of inputs) {
        const value = parseFloat(input.value);
        if (isNaN(value) || value < 0 || value > 3) {
            alert('Skriv inn ett tall mellom 0 og 3.');
            return false;
        }
    }
    return true;
}

function nextDomain(currentDomain) {
    if (!validateDomain(currentDomain)) {
        return;
    }

    const currentElement = document.getElementById(`domain${currentDomain}`);
    const nextElement = document.getElementById(`domain${currentDomain + 1}`);

    if (nextElement) {
        currentElement.style.display = 'none';
        nextElement.style.display = 'block';
    } else {
        currentElement.style.display = 'none';
        document.getElementById('submit-button').style.display = 'block';
    }
}

function prevDomain(currentDomain) {
    const currentElement = document.getElementById(`domain${currentDomain}`);
    const prevElement = document.getElementById(`domain${currentDomain - 1}`);

    if (prevElement) {
        currentElement.style.display = 'none';
        prevElement.style.display = 'block';
    }
}

function printPage() {
    window.print();
  }
  