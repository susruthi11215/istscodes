let form = document.getElementById("registrationForm");

form.addEventListener("submit", function(event) {

    event.preventDefault();

    let username = document.querySelector('[name="username"]').value;
    let password = document.querySelector('[name="password"]').value;

    console.log("Username:", username);
    console.log("Password:", password);

});