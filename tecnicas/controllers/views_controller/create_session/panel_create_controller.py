from django.http import HttpRequest, JsonResponse
from django.db import transaction
from django.shortcuts import render
from tecnicas.utils import general_error
from tecnicas.controllers import TecnicaController, EscalaController, ProductosController, OrdenesController, EstiloPalabrasController, PalabrasController, SesionController
from tecnicas.utils import deleteDataSession


class PanelCreateController():
    def __init__(self):
        pass

    @staticmethod
    def controllGetEscalas(request: HttpRequest):
        return render(
            request, 'tecnicas/create_sesion/creando_sesion.html')

    @staticmethod
    def controllPostEscalas(request: HttpRequest):
        if request.POST.get('action') == 'create_session':
            if not request.session.get("form_tags") or not request.session.get("form_codes") or not request.session.get("form_words"):
                deleteDataSession(request)
                return general_error("No se ha especificado información necesaria para la creación de la sesión, por favor, vuelve a intentarlo")

            with transaction.atomic():
                # ////////////////////////////////////////////////////// #
                #
                # First step: Create technique and scale with their tags #
                #
                # ////////////////////////////////////////////////////// #
                data_basic = request.session["form_basic"]
                controllerTechnique = TecnicaController()
                controllerTechnique.setTechniqueFromBasicData(basic=data_basic)
                technique = controllerTechnique.saveTechnique()
                if not technique:
                    return general_error("Error al guardar la técnica")

                data_scale = {
                    "id_scale": data_basic["tipo_escala"],
                    "size": data_basic["tamano_escala"],
                    "technique": technique
                }

                controllerScale = EscalaController(data=data_scale)

                scale = controllerScale.saveScale()
                if isinstance(scale, dict):
                    return general_error(scale["error"])

                dict_tags = request.session["form_tags"]
                saved_related_tags = controllerScale.realteTags(dict_tags)
                if "error" in saved_related_tags:
                    return general_error(saved_related_tags["error"])

                # ////////////////////////////////////////////////////////// #
                #
                # Second step: Create orders, productos and set the position #
                #
                # ////////////////////////////////////////////////////////// #
                data_codes = request.session["form_codes"]

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
                    return general_error(saved_orders["error"])

                seded_positions = controllerOrdes.setPositions()
                if isinstance(seded_positions, dict):
                    return general_error(seded_positions["error"])

                saved_postions = controllerOrdes.savePositions()
                if isinstance(saved_postions, dict):
                    return general_error(saved_prodcuts["error"])

                # /////////////////////////////////////////////////////// #
                #
                # Third step: Create relations technique with Words Style #
                #
                # /////////////////////////////////////////////////////// #
                ids_words = request.session["form_words"]
                words_controller = PalabrasController(ids=ids_words)

                words_to_use = words_controller.setWords()
                if isinstance(words_to_use, dict):
                    return general_error(words_to_use["error"])

                style_controller = EstiloPalabrasController(
                    technique=technique, words=words_to_use)

                instace_style = style_controller.createAndSaveInstaceStyle()
                if isinstance(instace_style, dict):
                    return general_error(instace_style["error"])

                words_using = style_controller.relatedWords()
                if isinstance(words_using, dict):
                    return general_error(words_using["error"])

                # //////////////////////////////////////////////////////// #
                #
                # Fourth step: Create session and relat with the technique #
                #
                # //////////////////////////////////////////////////////// #
                session_controller = SesionController(
                    name_session=data_basic["nombre_sesion"] if data_basic["nombre_sesion"] != "" else None,
                    technique=technique,
                    creator=request.user.user_presentador
                )

                setting_session = session_controller.setSession()
                if isinstance(setting_session, dict):
                    return general_error(setting_session["error"])

                saved_session = session_controller.saveSession()
                if isinstance(saved_session, dict):
                    return general_error(saved_session["error"])

                context = {
                    "message": "sesión creada",
                    "data": {
                        "codigo_sesion": saved_session.codigo_sesion,
                        "nombre_sesion": saved_session.nombre_sesion
                    }
                }

                # ////////////////////////////////// #
                #
                # Final step: Delete date in session #
                #
                # ////////////////////////////////// #

                deleteDataSession(request)
                return JsonResponse(context)
        else:
            return general_error("No se ha establecido acción")

    @staticmethod
    def controllPostRATA(request: HttpRequest):
        if request.POST.get('action') == 'create_session':
            if not request.session.get("form_tags") or not request.session.get("form_codes") or not request.session.get("form_words"):
                deleteDataSession(request)
                return general_error("No se ha especificado información necesaria para la creación de la sesión, por favor, vuelve a intentarlo")

            with transaction.atomic():
                # ////////////////////////////////////////////////////// #
                #
                # First step: Create technique and scale with their tags #
                #
                # ////////////////////////////////////////////////////// #
                data_basic = request.session["form_basic"]
                data_basic["numero_catadores"] = 0
                data_basic["numero_repeticiones"] = 1
                controllerTechnique = TecnicaController()
                controllerTechnique.setTechniqueFromBasicData(basic=data_basic)
                technique = controllerTechnique.saveTechnique()
                if not technique:
                    return general_error("Error al guardar la técnica")

                data_scale = {
                    "id_scale": data_basic["tipo_escala"],
                    "size": data_basic["tamano_escala"],
                    "technique": technique
                }

                controllerScale = EscalaController(data=data_scale)

                scale = controllerScale.saveScale()
                if isinstance(scale, dict):
                    return general_error(scale["error"])

                dict_tags = request.session["form_tags"]
                saved_related_tags = controllerScale.realteTags(dict_tags)
                if "error" in saved_related_tags:
                    return general_error(saved_related_tags["error"])

                # ////////////////////////////////////////////// #
                #
                # Second step: Create productos with their codes #
                #
                # ////////////////////////////////////////////// #
                codes = request.session["form_codes"]

                controllerProducts = ProductosController(
                    codes=codes,
                    technique=technique
                )

                controllerProducts.setProductsNoSave()
                saved_prodcuts = controllerProducts.saveProducts()
                if isinstance(saved_prodcuts, dict):
                    return general_error(saved_prodcuts["error"])

                # /////////////////////////////////////////////////////// #
                #
                # Third step: Create relations technique with Words Style #
                #
                # /////////////////////////////////////////////////////// #
                ids_words = request.session["form_words"]
                words_controller = PalabrasController(ids=ids_words)

                words_to_use = words_controller.setWords()
                if isinstance(words_to_use, dict):
                    return general_error(words_to_use["error"])

                style_controller = EstiloPalabrasController(
                    technique=technique, words=words_to_use)

                instace_style = style_controller.createAndSaveInstaceStyle()
                if isinstance(instace_style, dict):
                    return general_error(instace_style["error"])

                words_using = style_controller.relatedWords()
                if isinstance(words_using, dict):
                    return general_error(words_using["error"])

                # //////////////////////////////////////////////////////// #
                #
                # Fourth step: Create session and relat with the technique #
                #
                # //////////////////////////////////////////////////////// #
                session_controller = SesionController(
                    name_session=data_basic["nombre_sesion"] if data_basic["nombre_sesion"] != "" else None,
                    technique=technique,
                    creator=request.user.user_presentador
                )

                setting_session = session_controller.setSession()
                if isinstance(setting_session, dict):
                    return general_error(setting_session["error"])

                saved_session = session_controller.saveSession()
                if isinstance(saved_session, dict):
                    return general_error(saved_session["error"])

                context = {
                    "message": "sesión creada",
                    "data": {
                        "codigo_sesion": saved_session.codigo_sesion,
                        "nombre_sesion": saved_session.nombre_sesion
                    }
                }

                # ////////////////////////////////// #
                #
                # Final step: Delete date en session #
                #
                # ////////////////////////////////// #
                deleteDataSession(request)
                return JsonResponse(context)
        else:
            return general_error("No se ha establecido acción")
