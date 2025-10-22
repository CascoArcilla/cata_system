from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied


def required_presenter(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("cata_system:autenticacion")
        
        if not hasattr(request.user, "user_presentador"):
            raise PermissionDenied(
                "Solo los presentadores pueden acceder a esta vista")
        return view_func(request, *args, **kwargs)
    return wrapper