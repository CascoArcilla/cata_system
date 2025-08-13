from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.db import Error
from django.core.exceptions import ObjectDoesNotExist
from ..forms import CatadorForm
from ..models import Catador

def testerSearch(req : HttpRequest):
    if req.method == "GET":
        context = {}

        try:
            user = req.GET["user"]
        except:
            user = False

        if not user:
            return render(req, "tecnicas/manage_tester/catador-buscar.html")
        
        try:
            tester = Catador.objects.get(usuarioCatador=user)
            context["form_catador"] = CatadorForm(instance=tester)
        except Catador.DoesNotExist:
            context["error"] = "usuario no encontrado"

        return render(req, "tecnicas/manage_tester/catador-buscar.html", context)
    elif req.method == "POST":
        context = {}

        try:
            infoTester = req.POST
        except:
            infoTester = False

        nameUser = req.POST["usuarioCatador"]

        if not infoTester:
            context["error"] = "ha ocurrido un error en recueperar los datos"
            return render(req, "tecnicas/manage_tester/catador-buscar.html", context)
        
        user = get_object_or_404(Catador, usuarioCatador=nameUser)
        
        modelForm = CatadorForm(infoTester, instance=user)

        try:
            if not modelForm.is_valid():
                context["error"] = "ha ocurrido un error en guardar los datos"
                return render(req, "tecnicas/manage_tester/catador-buscar.html", context)
            modelForm.save()
            context["form_catador"] = modelForm
            context["message"] = "usuario actualizado"
        except:
            context["form_catador"] = modelForm
            context["error"] = "ha ocurrido un error en guardar los datos"

        return render(req, "tecnicas/manage_tester/catador-buscar.html", context)