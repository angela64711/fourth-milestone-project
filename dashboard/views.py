from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


@login_required
def dashboard(request):
    """
    Display the dashboard to superusers and authorized artists.
    """
    user = request.user

    if not (user.is_superuser or user.groups.filter(name="Artists").exists()):
        raise PermissionDenied

    return render(request, "dashboard/dashboard.html")
