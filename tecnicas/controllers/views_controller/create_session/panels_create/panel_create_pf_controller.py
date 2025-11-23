from .panel_create_controller import PanelCreateController
from django.http import HttpRequest, JsonResponse
from django.db import transaction
from tecnicas.models import Tecnica, TipoTecnica, EstiloPalabra, SesionSensorial, Escala, TipoEscala, Producto
from tecnicas.utils import deleteDataSession, general_error


class PanelCreatePFController(PanelCreateController):
    def __init__(self):
        super().__init__()

    @staticmethod
    def controllPost(request: HttpRequest):
        if request.POST.get('action') == 'create_session':
            if not request.session.get("form_codes"):
                deleteDataSession(request)
                return general_error("No se ha especificado información necesaria para la creación de la sesión, por favor, vuelve a intentarlo")
            try:
                with transaction.atomic():
                    # ////////////////////////////////////// #
                    #
                    # First step: Create technique and scale #
                    #
                    # ////////////////////////////////////// #
                    data_basic = request.session["form_basic"]
                    phases_before_reptition = 2

                    technique = Tecnica.objects.create(
                        tipo_tecnica=TipoTecnica.objects.get(
                            nombre_tecnica=data_basic["name_tecnica"]),
                        id_estilo=EstiloPalabra.objects.get(
                            nombre_estilo="vocabulario"),
                        repeticiones_max=data_basic["numero_repeticiones"] +
                        phases_before_reptition,
                        limite_catadores=data_basic["numero_catadores"],
                        instrucciones=data_basic["instrucciones"] or "Espere instrucciones del Analista",
                    )

                    if not technique:
                        raise ValueError("Error al guardar la técnica")

                    created_scale = Escala.objects.create(
                        id_tipo_escala=TipoEscala.objects.get(
                            nombre_escala="estructurada"),
                        longitud=data_basic["numero_productos"],
                        tecnica=technique
                    )

                    if not created_scale:
                        raise ValueError("No se ha podido crear la escala")

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
                    # Third step: Create session and relat with the technique #
                    #
                    # /////////////////////////////////////////////////////// #
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
