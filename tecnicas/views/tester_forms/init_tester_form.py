from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.controllers import InitSessionTesterController, ParticipacionController
from tecnicas.models import SesionSensorial


def initTesterForm(req: HttpRequest, code_sesion: str):
    session = SesionSensorial.objects.get(codigo_sesion=code_sesion)
    type_technique = session.tecnica.tipo_tecnica.nombre_tecnica
    template_url = "tecnicas/forms_tester/init_session.html"

    view_controller = InitSessionTesterController(
        sensorial_session=session, user_tester=req.user.user_catador)

    if req.method == "GET":
        if type_technique == "escalas":
            response = view_controller.controllGetEscalas(request=req)
        elif type_technique == "rata":
            response = view_controller.controllGetRATA(request=req)
        else:
            context = {
                "session": session,
                "error": "La técnica usada en esta sesión o ha sido implementada para ingresar a ella"
            }
            response = render(
                req, template_url, context)

        return response
    elif req.method == "POST":
        if type_technique == "escalas" or type_technique == "rata":
            response = view_controller.controllPostEscalas(request=req)
        else:
            context = {
                "session": session,
                "error": "Esta opción aun no esta disponible para la técnica usada por la sesión"
            }
            response = render(
                req, template_url, context)

        return response
    else:
        return JsonResponse({"error": "metodo no permitido"})
