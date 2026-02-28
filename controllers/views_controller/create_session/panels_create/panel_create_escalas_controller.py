from .panel_create_controller import PanelCreateController
from django.http import HttpRequest, JsonResponse
from django.db import transaction
from controllers import TecnicaController, EscalaController, ProductosController, OrdenesController, PalabrasController, EstiloPalabrasController, SesionController
from tecnicas.models import EsVocabulario, Vocabulario
from utils import deleteDataSession, general_error


class PanelCreateEscalasController(PanelCreateController):
    def __init__(self, url_home="cata_system:index_escalas"):
        super().__init__(url_home=url_home)

    def controllPost(self, request: HttpRequest):
        if request.POST.get('action') == 'create_session':
            if not request.session.get("form_tags") or not request.session.get("form_codes") or not request.session.get("form_words"):
                deleteDataSession(request)
                return general_error("No se ha especificado información necesaria para la creación de la sesión, por favor, vuelve a intentarlo")
            try:
                with transaction.atomic():
                    # ////////////////////////////////////////////////////// #
                    #
                    # First step: Create technique and scale with their tags #
                    #
                    # ////////////////////////////////////////////////////// #
                    data_basic = request.session["form_basic"]
                    controllerTechnique = TecnicaController()
                    controllerTechnique.setTechniqueFromBasicData(
                        basic=data_basic)
                    technique = controllerTechnique.saveTechnique()
                    if not technique:
                        raise ValueError("Error al guardar la técnica")

                    data_scale = {
                        "id_scale": data_basic["tipo_escala"],
                        "size": data_basic["tamano_escala"],
                        "technique": technique
                    }

                    controllerScale = EscalaController(data=data_scale)

                    scale = controllerScale.saveScale()
                    if isinstance(scale, dict):
                        raise ValueError(scale["error"])

                    dict_tags = request.session["form_tags"]
                    saved_related_tags = controllerScale.realteTags(dict_tags)
                    if "error" in saved_related_tags:
                        raise ValueError(saved_related_tags["error"])

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
                        raise ValueError(saved_prodcuts["error"])

                    raw_sort_codes = data_codes["sort_codes"]
                    controllerOrdes = OrdenesController(
                        raw_orders=raw_sort_codes,
                        list_products=saved_prodcuts,
                        technique=technique
                    )

                    controllerOrdes.setOrdersToSave()
                    saved_orders = controllerOrdes.saveOrders()
                    if isinstance(saved_orders, dict):
                        raise ValueError(saved_orders["error"])

                    seded_positions = controllerOrdes.setPositions()
                    if isinstance(seded_positions, dict):
                        raise ValueError(seded_positions["error"])

                    saved_postions = controllerOrdes.savePositions()
                    if isinstance(saved_postions, dict):
                        raise ValueError(saved_prodcuts["error"])

                    # /////////////////////////////////////////////////////// #
                    #
                    # Third step: Create relations technique with Words Style #
                    #
                    # /////////////////////////////////////////////////////// #
                    style_words = technique.id_estilo.nombre_estilo
                    if style_words == "atributos":
                        ids_words = request.session["form_words"]
                        words_controller = PalabrasController(ids=ids_words)

                        words_to_use = words_controller.setWords()
                        if isinstance(words_to_use, dict):
                            raise ValueError(words_to_use["error"])

                        style_controller = EstiloPalabrasController(
                            technique=technique, words=words_to_use)

                        instace_style = style_controller.createAndSaveInstaceStyle()
                        if isinstance(instace_style, dict):
                            raise ValueError(instace_style["error"])

                        words_using = style_controller.relatedWords()
                        if isinstance(words_using, dict):
                            raise ValueError(words_using["error"])
                    elif style_words == "vocabulario":
                        name_vocabulary = request.session["form_words"]
                        vocabulary = Vocabulario.objects.get(
                            nombre_vocabulario=name_vocabulary)

                        es_vocabulary = EsVocabulario.objects.create(
                            id_tecnica=technique,
                            id_vocabulario=vocabulary
                        )
                    else:
                        raise ValueError("Estilo de palabas no permitido")

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
                        raise ValueError(setting_session["error"])

                    saved_session = session_controller.saveSession()
                    if isinstance(saved_session, dict):
                        raise ValueError(saved_session["error"])

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
            except ValueError as e:
                return general_error(f"Error: {e}")
        else:
            return general_error("No se ha establecido acción")
