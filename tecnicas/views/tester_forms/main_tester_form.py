from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from ...controllers import SesionController, MainTesterFormController, ParticipacionController


def mainTesterForm(req: HttpRequest):
    session = SesionController.getSessionByCodePanelTester(
        req.session["code_session"])

    context = {
        "session": session
    }

    view_controller = MainTesterFormController(
        req.session["code_session"], req.session["cata_username"])

    if req.method == "GET":
        order = view_controller.checkAssignOrder()

        if not isinstance(order, dict):
            req.session["id_order"] = order.id
            is_end = view_controller.isEndedSession(
                id_participation=req.session["id_participation"], repetition=session.tecnica.repeticion)
            
            if is_end:
                print("Estoy dentro y termine [0_0]")
                context["message"] = "El catador ha terminado de realizar su evaluación, espere instrucciones del presentador"
                context["has_ended"] = True

        return render(req, "tecnicas/forms_tester/main_tester.html", context)
    elif req.method == "POST":
        if req.POST["action"] == "start_posting":
            if "id_order" in req.session:
                update_participation = ParticipacionController.enterSession(
                    id_participation=req.session["id_participation"])
                if isinstance(update_participation, dict):
                    context["error"] = update_participation["error"]
                    return render(req, "tecnicas/forms_tester/main_tester.html", context)

                return redirect(reverse("cata_system:session_convencional"))

            order = view_controller.assignOrder()
            if isinstance(order, dict):
                context["error"] = order["error"]
                return render(req, "tecnicas/forms_tester/main_tester.html", context)

            update_participation = ParticipacionController.enterSession(
                id_participation=req.session["id_participation"])
            if isinstance(update_participation, dict):
                context["error"] = update_participation["error"]
                return render(req, "tecnicas/forms_tester/main_tester.html", context)

            return redirect(reverse("cata_system:session_convencional"))
        elif req.POST["action"] == "close_session":
            req.session.flush()
            return redirect(reverse("cata_system:catador_login"))
        elif req.POST["action"] == "exit_session":
            response = ParticipacionController.outSession(
                req.session["id_participation"])
            if isinstance(response, dict):
                context["error"] = response["error"]
            return render(req, "tecnicas/forms_tester/main_tester.html", context)
        else:
            context["error"] = "Acción sin especificar"
            return render(req, "tecnicas/forms_tester/main_tester.html", context)
    else:
        return JsonResponse({"error": "metodo no permitido"})
