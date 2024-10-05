function validateForm() {
    const emailPattern = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/;
    const phonePattern = /^\+?[0-9]{10,13}$/;
    const usernamePattern = /^[a-zA-Z0-9]{3,20}$/;
    const passwordPattern = /.{8,}/;

    const email = document.getElementById('email').value;
    const phone_number = document.getElementById('phone_number').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!emailPattern.test(email)) {
        alert('Please enter a valid email address.');
        return false;
    }
    if (!phonePattern.test(phone_number)) {
        alert('Please enter a valid phone number.');
        return false;
    }
    if (!usernamePattern.test(username)) {
        alert('Username should be 3-20 characters long and contain only letters and numbers.');
        return false;
    }
    if (!passwordPattern.test(password)) {
        alert('Password should be at least 8 characters long.');
        return false;
    }
    return true;
}
