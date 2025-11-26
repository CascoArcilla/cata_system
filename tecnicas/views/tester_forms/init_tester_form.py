from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from tecnicas.controllers import InitSessionEscalasController, InitSessionRATAController, InitSessionPFController, InitSessionSortController
from tecnicas.models import SesionSensorial


def initTesterForm(req: HttpRequest, code_sesion: str):
    session = SesionSensorial.objects.get(codigo_sesion=code_sesion)
    type_technique = session.tecnica.tipo_tecnica.nombre_tecnica
    template_url = "tecnicas/forms_tester/init_scales_test.html"

    if req.method == "GET":
        if type_technique == "escalas":
            view_controller = InitSessionEscalasController(
                sensorial_session=session, user_tester=req.user.user_catador)
            response = view_controller.controllGet(request=req)

        elif type_technique == "rata" or type_technique == "cata":
            view_controller = InitSessionRATAController(
                sensorial_session=session, user_tester=req.user.user_catador)
            response = view_controller.controllGet(request=req)

        elif type_technique == "perfil flash":
            view_controller = InitSessionPFController(
                sensorial_session=session, user_tester=req.user.user_catador)
            response = view_controller.controllGet(request=req)

        elif type_technique == "sort":
            view_controller = InitSessionSortController(
                sensorial_session=session, user_tester=req.user.user_catador)
            response = view_controller.controllGet(request=req)

        else:
            context = {
                "session": session,
                "error": "La técnica usada en esta sesión o ha sido implementada para ingresar a ella"
            }
            response = render(
                req, template_url, context)

        return response

    elif req.method == "POST":
        if type_technique == "escalas" or type_technique == "rata" or type_technique == "cata":
            view_controller = InitSessionEscalasController(
                sensorial_session=session, user_tester=req.user.user_catador)
            response = view_controller.controllPost(request=req)

        elif type_technique == "perfil flash":
            view_controller = InitSessionPFController(
                sensorial_session=session, user_tester=req.user.user_catador)
            response = view_controller.controllPost(request=req)

        elif type_technique == "sort":
            view_controller = InitSessionSortController(
                sensorial_session=session, user_tester=req.user.user_catador)
            response = view_controller.controllPost(request=req)
        
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
