from ..models import SesionSensorial, Presentador, Tecnica
from . import CalificacionController, PalabrasController
from ..utils import controller_error


class DetallesSesionController():
    @staticmethod
    def getContextForView(session_code: str):
        context = {}

        session = SesionSensorial.objects.get(codigo_sesion=session_code)
        context["sesion"] = session

        words = PalabrasController.getWordsInTechnique(session.tecnica)
        context["palabras"] = words

        rating = CalificacionController.getRatingsByTechnique(
            technique=session.tecnica)
        context["calificaciones"] = rating

        return context

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
        elif technique.repecion == technique.repeticiones_max:
            return controller_error("se ha alcanzado el número de repeticiones máxima")

        session.activo = True
        technique.repecion = technique.repecion + 1

        technique.save()
        session.save()
    
        return session
