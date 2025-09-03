from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from ..utils import general_error
from ..controllers import TecnicaController
from ..models import TipoTecnica, EstiloPalabra


def createSession(req: HttpRequest):
    if req.method == "GET":
        return render(req, 'tecnicas/create_sesion/creando_sesion.html')
    if req.method == "POST":
        if req.POST.get('action') == 'create_session':
            if not req.session.get("form_basic") or not req.session.get("form_tags") or not req.session.get("form_codes") or not req.session["form_words"]:
                req.session.flush()
                return general_error("no se ha especificado informacion necesaria para la creacion de la sesion")

            data_basic = req.session["form_basic"]
            controllTechnique = TecnicaController()
            controllTechnique.setTechniqueFromBasicData(basic=data_basic)
            print(controllTechnique.getDataTechnique())

            return JsonResponse({"message": "sesion creada", "data": {"session_id": "asd548ad4a"}})
        return general_error("ha orcurrido un error inesperado")


{
    'id_tecnica': 1,
    'nombre_sesion': '',
    'numero_productos': 3,
    'numero_catadores': 3,
    'numero_repeticiones': 3,
    'estilo_palabras': 1,
    'tipo_escala': 2,
    'tamano_escala': 9,
    'instrucciones': ''
}
