from django.http import HttpRequest, JsonResponse
from django.db import IntegrityError
from ..models import Etiqueta
from ..forms import EtiquetaForm
from ..utils import general_error


def newTag(req: HttpRequest):
    if req.method == "GET":
        return general_error()
    elif req.method == "POST":
        try:
            form = EtiquetaForm(req.POST)
            if form.is_valid():
                value_etiqueta = form.cleaned_data["nueva_etiqueta"]
                value_etiqueta = value_etiqueta.strip()
                value_etiqueta = value_etiqueta.lower()
            else:
                return general_error()
        except KeyError:
            return general_error()

        try:
            new_etiqueta = Etiqueta.objects.create(
                valor_etiqueta=value_etiqueta)
        except IntegrityError:
            return general_error("etiqueta repetida")

        return JsonResponse({
            "message": "etiqueta registrada",
            "new_tag": {
                "id": new_etiqueta.id,
                "valor": new_etiqueta.valor_etiqueta
            }
        })
