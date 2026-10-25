
document.addEventListener("DOMContentLoaded", function () {
    const preferencesForm = document.querySelector("#preferences-form");

    if (!preferencesForm) {
        return;
    }

    const authModalElement = document.querySelector("#commissionAuthModal");

    // Authentication modal for visitors who are not logged in.
    if (authModalElement) {
        const authModal = new bootstrap.Modal(authModalElement);

        preferencesForm.addEventListener("click", function (event) {
            if (event.target.closest("input, textarea, select, label, button")) {
                event.preventDefault();
                authModal.show();
            }
        });

        preferencesForm.addEventListener("submit", function (event) {
            event.preventDefault();
            authModal.show();
        });

        return;
    }

    // -------------------------------------------------
    // Limit moods and colours to two selections.
    // -------------------------------------------------

    function limitSelections(fieldsetId) {
        const fieldset = document.querySelector(fieldsetId);
        const checkboxes = fieldset.querySelectorAll('input[type="checkbox"]');

        function updateSelections() {
            const selected = Array.from(checkboxes).filter(
                checkbox => checkbox.checked
            ).length;

            checkboxes.forEach(function (checkbox) {
                checkbox.disabled = fieldset.disabled ||
                    (selected >= 2 && !checkbox.checked);
            });
        }

        fieldset.addEventListener("change", updateSelections);
        updateSelections();

        return updateSelections;
    }

    const updateMoods = limitSelections("#moods");
    const updateColours = limitSelections("#colours");

    // -------------------------------------------------
    // Creative direction: idea or surprise.
    // -------------------------------------------------

    const creativeDirections = document.querySelectorAll(
        'input[name="creative_direction"]'
    );

    const creativeFieldsets = [
        document.querySelector("#story"),
        document.querySelector("#moods"),
        document.querySelector("#colours"),
        document.querySelector("#imagery")
    ];

    function updateCreativeDirection() {
        const selectedDirection = document.querySelector(
            'input[name="creative_direction"]:checked'
        );

        const isSurprise = selectedDirection?.value === "surprise";

        creativeFieldsets.forEach(function (fieldset) {
            if (isSurprise) {
                fieldset.querySelectorAll("input, textarea, select").forEach(
                    function (input) {
                        if (input.type === "checkbox" || input.type === "radio") {
                            input.checked = false;
                        } else {
                            input.value = "";
                        }
                    }
                );
            }

            fieldset.disabled = isSurprise;
        });

        updateMoods();
        updateColours();
    }

    creativeDirections.forEach(function (radio) {
        radio.addEventListener("change", updateCreativeDirection);
    });

    updateCreativeDirection();

    // -------------------------------------------------
    // Artwork size depends on the selected format.
    // -------------------------------------------------

    const artworkFormats = document.querySelectorAll(
        'input[name="artwork_format"]'
    );

    const artworkSize = document.querySelector("#artwork-size");

    function updateArtworkSize() {
        const selectedFormat = document.querySelector(
            'input[name="artwork_format"]:checked'
        );

        const requiresSize = selectedFormat &&
            ["print", "framed"].includes(selectedFormat.value);

        artworkSize.disabled = !requiresSize;

        if (!requiresSize) {
            artworkSize.querySelectorAll('input[type="radio"]').forEach(
                function (radio) {
                    radio.checked = false;
                }
            );
        }
    }

    artworkFormats.forEach(function (radio) {
        radio.addEventListener("change", updateArtworkSize);
    });

    updateArtworkSize();
});
