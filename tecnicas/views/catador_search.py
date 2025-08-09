from django.http import HttpRequest
from django.shortcuts import render
from django.db import Error
from ..forms import CatadorForm
from ..models import Catador

def searchCatador(req : HttpRequest):
    if req.method == "GET":
        try:
            user = req.GET["user"]
        except:
            user = False
        
        context = {}
        if user:
            try:
                catador = Catador.objects.get(usuarioCatador=user)
                print(catador.fechaNacimiento)
                context["form_catador"] = CatadorForm(instance=catador)
            except Error:
                context["error"] = "usuario no encontrado"

            return render(req, "tecnicas/catador-buscar.html", context)

        return render(req, "tecnicas/catador-buscar.html")