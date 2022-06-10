// deletion alert 
const deletionForms = document.querySelectorAll(".deletion-forms");
deletionForms.forEach((form) => {
    form.addEventListener("submit", (event) => {
        const response = confirm(
            "This action will permanently delete the item. Click on okay to continue."
        );
        if (!response) {
            event.preventDefault();
        }
    });
});


const alertContainer = document.querySelector(".alert-container");
function hideAlert() {
    alertContainer?.classList.add("hide");
}