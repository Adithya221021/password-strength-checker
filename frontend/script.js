// ===== SHOW / HIDE PASSWORD =====
function togglePassword() {

    let input = document.getElementById("password");

    if (input.type === "password")
        input.type = "text";
    else
        input.type = "password";
}


// ===== LIVE CHECK WHILE TYPING =====
async function checkPassword() {

    let pwd = document.getElementById("password").value;

    // Reset if empty
    if (pwd.length === 0) {
        document.getElementById("result").innerHTML = "";
        document.getElementById("strengthBar").style.width = "0%";
        document.getElementById("feedback").innerHTML = "";
        return;
    }

    let response = await fetch("http://127.0.0.1:5000/check", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            password: pwd
        })
    });

    let data = await response.json();

    // Show Result Text
    let resultDiv = document.getElementById("result");

    resultDiv.innerHTML =
        "Strength: " + data.strength +
        " (Score: " + data.score + ")";

    resultDiv.className = data.strength;

    // Strength Bar
    let bar = document.getElementById("strengthBar");

    if (data.strength === "STRONG") {
        bar.style.width = "100%";
        bar.style.background = "#22c55e";
    }
    else if (data.strength === "MEDIUM") {
        bar.style.width = "60%";
        bar.style.background = "#eab308";
    }
    else {
        bar.style.width = "30%";
        bar.style.background = "#ef4444";
    }

    // Feedback Messages
    let fb = document.getElementById("feedback");
    fb.innerHTML = "";

    data.feedback.forEach(f => {
        fb.innerHTML += "- " + f + "<br>";
    });
}
