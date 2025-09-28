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
from ...controllers import ApiRatingController, CalificacionController, DatoController


def reatingWord(req:  HttpRequest):
    if req.method == "POST":
        if not req.POST["rating-word"] or not req.POST["info-product"] or not req.POST["info-word"]:
            return JsonResponse({"error": "No se mandó información necesaria para la calificación"})

        received_rating = req.POST["rating-word"]
        received_word = req.POST["info-word"]
        received_product = req.POST["info-word"]

        view_controller = ApiRatingController(
            CalificacionController(technique=req.session["id_techniqe"], product=received_product.id)
            )

        return JsonResponse({
            "message": "Ok",
            "data": {
                "word": word,
                "rating": rating,
                "cata_ser": req.session["cata_username"]
            }
        })
