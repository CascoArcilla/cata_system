from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.utils import general_error
from tecnicas.controllers import LoginTesterController


def loginSessionTester(req: HttpRequest):
    if req.method == "GET":
        return render(req, "tecnicas/forms_tester/login_session.html")
    elif req.method == "POST":
        tester_user = req.user.username
        session_code = req.POST.get("code_session")
        if not tester_user or not session_code:
            return general_error("Se esperan credenciales")

        login_controller = LoginTesterController()

        existCredentials = login_controller.existCredential(
            tester_user, session_code)
        if isinstance(existCredentials, dict):
            context = {"error": existCredentials["error"]}
            return render(req, "tecnicas/forms_tester/login_session.html", context)

        tester = existCredentials[0]
        session = existCredentials[1]

        type_technique = session.tecnica.tipo_tecnica.nombre_tecnica

        if type_technique == "escalas":
            response = login_controller.validateEntryEscalas()
        elif type_technique == "rata":
            response = login_controller.validateEntryRATA()
        else:
            context = {
                "error": "La técnica usada en esta sesión o ha sido implementada para ingresar a ella"
            }
            response = render(
                req, "tecnicas/forms_tester/login_session.html", context)

        return response
    else:
        return JsonResponse({"message": "Método no valido"})
