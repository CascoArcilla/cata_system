from django.http import HttpRequest
from django.forms import ValidationError
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import transaction, DatabaseError
from tecnicas.models import Catador
from django.urls import reverse
from tecnicas.forms import CatadorForm


def testerCreate(req: HttpRequest):
    url_template = "tecnicas/manage_tester/tester-create.html"

    url_home = req.session.get("sensorial_url_main")
    if req.method == "GET":
        form_tester = CatadorForm()

        context = {
            "form_cata": form_tester,
            "url_home": reverse(url_home)
        }

        return render(req, url_template, context)
    elif req.method == "POST":
        new_values = {}

        for key, value in req.POST.items():
            new_values[key] = value

        new_values["is_update"] = False

        form_tester = CatadorForm(new_values)
        context = {
            "form_cata": form_tester,
            "url_home": reverse(url_home)
        }

        if form_tester.is_valid():
            with transaction.atomic():
                try:
                    user = User.objects.create(
                        username=form_tester.cleaned_data.get(
                            "nombre_usuario"),
                        first_name=form_tester.cleaned_data.get("nombre"),
                        last_name=form_tester.cleaned_data.get("apellido"),
                        email=form_tester.cleaned_data.get("correo")
                    )
                    user.set_unusable_password()
                    user.save()

                    tester = Catador.objects.create(
                        user=user,
                        nacimiento=form_tester.cleaned_data.get(
                            "fecha_nacimiento"),
                        genero=form_tester.cleaned_data.get("genero"),
                        telefono=form_tester.cleaned_data.get("telefono")
                    )
                except (ValidationError, DatabaseError):
                    context["error"] = "nombre de usuario en uso"
                    return render(req, url_template, context)
            context["message"] = "Datos guardados, consúltelo en Listar Catadores"
            context["form_cata"] = CatadorForm()
            return render(req, url_template, context)
        else:
            context["error"] = "Datos no validos"
            return render(req, url_template, context)
