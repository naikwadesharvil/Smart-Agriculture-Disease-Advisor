// ==========================================
// Smart Agriculture Disease Advisor
// Main JavaScript
// ==========================================


document.addEventListener(
    "DOMContentLoaded",
    function () {


        // ==================================
        // Initialize AOS
        // ==================================

        if (typeof AOS !== "undefined") {

            AOS.init({
                duration: 700,
                once: true,
                offset: 80
            });

        }


        // ==================================
        // Dark Mode
        // ==================================

        const themeToggle =
            document.getElementById(
                "themeToggle"
            );

        const themeIcon =
            themeToggle
                ? themeToggle.querySelector("i")
                : null;


        // Restore saved theme

        const savedTheme =
            localStorage.getItem(
                "theme"
            );


        if (savedTheme === "dark") {

            document.body.classList.add(
                "dark-mode"
            );

            updateThemeIcon(true);

        }


        // Theme button

        if (themeToggle) {

            themeToggle.addEventListener(
                "click",
                function () {

                    const isDark =
                        document.body.classList.toggle(
                            "dark-mode"
                        );


                    localStorage.setItem(
                        "theme",
                        isDark
                            ? "dark"
                            : "light"
                    );


                    updateThemeIcon(
                        isDark
                    );

                }
            );

        }


        // ==================================
        // Update Theme Icon
        // ==================================

        function updateThemeIcon(
            isDark
        ) {

            if (!themeIcon) {
                return;
            }


            if (isDark) {

                themeIcon.className =
                    "bi bi-sun-fill";

            } else {

                themeIcon.className =
                    "bi bi-moon-stars-fill";

            }

        }


        // ==================================
        // Back To Top
        // ==================================

        const backToTop =
            document.getElementById(
                "backToTop"
            );


        if (backToTop) {

            window.addEventListener(
                "scroll",
                function () {

                    if (
                        window.scrollY > 300
                    ) {

                        backToTop.classList.add(
                            "show"
                        );

                    } else {

                        backToTop.classList.remove(
                            "show"
                        );

                    }

                }
            );


            backToTop.addEventListener(
                "click",
                function () {

                    window.scrollTo({

                        top: 0,

                        behavior: "smooth"

                    });

                }
            );

        }


        // ==================================
        // Success Toast
        // ==================================

        const successToast =
            document.getElementById(
                "successToast"
            );


        if (
            successToast &&
            typeof bootstrap !== "undefined"
        ) {

            const toast =
                new bootstrap.Toast(
                    successToast,
                    {
                        delay: 4000
                    }
                );


            // Show only on the home page

            if (
                window.location.pathname ===
                "/"
            ) {

                setTimeout(
                    function () {

                        toast.show();

                    },
                    800
                );

            }

        }


        // ==================================
        // Upload Form
        // ==================================

        const uploadForm =
            document.getElementById("uploadForm");


        const loadingSpinner =
            document.getElementById(
                "loadingSpinner"
            );


        if (uploadForm) {

            uploadForm.addEventListener(
                "submit",
                function () {

                    const fileInput =
                        uploadForm.querySelector(
                            'input[type="file"]'
                        );


                    // Validate file

                    if (
                        !fileInput ||
                        !fileInput.files ||
                        fileInput.files.length === 0
                    ) {

                        return;

                    }


                    const file =
                        fileInput.files[0];


                    // Validate extension

                    const allowedTypes = [
                        "image/jpeg",
                        "image/png"
                    ];


                    if (
                        !allowedTypes.includes(
                            file.type
                        )
                    ) {

                        alert(
                            "Please upload a JPG, JPEG or PNG image."
                        );

                        return;

                    }


                    // Show loading spinner

                    if (loadingSpinner) {

                        loadingSpinner.classList.remove(
                            "d-none"
                        );

                    }


                    // Disable submit button

                    const submitButton =
                        uploadForm.querySelector(
                            'button[type="submit"]'
                        );


                    if (submitButton) {

                        submitButton.disabled =
                            true;

                        submitButton.innerHTML = `
                            <span
                                class="spinner-border spinner-border-sm me-2"
                                role="status">
                            </span>
                            Analyzing...
                        `;

                    }

                }
            );

        }


        // ==================================
        // File Input Preview
        // ==================================

        const fileInput =
            document.querySelector(
                'input[type="file"]'
            );


        if (fileInput) {

            fileInput.addEventListener(
                "change",
                function () {

                    if (
                        !this.files ||
                        this.files.length === 0
                    ) {

                        return;

                    }


                    const file =
                        this.files[0];


                    const allowedTypes = [
                        "image/jpeg",
                        "image/png"
                    ];


                    if (
                        !allowedTypes.includes(
                            file.type
                        )
                    ) {

                        alert(
                            "Please select a JPG, JPEG or PNG image."
                        );

                        this.value = "";

                        return;

                    }

                }
            );

        }


    }
);