from django.http import HttpRequest, JsonResponse
from django.db import IntegrityError
from ..models import Etiqueta
from ..forms import EtiquetaForm
import json

def newTag(req:HttpRequest):
    if req.method == "GET":
        return error()
    elif req.method == "POST":
        try:
            form = EtiquetaForm(req.POST)
            if form.is_valid():
                value_etiqueta = form.cleaned_data["nueva_etiqueta"]
                value_etiqueta = value_etiqueta.strip()
                value_etiqueta = value_etiqueta.lower()
            else:
                return error()
        except KeyError:
            return error()

        try:
            new_etiqueta = Etiqueta.objects.create(valor_etiqueta=value_etiqueta)
        except IntegrityError:
            return error("etiqueta repetida")
        
        return JsonResponse({
            "message": "etiqueta registrada",
            "new_tag": {
                "id": new_etiqueta.id,
                "valor": new_etiqueta.valor_etiqueta
            }
        })

def error(message="informacion incorrecta"):
    respuesta = { "error" : message }
    return JsonResponse(respuesta)