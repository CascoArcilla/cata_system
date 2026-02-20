from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode
from django.core.exceptions import PermissionDenied
# El analista se le denomino como presentador, para esta version aun se conserva el modelo con nombre de presentador.


def required_analist(technique: str = "escalas"):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                params = { 'technique': technique }
                query_string = urlencode(params)
                url_login = reverse("analist:login_analista")
                url_destinny = f"{url_login}?{query_string}"
                return redirect(url_destinny)

            if not hasattr(request.user, "user_presentador"):
                raise PermissionDenied(
                    "Solo los presentadores pueden acceder a esta vista")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
