from django.http import HttpRequest
from django.shortcuts import render
from controllers import ConfCodesController
from utils.delete_data_session import deleteDataSession
from analist.decorators.required_analist import required_analist
from django.shortcuts import redirect
from django.urls import reverse
from utils import delete_images


@required_analist(technique="escalas")
def conf_codes(request: HttpRequest):
    if not request.session.get("form_basic"):
        images_cata = request.session.get("form_images_cata", {})
        if images_cata:
            delete_images(list(images_cata.values()))
        deleteDataSession(request)
        return redirect(reverse('analist:scales:conf_basic_scales') + "?error=datos requeridos no encontrados")

    basic_data = request.session.get("form_basic")
    template = "scales/conf-codes-scales.html"

    if request.method == "GET": 
        conf_codes_controller = ConfCodesController(
            data=basic_data, template=template)

        return conf_codes_controller.getOrders(request)

    elif request.method == "POST":
        conf_codes_controller = ConfCodesController(
            data=basic_data, template=template, next_url='analist:scales:main_escalas')

        return conf_codes_controller.postOrders(request)
    else:
        return redirect(reverse('analist:scales:main_escalas') + "?error=metodo no permitido")
