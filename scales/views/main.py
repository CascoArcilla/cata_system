from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from controllers import PanelMainCotroller
from utils import general_error, deleteDataSession
from analist.decorators.required_analist import required_analist
from tecnicas.models import Presentador, SesionSensorial


@required_analist(technique="escalas")
def main(req: HttpRequest):
    if req.method == "GET":
        deleteDataSession(req)
        controller = PanelMainCotroller(
            "scales/main.html", {"tecnica__tipo_tecnica__nombre_tecnica": "escalas"})
        return controller.get(req)
    elif req.method == "POST":
        controller = PanelMainCotroller(
            "scales/main.html", {"tecnica__tipo_tecnica__nombre_tecnica": "escalas"})
        return controller.post(req)
    else:
        general_error("Método no permitido")
