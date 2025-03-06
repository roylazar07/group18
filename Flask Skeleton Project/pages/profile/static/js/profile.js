function validateForm(event) {
    event.preventDefault(); // Prevent form submission if errors exist

    // Clear all previous error messages
    document.querySelectorAll('.error-message').forEach(el => el.textContent = '');

    // Collect fields
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const email = document.getElementById('email').value;
    const phoneNumber = document.getElementById('phone-number').value;
    const day = parseInt(document.getElementById('day').value);
    const month = parseInt(document.getElementById('month').value);
    const year = parseInt(document.getElementById('year').value);

    // Error flags
    let hasErrors = false;

    // Validation for first name
    const firstNameError = document.getElementById('first-name-error');
    const nameRegex = /^[א-תa-zA-Z]+$/;
    if (!nameRegex.test(firstName)) {
        firstNameError.textContent = "First name must contain only letters.";
        hasErrors = true;
    }

    // Validation for last name
    const lastNameError = document.getElementById('last-name-error');
    if (!nameRegex.test(lastName)) {
        lastNameError.textContent = "Last name must contain only letters.";
        hasErrors = true;
    }

    // Validation for email
    const emailError = document.getElementById('email-error');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        emailError.textContent = "Invalid email address format.";
        hasErrors = true;
    }

    // Validation for phone number
    const phoneError = document.getElementById('phone-number-error');
    const phoneRegex = /^0\d{9}$/;
    if (!phoneRegex.test(phoneNumber)) {
        phoneError.textContent = "Phone number must start with 0 and have exactly 10 digits.";
        hasErrors = true;
    }

    // Validation for birth date
    const dateError = document.getElementById('date-error');
    const isValidDate = (d, m, y) => {
        const date = new Date(y, m - 1, d);
        return date.getFullYear() === y && date.getMonth() === m - 1 && date.getDate() === d;
    };

    if (isNaN(day) || day < 1 || day > 31) {
        dateError.textContent = "Day must be a valid number between 1 and 31.";
        hasErrors = true;
    } else if (isNaN(month) || month < 1 || month > 12) {
        dateError.textContent = "Month must be a valid number between 1 and 12.";
        hasErrors = true;
    } else if (isNaN(year) || year < 1900 || year > new Date().getFullYear()) {
        dateError.textContent = `Year must be between 1900 and ${new Date().getFullYear()}.`;
        hasErrors = true;
    } else if (!isValidDate(day, month, year)) {
        dateError.textContent = "The date you entered does not exist in the calendar.";
        hasErrors = true;
    } else {
        // Check if the date is in the future
        const inputDate = new Date(year, month - 1, day); // תאריך שהוזן
        const today = new Date(); // תאריך היום
        if (inputDate > today) {
            dateError.textContent = "The date cannot be in the future";
            hasErrors = true;
        }
    }

    // Submit the form if there are no errors
    if (!hasErrors) {
        alert("The form has been successfully submitted!");
        document.querySelector('form').submit();
    }
}