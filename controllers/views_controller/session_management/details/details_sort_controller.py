from .details_controller import DetallesController
from tecnicas.models import SesionSensorial, GrupoProducto, Producto, Participacion
from collections import defaultdict


class DetallesSortController(DetallesController):
    def __init__(
        self,
        session: SesionSensorial,
        back_url: str = "cata_system:panel_sesiones",
        home_url: str = "cata_system:index"
    ):
        super().__init__(session, back_url, home_url)
        self.url_template = "manage_sesions/details-session-sort.html"
        self.url_next = "cata_system:monitor_sesion"

    def getContext(self):
        technique = self.session.tecnica

        self.context = {
            "use_technique": technique.tipo_tecnica.descripcion,
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

        rep = technique.repeticion
        self.context["end_collection"] = False

        if rep == 0:
            self.context["session"]["session_status"] = "Listo para iniciar"
        elif rep == 1 and self.session.activo:
            self.context["session"]["session_status"] = "Sesión en curso"
        elif rep == 1 and not self.session.activo:
            self.context["session"]["session_status"] = "Se ha finalizado la recolección de datos"
            self.context["end_collection"] = True

        self.context["data_groups"] = {
            "data": self.setDataSort(),
            "testers": self.setHeaders()
        }

        return self.context

    def setDataSort(self):
        data = []
        technique = self.session.tecnica

        products = Producto.objects.filter(id_tecnica=technique)

        groups = GrupoProducto.objects.select_related("catador").filter(
            tecnica=technique
        )

        if len(groups):
            self.context["there_data"] = True
        else:
            self.context["there_data"] = False
            return []

        for product in products:
            product_data = {
                "codigo_producto": product.codigoProducto,
                "palabras": {}
            }

            related_groups = groups.filter(productos=product).select_related(
                "catador__user"
            ).prefetch_related("palabras")

            data_words = defaultdict(set)

            for group in related_groups:
                catador_username = group.catador.user.username

                for word in group.palabras.all():
                    data_words[catador_username].add(word.nombre_palabra)

            product_data["palabras"] = {
                username: list(words)
                for username, words in data_words.items()
            }

            data.append(product_data)

        return data

    def setHeaders(self):
        participacions = list(Participacion.objects.filter(
            tecnica=self.session.tecnica
        ).only("catador").select_related("catador__user"))

        testers = [
            participacion.catador.user.username for participacion in participacions]

        return testers
