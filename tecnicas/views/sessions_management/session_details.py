from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.models import SesionSensorial
from tecnicas.utils import noValidTechnique
from ...controllers import DetallesEscalasController


def sessionDetails(req: HttpRequest, session_code: str):
    if req.method == "GET":
        if "message" in req.GET:
            message = req.GET.get("message")
        else:
            message = ""

        sensorial_session = SesionSensorial.objects.get(
            codigo_sesion=session_code)
        use_techinique = sensorial_session.tecnica.tipo_tecnica.nombre_tecnica

        if use_techinique == "escalas" or use_techinique == "rata":
            controller_view = DetallesEscalasController(
                session=sensorial_session)
            response = controller_view.getResponse(
                request=req, message=message)
        else:
            response = noValidTechnique(
                params={"page": 1},
                query_params={
                    "message": "Al parecer la sesión usa una técnica que aun no se ha implementado para ver detalles"
                },
                name_view="cata_system:panel_sesiones"
            )

        return response
    elif req.method == "POST":
        sensorial_session = SesionSensorial.objects.get(
            codigo_sesion=session_code)
        use_techinique = sensorial_session.tecnica.tipo_tecnica.nombre_tecnica

        if use_techinique == "escalas" or use_techinique == "rata":
            controller_view = DetallesEscalasController(sensorial_session)

            if req.POST["action"] == "start_session":
                response = controller_view.startRepetition(
                    presenter=req.user.user_presentador, request=req)
            elif req.POST.get("action") == "delete_session":
                controller_view.deleteSesorialSession()
                response = redirect(
                    reverse("cata_system:panel_sesiones", kwargs={"page": 1}))
            else:
                response = controller_view.getResponse(
                    error="No se reconoce la acción a realizar")
        else:
            response = noValidTechnique()

        return response
    else:
        return JsonResponse({"error": "Método no permitido"})
