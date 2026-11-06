/* jshint esversion: 11 */

document.addEventListener("DOMContentLoaded", () => {
    const grid = document.querySelector("#cover-artwork-grid");
    const toggleButton = document.querySelector("#toggle-cover-artworks");

    if (!grid || !toggleButton) return;

    const items = Array.from(grid.querySelectorAll(".cover-artwork-item"));
    let expanded = false;

    function updateGrid() {
        items.forEach((item, index) => {
            const selected = item.querySelector("input[type='radio']:checked");

            item.hidden = !expanded && index >= 8 && !selected;
        });

        toggleButton.textContent = expanded ? "Show Less" : "Show All";
        toggleButton.setAttribute("aria-expanded", String(expanded));
    }

    toggleButton.addEventListener("click", () => {
        expanded = !expanded;
        updateGrid();
    });

    grid.addEventListener("change", updateGrid);

    updateGrid();
});
