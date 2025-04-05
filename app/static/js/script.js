// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const myButton = document.getElementById('myButton');
    const message = document.getElementById('message');

    myButton.addEventListener('click', function() {
        message.textContent = 'Button clicked!';
        message.style.color = 'red';
    });
});