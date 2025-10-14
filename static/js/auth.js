
document.getElementById("form-account").addEventListener("submit", function(event) {
            const pass = document.getElementById("password").value;

            if (pass.length < 8) {
                alert("The password must be at least 8 characters long!");
                event.preventDefault();
            }
        });