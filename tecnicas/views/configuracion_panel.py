from django.shortcuts import render, redirect
from django.http import HttpRequest
from ..forms import SesionFirtsForm
from ..models import TipoTecnica

def configuracionPanel(req: HttpRequest):
    if req.method == "POST":
        form = SesionFirtsForm(req.POST)
        if form.is_valid():
            return redirect("/cata")
        else:
            return render(req, "tecnicas/configuracion-panel.html", { "form_sesion": form })
    elif req.method == "GET":
        if req.GET["id_tecnica"]:
            try:
                tecnica = TipoTecnica.objects.get(pk=int(req.GET["id_tecnica"]))
            except (ValueError, TipoTecnica.DoesNotExist):
                
                pass
        else:
            redirect("/seleccion-tecnica")
            pass
        
        form_sesion = SesionFirtsForm()

        return render(req, "tecnicas/configuracion-panel.html", { "form_sesion": form_sesion })