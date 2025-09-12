from django.http import HttpRequest
from django.shortcuts import render
from ..models import SesionSensorial
from ..controllers import PalabrasController, CalificacionController


def sessionDetails(req: HttpRequest, session_code: str):
    if req.method == "GET":
        context = {}

        sesion = SesionSensorial.objects.get(codigo_sesion=session_code)
        context["sesion"] = sesion

        words = PalabrasController.getWordsInTechnique(sesion.tecnica)
        context["palabras"] = words

        rating = CalificacionController.getRatingsByTechnique(
            technique=sesion.tecnica)
        context["calificaciones"] = rating

        return render(req, "tecnicas/manage_sesions/detalles-sesion.html", context)
