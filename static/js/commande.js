document.addEventListener("DOMContentLoaded", function () {
    const numberInput = document.querySelector("input[aria-label='Sizing example input']");
    const container = document.querySelector("#container");
    const prixTotalDiv = document.querySelector("input[placeholder='Prix Total']").parentNode; // Targeting the parent div of "Prix Total" input for reference
    const clothesData = [];

    numberInput.addEventListener("input", function () {
        // Clear existing fields that were previously dynamically added
        const existingDynamicFields = document.querySelectorAll(".dynamic-field");
        existingDynamicFields.forEach(field => field.remove());

        const numberOfArticles = parseInt(numberInput.value, 10);
        for (let i = 0; i < numberOfArticles; i++) {
            const articleDiv = document.createElement("div");
            articleDiv.classList.add("dynamic-field");

            const typeDiv = document.createElement("div");
            typeDiv.className = "input-group mb-3";
            const typeLabel = document.createElement("label");
            typeLabel.className = "input-group-text";
            typeLabel.innerHTML = "Article " + (i + 1);
            const typeSelect = document.createElement("select");
            typeSelect.className = "form-select";
            typeSelect.innerHTML = `
                <option selected>Type d'article</option>
                <option value="1">T-shirt</option>
                <option value="2">Jeans</option>
                <option value="3">Chemise</option>
                <option value="3">Pantalon</option>
                <option value="3">Djelaba</option>
                <option value="3">Autre (Veuillez specifier dans la note)</option>
            `;
            typeDiv.appendChild(typeLabel);
            typeDiv.appendChild(typeSelect);

            const colorDiv = document.createElement("div");
            colorDiv.className = "input-group mb-3";
            const colorLabel = document.createElement("label");
            colorLabel.className = "input-group-text";
            colorLabel.innerHTML = "Article " + (i + 1);
            const colorSelect = document.createElement("select");
            colorSelect.className = "form-select";
            colorSelect.innerHTML = `
                <option selected>Couleur</option>
                <option value="rouge">Rouge</option>
                <option value="bleu">Bleu</option>
                <option value="jaune">Jaune</option>
                <option value="vert">Vert</option>
                <option value="orange">Orange</option>
                <option value="violet">Violet</option>
                <option value="marron">Marron</option>
                <option value="noir">Noir</option>
                <option value="blanc">Blanc</option>
                <option value="gris">Gris</option>
                <option value="rose">Rose</option>
                <option value="cyan">Cyan</option>
                <option value="magenta">Magenta</option>
                <option value="3">Autre (Veuillez specifier dans la note)</option>
            `;
            colorDiv.appendChild(colorLabel);
            colorDiv.appendChild(colorSelect);

            const priceDiv = document.createElement("div");
            priceDiv.className = "input-group mb-3";
            const priceLabel = document.createElement("label");
            priceLabel.className = "input-group-text";
            priceLabel.innerHTML = "Article " + (i + 1);
            const priceInput = document.createElement("input");
            priceInput.className = "form-control";
            priceInput.type = "number";
            priceInput.placeholder = "Prix Unitaire";
            const priceUnit = document.createElement("span");
            priceUnit.className = "input-group-text";
            priceUnit.innerHTML = "DH";
            priceDiv.appendChild(priceLabel);
            priceDiv.appendChild(priceInput);
            priceDiv.appendChild(priceUnit);

            // Added this line to attach an event listener to the price input
            priceInput.addEventListener("input", computeTotal);

            const detailsDiv = document.createElement("div");
            detailsDiv.className = "mb-3";
            const detailsLabel = document.createElement("label");
            detailsLabel.className = "form-label";
            detailsLabel.innerHTML = "Details";
            const detailsTextarea = document.createElement("textarea");
            detailsTextarea.className = "form-control";
            detailsTextarea.rows = "3";
            detailsDiv.appendChild(detailsLabel);
            detailsDiv.appendChild(detailsTextarea);

            articleDiv.appendChild(typeDiv);
            articleDiv.appendChild(colorDiv);
            articleDiv.appendChild(priceDiv);
            articleDiv.appendChild(detailsDiv);

            // Inserting the dynamically generated content before the "Prix Total" div
            container.insertBefore(articleDiv, prixTotalDiv);
        }
    });

    function computeTotal() {
        const priceInputs = document.querySelectorAll(".dynamic-field input[placeholder='Prix Unitaire']");
        let total = 0;
        priceInputs.forEach(input => {
            const value = parseFloat(input.value);
            if (!isNaN(value)) {
                total += value;
            }
        });
        console.log("Computed Total: ", total); // This line is added for debugging
        document.querySelector("input[placeholder='Prix Total']").value = total; // Removed the extra space in 'Prix total' and "DH"
    }

    // Handling form submission
    const form = document.querySelector("form");
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Collect form data
        const formData = new FormData(form);

        // Send the form data to the server using fetch
        fetch("/submit", {
            method: "POST",
            body: formData
        })
            .then(response => response.json()) // Assuming the server responds with JSON
            .then(data => {
                console.log("Form submitted successfully:", data);
                // Handle success or redirection here
            })
            .catch(error => {
                console.error("Error submitting form:", error);
                // Handle errors here
            });
    });
});
