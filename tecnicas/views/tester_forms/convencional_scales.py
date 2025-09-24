from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from ...controllers import SesionController, PosicionController, CalificacionController, ParticipacionController, PalabrasController, EscalaController, DatoController

'''
 **** Esta vista para sesion con tecnica convencional de escalas, al entrar debe:
 **** ****
 * Obtner los productos que se evaluan en la tecnica
 * Ordenar los productos segun la Poscion en que se encuentre en el Orden ya establecidos
 * Obtner las palabras para evaluar
    - Revisar que estilo usan
    - Obtner las palabras si el estilo es atributos
    - Obtner las palabras si el estilo es Vocabulario
    - El Catador plasma sus resultados para las palabras sin importar el estilo
 * Comprobar que productos se han calificado
    - Revisar el numero de palabras
    - Comenzar con el primer producto e ir revisando uno a uno
        - Revisar el numero de calificaciones del producto
        - Numero de calificaciones del producto == 0
            - Continuar con la evaluacion o comezar con este producto
        - Numero de calificaciones del producto < numero de palabras
            - Continuar con la evaluacion
        - Numero de calificacion == numero de palabras
            - Pasar con el siguiente producto
 * Si no quedan mas productos por revisar
    - Participacion.finalizado = True
    - Participacion.activo = False
    - Redirigir a "catador_main"
 * Optner la siguiente palabra sin calificar
    - Obtener las calificaiones de producto
    - Obtener los datos de las calificaciones
    - Comprobar que palabras no estan tienen dato
    - Mandar palabras para el usuario
 * Obtener informacion de la escala para mandar
'''


def convencionalScales(req: HttpRequest):
    if not "id_order" in req.session:
        return redirect(reverse("cata_system:catador_main"))

    session = SesionController.getSessionByCode(req.session["code_session"])
    technique = session.tecnica

    context = {
        "session": session
    }

    if req.method == "GET":
        positions = PosicionController.getPostionsInOrder(
            id_order=req.session["id_order"])

        sorted_positions = sorted(positions, key=lambda posi: posi.posicion)

        words = PalabrasController.getWordsInTechnique(technique=technique)

        next_position = CalificacionController.checkProducsWithoutRating(
            positions=sorted_positions,
            user_cata=req.session["cata_username"],
            id_technique=req.session["id_techniqe"],
            repetition=session.tecnica.repecion,
            technique=technique,
            num_words=len(words)
        )

        if isinstance(next_position, dict):
            updated_participation = ParticipacionController.finishSession(
                req.session["id_participation"])
            return redirect(reverse("cata_system:catador_main"))

        if isinstance(next_position, list):
            next_position = next_position[0]

        context["product"] = next_position.id_producto

        ratings_product = CalificacionController.getRatings(
            technique=technique,
            product=next_position.id_producto,
            repetition=technique.repecion,
            user_tester=req.session["cata_username"]
        )

        if isinstance(ratings_product, dict):
            context["error"] = ratings_product["error"]
            return render(req, "tecnicas/forms_tester/convencional.html", context)
        elif not ratings_product:
            context["words"] = words
        else:
            recoreded_data = DatoController.getRerecordedData(ratings=ratings_product)
            if not recoreded_data:
                context["words"] = words
            
            words_to_use = PalabrasController.getWordsWithoutData(recoreded_data=recoreded_data, words=words)
            context["words"] = words_to_use

        scale = EscalaController.getScaleByTechnique(technique=technique)
        context["scale"] = scale

        use_tags = EscalaController.getRelatedTagsInScale(scale=scale)
        context["tags"] = use_tags

        return render(req, "tecnicas/forms_tester/convencional.html", context)
