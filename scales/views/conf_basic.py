from django.http import HttpRequest
from scales.controllers import ConfBasicScalesController
from utils import general_error, deleteDataSession

def conf_basic_scales_view(request: HttpRequest):
    if request.method == "GET":
        deleteDataSession(request)
        controller = ConfBasicScalesController()
        return controller.get(request=request)
    elif request.method == "POST":
        controller = ConfBasicScalesController()
        return controller.post(request=request)
    else:
        return general_error(request, "Método no permitido")