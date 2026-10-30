document.addEventListener("DOMContentLoaded", function () {

    const container = document.getElementById("container");

    const registerButton = document.getElementById("register");

    const loginButton = document.getElementById("login");


    // Register button
    registerButton.addEventListener("click", function () {

        container.classList.add("right-panel-active");

    });


    // Login button
    loginButton.addEventListener("click", function () {

        container.classList.remove("right-panel-active");

    });

});