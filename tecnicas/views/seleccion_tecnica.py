from django.shortcuts import render

from ..controllers  import TecnicaController

def selecionTecnica(req):
    tipos = TecnicaController.getTypesTechnique()
    return render(req, "tecnicas/seleccion-tecnica.html", context={"tipos":tipos})