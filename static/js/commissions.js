document.addEventListener("DOMContentLoaded", function () {
    const preferencesForm = document.querySelector("#preferences-form");
    const authModalElement = document.querySelector("#commissionAuthModal");

    // The modal only exists for unauthenticated visitors.
    if (!preferencesForm || !authModalElement) {
        return;
    }

    const authModal = new bootstrap.Modal(authModalElement);

    // Show authentication options when a visitor interacts with the form.
    preferencesForm.addEventListener("click", function (event) {
        if (event.target.closest("input, textarea, select, label, button")) {
            event.preventDefault();
            authModal.show();
        }
    });

    // Prevent unauthenticated form submissions.
    preferencesForm.addEventListener("submit", function (event) {
        event.preventDefault();
        authModal.show();
    });
});