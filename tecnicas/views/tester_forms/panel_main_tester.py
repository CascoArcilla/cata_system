from django.http import HttpRequest, JsonResponse
from django.shortcuts import render


def mainPanelTester(req: HttpRequest):
    if req.method == "GET":
        view_context = {
            "name": f"{req.user.first_name} {req.user.last_name}",
            "username": req.user.username,
            "email": req.user.email,
            "phone": req.user.user_catador.telefono,
            "genere": req.user.user_catador.genero,
            "birthday": req.user.user_catador.nacimiento
        }
        return render(req, "tecnicas/forms_tester/main_panel_tester.html", view_context)
    else:
        return JsonResponse({"message": "Método no permitido"})
