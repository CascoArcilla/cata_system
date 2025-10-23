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

        taster_participation = login_controller.validateEntry()
        if isinstance(taster_participation, dict):
            context = {"error": taster_participation["error"]}
            return render(req, "tecnicas/forms_tester/login_session.html", context)

        params = {
            "code_sesion": session_code
        }

        return redirect(reverse("cata_system:catador_init_session", kwargs=params))
    else:
        return JsonResponse({"message": "Método no valido"})
