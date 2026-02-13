'''
****  Para este endpoint es necesario:
**** ****

 * Manejar el metodo POST
 * Recibir los siguientes datos
    - ID y Codigo del producto calificando
    - ID y nombre de la palabra que se califico
    - Valor de calificacion que se dio
        - Valor numerico asociado a escalas de rango
        - Valor booleano asociado a escalas esctructuradas
 * Dentro de la sesion se debe tener
    - ID del catador
    - ID de la sesion, para acceder a la tecnica
 * Crear una instancia de la calificacion a partir de
    - Numero de repeticion
    - Producto calificado
    - Catodor
    - Tecnica
 * Cuando la instancia calificacion se haya creado, hacer otra instancia para dato con
    - La palabra calificada
    - La calificacion creada previamente
 * Dependiendo de la escala o tecnica usada
    - Guardar dato como valor decimal
    - Guardar el dato como valor booleano
 * Retornar un json con el mensaje de exito
 * En caso de haber un error se manda un json con el error
 * Calquier otro metodo que se maneje mandar un error
'''
from django.http import HttpRequest, JsonResponse
from tecnicas.controllers import RatingScalesController, CalificacionController, DatoController
from tecnicas.utils import general_error
import json


def ratingWordScales(req:  HttpRequest):
    if req.method == "POST":
        if not req.POST["rating-word"] or not req.POST["id-word"] or not req.POST["id-product"]:
            return JsonResponse({"error": "No se mandó información necesaria para la calificación"})

        received_rating = json.loads(req.POST.get("rating-word"))
        received_id_word = json.loads(req.POST.get("id-word"))
        received_id_product = json.loads(req.POST.get("id-product"))
        id_technique = json.loads(req.POST.get("id-technique"))

        view_controller = RatingScalesController(
            rating_controller=CalificacionController(
                technique=id_technique,
                product=received_id_product,
                tester=req.user.user_catador
            ),
            data_controller=DatoController(
                word=received_id_word,
                rating=0,
                value_rating=received_rating
            )
        )

        response_data = view_controller.controllPostScales()

        return JsonResponse(response_data)
    else:
        return general_error("No puede usar este método aquí")