// =====================================================
// Dashboard Animations
// =====================================================

document.addEventListener("DOMContentLoaded", () => {

    // ==========================================
    // Dashboard Cards Animation
    // ==========================================

    const cards = document.querySelectorAll(".dashboard-grid .card");

    cards.forEach((card, index) => {

        card.style.opacity = "0";
        card.style.transform = "translateY(35px)";

        setTimeout(() => {

            card.style.transition =
                "all .6s ease";

            card.style.opacity = "1";

            card.style.transform =
                "translateY(0)";

        }, index * 100);

    });

    // ==========================================
    // Analytics Cards
    // ==========================================

    const analytics =
        document.querySelectorAll(".analytics-item");

    analytics.forEach((card, index) => {

        card.style.opacity = "0";
        card.style.transform = "translateY(30px)";

        setTimeout(() => {

            card.style.transition =
                "all .6s ease";

            card.style.opacity = "1";

            card.style.transform =
                "translateY(0)";

        }, 800 + index * 70);

    });

    // ==========================================
    // Chart
    // ==========================================

    const chart =
        document.querySelector(".chart-card");

    if (chart) {

        chart.style.opacity = "0";

        chart.style.transform =
            "translateY(40px)";

        setTimeout(() => {

            chart.style.transition =
                "all .8s ease";

            chart.style.opacity = "1";

            chart.style.transform =
                "translateY(0)";

        }, 1200);

    }

    // ==========================================
    // AI Card
    // ==========================================

    const aiCard =
        document.querySelector(".ai-card");

    if (aiCard) {

        aiCard.style.opacity = "0";

        aiCard.style.transform =
            "translateY(40px)";

        setTimeout(() => {

            aiCard.style.transition =
                "all .8s ease";

            aiCard.style.opacity = "1";

            aiCard.style.transform =
                "translateY(0)";

        }, 1500);

    }

    // ==========================================
    // Counter Animation
    // ==========================================

    const counters =
        document.querySelectorAll(".counter");

    counters.forEach(counter => {

        const target =
            parseFloat(counter.dataset.target);

        if (isNaN(target))
            return;

        const prefix =
            counter.dataset.prefix || "";

        const suffix =
            counter.dataset.suffix || "";

        const isInteger =
            Number.isInteger(target);

        let current = 0;

        const increment =
            target / 80;

        function updateCounter() {

            current += increment;

            if (current >= target)
                current = target;

            let value;

            if (isInteger) {

                value =
                    Math.round(current).toLocaleString();

            }

            else {

                value =
                    current.toFixed(2);

            }

            counter.textContent =
                prefix + value + suffix;

            if (current < target) {

                requestAnimationFrame(updateCounter);

            }

        }

        updateCounter();

    });

});