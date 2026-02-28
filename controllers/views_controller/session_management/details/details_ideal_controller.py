from tecnicas.models import SesionSensorial, Dato, Calificacion, Escala, CalificacionEscala, DatoHedonico
from django.db.models import Prefetch
from controllers import PalabrasController
from .details_controller import DetallesController


class DetallesIdealController(DetallesController):
    def __init__(
        self,
        session: SesionSensorial,
        back_url: str = "cata_system:panel_sesiones",
        home_url: str = "cata_system:index"
    ):
        super().__init__(session, back_url, home_url)
        self.url_template = "tecnicas/manage_sesions/details-session-ideal.html"
        self.url_next = "cata_system:monitor_sesion"

    def getContext(self):
        technique = self.session.tecnica

        self.context = {
            "use_technique": "Perfil Ideal",
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
                "max_repetitions": technique.repeticiones_max,
                "current_repetition": technique.repeticion,
            },
        }

        # Establecer estado
        if technique.repeticion == 0:
            self.context["session"]["session_status"] = "Sesion lista para iniciar"
        elif technique.repeticion == 1 and self.session.activo:
            self.context["session"]["session_status"] = "Sesion en curso"
        elif technique.repeticion == 1 and not self.session.activo:
            self.context["session"]["session_status"] = "Recoleccion de datos finalizada"
        else:
            self.context["session"]["session_status"] = "Estado desconocido"

        # Recuperar palabras
        self.words = PalabrasController.getWordsInTechnique(
            self.session.tecnica)
        self.context["palabras"] = [word.nombre_palabra for word in self.words]

        # Se comprueba que ya no se pueda iniciar la repeticion
        self.context["fin_repeticiones"] = technique.repeticion >= technique.repeticiones_max and not self.session.activo
        self.context["existen_calificaciones"] = False

        # Datos hedonicos por de cada producto por catador con diccionario
        ratings_hedonic = DatoHedonico.objects.filter(
            calificacion__id_tecnica=self.session.tecnica,
            calificacion__num_repeticion=1,
            calificacion__calificacion_escala__escala__id_tipo_escala__nombre_escala="hedonica"
        ).select_related(
            'calificacion', 'calificacion__id_producto', 'calificacion__id_catador', 'calificacion__id_catador__user'
        )

        ratings_hedonic_dict = {}
        try:
            for rating in ratings_hedonic:
                test_user = rating.calificacion.id_catador.user.username
                code = rating.calificacion.id_producto.codigoProducto

                if test_user not in ratings_hedonic_dict:
                    ratings_hedonic_dict[test_user] = {}

                ratings_hedonic_dict[test_user][code] = rating.valor
        except Exception as e:
            print(
                f"Error generando diccionario de calificaciones hedonicas: {e}")
            ratings_hedonic_dict = {}

        # Crear prefetch para los datos de calificación
        data_prefetch = Prefetch(
            'dato_calificacion',
            queryset=Dato.objects.select_related(
                'id_palabra', 'dato_decimal')
        )

        scale_prefetch = Prefetch(
            'calificacion_escala',
            queryset=CalificacionEscala.objects.select_related(
                'escala', 'escala__id_tipo_escala')
        )

        # Obtener todas las calificaciones de Intensidad y diccionario de acceso rápido por Producto
        ratings_intens_ideal = Calificacion.objects.filter(
            num_repeticion=1,
            id_tecnica=self.session.tecnica,
            calificacion_escala__escala__id_tipo_escala__nombre_escala__in=[
                "estructurada", "ideal",]
        ).select_related(
            'id_producto', "id_catador", "id_catador__user"
        ).prefetch_related(data_prefetch, scale_prefetch)

        all_ratings_dict = {}
        try:
            for rating in ratings_intens_ideal:
                test_user = rating.id_catador.user.username
                code = rating.id_producto.codigoProducto
                data_rating = rating.dato_calificacion.all()

                if test_user not in all_ratings_dict:
                    all_ratings_dict[test_user] = {}

                if code not in all_ratings_dict[test_user]:
                    all_ratings_dict[test_user][code] = {}

                type_scale = rating.calificacion_escala.all(
                )[0].escala.id_tipo_escala.nombre_escala

                all_ratings_dict[test_user][code][type_scale] = {
                    dat.id_palabra.nombre_palabra: dat.dato_decimal.valor for dat in data_rating} or {}

                if "hedonica" not in all_ratings_dict[test_user][code]:
                    all_ratings_dict[test_user][code][
                        "hedonica"] = ratings_hedonic_dict[test_user][code]
        except Exception as e:
            print(
                f"Error generando diccionario de calificaciones intensidad ideal: {e}")
            all_ratings_dict = {}

        self.context["existen_calificaciones"] = True if all_ratings_dict else False
        self.context["ratings"] = all_ratings_dict

        return self.context
