from .panel_create_controller import PanelCreateController
from django.http import HttpRequest, JsonResponse
from django.db import transaction
from tecnicas.models import EsVocabulario, Tecnica, TipoTecnica, EstiloPalabra, EsAtributo, Vocabulario, Palabra, SesionSensorial, Producto
from tecnicas.utils import deleteDataSession, general_error


class PanelCreateCataController(PanelCreateController):
    def __init__(self):
        super().__init__()

    def controllPost(self, request: HttpRequest):
        if request.POST.get('action') == 'create_session':
            if not request.session.get("form_codes") or not request.session.get("form_words"):
                deleteDataSession(request)
                return general_error("No se ha especificado información necesaria para la creación de la sesión, por favor, vuelve a intentarlo")
            try:
                with transaction.atomic():
                    # //////////////////////////// #
                    #
                    # First step: Create technique #
                    #
                    # //////////////////////////// #
                    data_basic = request.session["form_basic"]
                    data_basic["numero_catadores"] = 0
                    data_basic["numero_repeticiones"] = 1

                    technique = Tecnica.objects.create(
                        tipo_tecnica=TipoTecnica.objects.get(
                            nombre_tecnica=data_basic["name_tecnica"]),
                        id_estilo=EstiloPalabra.objects.get(
                            nombre_estilo=data_basic["estilo_palabras"]),
                        repeticiones_max=data_basic["numero_repeticiones"] or 1,
                        limite_catadores=data_basic["numero_catadores"],
                        instrucciones=data_basic["instrucciones"] or "Espere instrucciones del Presentador",
                    )

                    if not technique:
                        raise ValueError("Error al guardar la técnica")

                    # ////////////////////////////////////////////// #
                    #
                    # Second step: Create productos with their codes #
                    #
                    # ////////////////////////////////////////////// #
                    codes = request.session["form_codes"]

                    if not codes:
                        raise ValueError("No hay códigos de productos")

                    products_without_save = []
                    for code in codes:
                        product = Producto(
                            codigoProducto=code,
                            id_tecnica=technique
                        )
                        products_without_save.append(product)

                    Producto.objects.bulk_create(products_without_save)

                    # /////////////////////////////////////////////////////// #
                    #
                    # Third step: Create relations technique with Words Style #
                    #
                    # /////////////////////////////////////////////////////// #
                    style_words = technique.id_estilo.nombre_estilo

                    if style_words == "atributos":
                        raw_ids_words = request.session["form_words"]
                        ids_words = [int(id_w) for id_w in raw_ids_words]

                        words = Palabra.objects.filter(id__in=ids_words)

                        style_atribute = EsAtributo.objects.create(
                            id_tecnica=technique
                        )

                        if not style_atribute:
                            raise ValueError(
                                "Error al intentar relacionar las palabras con la técnica")

                        style_atribute.palabras.set(words)

                    elif style_words == "vocabulario":
                        name_vocabulary = request.session["form_words"]
                        try:
                            vocabulary = Vocabulario.objects.get(
                                nombre_vocabulario=name_vocabulary)
                        except Vocabulario.DoesNotExist:
                            raise ValueError("Vocabulario no encontrado")

                        es_vocabulary = EsVocabulario.objects.create(
                            id_tecnica=technique,
                            id_vocabulario=vocabulary
                        )
                        if not es_vocabulary:
                            raise ValueError(
                                "Error al intentar relacionar el vocabulario con la técnica")

                    else:
                        raise ValueError("Estilo de palabas no permitido")

                    # //////////////////////////////////////////////////////// #
                    #
                    # Fourth step: Create session and relat with the technique #
                    #
                    # //////////////////////////////////////////////////////// #
                    session = SesionSensorial.objects.create(
                        nombre_sesion=data_basic["nombre_sesion"] if data_basic["nombre_sesion"] != "" else None,
                        tecnica=technique,
                        creadoPor=request.user.user_presentador
                    )

                    if not session:
                        raise ValueError("Error al crear sesion sensorial")

                    context = {
                        "message": "sesión creada",
                        "data": {
                            "codigo_sesion": session.codigo_sesion,
                            "nombre_sesion": session.nombre_sesion
                        }
                    }

                    # ////////////////////////////////// #
                    #
                    # Final step: Delete date en session #
                    #
                    # ////////////////////////////////// #
                    deleteDataSession(request)
                    return JsonResponse(context)

            except ValueError as e:
                return general_error(f"Error: {e}")
        else:
            return general_error("No se ha establecido acción")
