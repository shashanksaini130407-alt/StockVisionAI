// =====================================================
// Generic Page Animations
// =====================================================

document.addEventListener("DOMContentLoaded", () => {

    // ==========================================
    // Fade & Slide Elements
    // ==========================================

    const animatedElements = document.querySelectorAll(
        ".fade-in, .slide-up"
    );

    animatedElements.forEach((element, index) => {

        setTimeout(() => {

            element.classList.add("show");

        }, index * 120);

    });

});