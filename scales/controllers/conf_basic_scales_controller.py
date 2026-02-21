from django.http import HttpRequest
from controllers import ConfBasicController
from scales.forms import ConfBasicScalesForm

class ConfBasicScalesController(ConfBasicController):
    def __init__(self):
        super().__init__(
            template_name="scales/conf-basic-scales.html",
            next_url="cata_system:panel_configuracion_tags",
            form_class=ConfBasicScalesForm,
        )

    def get(self, request: HttpRequest):
        return super().get(request=request, name_tecnica="escalas")

    def post(self, request: HttpRequest):
        return super().post(request=request, name_tecnica="escalas")