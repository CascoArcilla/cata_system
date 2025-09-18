from ..models import Catador, SesionSensorial, Participacion
from ..utils import controller_error
from django.db import transaction


class LoginTesterController():
    tester: Catador
    session: SesionSensorial
    taster_participation: Participacion

    def __init__(self):
        self.tester = Catador()
        self.session = SesionSensorial()

    def existCredential(self, user_tester: str, code_session: str):
        try:
            self.tester = Catador.objects.get(usuarioCatador=user_tester)
            self.session = SesionSensorial.objects.get(
                codigo_sesion=code_session)

            return True
        except (Catador.DoesNotExist, SesionSensorial.DoesNotExist):
            return controller_error("Credenciales inválidas")

    def validateEntry(self):
        if not self.tester.nombre or not self.session.codigo_sesion:
            return controller_error("Credenciales no definidas")

        if not self.session.activo:
            return controller_error("La sesión no está activa actualmente")

        if self.session.tecnica.repecion > 1:
            try:
                self.taster_participation = Participacion.objects.get(
                    tecnica=self.session.tecnica, catador=self.tester)
                return self.taster_participation
            except Participacion.DoesNotExist:
                return controller_error("No tienes permitido entrar a esta sesión")
        else:
            try:
                self.taster_participation = Participacion.objects.get(
                    tecnica=self.session.tecnica, catador=self.tester)
                return self.taster_participation
            except Participacion.DoesNotExist:
                with transaction.atomic():
                    code_session = self.session.codigo_sesion
                    self.session = SesionSensorial.objects.select_for_update().get(
                        codigo_sesion=code_session)

                    max_testers = self.session.tecnica.limite_catadores
                    current_num_testers = Participacion.objects.filter(
                        tecnica=self.session.tecnica).count()

                    if current_num_testers >= max_testers:
                        return controller_error("La sesión ha alcanzado el número máximo de catadores")

                    self.taster_participation = Participacion.objects.create(
                        tecnica=self.session.tecnica,
                        catador=self.tester
                    )

                    return self.taster_participation
