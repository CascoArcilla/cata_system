from django.shortcuts import render
from ..controllers import EscalaController

def configuracionPanel(req):
    # escalas = EscalaController.getTypesScale()
    escalas = [1,1]

    return render(req, "tecnicas/configuracion-panel.html", { "escalas":escalas })