from django.http import HttpRequest
from django.shortcuts import render
from controllers import TesterListController
from utils import general_error


def testerList(req: HttpRequest, num_page: int):
    if req.method == "GET":
        view_controller = TesterListController(page=num_page)
        view_context = view_controller.getContext()
        return render(req, "tecnicas/manage_tester/tester-list.html", view_context)
    else:
        return general_error("Método no permitido")
