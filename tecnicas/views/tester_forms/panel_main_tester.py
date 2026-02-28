from django.contrib.auth import logout
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect


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
        return render(req, "forms_tester/main_panel_tester.html", view_context)
    elif req.method == "POST":
        if req.POST["action"] == "exit_session":
            logout(req)
            return redirect("cata_system:catador_login")
        else:
            return JsonResponse({"message": "Acción no definida"})
    else:
        return JsonResponse({"message": "Método no permitido"})
