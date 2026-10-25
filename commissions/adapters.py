from django.urls import reverse

from allauth.account.adapter import DefaultAccountAdapter


class CommissionAccountAdapter(DefaultAccountAdapter):
    """Return customers to their commission after email verification."""

    def get_email_verification_redirect_url(self, email_address):
        request = self.request

        if (
            request
            and request.user.is_authenticated
            and request.user.pk == email_address.user_id
            and "commission_creative" in request.session
        ):
            return reverse("commissions:customer_details")

        return super().get_email_verification_redirect_url(email_address)
