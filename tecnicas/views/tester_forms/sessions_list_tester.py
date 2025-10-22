from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from tecnicas.controllers import ListSessionsTesterController


def sessionsListTester(req: HttpRequest, num_page: int):
    if req.method == "GET":
        view_controller = ListSessionsTesterController()
        contex_view = view_controller.getContext(req.user.user_catador, num_page)

        return render(req, "tecnicas/forms_tester/sessions_list_tester.html", contex_view)
    else:
        return JsonResponse({"message": "Método no permitido"})
