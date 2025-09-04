from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from ..utils import general_error
from ..controllers import TecnicaController, EscalaController


def createSession(req: HttpRequest):
    if req.method == "GET":
        return render(req, 'tecnicas/create_sesion/creando_sesion.html')
    if req.method == "POST":
        if req.POST.get('action') == 'create_session':
            if not req.session.get("form_basic") or not req.session.get("form_tags") or not req.session.get("form_codes") or not req.session["form_words"]:
                req.session.flush()
                return general_error("no se ha especificado informacion necesaria para la creacion de la sesion")

            # ////////////////////////////////////////////////////// #
            #
            # First step: Create technique and scale with their tags #
            #
            # ////////////////////////////////////////////////////// #
            data_basic = req.session["form_basic"]
            controllerTechnique = TecnicaController()
            controllerTechnique.setTechniqueFromBasicData(basic=data_basic)

            technique = controllerTechnique.saveTechnique()
            if not technique:
                return general_error("error al guardar la tecnica")

            data_scale = {
                "scale": data_basic["tipo_escala"],
                "size": data_basic["tamano_escala"],
                "technique": technique
            }

            controllerScale = EscalaController(data=data_scale)

            scale = controllerScale.saveScale()
            if not scale:
                controllerTechnique.deleteTechnique()
                return general_error("error al guardar la escala, datos agregados previeamante borrados")

            list_tags = req.session["form_tags"]

            saved_tags = controllerScale.addAndSaveTags(list_tags)
            if not saved_tags:
                return general_error("error al guardar asociar escalas, datos agregados previeamante borrados")

            return JsonResponse({"message": "sesion creada", "data": {"session_id": "asd548ad4a"}})
        return general_error("ha orcurrido un error inesperado")
