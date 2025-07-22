from django.shortcuts import render
from ..controllers import EscalaController
from ..forms import SesionFirtsForm

def configuracionPanel(req):
    # escalas = EscalaController.getTypesScale()
    form_sesion = SesionFirtsForm()

    return render(req, "tecnicas/configuracion-panel.html", { "form_sesion": form_sesion })