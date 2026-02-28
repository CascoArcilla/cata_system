# usuarios/middleware/catador_middleware.py
from django.core.exceptions import PermissionDenied


class TesterAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if path.startswith('/sensorial/testers/'):
            if not request.user.is_authenticated:
                from django.shortcuts import redirect
                return redirect("cata_system:catador_login")

            if not hasattr(request.user, 'user_catador'):
                from django.shortcuts import redirect
                return redirect("cata_system:catador_login")

        return self.get_response(request)
