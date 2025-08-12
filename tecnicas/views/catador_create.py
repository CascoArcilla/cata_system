from django.http import HttpRequest
from django.forms import ValidationError
from django.shortcuts import render
from ..forms import CatadorForm

def crearCatador(req : HttpRequest):
    if req.method == "GET":
        formCatador =  CatadorForm()

        context = {
            "form_cata": formCatador
        }
    
        return render(req, "tecnicas/manage_tester/catador-crear.html", context)
    elif req.method == "POST":
        formCatadorValues = CatadorForm(req.POST)
        context = {
            "form_cata": formCatadorValues
        }

        if formCatadorValues.is_valid():
            try:
                formCatadorValues.save()
                context["message"] = "datos guardados"
                context["form_cata"] = CatadorForm()
            except ValidationError:
                context["error"] = "nombre de usuario en uso"
                return render(req, "tecnicas/manage_tester/catador-crear.html", context)

            return render(req, "tecnicas/manage_tester/catador-crear.html", context)
        else:
            context["error"] = "datos no validos"
            return render(req, "tecnicas/manage_tester/catador-crear.html", context)