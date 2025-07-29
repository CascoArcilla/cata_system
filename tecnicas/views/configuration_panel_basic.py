from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.urls import reverse
from ..forms import SesionBasicForm
from ..models import TipoTecnica

def configuracionPanelBasic(req: HttpRequest):
    if req.method == "POST":
        form = SesionBasicForm(req.POST)

        if form.is_valid():
            values = {}
            
            for name, value in form.cleaned_data.items():
                if not name == "tipo_escala":
                    values[name] = value
                else:
                    values[name] = value.id
            
            req.session['datos_formulario'] = values
            return redirect(reverse("cata_system:panel_configuracion_tags"))

        return render(req, "tecnicas/configuracion-panel-basic.html", { "form_sesion": form, "error": "Ha ocurrido un error al continuar al siguiente paso." })
    elif req.method == "GET":
        try:
            id_tecnica = req.GET["id_tecnica"]
            tecnica = TipoTecnica.objects.get(pk=id_tecnica)
        except KeyError:
            return redirect(reverse("cata_system:seleccion_tecnica") + "?error=tecnica_no_establecida")
        except (ValueError, TipoTecnica.DoesNotExist):
            return redirect(reverse("cata_system:seleccion_tecnica") + "?error=tecnica_no_establecida")

        if tecnica:
            form_sesion = SesionBasicForm(id_tecnica_new=id_tecnica)
            return render(req, "tecnicas/configuracion-panel-basic.html", { "form_sesion": form_sesion })
        else:
            return redirect(reverse("cata_system:seleccion_tecnica") + "?error=la_tecnica_no_existe")