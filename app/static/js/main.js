/* ==========================================
   SMART AGRICULTURE DISEASE ADVISOR
   Global JavaScript
========================================== */

document.addEventListener("DOMContentLoaded", function () {

    console.log("🌿 Smart Agriculture Disease Advisor Loaded");

    // ==========================================
    // Active Navbar Link
    // ==========================================

    const currentPath = window.location.pathname;

    document.querySelectorAll(".navbar .nav-link").forEach(link => {

        if (link.getAttribute("href") === currentPath) {

            link.classList.add("active");

        }

    });

    // ==========================================
    // Fade-in Animation on Scroll
    // ==========================================

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("show");

            }

        });

    }, {
        threshold: 0.15
    });

    document.querySelectorAll(".dashboard-card, .info-card").forEach(card => {

        card.classList.add("hidden");

        observer.observe(card);

    });

    // ==========================================
    // Smooth Scroll
    // ==========================================

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            e.preventDefault();

            const target = document.querySelector(this.getAttribute("href"));

            if (target) {

                target.scrollIntoView({

                    behavior: "smooth"

                });

            }

        });

    });

});

/* ================= COUNTER ================= */

const counters = document.querySelectorAll(".display-5");

counters.forEach(counter=>{

const update=()=>{

const target=parseInt(counter.innerText);

let count=0;

const increment=target/80;

const timer=setInterval(()=>{

count+=increment;

if(count>=target){

counter.innerText=target+"+";

clearInterval(timer);

}

else{

counter.innerText=Math.floor(count);

}

},20);

}

update();

});

/* ==========================================
   Scroll To Top Button
========================================== */

const topButton = document.createElement("button");

topButton.innerHTML = "↑";

topButton.id = "topButton";

document.body.appendChild(topButton);

window.addEventListener("scroll", () => {

    if (window.scrollY > 400) {

        topButton.style.display = "block";

    }

    else {

        topButton.style.display = "none";

    }

});

topButton.addEventListener("click", () => {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

});