from django.http import HttpRequest
from django.shortcuts import render
from controllers import SesionController
from scales.controllers import ListSessionsScalesController
from analist.decorators.required_analist import required_analist
from utils import general_error


@required_analist(technique="escalas")
def list_sessions_scales(req: HttpRequest, page: int):
    if req.method == "GET":
        controller = ListSessionsScalesController()
        return controller.getSessionByCreator(req, page)
    else:
        general_error("Método no permitido")