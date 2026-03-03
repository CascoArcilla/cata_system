from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import F
from .details_controller import DetallesController
from tecnicas.models import (
    SesionSensorial, Presentador, Modalidad, TecnicaModalidad, Catador,
    Participacion, DatoPunto, Calificacion, GrupoProducto, ValorBooleano,
    ValorDecimal, Producto, Escala, EsVocabulario, Vocabulario
)
from utils import defaultdict_to_dict
from collections import defaultdict


class DetallesNappingController(DetallesController):
    def __init__(
        self,
        session: SesionSensorial,
        back_url: str = "cata_system:panel_sesiones",
        home_url: str = "cata_system:index"
    ):
        super().__init__(session, back_url, home_url)
        self.url_template = "manage_sesions/details-session-napping.html"
        self.url_next = "cata_system:monitor_sesion"
        self.context = {}

    def getContext(self):
        self.context["use_technique"] = self.session.tecnica.tipo_tecnica.nombre_tecnica
        self.context["session"] = {
                "session_code": self.session.codigo_sesion,
                "session_name": self.session.nombre_sesion or "Sin nombre asignado",
                "session_date": self.session.fechaCreacion,
                "activated": self.session.activo,
                "session_instructions": self.session.tecnica.instrucciones,
            }
        self.context["technique"] = {
            "max_catadores": self.session.tecnica.limite_catadores
        }

        self.defineStatus()
        self.setDataTable()

        return self.context

    def defineStatus(self):
        repetition = self.session.tecnica.repeticion
        mod = TecnicaModalidad.objects.get(
            tecnica=self.session.tecnica)

        self.context["session"]["mod_tech"] = mod.modalidad.nombre
        self.context["finished"] = False

        if repetition == 0:
            self.context["session"]["session_status"] = "Listo para iniciar la sesión"
        elif repetition == 1 and self.session.activo:
            self.context["session"]["session_status"] = "Sesión en curso"
        elif repetition >= 1 and not self.session.activo:
            self.context["session"]["session_status"] = "Recolección de datos finalizada"
            self.context["finished"] = True

    def controllPostResponse(self, request: HttpRequest, action: str):
        if action == "start_session":
            response = self.startNapping(request=request)

        elif action == "combine_sessions":
            response = self.combineSessions(request=request)

        elif action == "delete_session":
            self.deleteSesorialSession()
            response = redirect(
                reverse(self.back_url, kwargs={"page": 1}))

        else:
            response = self.controllGetResponse(
                error="Modalidad sin implantar", request=request)

        return response

    def startNapping(self, request: HttpRequest):
        if request.user.user_presentador.user.username != self.session.creadoPor.user.username:
            return self.controllGetResponse(error="Solo el analista que crea la sesión puede iniciar la repetición", request=request)
        elif self.session.activo:
            return self.controllGetResponse(error="La sesión ya está activada", request=request)

        is_update_participations = self.setParticipationsToNoFinished()
        if not is_update_participations:
            return self.controllGetResponse(error="Error al actualizar las participaciones", request=request)

        self.session.activo = True
        self.session.save()

        parameters = {
            "session_code": self.session.codigo_sesion
        }
        return redirect(
            reverse(self.url_next, kwargs=parameters))

    def setDataTable(self):
        participations = Participacion.objects.filter(
            tecnica=self.session.tecnica).select_related("catador")
        testers = [participation.catador for participation in participations]
        self.context["testers"] = testers

        ratings = Calificacion.objects.filter(id_tecnica=self.session.tecnica)

        coordinates = (
            DatoPunto.objects.filter(calificacion__in=ratings)
            .values(
                producto=F("calificacion__id_producto__codigoProducto"),
                catador=F("calificacion__id_catador__user__username"),
                px=F("x"),
                py=F("y"),
            ))

        if not coordinates.exists():
            self.context["there_data"] = False
            return []

        coordinates_by_product = defaultdict(dict)

        for coordinate in coordinates:
            coordinates_by_product[coordinate["producto"]][coordinate["catador"]] = {
                "px": coordinate["px"],
                "py": coordinate["py"],
            }

        self.context["coordinates_no_mode"] = defaultdict_to_dict(
            coordinates_by_product)

        # Add word frequency data for perfil ultra flash mode
        mod = TecnicaModalidad.objects.get(tecnica=self.session.tecnica)
        if mod.modalidad.nombre == "perfil ultra flash":
            self.setWordFrequencies(ratings)
        elif mod.modalidad.nombre == "sorting":
            self.setSortingData()

        self.context["there_data"] = True

    def setWordFrequencies(self, ratings):
        from collections import Counter

        # Prefetch palabras to optimize queries
        ratings_with_words = ratings.prefetch_related(
            'palabras').select_related('id_producto')

        # Dictionary to store word frequencies by product
        word_frequencies_by_product = defaultdict(Counter)
        all_words_set = set()

        for rating in ratings_with_words:
            producto_code = rating.id_producto.codigoProducto
            words = rating.palabras.all()

            for word in words:
                word_name = word.nombre_palabra
                word_frequencies_by_product[producto_code][word_name] += 1
                all_words_set.add(word_name)

        # Convert Counter objects to regular dicts and sort words alphabetically
        word_frequencies_dict = {
            product: dict(frequencies)
            for product, frequencies in word_frequencies_by_product.items()
        }

        # Sort all words alphabetically for consistent column ordering
        all_words_sorted = sorted(all_words_set)

        self.context["word_frequencies"] = word_frequencies_dict
        self.context["all_words"] = all_words_sorted

    def setSortingData(self):
        # Get all ratings for this technique to access DatoPunto
        ratings = Calificacion.objects.filter(id_tecnica=self.session.tecnica)

        # Get coordinates for all products
        coordinates = (
            DatoPunto.objects.filter(calificacion__in=ratings)
            .values(
                producto=F("calificacion__id_producto__codigoProducto"),
                producto_id=F("calificacion__id_producto__id"),
                catador=F("calificacion__id_catador__user__username"),
                catador_id=F("calificacion__id_catador__id"),
                px=F("x"),
                py=F("y"),
            ))

        # Create a mapping of (catador_id, producto_id) -> coordinates
        coord_map = {}
        for coord in coordinates:
            key = (coord["catador_id"], coord["producto_id"])
            coord_map[key] = {
                "px": coord["px"],
                "py": coord["py"],
                "producto": coord["producto"],
                "catador": coord["catador"]
            }

        # Get all groups with their products and words
        grupos = (
            GrupoProducto.objects.filter(tecnica=self.session.tecnica)
            .prefetch_related("productos", "palabras")
            .select_related("catador__user")
        )

        # Create a mapping of (catador_id, producto_id) -> words
        words_map = defaultdict(list)
        for grupo in grupos:
            catador_id = grupo.catador.id
            words = [palabra.nombre_palabra for palabra in grupo.palabras.all()]
            words_str = ";".join(words) if words else ""

            for producto in grupo.productos.all():
                key = (catador_id, producto.id)
                words_map[key] = words_str

        # Structure final data: product -> catador -> {px, py, words}
        sorting_data = defaultdict(dict)

        for key, coord_data in coord_map.items():
            catador_id, producto_id = key
            producto_code = coord_data["producto"]
            catador_username = coord_data["catador"]

            sorting_data[producto_code][catador_username] = {
                "px": coord_data["px"],
                "py": coord_data["py"],
                "words": words_map.get(key, "")
            }

        self.context["sorting_data"] = defaultdict_to_dict(sorting_data)

    # ==================== SESSION COMBINATION METHODS ====================

    def combineSessions(self, request: HttpRequest):
        """Handle session combination request"""
        session_b_code = request.POST.get("session_b_code", "").strip()

        if not session_b_code:
            return self.controllGetResponse(
                error="Debe proporcionar un código de sesión", request=request)

        # Validate and get session B
        validation_result = self.validateSessionCombination(session_b_code)

        if validation_result.get("error"):
            return self.controllGetResponse(
                error=validation_result["error"], request=request)

        session_b = validation_result["session_b"]
        technique_type = validation_result["technique_type"]

        # Get combined data based on technique type
        if technique_type == "cata":
            combined_data = self.getCombinedDataForCATA(session_b)
        elif technique_type == "rata":
            combined_data = self.getCombinedDataForRATA(session_b)
        elif technique_type == "escalas":
            combined_data = self.getCombinedDataForEscalas(session_b)
        else:
            return self.controllGetResponse(
                error="Tipo de técnica no soportado para combinación", request=request)

        # Add combined data to context
        self.context["combined_data"] = combined_data
        self.context["session_b"] = session_b
        self.context["session_b_technique_type"] = technique_type

        return self.controllGetResponse(request=request)

    def validateSessionCombination(self, session_b_code: str):
        """Validate that Session B can be combined with Session A (Napping)"""
        result = {"error": None, "session_b": None, "technique_type": None}

        # Check if Session B exists
        try:
            session_b = SesionSensorial.objects.select_related(
                "tecnica__tipo_tecnica").get(codigo_sesion=session_b_code)
        except SesionSensorial.DoesNotExist:
            result["error"] = f"No existe una sesión con el código: {session_b_code}"
            return result

        # Check if Session B technique is CATA, RATA, or Escalas
        technique_type = session_b.tecnica.tipo_tecnica.nombre_tecnica
        valid_techniques = ["cata", "rata", "escalas"]

        if technique_type not in valid_techniques:
            result[
                "error"] = f"La sesión B debe usar CATA, RATA o Escalas. Técnica actual: {technique_type}"
            return result

        # Check if Session B is finished
        if session_b.activo:
            result["error"] = "La sesión B debe estar finalizada (no activa)"
            return result

        if session_b.tecnica.repeticion < 1:
            result["error"] = "La sesión B debe haber completado al menos una repetición"
            return result

        # Get products from both sessions
        products_a = set(
            Producto.objects.filter(
                calificacion_producto__id_tecnica=self.session.tecnica
            ).values_list("codigoProducto", flat=True).distinct()
        )

        products_b = set(
            Producto.objects.filter(
                calificacion_producto__id_tecnica=session_b.tecnica
            ).values_list("codigoProducto", flat=True).distinct()
        )

        # Check if products match
        if products_a != products_b:
            result["error"] = f"Los productos no coinciden. Sesión A: {len(products_a)} productos, Sesión B: {len(products_b)} productos"
            return result

        # Get tasters from both sessions
        tasters_a = set(
            Participacion.objects.filter(
                tecnica=self.session.tecnica
            ).values_list("catador__user__username", flat=True)
        )

        tasters_b = set(
            Participacion.objects.filter(
                tecnica=session_b.tecnica
            ).values_list("catador__user__username", flat=True)
        )

        # Check if tasters match
        if tasters_a != tasters_b:
            result["error"] = f"Los catadores no coinciden. Sesión A: {len(tasters_a)} catadores, Sesión B: {len(tasters_b)} catadores"
            return result

        result["session_b"] = session_b
        result["technique_type"] = technique_type
        return result

    def getCombinedDataForCATA(self, session_b: SesionSensorial):
        """Get combined data for CATA technique (word frequencies)"""
        from collections import Counter

        # Get all ratings for session B
        ratings_b = Calificacion.objects.filter(id_tecnica=session_b.tecnica)

        # Get boolean values (CATA uses boolean)
        data = (
            ValorBooleano.objects
            .filter(id_dato__id_calificacion__in=ratings_b, valor=True)
            .values(
                palabra=F("id_dato__id_palabra__nombre_palabra"),
                producto=F(
                    "id_dato__id_calificacion__id_producto__codigoProducto"),
            )
        )

        # Count word frequencies per product
        word_frequencies = defaultdict(Counter)
        all_words_set = set()

        for item in data:
            palabra = item["palabra"]
            producto = item["producto"]
            word_frequencies[producto][palabra] += 1
            all_words_set.add(palabra)

        # Get vocabulary info if exists
        vocabulary_info = self.getVocabularyInfo(session_b.tecnica)

        return {
            "word_frequencies": defaultdict_to_dict(word_frequencies),
            "all_words": sorted(all_words_set),
            "vocabulary_info": vocabulary_info,
        }

    def getCombinedDataForRATA(self, session_b: SesionSensorial):
        """Get combined data for RATA technique (word averages)"""

        # Get all ratings for session B
        ratings_b = Calificacion.objects.filter(id_tecnica=session_b.tecnica)

        # Get decimal values (RATA uses decimal)
        data = (
            ValorDecimal.objects
            .filter(id_dato__id_calificacion__in=ratings_b)
            .values(
                palabra=F("id_dato__id_palabra__nombre_palabra"),
                producto=F(
                    "id_dato__id_calificacion__id_producto__codigoProducto"),
                valor_decimal=F("valor"),
            )
        )

        # Calculate averages per product per word
        word_sums = defaultdict(lambda: defaultdict(list))
        all_words_set = set()

        for item in data:
            palabra = item["palabra"]
            producto = item["producto"]
            valor = item["valor_decimal"]
            word_sums[producto][palabra].append(valor)
            all_words_set.add(palabra)

        # Calculate averages
        word_averages = {}
        for producto, palabras in word_sums.items():
            word_averages[producto] = {}
            for palabra, valores in palabras.items():
                word_averages[producto][palabra] = sum(valores) / len(valores)

        # Get vocabulary info if exists
        vocabulary_info = self.getVocabularyInfo(session_b.tecnica)

        return {
            "word_averages": word_averages,
            "all_words": sorted(all_words_set),
            "vocabulary_info": vocabulary_info,
        }

    def getCombinedDataForEscalas(self, session_b: SesionSensorial):
        """Get combined data for Escalas technique (averages across repetitions)"""

        # Get all ratings for session B
        ratings_b = Calificacion.objects.filter(id_tecnica=session_b.tecnica)

        # Get decimal values grouped by repetition
        data = (
            ValorDecimal.objects
            .filter(id_dato__id_calificacion__in=ratings_b)
            .values(
                palabra=F("id_dato__id_palabra__nombre_palabra"),
                producto=F(
                    "id_dato__id_calificacion__id_producto__codigoProducto"),
                repeticion=F("id_dato__id_calificacion__num_repeticion"),
                valor_decimal=F("valor"),
            )
        )

        # Calculate averages per repetition (like RATA), then average across repetitions
        # Structure: {producto: {repeticion: {palabra: [valores]}}}
        repetition_values = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list)))
        all_words_set = set()

        for item in data:
            palabra = item["palabra"]
            producto = item["producto"]
            repeticion = item["repeticion"]
            valor = item["valor_decimal"]
            # Collect all values for averaging
            repetition_values[producto][repeticion][palabra].append(valor)
            all_words_set.add(palabra)

        # Calculate average per repetition, then average across repetitions
        word_averages = {}
        for producto, repeticiones in repetition_values.items():
            word_averages[producto] = {}
            # Get all words for this product across all repetitions
            all_product_words = set()
            for rep_words in repeticiones.values():
                all_product_words.update(rep_words.keys())

            # Calculate average for each word
            for palabra in all_product_words:
                # Get average for each repetition
                rep_averages = []
                for rep in repeticiones.keys():
                    if palabra in repeticiones[rep]:
                        valores = repeticiones[rep][palabra]
                        rep_averages.append(sum(valores) / len(valores))

                # Average the repetition averages
                if rep_averages:
                    word_averages[producto][palabra] = sum(
                        rep_averages) / len(rep_averages)

        # Get scale and vocabulary info
        scale = Escala.objects.get(tecnica=session_b.tecnica)
        scale_info = None
        if scale:
            scale_info = {
                "type": scale.id_tipo_escala.nombre_escala,
                "size": scale.longitud
            }

        vocabulary_info = self.getVocabularyInfo(session_b.tecnica)

        return {
            "word_averages": word_averages,
            "all_words": sorted(all_words_set),
            "scale_info": scale_info,
            "vocabulary_info": vocabulary_info,
            "num_repetitions": session_b.tecnica.repeticion,
        }

    def getVocabularyInfo(self, tecnica):
        es_vocabulario = EsVocabulario.objects.filter(
            id_tecnica=tecnica).first()
        if es_vocabulario:
            vocabulario = es_vocabulario.id_vocabulario
            return {
                "nombre": vocabulario.nombre_vocabulario,
            }
        return None
