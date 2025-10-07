from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from ..utils import general_error
from ..controllers import LoginTesterController


def testerLogin(req: HttpRequest):
    if req.method == "GET":
        return render(req, "tecnicas/cata-login.html")
    elif req.method == "POST":
        tester_user = req.POST.get("user_tester")
        session_code = req.POST.get("code_session")
        if not tester_user or not session_code:
            return general_error("Se esperan credenciales")

        login_controller = LoginTesterController()

        existCredentials = login_controller.existCredential(
            tester_user, session_code)
        if isinstance(existCredentials, dict):
            context = {"error": existCredentials["error"]}
            return render(req, "tecnicas/cata-login.html", context)

        tester = existCredentials[0]
        session = existCredentials[1]

        taster_participation = login_controller.validateEntry()
        if isinstance(taster_participation, dict):
            context = {"error": taster_participation["error"]}
            return render(req, "tecnicas/cata-login.html", context)

        req.session["cata_username"] = tester_user
        req.session["id_cata"] = tester.id
        req.session["code_session"] = session_code
        req.session["id_techniqe"] = session.tecnica.id
        req.session["id_participation"] = taster_participation.id

        req.session.set_expiry(15*60)

        response = redirect(reverse("cata_system:catador_main"))
        response.set_cookie('id_participacion',
                            taster_participation.id, max_age=60*60*24)
        return response
    else:
        return render(req, "tecnicas/cata-login.html")
