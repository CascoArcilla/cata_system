'''
 **** Esta vista para sesion con tecnica convencional de escalas, al entrar debe:
 **** ****

 ++++ Por el lado del servidor
 ++++ ++++
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

 ++++ Por el lado del cliente
 ++++ ++++
 + Mostrar en todo momento las instrucciones en la parte superior de la pagina
 + Mostrar la repeticion en la que esta
 + Mostrar el producto que esta calificando
 + Desglozar las palabras para calificar
    - Cada palabra debe contar con su input segun el tipo
    - Para cada input se debe poder guardar la calificacion
    - Anstes de guardar la calificacion preguntar por la confirmacion a la hora de guardar el dato
    - Especficar las etiquetas por debajo del input de ripo rango
        - Para las escalas de tipo continua
            - La longitud de la barra de la escala debe ser igual al tamaño que se especifico en la configuracion
            - Contar con un input de tipo range
            - Contar con etiqueta en el inicio de la barra, en el medio y al final
            - La escala debe terner marcas al inicio, medio y final
            - El rango de la barra debe ir de 0 a 1000
        - Para las escalas de tipo estructurada
            - Su longitud sera tan largo como el contendor que lo aloja
            - La barra se divide segun el numero de etiquetas que estas posean
            - Cata longitud debe poser una marca y solo estas seran las unicas posibles respuestas
            - Cata segmento en el que se divide debe tener la etiqueda correspondiente por debajo
'''
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import urlencode
from tecnicas.models import Participacion
from tecnicas.controllers import SesionController, PosicionController, CalificacionController, ParticipacionController, PalabrasController, EscalaController, DatoController


def convencionalScales(req: HttpRequest, code_sesion: str):
    if not "id_order" in req.session:
        return redirect(reverse("cata_system:catador_main"))

    session = SesionController.getSessionByCode(code_sesion)
    technique = session.tecnica
    participation = Participacion.objects.get(
        tecnica=technique, catador=req.user.user_catador)

    context = {
        "session": session
    }

    req.session["id_technique"] = session.tecnica.id

    if req.method == "GET":
        positions = PosicionController.getPostionsInOrder(
            id_order=req.session["id_order"])

        sorted_positions = sorted(positions, key=lambda posi: posi.posicion)

        words = PalabrasController.getWordsInTechnique(technique=technique)

        next_position = CalificacionController.checkProducsWithoutRating(
            positions=sorted_positions,
            user_cata=req.user.username,
            id_technique=session.tecnica.id,
            repetition=session.tecnica.repeticion,
            technique=technique,
            num_words=len(words)
        )

        if isinstance(next_position, dict):
            updated_participation = ParticipacionController.finishSession(
                participation)
            params = {
                "code_sesion": code_sesion
            }
            return redirect(reverse('cata_system:catador_init_session', kwargs=params))

        if isinstance(next_position, list):
            next_position = next_position[0]

        context["product"] = next_position.id_producto

        ratings_product = CalificacionController.getRatings(
            technique=technique,
            product=next_position.id_producto,
            repetition=technique.repeticion,
            user_tester=req.user.username
        )

        if isinstance(ratings_product, dict):
            context["error"] = ratings_product["error"]
            return render(req, "tecnicas/forms_tester/convencional.html", context)
        elif not ratings_product:
            context["words"] = words
        else:
            recoreded_data = DatoController.getRerecordedData(
                ratings=ratings_product)
            if not recoreded_data:
                context["words"] = words
            else:
                words_to_use = PalabrasController.getWordsWithoutData(
                    recoreded_data=recoreded_data, words=words)
                context["words"] = words_to_use

        scale = EscalaController.getScaleByTechnique(technique=technique)
        context["scale"] = scale
        context["type_scale"] = scale.id_tipo_escala.nombre_escala

        use_tags = EscalaController.getRelatedTagsInScale(scale=scale)
        context["tags"] = use_tags

        return render(req, "tecnicas/forms_tester/convencional.html", context)
