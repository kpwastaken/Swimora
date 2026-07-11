// Swimora Dark Mode


// Load saved theme when opening any page

document.addEventListener("DOMContentLoaded", function () {


    const savedTheme = localStorage.getItem("theme");



    if (savedTheme === "dark") {


        document.body.classList.add("dark");


    }


});





// Dark mode button

function toggleDarkMode() {


    document.body.classList.toggle("dark");



    if (document.body.classList.contains("dark")) {


        localStorage.setItem(
            "theme",
            "dark"
        );


    } else {


        localStorage.setItem(
            "theme",
            "light"
        );


    }


}