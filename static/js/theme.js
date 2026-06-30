const themeButton = document.getElementById("theme-btn");

function applyTheme(theme){

    if(theme === "dark"){

        document.documentElement.classList.add("dark");

        themeButton.innerHTML = "☀️";

    }

    else{

        document.documentElement.classList.remove("dark");

        themeButton.innerHTML = "🌙";

    }

}

const savedTheme = localStorage.getItem("theme") || "light";

applyTheme(savedTheme);

themeButton.addEventListener("click",()=>{

    const newTheme = document.documentElement.classList.contains("dark")

        ? "light"

        : "dark";
   
    localStorage.setItem("theme",newTheme);

    applyTheme(newTheme);

});