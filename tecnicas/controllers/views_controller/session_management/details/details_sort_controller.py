from .details_controller import DetallesController
from tecnicas.models import SesionSensorial, GrupoProducto, Producto, Participacion
from collections import defaultdict


class DetallesSortController(DetallesController):
    def __init__(self, session: SesionSensorial):
        super().__init__(session)
        self.url_template = "tecnicas/manage_sesions/details-session-sort.html"
        self.url_next = "cata_system:monitor_sesion"

    def getContext(self):
        technique = self.session.tecnica

        finished = False
        status = ""

        if technique.repeticion < technique.repeticiones_max and not self.session.activo:
            status = "En espera para iniciar la sesión"
        elif technique.repeticion >= technique.repeticiones_max and not self.session.activo:
            status = "Esta sesión ha sido finalizada"
            finished = True
        else:
            status = "La sesión está en progreso"

        self.context = {
            "sesion": self.session,
            "technique": technique,
            "status": status,
            "finished": finished
        }

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
