from django.http import HttpRequest
from scales.controllers import ConfBasicScalesController
from utils import general_error, deleteDataSession, delete_images

def conf_basic_scales_view(request: HttpRequest):
    if request.method == "GET":
        images_cata = request.session.get("form_images_cata", {})
        if images_cata:
            delete_images(list(images_cata.values()))
        deleteDataSession(request)
        controller = ConfBasicScalesController()
        return controller.get(request=request)
    elif request.method == "POST":
        controller = ConfBasicScalesController()
        return controller.post(request=request)
    else:
        return general_error(request, "Método no permitido")