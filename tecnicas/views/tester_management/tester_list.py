from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from controllers import TesterListController
from utils import general_error


def testerList(req: HttpRequest, num_page: int):
    if req.method == "GET":
        url_home = req.session.get("sensorial_url_main")
        view_controller = TesterListController(page=num_page)
        view_context = view_controller.getContext()
        view_context["url_home"] = reverse(url_home)
        return render(req, "manage_tester/tester-list.html", view_context)
    else:
        return general_error("Método no permitido")
