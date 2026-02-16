from tecnicas.models import SesionSensorial, ListaPalabras, Calificacion, Catador, Producto
from tecnicas.controllers import DatoController
from tecnicas.utils import defaultdict_to_dict
from .details_controller import DetallesController
from collections import defaultdict


class DetallesPFController(DetallesController):
    skip_repetition = 2

    def __init__(self, session: SesionSensorial):
        super().__init__(session)
        self.url_template = "tecnicas/manage_sesions/details-session-pf.html"
        self.url_next = "cata_system:monitor_sesion"

    def getContext(self):
        technique = self.session.tecnica

        self.context = {
            "use_technique": technique.tipo_tecnica.nombre_tecnica,
            "tipo_escala": "Ordinal",
            "repeticiones_max": technique.repeticiones_max - self.skip_repetition,
            "session": {
                "session_code": self.session.codigo_sesion,
                "session_name": self.session.nombre_sesion or "Sin nombre asignado",
                "session_date": self.session.fechaCreacion,
                "activated": self.session.activo,
                "session_instructions": technique.instrucciones,
            },
            "technique": {
                "words_style": technique.id_estilo,
                "max_catadores": technique.limite_catadores,
                "max_repetitions": technique.repeticiones_max - self.skip_repetition,
            },
            "valor_max": Producto.objects.filter(
                id_tecnica=self.session.tecnica).count()
        }

        if technique.repeticion <= self.skip_repetition:
            self.context["technique"]["current_repetition"] = "0"
        elif technique.repeticion > self.skip_repetition:
            self.context["technique"]["current_repetition"] = technique.repeticion - \
                self.skip_repetition
        elif technique.repeticion > technique.repeticiones_max:
            self.context["technique"]["current_repetition"] = technique.repeticion - \
                self.skip_repetition

        # Definir el estado de la sesion
        rep = technique.repeticion
        max_rep = technique.repeticiones_max
        activate = self.session.activo
        self.context["session"]["session_status"] = self.getStatus(
            rep, activate, max_rep)

        self.getDataPhases()

        self.isEndSession()

        return self.context

    def isEndSession(self):
        current_rep = self.session.tecnica.repeticion - self.skip_repetition
        max_rep = self.session.tecnica.repeticiones_max - self.skip_repetition
        self.context["finished"] = current_rep >= max_rep

    def getDataPhases(self):
        curren_repetition = self.session.tecnica.repeticion

        if curren_repetition == 1:
            self.context["fisrt_phase"] = self.getDataFirstPhase()
            self.context["repeticion"] = 0

        elif curren_repetition == 2:
            self.context["fisrt_phase"] = self.getDataFirstPhase()
            self.context["second_phase"] = self.getDataSecondPhase()
            self.context["repeticion"] = 0

        elif curren_repetition >= 3:
            self.context["fisrt_phase"] = self.getDataFirstPhase()
            self.context["second_phase"] = self.getDataSecondPhase()
            self.context["data_ratings"] = self.getDataRatings()
            self.context["repeticion"] = self.session.tecnica.repeticion - \
                self.skip_repetition

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
        technique = self.session.tecnica

        if technique.repeticion > 3:
            return self.getDataRatingsFinal()

        elif technique.repeticion == 3:
            return self.getDataRatingsInitial()

    def getStatus(self, rep: int, activate: bool, max_rep: int):
        status = ""

        if rep >= max_rep:
            return "Recolección de datos finalizada"

        if rep == 0 and not activate:
            status = "Fase 1 - Listo para iniciar"

        elif rep == 1 and activate:
            status = "Fase 1 - Creando listas iniciales"
        elif rep == 1 and not activate:
            status = "Fase 2 - Listo para iniciar"

        elif rep == 2 and activate:
            status = "Fase 2 - Creando listas finales"
        elif rep == 2 and not activate:
            status = "Fase 3 - Listo para iniciar"

        elif rep >= 3 and activate:
            status = "Fase 3 - En proceso"
        elif rep >= 3 and not activate:
            status = "Fase 3 - Listo para iniciar"

        return status

    def getDataRatingsInitial(self):
        ratings = list(Calificacion.objects.filter(
            id_tecnica=self.session.tecnica, num_repeticion=3))

        structured_data = None

        if ratings:
            raw_data = DatoController.getWordValuesForConvecional(
                technique=self.session.tecnica,
                ratings=ratings
            )

            if not raw_data:
                return None

            structured_data = defaultdict(lambda: defaultdict(list))

            for item in raw_data:
                prod_code = item["producto_code"]
                username = item["usuario_catador"]

                structured_data[prod_code][username].append({
                    "palabra": item["nombre_palabra"],
                    "valor": item["dato_valor"]
                })

        return defaultdict_to_dict(structured_data)

    def getDataRatingsFinal(self):
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

            # Estructurar los datos
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

        return ratings_for_tester
