from django.http import HttpRequest, JsonResponse
from tecnicas.models import SesionSensorial, Producto, Tecnica, Escala, Calificacion, DatoHedonico
from controllers import CalificacionController, DatoController
from controllers import TestPerfilIdealPhase1Controller, TestPerfilIdealPhase2Controller
from controllers import RatingPerfilIdealPhase1Controller, RatingPerfilIdealPhase2Controller
from utils import general_error


def perfilIdealPhase1(request: HttpRequest, code_sesion: str):
    """Vista para Fase 1 de Perfil Ideal - Escalas de Intensidad e Ideal"""
    try:
        session = SesionSensorial.objects.select_related("tecnica").get(
            codigo_sesion=code_sesion)
    except SesionSensorial.DoesNotExist:
        return general_error("Sesión no encontrada")

    controller = TestPerfilIdealPhase1Controller(
        sensorial_session=session,
        user_tester=request.user.user_catador
    )

    if request.method == "GET":
        return controller.controllGet(request)
    else:
        return controller.controllPost(request)


def perfilIdealPhase2(request: HttpRequest, code_sesion: str):
    """Vista para Fase 2 de Perfil Ideal - Escala Hedónica"""
    try:
        session = SesionSensorial.objects.select_related("tecnica").get(
            codigo_sesion=code_sesion)
    except SesionSensorial.DoesNotExist:
        return general_error("Sesión no encontrada")

    controller = TestPerfilIdealPhase2Controller(
        sensorial_session=session,
        user_tester=request.user.user_catador
    )

    if request.method == "GET":
        return controller.controllGet(request)
    else:
        return controller.controllPost(request)


def ratingPerfilIdealPhase1(request: HttpRequest):
    """API para guardar calificaciones de Fase 1 (Intensidad e Ideal)"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        # Obtener datos del request
        id_technique = int(request.POST.get("id-technique"))
        id_product = int(request.POST.get("id-product"))
        id_word = int(request.POST.get("id-word"))
        value_rating_intensity = int(request.POST.get("rating-intensity"))
        value_rating_ideal = int(request.POST.get("rating-ideal"))

        # Obtener técnica y escalas
        technique = Tecnica.objects.get(id=id_technique)
        product = Producto.objects.get(id=id_product)

        intensity_scale = Escala.objects.get(
            tecnica=technique,
            id_tipo_escala__nombre_escala="estructurada"
        )
        ideal_scale = Escala.objects.get(
            tecnica=technique,
            id_tipo_escala__nombre_escala="ideal"
        )

        # Crear controladores de calificación
        rating_intensity = Calificacion(
            id_producto=product,
            id_tecnica=technique,
            id_catador=request.user.user_catador,
            num_repeticion=technique.repeticion
        )

        rating_ideal = Calificacion(
            id_producto=product,
            id_tecnica=technique,
            id_catador=request.user.user_catador,
            num_repeticion=technique.repeticion
        )

        # Crear controladores de datos
        data_controller_intensity = DatoController(
            word=id_word,
            rating=rating_intensity,
            value_rating=value_rating_intensity
        )

        data_controller_ideal = DatoController(
            word=id_word,
            rating=rating_ideal,
            value_rating=value_rating_ideal
        )

        # Crear controlador de API y procesar
        api_controller = RatingPerfilIdealPhase1Controller(
            rating_intensity=rating_intensity,
            rating_ideal=rating_ideal,
            data_controller_intensity=data_controller_intensity,
            data_controller_ideal=data_controller_ideal,
            intensity_scale=intensity_scale,
            ideal_scale=ideal_scale
        )

        response = api_controller.controllPostPhase1()
        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({"error": f"Error al procesar la solicitud: {str(e)}"}, status=400)


def ratingPerfilIdealPhase2(request: HttpRequest):
    """API para guardar calificaciones de Fase 2 (Hedónica)"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        # Obtener datos del request
        id_technique = int(request.POST.get("id-technique"))
        id_product = int(request.POST.get("id-product"))
        value_rating_hedonic = int(request.POST.get("rating-hedonic"))

        # Obtener técnica y escala hedónica
        technique = Tecnica.objects.get(id=id_technique)
        product = Producto.objects.get(id=id_product)

        hedonic_scale = Escala.objects.get(
            tecnica=technique,
            id_tipo_escala__nombre_escala="hedonica"
        )

        # Crear instacia calificación
        rating_hedonic_instance = Calificacion(
            id_producto=product,
            id_tecnica=technique,
            id_catador=request.user.user_catador,
            num_repeticion=technique.repeticion
        )

        # Crear controlador de API y procesar
        api_controller = RatingPerfilIdealPhase2Controller(
            rating_hedonic=rating_hedonic_instance,
            value_hedonic=value_rating_hedonic,
            hedonic_scale=hedonic_scale
        )

        response = api_controller.controllPostPhase2()
        return JsonResponse(response)

    except Exception as e:
        print(e)
        return JsonResponse({"error": "Error al procesar la solicitud"})
