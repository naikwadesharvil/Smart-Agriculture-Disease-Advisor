/*
=========================================
Smart Agriculture Disease Advisor
Main JavaScript
=========================================
*/

document.addEventListener("DOMContentLoaded", function () {

    console.log("Smart Agriculture Loaded");

    /* =====================================
       Dark Mode
    ===================================== */

    const themeToggle = document.getElementById("themeToggle");

    if (localStorage.getItem("theme") === "dark") {

        document.body.classList.add("dark-mode");

        if (themeToggle) {

            themeToggle.innerHTML =
                '<i class="bi bi-sun-fill"></i>';

        }

    }

    if (themeToggle) {

        themeToggle.addEventListener("click", function () {

            document.body.classList.toggle("dark-mode");

            if (document.body.classList.contains("dark-mode")) {

                localStorage.setItem("theme", "dark");

                themeToggle.innerHTML =
                    '<i class="bi bi-sun-fill"></i>';

            } else {

                localStorage.setItem("theme", "light");

                themeToggle.innerHTML =
                    '<i class="bi bi-moon-stars-fill"></i>';

            }

        });

    }

    /* =====================================
       Loading Spinner
    ===================================== */

    const loader = document.getElementById("loader");

    if (loader) {

        loader.style.display = "none";

    }

    document.querySelectorAll("form").forEach(function (form) {

        form.addEventListener("submit", function () {

            if (loader) {

                loader.style.display = "flex";

            }

        });

    });

    /* =====================================
       Scroll To Top Button
    ===================================== */

    const topBtn = document.getElementById("topBtn");

    if (topBtn) {

        window.addEventListener("scroll", function () {

            if (window.scrollY > 300) {

                topBtn.style.display = "block";

            } else {

                topBtn.style.display = "none";

            }

        });

        topBtn.addEventListener("click", function () {

            window.scrollTo({

                top: 0,

                behavior: "smooth"

            });

        });

    }

    /* =====================================
       Bootstrap Toast
    ===================================== */

    const toastElement = document.getElementById("successToast");

    if (toastElement && typeof bootstrap !== "undefined") {

        const toast = new bootstrap.Toast(toastElement, {

            delay: 3000

        });

        toast.show();

    }

    /* =====================================
       Card Hover Animation
    ===================================== */

    const cards = document.querySelectorAll(".card");

    cards.forEach(function (card) {

        card.addEventListener("mouseenter", function () {

            card.style.transform = "translateY(-6px)";

            card.style.transition = "0.3s ease";

        });

        card.addEventListener("mouseleave", function () {

            card.style.transform = "translateY(0px)";

        });

    });

    /* =====================================
       Button Ripple Effect
    ===================================== */

    document.querySelectorAll(".btn").forEach(function (button) {

        button.addEventListener("click", function () {

            button.classList.add("active");

            setTimeout(function () {

                button.classList.remove("active");

            }, 200);

        });

    });

    /* =====================================
       Fade Images After Load
    ===================================== */

    document.querySelectorAll("img").forEach(function (img) {

        img.onload = function () {

            img.style.opacity = "1";

            img.style.transition = "opacity 0.5s ease";

        };

    });

    /* =====================================
       Smooth Anchor Links
    ===================================== */

    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {

        anchor.addEventListener("click", function (e) {

            const target = document.querySelector(this.getAttribute("href"));

            if (target) {

                e.preventDefault();

                target.scrollIntoView({

                    behavior: "smooth"

                });

            }

        });

    });

    /* =====================================
       Auto Hide Loader After Page Load
    ===================================== */

    window.addEventListener("load", function () {

        if (loader) {

            loader.style.display = "none";

        }

    });

});