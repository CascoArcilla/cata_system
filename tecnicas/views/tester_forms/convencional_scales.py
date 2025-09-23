from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from ...controllers import SesionController


def convencionalScales(req: HttpRequest):
    if not "id_order" in req.session:
        return redirect(reverse("cata_system:panel_configuracion_words"))

    session = SesionController.getSessionByCode(req.session["code_session"])

    context = {
        "session": session
    }

    return render(req, "tecnicas/forms_tester/convencional.html", context)
