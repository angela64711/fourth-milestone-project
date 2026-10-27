
/*
 * Commission payment processing with Stripe Elements.
 * Based on the Boutique Ado checkout implementation.
 * Django verifies the payment before confirming the order.
 */

// Retrieve Stripe configuration from the Django template.
const stripePublicKey = JSON.parse(
    document.getElementById('id_stripe_public_key').textContent
);

const clientSecret = JSON.parse(
    document.getElementById('id_client_secret').textContent
);

// Initialize Stripe and create the card input.
const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();

const style = {
    base: {
        color: '#383838',
        fontFamily: '"IBM Plex Mono", monospace',
        fontSize: '16px',
        '::placeholder': {
            color: '#777777'
        }
    },
    invalid: {
        color: '#b42318',
        iconColor: '#b42318'
    }
};

const card = elements.create('card', { style: style });
card.mount('#card-element');

// Payment form elements.
const form = document.getElementById('payment-form');
const submitButton = document.getElementById('submit-button');
const errorContainer = document.getElementById('card-errors');
const loadingOverlay = document.getElementById('loading-overlay');

// Display payment errors safely.
function showPaymentError(message) {
    errorContainer.textContent = message;
}

// Enable or disable the payment interface.
function setProcessing(processing) {
    submitButton.disabled = processing;
    card.update({ disabled: processing });

    loadingOverlay.hidden = !processing;
}

// Display real-time card validation errors.
card.on('change', function (event) {
    showPaymentError(event.error ? event.error.message : '');
});

// Handle payment submission.
form.addEventListener('submit', async function (event) {
    event.preventDefault();

    if (submitButton.disabled) {
        return;
    }

    showPaymentError('');
    setProcessing(true);

    try {
        // Stripe securely processes the card payment.
        const result = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card
            }
        });

        if (result.error) {
            showPaymentError(result.error.message);
            return;
        }

        if (
            !result.paymentIntent ||
            result.paymentIntent.status !== 'succeeded'
        ) {
            showPaymentError(
                'Payment has not been completed. Please check its status.'
            );
            return;
        }

        // Ask Django to verify the completed payment with Stripe.
        const csrfToken = form.querySelector(
            'input[name="csrfmiddlewaretoken"]'
        ).value;

        const verificationUrl = form.dataset.verifyUrl;

        const response = await fetch(verificationUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        });

        if (!response.ok) {
            throw new Error('Payment verification could not be completed.');
        }

        const data = await response.json();

        if (data.success && data.redirect_url) {
            window.location.assign(data.redirect_url);
            return;
        }

        showPaymentError(
            data.message || 'Unable to confirm your payment.'
        );

    } catch (error) {
        console.error('Commission payment error:', error);

        showPaymentError(
            'Unable to confirm your payment. Please do not pay again. ' +
            'Refresh the page to check your order status.'
        );
    } finally {
        setProcessing(false);
    }
});
