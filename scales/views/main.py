from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from controllers import PanelMainCotroller
from utils import general_error, deleteDataSession, delete_images
from analist.decorators.required_analist import required_analist
from tecnicas.models import Presentador, SesionSensorial


@required_analist(technique="escalas")
def main(req: HttpRequest):
    if req.method == "GET":
        images_cata = req.session.get("form_images_cata", {})
        if images_cata:
            delete_images(list(images_cata.values()))
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
