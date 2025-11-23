from django.http import JsonResponse, HttpRequest
from django.db import transaction, IntegrityError
from tecnicas.models import Palabra, ListaPalabras, Participacion, Calificacion, Producto, Dato, ValorDecimal
from tecnicas.forms import ListWordsForm


class RatingPFListController():
    def __init__(self):
        pass

    @staticmethod
    def getListWords(request: HttpRequest):
        participation_current_tester = Participacion.objects.get(
            id=request.session["id_participation"])

        technique = participation_current_tester.tecnica

        participations_testers = Participacion.objects.exclude(
            catador=participation_current_tester.catador).filter(tecnica=technique)

        all_testers = [
            participation.catador for participation in participations_testers]

        list_words_testers = list(ListaPalabras.objects.filter(
            tecnica=technique, catador__in=all_testers, es_final=True))

        if not list_words_testers:
            return JsonResponse({"error": "Aun no hay listas finales de Catadores"})

        result = []
        for list_tester in list_words_testers:
            try:
                username = list_tester.catador.user.username
            except Exception:
                username = None

            finish = [
                participation.finalizado for participation in participations_testers if participation.catador.user.username == username][0]

            status = "Lista terminada" if finish else "Lista en proceso"

            words_qs = list_tester.palabras.all()
            words = []
            for p in words_qs:
                nombre = getattr(p, 'nombre_palabra', None)
                words.append({
                    'id': getattr(p, 'id', None),
                    'nombre_palabra': nombre
                })

            result.append({
                'username': username,
                'words': words,
                'status': status
            })

        return JsonResponse({
            "message": "Listas encontradas",
            "lists_words": result
        })

    @staticmethod
    def saveList(request: HttpRequest, words: list, current_phase: int):
        dic_words = {}
        for index, word in enumerate(words, start=1):
            dic_words[f"palabra_{index}"] = word

        form = ListWordsForm(dic_words, new_words=words)

        if form.is_valid():
            participation = Participacion.objects.get(
                id=request.session["id_participation"])

            if not participation:
                return JsonResponse({"error": "No está autorizado en la sesión"})

            technique = participation.tecnica

            list_words_tester: ListaPalabras
            if current_phase == 1:
                (list_words_tester, created) = ListaPalabras.objects.get_or_create(
                    tecnica=technique,
                    catador=request.user.user_catador,
                    es_final=False,
                )
            elif current_phase == 2:
                (list_words_tester, created) = ListaPalabras.objects.get_or_create(
                    tecnica=technique,
                    catador=request.user.user_catador,
                    es_final=True,
                )

            added_words = RatingPFListController.addWordsToListWordsTester(
                list_words=words, list_tester=list_words_tester)

            response = JsonResponse({
                "message": "Palabras guardadas con exito",
                "words": [word.nombre_palabra for word in added_words]
            })
        else:
            response = JsonResponse({"error": "Palabras invalidas"})

        return response

    @staticmethod
    def addWordsToListWordsTester(list_words: list[str], list_tester: ListaPalabras):
        # Normalizar
        clean_words = [s.strip() for s in list_words if s.strip()]

        # Obtener existentes
        all_words = Palabra.objects.filter(nombre_palabra__in=clean_words)

        names_words_exist = set(
            all_words.values_list('nombre_palabra', flat=True))

        # Ejecutar el query para no sumar palabras repetidas
        all_words = list(all_words)

        # Determinar faltantes
        missing_words = [
            nombre for nombre in clean_words if nombre not in names_words_exist]
        print("No save words", missing_words)

        created_words = []

        # Intentar crear missing_words
        for nombre in missing_words:
            try:
                with transaction.atomic():
                    palabra, created = Palabra.objects.get_or_create(
                        nombre_palabra=nombre)
                    if created:
                        created_words.append(palabra)
            except IntegrityError:
                palabra = Palabra.objects.get(nombre_palabra=nombre)
                created_words.append(palabra)

        # Combinar todas (all_words + created_words)
        all_new_words = all_words + created_words

        list_tester.palabras.set(all_new_words)

        return all_new_words

    @staticmethod
    def saveRatings(request: HttpRequest, word_rating: str, data: list):
        participation = Participacion.objects.get(
            id=request.session["id_participation"])

        technique = participation.tecnica
        products = Producto.objects.filter(id_tecnica=technique)

        # Crear o obtener las instancias Calificacion en la repeticion de todos los producutos
        ratings = Calificacion.objects.filter(
            num_repeticion=technique.repeticion,
            id_tecnica=technique,
            id_catador=participation.catador,
            id_producto__in=products
        )

        existing_dict = {rating.id_producto_id: rating for rating in ratings}
        to_create = []

        for product in products:
            if product.id not in existing_dict:
                to_create.append(
                    Calificacion(
                        num_repeticion=technique.repeticion,
                        id_producto=product,
                        id_tecnica=technique,
                        id_catador=participation.catador
                    )
                )
        Calificacion.objects.bulk_create(to_create)

        ratings = Calificacion.objects.filter(
            num_repeticion=technique.repeticion,
            id_tecnica=technique,
            id_catador=participation.catador,
            id_producto__in=products
        )

        # Guardar datos con ValorDecimal
        word = Palabra.objects.get(nombre_palabra=word_rating)
        try:
            if (
                len(data) != len(products) or 
                len(data) != len(ratings) or 
                len(products) != len(ratings)
            ):
                raise ValueError(
                    "Al parecer los datos mandados no corresponden con el total de productos")

            product_values = {info["product"]["code"]: info["value"] for info in data}

            datos_to_create = []
            values_to_create = []

            with transaction.atomic():
                for rating in ratings:
                    datos_to_create.append(Dato(
                        id_palabra=word,
                        id_calificacion=rating
                    ))

                datos_save = Dato.objects.bulk_create(datos_to_create)
                save_data = Dato.objects.filter(id_palabra=word, id_calificacion__in=ratings)

                for data_save in save_data:
                    values_to_create.append(ValorDecimal(
                        id_dato=data_save,
                        valor=product_values.get(data_save.id_calificacion.id_producto.codigoProducto)
                    ))

                ValorDecimal.objects.bulk_create(values_to_create)

            return JsonResponse({"message": "Calificaciones guardadas con exito"})
        except ValueError as e:
            error_message = str(e)
            print(f"Error de calificacion: {error_message}")
            return JsonResponse({"error": error_message})
