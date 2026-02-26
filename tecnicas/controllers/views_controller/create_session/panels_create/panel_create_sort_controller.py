from .panel_create_controller import PanelCreateController
from django.http import HttpRequest, JsonResponse
from django.db import transaction
from tecnicas.models import Tecnica, TipoTecnica, EstiloPalabra, SesionSensorial, Producto
from tecnicas.utils import deleteDataSession, general_error


class PanelCreateSortController(PanelCreateController):
    def __init__(self):
        super().__init__()

    def controllPost(self, request: HttpRequest):
        if request.POST.get('action') == 'create_session':
            if not request.session.get("form_basic") or not request.session.get("form_codes"):
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
                    data_basic["numero_catadores"] = data_basic["numero_catadores"] or 1
                    data_basic["numero_repeticiones"] = 1

                    technique = Tecnica.objects.create(
                        tipo_tecnica=TipoTecnica.objects.get(
                            nombre_tecnica=data_basic["name_tecnica"]),
                        id_estilo=EstiloPalabra.objects.get(
                            nombre_estilo="sort"),
                        repeticiones_max=data_basic["numero_repeticiones"],
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
