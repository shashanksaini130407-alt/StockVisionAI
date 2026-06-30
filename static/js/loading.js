const form = document.querySelector(".search-form");

const messages = [

    "Initializing AI Engine...",

    "Fetching Stock Data...",

    "Calculating Technical Indicators...",

    "Running Random Forest Model...",

    "Generating AI Recommendation...",

    "Preparing Dashboard..."

];

if(form){

    form.addEventListener("submit", function(){

        document
            .querySelector(".loader-overlay")
            .classList.add("active");

        const button = document.querySelector(".analyze-btn");

        button.disabled = true;

        button.innerHTML = "Analyzing...";

        let index = 0;

        const message = document.getElementById("loader-message");

        message.innerHTML = messages[index];

        const interval = setInterval(function(){

            index++;

            if(index < messages.length){

                message.style.opacity = 0;

                setTimeout(function(){

                    message.innerHTML = messages[index];

                    message.style.opacity = 1;

                },200);

            }else{

                clearInterval(interval);

            }

        },900);

    });

}