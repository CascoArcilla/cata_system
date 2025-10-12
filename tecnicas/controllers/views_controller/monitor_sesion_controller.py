from tecnicas.models import SesionSensorial, EsAtributo, EsVocabulario, Producto, Calificacion
from tecnicas.controllers import ParticipacionController, SesionController
from tecnicas.utils import controller_error


class MonitorSesionController():
    def __init__(self, session_code: str):
        self.code_session = session_code

    def defineSession(self):
        self.session = SesionSensorial.objects.get(
            codigo_sesion=self.code_session)

    def monitorView(self):
        try:
            self.sensorial_session = SesionSensorial.objects.select_related(
                "tecnica"
            ).only(
                "nombre_sesion",
                "tecnica__limite_catadores",
            ).get(codigo_sesion=self.code_session)

            self.participations = ParticipacionController.getParticipationsInTechinique(
                self.sensorial_session.tecnica)
        except SesionSensorial.DoesNotExist as error:
            return controller_error("No existe Sesión sensorial")

        context = {
            "session_name": self.sensorial_session.nombre_sesion,
            "max_testers": self.sensorial_session.tecnica.limite_catadores,
            "current_testers": len(self.participations),
            "active_testers": len([part for part in self.participations if part.activo]),
            "participations": self.participations
        }

        return context

    def getExpectedRatings(self):
        num_products = Producto.objects.filter(
            id_tecnica=self.session.tecnica).count()

        style_words = self.session.tecnica.id_estilo

        num_words: int

        if style_words.nombre_estilo == "atributos":
            num_words = EsAtributo.objects.get(
                id_tecnica=self.session.tecnica).palabras.count()
        elif style_words.nombre_estilo == "vocabulario":
            num_words = EsVocabulario.objects.get(
                id_tecnica=self.session.tecnica).id_vocabulario.palabras.count()

        return num_products * num_words

    def checkAllParticipantsEnded(self):
        self.defineSession()

        technique = self.session.tecnica

        expected_ratings_repetition = self.getExpectedRatings()

        all_participations = ParticipacionController.getParticipationsInTechinique(
            technique=technique)

        if len(all_participations) < technique.limite_catadores:
            return (False, "No se ha alcanzado el número máximo de Catadores")

        for particiapation in all_participations:
            num_ratings_now = Calificacion.objects.filter(
                id_tecnica=technique, id_catador=particiapation.catador, num_repeticion=technique.repeticion).count()

            if num_ratings_now < expected_ratings_repetition:
                return (False, "No todos los catadores han finalizado su evaluación")

        return (True, "Puedes finalizar la sesión")

    def finishSession(self):
        response = SesionController.finishRepetion(self.session)
        if isinstance(response, dict):
            return controller_error(response["error"])
        self.defineSession()
        return self.session
