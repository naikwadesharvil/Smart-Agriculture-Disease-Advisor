/*
=========================================
Smart Agriculture Disease Advisor
Dashboard JavaScript
=========================================
*/

document.addEventListener("DOMContentLoaded", function () {

    if (typeof chartData === "undefined") {
        return;
    }

    /* =====================================
       Color Palette
    ===================================== */

    const colors = [
        "#2E7D32",
        "#43A047",
        "#66BB6A",
        "#81C784",
        "#A5D6A7"
    ];

    /* =====================================
       Prediction Bar Chart
    ===================================== */

    const predictionCanvas = document.getElementById("predictionChart");

    if (predictionCanvas) {

        const ctx = predictionCanvas.getContext("2d");

        const gradient = ctx.createLinearGradient(0, 0, 0, 400);

        gradient.addColorStop(0, "#2E7D32");
        gradient.addColorStop(1, "#81C784");

        new Chart(ctx, {

            type: "bar",

            data: {

                labels: chartData.labels,

                datasets: [{

                    label: "Confidence (%)",

                    data: chartData.values,

                    backgroundColor: gradient,

                    borderRadius: 12,

                    borderSkipped: false

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: {

                    duration: 1500,

                    easing: "easeOutQuart"

                },

                plugins: {

                    legend: {

                        display: false

                    },

                    tooltip: {

                        callbacks: {

                            label: function (context) {

                                return context.raw + "%";

                            }

                        }

                    }

                },

                scales: {

                    y: {

                        beginAtZero: true,

                        max: 100,

                        ticks: {

                            callback: function (value) {

                                return value + "%";

                            }

                        }

                    }

                }

            }

        });

    }

    /* =====================================
       Confidence Doughnut
    ===================================== */

    const confidenceCanvas = document.getElementById("confidenceChart");

    if (confidenceCanvas) {

        let confidence = parseFloat(chartData.values[0]);

        if (isNaN(confidence)) {

            confidence = 0;

        }

        new Chart(confidenceCanvas, {

            type: "doughnut",

            data: {

                labels: [

                    "Confidence",

                    "Remaining"

                ],

                datasets: [{

                    data: [

                        confidence,

                        100 - confidence

                    ],

                    backgroundColor: [

                        "#2E7D32",

                        "#EAEAEA"

                    ],

                    borderWidth: 0

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                cutout: "75%",

                animation: {

                    animateRotate: true,

                    duration: 1800

                },

                plugins: {

                    legend: {

                        position: "bottom"

                    },

                    tooltip: {

                        callbacks: {

                            label: function (context) {

                                return context.raw + "%";

                            }

                        }

                    }

                }

            }

        });

    }

    /* =====================================
       Animated Counters
    ===================================== */

    document.querySelectorAll(".counter").forEach(function (counter) {

        const target = Number(counter.dataset.target);

        if (isNaN(target)) return;

        let count = 0;

        const speed = Math.max(10, target / 60);

        const update = () => {

            count += speed;

            if (count < target) {

                counter.innerText = Math.floor(count);

                requestAnimationFrame(update);

            } else {

                counter.innerText = target;

            }

        };

        update();

    });

    /* =====================================
       Progress Bars
    ===================================== */

    document.querySelectorAll(".progress-bar").forEach(function (bar) {

        const width = bar.style.width;

        bar.style.width = "0%";

        setTimeout(function () {

            bar.style.transition = "width 1.5s ease";

            bar.style.width = width;

        }, 300);

    });

    /* =====================================
       Card Hover Effect
    ===================================== */

    document.querySelectorAll(".dashboard-card").forEach(function (card) {

        card.addEventListener("mouseenter", function () {

            card.style.transform = "translateY(-6px)";

            card.style.transition = ".3s";

        });

        card.addEventListener("mouseleave", function () {

            card.style.transform = "translateY(0px)";

        });

    });

    /* =====================================
       Print Button
    ===================================== */

    const printButton = document.getElementById("printReport");

    if (printButton) {

        printButton.addEventListener("click", function () {

            window.print();

        });

    }

});