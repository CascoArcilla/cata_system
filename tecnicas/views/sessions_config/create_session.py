from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from ...utils import general_error
from ...controllers import TecnicaController, EscalaController, ProductosController, OrdenesController, EstiloPalabrasController, PalabrasController, SesionController
from ...models import Presentador


def createSession(req: HttpRequest):
    if req.method == "GET":
        return render(req, 'tecnicas/create_sesion/creando_sesion.html')
    if req.method == "POST":
        if req.POST.get('action') == 'create_session':
            if not req.session.get("form_basic") or not req.session.get("form_tags") or not req.session.get("form_codes") or not req.session.get("form_words"):
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
                "id_scale": data_basic["tipo_escala"],
                "size": data_basic["tamano_escala"],
                "technique": technique
            }

            controllerScale = EscalaController(data=data_scale)

            scale = controllerScale.saveScale()
            if isinstance(scale, dict):
                controllerTechnique.deleteTechnique()
                return general_error(scale["error"])

            dict_tags = req.session["form_tags"]
            saved_related_tags = controllerScale.realteTags(dict_tags)
            if "error" in saved_related_tags:
                return general_error(saved_related_tags["error"])

            # ////////////////////////////////////////////////////////// #
            #
            # Second step: Create orders, productos and set the position #
            #
            # ////////////////////////////////////////////////////////// #
            data_codes = req.session["form_codes"]

            list_codes_dict = data_codes["product_codes"]

            codes = []
            for product in list_codes_dict:
                code = next(iter(product.values()))
                codes.append(code)

            controllerProducts = ProductosController(
                codes=codes,
                technique=technique
            )

            controllerProducts.setProductsNoSave()
            saved_prodcuts = controllerProducts.saveProducts()
            if isinstance(saved_prodcuts, dict):
                controllerTechnique.deleteTechnique()
                return general_error(saved_prodcuts["error"])

            raw_sort_codes = data_codes["sort_codes"]
            controllerOrdes = OrdenesController(
                raw_orders=raw_sort_codes,
                list_products=saved_prodcuts,
                technique=technique
            )

            controllerOrdes.setOrdersToSave()
            saved_orders = controllerOrdes.saveOrders()
            if isinstance(saved_orders, dict):
                controllerTechnique.deleteTechnique()
                return general_error(saved_orders["error"])

            seded_positions = controllerOrdes.setPositions()
            if isinstance(seded_positions, dict):
                controllerTechnique.deleteTechnique()
                return general_error(seded_positions["error"])

            saved_postions = controllerOrdes.savePositions()
            if isinstance(saved_postions, dict):
                controllerTechnique.deleteTechnique()
                return general_error(saved_prodcuts["error"])

            # /////////////////////////////////////////////////////// #
            #
            # Third step: Create relations technique with Words Style #
            #
            # /////////////////////////////////////////////////////// #
            ids_words = req.session["form_words"]
            words_controller = PalabrasController(ids=ids_words)

            words_to_use = words_controller.setWords()
            if isinstance(words_to_use, dict):
                controllerTechnique.deleteTechnique()
                return general_error(words_to_use["error"])

            style_controller = EstiloPalabrasController(
                technique=technique, words=words_to_use)

            instace_style = style_controller.createAndSaveInstaceStyle()
            if isinstance(instace_style, dict):
                controllerTechnique.deleteTechnique()
                return general_error(instace_style["error"])

            words_using = style_controller.relatedWords()
            if isinstance(words_using, dict):
                controllerTechnique.deleteTechnique()
                return general_error("error")

            # //////////////////////////////////////////////////////// #
            #
            # Fourth step: Create session and relat with the technique #
            #
            # //////////////////////////////////////////////////////// #
            session_controller = SesionController(
                name_session=data_basic["nombre_sesion"] if data_basic["nombre_sesion"] != "" else None,
                technique=technique,
                creator=Presentador.objects.get(nombre_usuario="aguBido")
            )

            setting_session = session_controller.setSession()
            if isinstance(setting_session, dict):
                controllerTechnique.deleteTechnique()
                return general_error(setting_session["error"])

            saved_session = session_controller.saveSession()
            if isinstance(saved_session, dict):
                return general_error(saved_session["error"])

            context = {
                "message": "sesion creada",
                "data": {
                    "codigo_sesion": saved_session.codigo_sesion,
                    "nombre_sesion": saved_session.nombre_sesion
                }
            }

            keys_forms = [
                "form_basic",
                "form_tags",
                "form_codes",
                "form_words"
            ]

            for key in keys_forms:
                if key in req.session:
                    del req.session[key]
                    
            return JsonResponse(context)
        return general_error("ha orcurrido un error inesperado")
