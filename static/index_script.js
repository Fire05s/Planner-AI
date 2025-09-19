document.addEventListener("DOMContentLoaded", () => {
    // Expanding parts menu script
    const yesRadio = document.getElementById("yesParts");
    const noRadio = document.getElementById("noParts");
    const yesDetails = document.getElementById("yes-details");
    const partsInput = document.getElementById("addParts");

    function updateVisibility() {
        yesDetails.style.display = yesRadio.checked ? "block" : "none";
        partsInput.value = 1;
    }

    yesRadio.addEventListener("change", updateVisibility);
    noRadio.addEventListener("change", updateVisibility);

    // Prevent page refresh on form submission
    const form = document.getElementById("addTaskForm");
    form.addEventListener("submit", async function (e) {
        e.preventDefault(); // stop normal refresh

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: formData
            });

            const result = await response.text(); // Flask returns plain text now
            console.log("Server response:", result);

            // close modal and reset form
            const modal = bootstrap.Modal.getInstance(document.getElementById("addTaskModal"));
            modal.hide();
            form.reset();

        } catch (err) {
            console.error("Error submitting form:", err);
        }
    });
});