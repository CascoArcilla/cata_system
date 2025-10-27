from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.forms import ValidationError
from django.db import transaction, DatabaseError
from django.contrib.auth.models import User
from tecnicas.forms import CatadorForm
from tecnicas.models import Catador


def testerSearch(req: HttpRequest):
    if req.method == "GET":
        context = {}

        if "user" in req.GET:
            username = req.GET["user"]
        else:
            return render(req, "tecnicas/manage_tester/catador-buscar.html")

        try:
            tester = Catador.objects.get(user__username=username)
            context["form_cata"] = CatadorForm({
                'nombre_usuario': tester.user.username,
                'nombre': tester.user.first_name,
                'apellido': tester.user.last_name,
                'telefono': tester.telefono,
                'correo': tester.user.email,
                'fecha_nacimiento': tester.nacimiento,
                'genero': tester.genero,
            })
        except Catador.DoesNotExist:
            context["error"] = "usuario no encontrado"

        return render(req, "tecnicas/manage_tester/catador-buscar.html", context)
    elif req.method == "POST":
        context = {}

        username = req.GET["user"]
        new_values = {}

        for key, value in req.POST.items():
            new_values[key] = value

        new_values["is_update"] = True

        tester = get_object_or_404(Catador, user__username=username)
        form_tester = CatadorForm(new_values)

        if form_tester.is_valid():
            with transaction.atomic():
                try:
                    user = User.objects.get(username=username)
                    user.username = form_tester.cleaned_data.get(
                        "nombre_usuario")
                    user.first_name = form_tester.cleaned_data.get("nombre")
                    user.last_name = form_tester.cleaned_data.get("apellido")
                    user.email = form_tester.cleaned_data.get("correo")
                    user.save()

                    tester.nacimiento = form_tester.cleaned_data.get(
                        "fecha_nacimiento")
                    tester.genero = form_tester.cleaned_data.get("genero")
                    tester.telefono = form_tester.cleaned_data.get("telefono")
                    tester.save()
                except (ValidationError, DatabaseError):
                    context["error"] = "nombre de usuario en uso"
                    return render(req, "tecnicas/manage_tester/catador-crear.html", context)
            context["message"] = "Datos actualizados, consúltelo en Listar Catadores"
            context["form_cata"] = form_tester
            return render(req, "tecnicas/manage_tester/catador-crear.html", context)
        else:
            context["error"] = "Datos no validos"
            return render(req, "tecnicas/manage_tester/catador-crear.html", context)
