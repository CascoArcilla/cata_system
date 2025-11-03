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
from tecnicas.controllers import SesionController, ConvencionalScalesController
from tecnicas.utils import noValidTechnique


def convencionalScales(req: HttpRequest, code_sesion: str):
    session = SesionController.getSessionByCode(code_sesion)
    type_technique = session.tecnica.tipo_tecnica.nombre_tecnica

    if req.method == "GET":
        view_controller = ConvencionalScalesController(
            sensorial_session=session, user_tester=req.user.user_catador)
        if type_technique == "escalas":
            respose = view_controller.controllGetEscalas(request=req)
        elif type_technique == "rata":
            respose = view_controller.controllGetRATA(request=req)
        else:
            respose = noValidTechnique(
                name_view='cata_system:catador_init_session',
                params={"code_sesion": session.codigo_sesion},
                query_params={"error": "No es posible poder usar esta técnica"}
            )

        return respose
