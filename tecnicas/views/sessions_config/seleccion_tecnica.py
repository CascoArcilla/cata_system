from django.shortcuts import render
from django.http import HttpRequest
from tecnicas.controllers  import TecnicaController

def selecionTecnica(req:HttpRequest):
    tipos = TecnicaController.getTypesTechnique()
    error = ""

    if req.GET.get("error"):
        error = req.GET.get("error")
        error = error.replace("_", " ")
        error = error.capitalize()
        return render(req, "tecnicas/create_sesion/select-tecnica.html", context={"tipos":tipos, "error":error})

    return render(req, "tecnicas/create_sesion/select-tecnica.html", context={"tipos":tipos})