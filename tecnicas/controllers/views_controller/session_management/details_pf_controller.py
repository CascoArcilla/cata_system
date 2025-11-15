from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.models import SesionSensorial, Presentador, Participacion, ListaPalabras
from tecnicas.controllers import ParticipacionController
from .details_controller import DetallesController


class DetallesPFController(DetallesController):
    def __init__(self, session: SesionSensorial):
        super().__init__(session)
        self.url_template = "tecnicas/manage_sesions/details-session-pf.html"
        self.url_next = "cata_system:monitor_sesion"

    def getContext(self):
        technique = self.session.tecnica

        self.context = {
            "sesion": self.session,
            "use_technique": technique,
            "calificaciones": [],
            "existen_calificaciones": False,
            "tipo_escala": technique.escala_tecnica.id_tipo_escala.nombre_escala,
            "valor_max": technique.escala_tecnica.longitud
        }

        # Definir el estado de la sesion
        rep = technique.repeticion
        activate = self.session.activo
        self.context["estado"] = self.getStatus(rep, activate)

        self.getDataPhases()

        return self.context

    def startRepetition(self, presenter: Presentador, request: HttpRequest):
        creator = presenter
        technique = self.session.tecnica

        if creator.user.username != self.session.creadoPor.user.username:
            return self.getResponse(error="Solo el presentador que crea la sesión puede iniciar la repetición o fase", request=request)
        elif self.session.activo:
            return self.getResponse(error="La sesión ya está activada", request=request)

        there_participacions = Participacion.objects.filter(
            tecnica=technique).exists()

        if there_participacions:
            (is_update_participations,
             message) = ParticipacionController.outAllInSession(self.session)
            if not is_update_participations:
                return self.getResponse(error=message, request=request)

        self.session.activo = True
        technique.repeticion = technique.repeticion + 1

        technique.save()
        self.session.save()

        parameters = {
            "session_code": self.session.codigo_sesion
        }
        return redirect(
            reverse(self.url_next, kwargs=parameters))

    def getDataPhases(self):
        curren_repetition = self.session.tecnica.repeticion

        if curren_repetition == 1:
            self.context["fisrt_phase"] = self.getDataFirstPhase()
        elif curren_repetition == 2:
            self.context["fisrt_phase"] = self.getDataFirstPhase()
            self.context["second_phase"] = self.getDataSecondPhase()
        elif curren_repetition >= 3:
            self.context["fisrt_phase"] = self.getDataFirstPhase()
            self.context["second_phase"] = self.getDataSecondPhase()
            self.context["data_ratings"] = self.getDataRatings()

        return self.context

    def getDataFirstPhase(self):
        lists_testers = ListaPalabras.objects.filter(
            tecnica=self.session.tecnica,
            es_final=False
        )

        result = []
        for list in lists_testers:
            try:
                username = list.catador.user.username
            except Exception:
                username = None

            words_qs = list.palabras.all()
            words = []
            for p in words_qs:
                nombre = getattr(p, 'nombre_palabra', None)
                words.append({
                    'id': getattr(p, 'id', None),
                    'nombre_palabra': nombre
                })

            result.append({
                'username': username,
                'words': words
            })

        return result

    def getDataSecondPhase(self):
        lists_testers = ListaPalabras.objects.filter(
            tecnica=self.session.tecnica,
            es_final=True
        )

        result = []
        for list in lists_testers:
            try:
                username = list.catador.user.username
            except Exception:
                username = None

            words_qs = list.palabras.all()
            words = []
            for p in words_qs:
                nombre = getattr(p, 'nombre_palabra', None)
                words.append({
                    'id': getattr(p, 'id', None),
                    'nombre_palabra': nombre
                })

            result.append({
                'username': username,
                'words': words
            })

        return result

    def getDataRatings(self):
        return []

    def getStatus(self, rep: int, activate: bool):
        status = ""

        if rep == 0 and not activate:
            status = "Listo para crear listas iniciales"

        elif rep == 1 and activate:
            status = "En primera fase, creación de listas iniciales"
        elif rep == 1 and not activate:
            status = "Listo para crear listas finales"

        elif rep == 2 and activate:
            status = "En segunda fase, creación de listas finales"
        elif rep == 2 and not activate:
            status = "Listo para calificaciones"

        elif rep > 2 and not activate:
            status = "Listo para calificaciones"
        elif rep > 2 and activate:
            status = "Catadores calificando"

        return status
