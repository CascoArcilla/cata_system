from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.models import SesionSensorial
from tecnicas.utils import noValidTechnique
from tecnicas.controllers import DetallesController, DetallesEscalasController, DetallesCATAController, DetallesPFController, DetallesSortController, DetallesNappingController, DetallesIdealController
from tecnicas.constants import URLS_LIST_SESSIONES


def sessionDetails(req: HttpRequest, session_code: str):
    technique_selected = req.session.get("technique_selected") or "general"
    back_url = URLS_LIST_SESSIONES.get(technique_selected) or URLS_LIST_SESSIONES["general"]

    if req.method == "GET":
        if "message" in req.GET:
            message = req.GET.get("message")
        else:
            message = ""

        try:
            sensorial_session = SesionSensorial.objects.get(
                codigo_sesion=session_code)
        except SesionSensorial.DoesNotExist:
            return noValidTechnique(
                params={"page": 1},
                query_params={"message": "Sesión no encontrada"},
                name_view=back_url
            )

        use_techinique = sensorial_session.tecnica.tipo_tecnica.nombre_tecnica

        if use_techinique == "escalas":
            controller_view = DetallesEscalasController(
                session=sensorial_session,
                template="tecnicas/manage_sesions/details-session.html"
            )

            response = controller_view.controllGetResponse(
                request=req, message=message)

        elif use_techinique == "rata":
            controller_view = DetallesEscalasController(
                session=sensorial_session,
                template="tecnicas/manage_sesions/details-session-rata.html",
                back_url=back_url,
                home_url=req.session.get("sensorial_url_main")
            )

            response = controller_view.controllGetResponse(
                request=req, message=message)

        elif use_techinique == "cata":
            controller_view = DetallesCATAController(
                session=sensorial_session
            )

            response = controller_view.controllGetResponse(
                request=req, message=message)

        elif use_techinique == "perfil flash":
            controller_view = DetallesPFController(
                session=sensorial_session,
                back_url=back_url,
                home_url=req.session.get("sensorial_url_main")
            )
            response = controller_view.controllGetResponse(
                request=req, message=message)

        elif use_techinique == "sort":
            controller_view = DetallesSortController(
                session=sensorial_session,
                back_url=back_url,
                home_url=req.session.get("sensorial_url_main")
            )
            response = controller_view.controllGetResponse(
                request=req, message=message)

        elif use_techinique == "napping":
            controller_view = DetallesNappingController(
                session=sensorial_session,
                back_url=back_url,
                home_url=req.session.get("sensorial_url_main")
            )
            response = controller_view.controllGetResponse(
                request=req, message=message)

        elif use_techinique == "perfil_ideal":
            controller_view = DetallesIdealController(
                session=sensorial_session,
                back_url=back_url,
                home_url=req.session.get("sensorial_url_main")
            )
            response = controller_view.controllGetResponse(
                request=req, message=message)

        else:
            response = noValidTechnique(
                params={"page": 1},
                query_params={
                    "message": "Al parecer la sesión usa una técnica que aun no se ha implementado para ver detalles"
                },
                name_view=back_url
            )

        return response

    elif req.method == "POST":
        try:
            sensorial_session = SesionSensorial.objects.get(
                codigo_sesion=session_code)
        except SesionSensorial.DoesNotExist:
            return noValidTechnique(
                params={"page": 1},
                query_params={"message": "Sesión no encontrada"},
                name_view=back_url
            )

        use_techinique = sensorial_session.tecnica.tipo_tecnica.nombre_tecnica
        controller_view = DetallesController(sensorial_session)

        action = req.POST.get("action")

        if use_techinique in ["escalas", "rata", "cata", "perfil flash", "sort", "perfil_ideal"]:
            if action == "start_session":
                response = controller_view.startRepetition(
                    presenter=req.user.user_presentador, request=req)

            elif action == "delete_session":
                controller_view.deleteSesorialSession()
                response = redirect(
                    reverse(back_url, kwargs={"page": 1}))

        elif use_techinique == "napping":
            controller_view = DetallesNappingController(
                session=sensorial_session,
                back_url=back_url
            )

            response = controller_view.controllPostResponse(
                request=req, action=action)

        else:
            response = controller_view.controllGetResponse(
                error="No se reconoce la acción a realizar")

        return response
    else:
        return JsonResponse({"error": "Método no permitido"})
