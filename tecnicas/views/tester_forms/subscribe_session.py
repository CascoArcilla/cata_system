from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from utils import general_error
from tecnicas.controllers import LoginSessionTesterController


def subscribeSessionTester(req: HttpRequest):
    if req.method == "GET":
        return render(req, "tecnicas/forms_tester/subscribe_session.html")
    elif req.method == "POST":
        tester_user = req.user.username
        session_code = req.POST.get("code_session")
        if not tester_user or not session_code:
            return general_error("Se esperan credenciales")

        login_controller = LoginSessionTesterController()

        existCredentials = login_controller.existCredential(
            tester_user, session_code)
        if isinstance(existCredentials, dict):
            context = {"error": existCredentials["error"]}
            return render(req, "tecnicas/forms_tester/subscribe_session.html", context)

        tester = existCredentials[0]
        session = existCredentials[1]

        type_technique = session.tecnica.tipo_tecnica.nombre_tecnica

        if type_technique in ["escalas", "perfil flash", "sort", "perfil_ideal"]:
            response = login_controller.validateEntryLimitTesters(request=req)

        elif type_technique in ["rata", "cata"]:
            response = login_controller.validateEntryRataCata(request=req)

        elif type_technique == "napping":
            response = login_controller.validateEntryNapping(request=req)

        else:
            context = {
                "error": "La técnica usada en esta sesión es invalida o no ha sido implementada para ingresar a ella"
            }
            response = render(
                req, "tecnicas/forms_tester/subscribe_session.html", context)

        return response
    else:
        return JsonResponse({"message": "Método no valido"})
