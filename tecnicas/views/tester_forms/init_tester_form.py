from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.controllers import SesionController, MainTesterFormController, ParticipacionController


def initTesterForm(req: HttpRequest, code_sesion: str):
    session = SesionController.getSessionByCodePanelTester(code_sesion)

    context = {
        "session": session
    }

    view_controller = MainTesterFormController(
        code_sesion, req.user.username)

    template_url = "tecnicas/forms_tester/init_session.html"

    if req.method == "GET":
        order = view_controller.checkAssignOrder()

        if not isinstance(order, dict):
            req.session["id_order"] = order.id
            is_end = view_controller.isEndedSession(
                repetition=session.tecnica.repeticion)

            if is_end:
                context["message"] = "El catador ha terminado de realizar su evaluación, espere instrucciones del presentador"
                context["has_ended"] = True

        return render(req, template_url, context)
    elif req.method == "POST":
        if req.POST["action"] == "start_posting":
            parameters = {
                "code_sesion": code_sesion
            }

            if "id_order" in req.session:
                update_participation = ParticipacionController.enterSession(
                    tester=req.user.user_catador, session=session)
                if isinstance(update_participation, dict):
                    context["error"] = update_participation["error"]
                    return render(req, template_url, context)

                return redirect(reverse("cata_system:session_convencional", kwargs=parameters))

            order = view_controller.assignOrder()
            if isinstance(order, dict):
                context["error"] = order["error"]
                return render(req, template_url, context)

            update_participation = ParticipacionController.enterSession(
                tester=req.user.user_catador, session=session)
            if isinstance(update_participation, dict):
                context["error"] = update_participation["error"]
                return render(req, template_url, context)

            return redirect(reverse("cata_system:session_convencional", kwargs=parameters))
        elif req.POST["action"] == "exit_session":
            response = ParticipacionController.outSession(
                tester=req.user.user_catador, session=session)
            if isinstance(response, dict):
                context["error"] = response["error"]
            return render(req, template_url, context)
        else:
            context["error"] = "Acción sin especificar"
            return render(req, template_url, context)
    else:
        return JsonResponse({"error": "metodo no permitido"})

# req.session["cata_username"] = tester_user
# req.session["id_cata"] = tester.id
# req.session["code_session"] = session_code
# req.session["id_techniqe"] = session.tecnica.id
# req.session["id_participation"] = taster_participation.id

# response.set_cookie('id_participacion', taster_participation.id, max_age=60*60*24)
