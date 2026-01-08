from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.models import SesionSensorial
from tecnicas.utils import noValidTechnique
from tecnicas.controllers import DetallesController, DetallesEscalasController, DetallesCATAController, DetallesPFController, DetallesSortController, DetallesNappingController


def sessionDetails(req: HttpRequest, session_code: str):
    if req.method == "GET":
        if "message" in req.GET:
            message = req.GET.get("message")
        else:
            message = ""

        try:
            sensorial_session = SesionSensorial.objects.get(
                codigo_sesion=session_code)
        except SesionSensorial.DoesNotExist:
            return noValidTechnique(params={"page": 1}, query_params={"message": "Sesión no encontrada"}, name_view="cata_system:panel_sesiones")

        use_techinique = sensorial_session.tecnica.tipo_tecnica.nombre_tecnica

        if use_techinique == "escalas" or use_techinique == "rata":
            controller_view = DetallesEscalasController(
                session=sensorial_session)
            response = controller_view.controllGetResponse(
                request=req, message=message)

        elif use_techinique == "cata":
            controller_view = DetallesCATAController(
                session=sensorial_session)
            response = controller_view.controllGetResponse(
                request=req, message=message)

        elif use_techinique == "perfil flash":
            controller_view = DetallesPFController(session=sensorial_session)
            response = controller_view.controllGetResponse(
                request=req, message=message)

        elif use_techinique == "sort":
            controller_view = DetallesSortController(session=sensorial_session)
            response = controller_view.controllGetResponse(
                request=req, message=message)

        elif use_techinique == "napping":
            controller_view = DetallesNappingController(
                session=sensorial_session)
            response = controller_view.controllGetResponse(
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
        try:
            sensorial_session = SesionSensorial.objects.get(
                codigo_sesion=session_code)
        except SesionSensorial.DoesNotExist:
            return noValidTechnique(params={"page": 1}, query_params={"message": "Sesión no encontrada"}, name_view="cata_system:panel_sesiones")

        use_techinique = sensorial_session.tecnica.tipo_tecnica.nombre_tecnica
        controller_view = DetallesController(sensorial_session)

        action = req.POST.get("action")

        if use_techinique in ["escalas", "rata", "cata", "perfil flash", "sort"]:
            if action == "start_session":
                response = controller_view.startRepetition(
                    presenter=req.user.user_presentador, request=req)

            elif action == "delete_session":
                controller_view.deleteSesorialSession()
                response = redirect(
                    reverse("cata_system:panel_sesiones", kwargs={"page": 1}))

        elif use_techinique == "napping":
            controller_view = DetallesNappingController(
                session=sensorial_session)

            response = controller_view.controllPostResponse(
                request=req, action=action)

        else:
            response = controller_view.controllGetResponse(
                error="No se reconoce la acción a realizar")

        return response
    else:
        return JsonResponse({"error": "Método no permitido"})
