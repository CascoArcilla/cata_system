from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from ...controllers import SesionController, MainTesterFormController
from ...models import Orden


def mainTesterForm(req: HttpRequest):
    session = SesionController.getSessionByCodePanelTester(
        req.session["code_session"])

    context = {
        "session": session
    }

    if req.method == "GET":
        return render(req, "tecnicas/forms_tester/main_tester.html", context)
    elif req.method == "POST":
        if req.POST["action"] == "start_posting":
            view_controller = MainTesterFormController(
                req.session["code_session"], req.session["cata_username"])

            order = view_controller.checkAssignOrder()
            if not isinstance(order, dict):
                req.session["id_order"] = order.id
                context["error"] = "Catador tiene orden"
                return render(req, "tecnicas/forms_tester/main_tester.html", context)

            order = view_controller.assignOrder()
            if isinstance(order, dict):
                context["error"] = order["error"]
                return render(req, "tecnicas/forms_tester/main_tester.html", context)

            print(order)
            return render(req, "tecnicas/forms_tester/main_tester.html", context)
        elif req.POST["action"] == "close_session":
            pass
        else:
            context["error"] = "Acción sin especificar"
            return render(req, "tecnicas/forms_tester/main_tester.html", context)
    else:
        return JsonResponse({"error": "metodo no permitido"})
