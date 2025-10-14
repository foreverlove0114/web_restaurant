document.getElementById("position-form").addEventListener("submit", function(event) {
            const weight = document.getElementById("weight").value;

            if (weight <= 150) {
                alert("The weight must be at least 150g.");
                event.preventDefault();
            }
        });