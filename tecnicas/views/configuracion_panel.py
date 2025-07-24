from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.urls import reverse
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
        try:
            id_tecnica = req.GET["id_tecnica"]
            tecnica = TipoTecnica.objects.get(pk=id_tecnica)
        except KeyError:
            return redirect(reverse("cata_system:seleccion_tecnica") + "?error=tecnica_no_establecida")
        except (ValueError, TipoTecnica.DoesNotExist):
            return redirect(reverse("cata_system:seleccion_tecnica") + "?error=tecnica_no_establecida")

        if tecnica:
            form_sesion = SesionFirtsForm()
            return render(req, "tecnicas/configuracion-panel.html", { "form_sesion": form_sesion })
        else:
            return redirect(reverse("cata_system:seleccion_tecnica") + "?error=la_tecnica_no_existe")