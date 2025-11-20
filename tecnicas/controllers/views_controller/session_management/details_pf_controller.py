from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.models import SesionSensorial, Presentador, Participacion, ListaPalabras, Calificacion, Catador
from tecnicas.controllers import ParticipacionController, DatoController
from tecnicas.utils import defaultdict_to_dict
from .details_controller import DetallesController
from collections import defaultdict


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
        lists_words_testers = self.context["second_phase"]
        technique = self.session.tecnica

        ratings_for_tester = []

        for list_tester in lists_words_testers:
            tester_username = list_tester["username"]
            # Se recuperan las calificaciones
            ratings_for_repetition = []

            ratings = list(Calificacion.objects.filter(
                id_tecnica=technique, id_catador__user__username=tester_username))

            if not ratings:
                continue

            data = DatoController.getWordValuesPF(
                ratings=ratings, technique=technique, tester=Catador.objects.get(user__username=tester_username))

            ratings_for_repetition = defaultdict(lambda: defaultdict(list))

            for item in data:
                rep = item["repeticion"]
                prod = item["producto_code"]

                ratings_for_repetition[rep-2][prod].append({
                    "nombre_palabra": item["nombre_palabra"],
                    "dato_valor": item["dato_valor"]
                })

            ratings_for_tester.append(
                {
                    "tester": tester_username,
                    "ratings": defaultdict_to_dict(
                        ratings_for_repetition),
                    "words": list_tester["words"]
                }
            )
            self.context["existen_calificaciones"] = True

        return ratings_for_tester

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
