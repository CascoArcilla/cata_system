from django.shortcuts import render
from django.http import HttpRequest

from ..controllers  import TecnicaController

def selecionTecnica(req:HttpRequest):
    tipos = TecnicaController.getTypesTechnique()
    try:
        error : str = req.GET["error"]
        error = error.replace("_", " ")
        error = error.capitalize()

        return render(req, "tecnicas/create_sesion/seleccion-tecnica.html", context={"tipos":tipos, "error":error})
    except KeyError:
        return render(req, "tecnicas/create_sesion/seleccion-tecnica.html", context={"tipos":tipos})