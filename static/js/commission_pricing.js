
document.addEventListener("DOMContentLoaded", function () {
    const summary = document.querySelector("#commission-summary");
    const customerForm = document.querySelector("#customer-details-form");

    if (!summary || !customerForm) {
        return;
    }

    const deliveryRegion = customerForm.querySelector(
        'select[name="delivery_region"]'
    );

    // Digital commissions already have their final price.
    if (!deliveryRegion) {
        return;
    }

    const artworkPrice = Number(summary.dataset.artworkPrice);

    const shippingPrices = {
        europe_uk: Number(summary.dataset.shippingEurope),
        international: Number(summary.dataset.shippingInternational)
    };

    const shippingAmount = summary.querySelector("#shipping-amount");
    const commissionTotal = summary.querySelector("#commission-total");

    function formatPrice(amount) {
        return `€${amount.toFixed(2)}`;
    }

    function updatePricing() {
        const region = deliveryRegion.value;

        if (!Object.hasOwn(shippingPrices, region)) {
            shippingAmount.textContent = "Select delivery region";
            commissionTotal.textContent = "Pending shipping";
            return;
        }

        const shipping = shippingPrices[region];

        shippingAmount.textContent = formatPrice(shipping);
        commissionTotal.textContent = formatPrice(
            artworkPrice + shipping
        );
    }

    deliveryRegion.addEventListener("change", updatePricing);

    // Also update when returning to previously entered details.
    updatePricing();
});
