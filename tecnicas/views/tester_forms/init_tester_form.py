from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.controllers import MainTesterFormController, ParticipacionController
from tecnicas.models import SesionSensorial


def initTesterForm(req: HttpRequest, code_sesion: str):
    session = SesionSensorial.objects.get(codigo_sesion=code_sesion)

    context = {
        "session": session
    }

    view_controller = MainTesterFormController(
        code_sesion, req.user.username)

    template_url = "tecnicas/forms_tester/init_session.html"

    if req.method == "GET":
        order = view_controller.checkAndAssignOrder()

        if isinstance(order, dict):
            context["error"] = order["error"]
            return render(req, template_url, context)

        is_end = view_controller.isEndedSession(
            repetition=session.tecnica.repeticion)

        req.session["id_order"] = order.id
        context["has_ended"] = is_end

        if is_end:
            context["message"] = "El catador ha terminado de realizar su evaluación, espere instrucciones del presentador"

        return render(req, template_url, context)
    elif req.method == "POST":
        if req.POST["action"] == "start_posting":
            parameters = {
                "code_sesion": code_sesion
            }

            update_participation = ParticipacionController.enterSession(
                tester=req.user.user_catador, session=session)
            if isinstance(update_participation, dict):
                context["error"] = update_participation["error"]
                return render(req, template_url, context)

            req.session["id_participation"] = update_participation.id
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
