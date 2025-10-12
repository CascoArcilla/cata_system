'''

Para Tecnicas Convencionales, CATA, RATA, Escala Hedonica
Encabezados de como deben de aparecer los datos por repeticion

| Repeticion: R
| Codigo Producto | Catador | P1 | P2 | P3 | Pn |

Encabezados de como deben de aparecer los datos juntos

| Repeticion | Codigo Producto | Catador | P1 | P2 | P3 | Pn |

'''

from ...models import SesionSensorial, Presentador, Tecnica, Palabra
from .. import CalificacionController, PalabrasController
from ...utils import controller_error
from collections import defaultdict
from tecnicas.controllers import DatoController
from tecnicas.utils import defaultdict_to_dict


class DetallesSesionController():
    def __init__(self, session_code: str):
        self.session = SesionSensorial.objects.get(codigo_sesion=session_code)

    def getContextForView(self):
        self.context = {}

        self.context["sesion"] = self.session

        self.words = PalabrasController.getWordsInTechnique(
            self.session.tecnica)
        self.context["palabras"] = [word.nombre_palabra for word in self.words]

    def getContextWithData(self):
        ratings_for_repetition = []

        ratings = CalificacionController.getRatingsByTechnique(
            technique=self.session.tecnica)

        if isinstance(ratings, dict) or not ratings:
            self.context["calificaciones"] = ratings_for_repetition
            self.context["existen_calificaciones"] = False
            return self.context

        data = DatoController.getWordValuesForConvecional(
            ratings=ratings, technique=self.session.tecnica)

        ratings_for_repetition = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list)))

        for item in data:
            user = item["usuarioCatador"]
            rep = item["repeticion"]
            prod = item["producto_code"]

            ratings_for_repetition[rep][user][prod].append({
                "nombre_palabra": item["nombre_palabra"],
                "dato_valor": item["dato_valor"]
            })

        self.context["calificaciones"] = defaultdict_to_dict(
            ratings_for_repetition)
        self.context["existen_calificaciones"] = True

        return self.context

    @staticmethod
    def startRepetition(session_code: str, username: str):
        try:
            creator = Presentador.objects.get(nombre_usuario=username)
            session = SesionSensorial.objects.get(codigo_sesion=session_code)
            technique = Tecnica.objects.get(id=session.tecnica.id)
        except Presentador.DoesNotExist:
            return controller_error("no existe presentador")
        except SesionSensorial.DoesNotExist:
            return controller_error("no existe sesión sensorial")
        except Tecnica.DoesNotExist:
            return controller_error("Ha ocurrido un error al recuperar la técnica")

        if creator.nombre_usuario != session.creadoPor.nombre_usuario:
            return controller_error("solo el presentador que crea la sesión puede iniciar la repetición")
        elif session.activo:
            return controller_error("la sesión ya está activada")
        elif technique.repeticion == technique.repeticiones_max:
            return controller_error("se ha alcanzado el número de repeticiones máxima")

        session.activo = True
        technique.repeticion = technique.repeticion + 1

        technique.save()
        session.save()

        return session
