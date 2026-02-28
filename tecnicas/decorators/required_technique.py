# Decorador para verificar que el usuario tiene una tecnica seleccionada en variable de sesion, sino se intenta acceder a una vista main de la tecnica, en caso no encontarla se cierra la sesion y se manda a logearse

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.constants import URLS_MAIN_TECHNIQUE


def required_technique(name_technique: str):
    def view_func(view_func):
        def wrapper(request, *args, **kwargs):
            technique_selected = request.session.get("technique_selected")

            if technique_selected not in URLS_MAIN_TECHNIQUE:
                logout(request)
                return redirect(
                    reverse("cata_system:autenticacion"),
                    error="No tienes una tecnica seleccionada"
                )

            if technique_selected != name_technique and request.method == "GET":
                return redirect(
                    reverse(URLS_MAIN_TECHNIQUE.get(technique_selected)),
                    error="Se intentado acceder a una técnica que no tienes seleccionada"
                )

            return view_func(request, *args, **kwargs)
        return wrapper
    return view_func
