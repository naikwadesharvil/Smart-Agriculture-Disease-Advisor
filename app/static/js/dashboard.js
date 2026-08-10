// ==========================================
// Smart Agriculture Disease Advisor
// Dashboard JavaScript
// ==========================================


document.addEventListener(
    "DOMContentLoaded",
    function () {


        // ==================================
        // Check Chart.js
        // ==================================

        if (
            typeof Chart === "undefined"
        ) {

            console.error(
                "Chart.js is not loaded."
            );

            return;

        }


        // ==================================
        // Check Chart Data
        // ==================================

        if (
            typeof chartData === "undefined"
        ) {

            console.warn(
                "Chart data is not available."
            );

            return;

        }


        // ==================================
        // Get Canvas
        // ==================================

        const canvas =
            document.getElementById(
                "predictionChart"
            );


        if (!canvas) {

            console.warn(
                "Prediction chart canvas not found."
            );

            return;

        }


        // ==================================
        // Prepare Chart Data
        // ==================================

        const labels =
            Array.isArray(
                chartData.labels
            )
                ? chartData.labels
                : [];


        const values =
            Array.isArray(
                chartData.values
            )
                ? chartData.values
                : [];


        if (
            labels.length === 0 ||
            values.length === 0
        ) {

            console.warn(
                "No prediction data available for chart."
            );

            return;

        }


        // ==================================
        // Destroy Existing Chart
        // ==================================

        if (
            window.predictionChartInstance
        ) {

            window.predictionChartInstance.destroy();

        }


        // ==================================
        // Create Prediction Chart
        // ==================================

        window.predictionChartInstance =
            new Chart(
                canvas,
                {

                    type: "bar",

                    data: {

                        labels: labels,

                        datasets: [

                            {

                                label:
                                    "Confidence (%)",

                                data: values,

                                borderWidth: 1,

                                borderRadius: 8,

                                maxBarThickness: 55

                            }

                        ]

                    },


                    options: {

                        responsive: true,

                        maintainAspectRatio: false,


                        plugins: {

                            legend: {

                                display: true,

                                position: "top"

                            },


                            tooltip: {

                                callbacks: {

                                    label:
                                        function (
                                            context
                                        ) {

                                            return (
                                                " Confidence: "
                                                +
                                                context.parsed.y
                                                +
                                                "%"
                                            );

                                        }

                                }

                            }

                        },


                        scales: {

                            y: {

                                beginAtZero: true,

                                max: 100,

                                title: {

                                    display: true,

                                    text:
                                        "Confidence (%)"

                                },

                                ticks: {

                                    callback:
                                        function (
                                            value
                                        ) {

                                            return (
                                                value
                                                +
                                                "%"
                                            );

                                        }

                                }

                            },


                            x: {

                                title: {

                                    display: true,

                                    text:
                                        "Predicted Disease"

                                }

                            }

                        }

                    }

                }
            );


        // ==================================
        // Animate Chart
        // ==================================

        window.predictionChartInstance.update();


    }
);