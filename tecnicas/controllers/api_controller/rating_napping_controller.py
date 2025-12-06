from django.http import JsonResponse
from django.http import HttpRequest
from django.db import transaction
from tecnicas.models import Calificacion, DatoPunto, Producto, Participacion, Palabra, GrupoProducto, TecnicaModalidad
from tecnicas.forms import ListWordsForm


class RatingNappingController:
    @staticmethod
    def saveRatingCoordinates(request: HttpRequest, data: list | dict):
        participation = Participacion.objects.get(
            id=request.session["id_participation"]
        )

        name_mod = TecnicaModalidad.objects.get(
            tecnica=participation.tecnica
        ).modalidad.nombre.lower()

        # Branch based on modality
        if name_mod == 'sorting':
            return RatingNappingController.processSortingMode(
                data, participation
            )

        if name_mod in ['sin modalidad', 'perfil ultra flash']:
            return RatingNappingController.processNappOrPUF(
                data, participation
            )

        else:
            return JsonResponse({"error": "Modalidad no soportada"})

    @staticmethod
    def processSortingMode(data: dict, participation):
        try:
            with transaction.atomic():
                # Extract products array (always present)
                products = data.get("products", [])
                if not products:
                    return JsonResponse({"error": "No se proporcionaron productos"})

                existing_ratings_map, products_map = RatingNappingController.savePoints(
                    isSorting=True, products=products, participation=participation
                )

                # Process groups if they exist
                groups = data.get("groups", {})
                if groups:
                    RatingNappingController.processGroupsForSorting(
                        products, groups, participation, existing_ratings_map, products_map
                    )
                else:
                    RatingNappingController.deleteAllGroups(participation)

            return JsonResponse({"message": "Datos guardados exitosamente"})

        except Exception as e:
            print("ERROR:", e)
            import traceback
            traceback.print_exc()
            return JsonResponse({"error": f"Error al procesar datos: {str(e)}"})

    @staticmethod
    def processNappOrPUF(data: list, participation):
        try:
            with transaction.atomic():
                existing_ratings_map, products_map = RatingNappingController.savePoints(
                    isSorting=False, products=data, participation=participation
                )

                RatingNappingController.processWordsForRatings(
                    data, existing_ratings_map
                )

            return JsonResponse({"message": "Datos guardados exitosamente"})

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"error": "Error al procesar datos"})

    @staticmethod
    def processGroupsForSorting(products, groups, participation, existing_ratings_map, products_map):
        """Process groups for sorting mode
        - Creates/updates GrupoProducto instances
        - Ensures products don't belong to multiple groups
        - Associates words with groups
        """
        # Build mapping of product_id to group_id from products array
        product_to_group = {}
        for product_item in products:
            group_code = product_item.get("group", "")
            if group_code:  # Only if product has a group assigned
                product_id = int(product_item["idProduct"])
                if product_id in product_to_group:
                    raise ValueError(
                        f"Producto {product_id} pertenece a múltiples grupos")
                product_to_group[product_id] = group_code

        # Get existing groups for this catador and technique
        existing_groups = GrupoProducto.objects.filter(
            tecnica=participation.tecnica,
            catador=participation.catador
        )

        # Create a map of existing groups by their product composition
        # We'll identify groups by the set of products they contain
        existing_groups_map = {}
        for group in existing_groups:
            product_ids = set(group.productos.values_list('id', flat=True))
            key = frozenset(product_ids)
            existing_groups_map[key] = group

        # Build new groups structure
        groups_to_create = []
        groups_to_update = []
        group_products_map = {}  # group_id -> [product_ids]

        # Organize products by group
        for product_id, group_code in product_to_group.items():
            if group_code not in group_products_map:
                group_products_map[group_code] = []
            group_products_map[group_code].append(product_id)

        # Process each group
        for group_code, product_ids in group_products_map.items():
            product_set = frozenset(product_ids)

            # Check if this group already exists
            if product_set in existing_groups_map:
                group = existing_groups_map[product_set]
                groups_to_update.append((group, group_code))
            else:
                # Create new group
                group = GrupoProducto(
                    tecnica=participation.tecnica,
                    catador=participation.catador
                )
                groups_to_create.append((group, product_ids, group_code))

        # Create new groups
        created_groups = []
        for group, product_ids, group_code in groups_to_create:
            group.save()  # Save first to get ID for M2M

            # Add products to group
            productos = [products_map[pid]
                         for pid in product_ids if pid in products_map]
            group.productos.set(productos)

            created_groups.append((group, group_code))

        # Combine created and existing groups for word processing
        all_groups_for_words = created_groups + groups_to_update

        # Delete groups that no longer exist
        current_group_sets = set(frozenset(pids)
                                 for pids in group_products_map.values())
        for product_set, group in existing_groups_map.items():
            if product_set not in current_group_sets:
                group.delete()

        # Process words for groups
        if groups:
            RatingNappingController.processWordsForGroups(
                groups, all_groups_for_words
            )
    
    @staticmethod
    def deleteAllGroups(participation):
        GrupoProducto.objects.filter(
            tecnica=participation.tecnica,
            catador=participation.catador
        ).delete()

    @staticmethod
    def processWordsForGroups(groups_data, groups_list):
        """Process and associate words to groups
        - Creates words that don't exist
        - Associates words to GrupoProducto instances
        - Handles concurrency
        """
        # Collect all unique words from all groups
        all_words = set()
        for group_id, words in groups_data.items():
            if words:
                all_words.update(words)

        if not all_words:
            # No words to process, just clear existing words from groups
            for grupo, _ in groups_list:
                grupo.palabras.clear()
            return

        # Get existing words
        existing_words = Palabra.objects.filter(
            nombre_palabra__in=all_words
        )
        existing_words_map = {w.nombre_palabra: w for w in existing_words}

        # Create missing words with concurrency handling
        word_objects = {}
        for word_name in all_words:
            if word_name in existing_words_map:
                word_objects[word_name] = existing_words_map[word_name]
            else:
                word_obj, created = Palabra.objects.get_or_create(
                    nombre_palabra=word_name
                )
                word_objects[word_name] = word_obj

        # Associate words with groups
        for grupo, group_id in groups_list:
            words = groups_data.get(group_id, [])
            if words:
                words_to_set = [word_objects[word_name]
                                for word_name in words if word_name in word_objects]
                grupo.palabras.set(words_to_set)
            else:
                grupo.palabras.clear()

    @staticmethod
    def savePoints(isSorting: bool, products, participation):
        try:
            with transaction.atomic():
                # Get products map for validation
                products_map = RatingNappingController.getProductsMap(
                    participation.tecnica)

                # Get existing ratings map
                existing_ratings_map = RatingNappingController.getExistingRatingsMap(
                    participation.tecnica, participation.catador)

                if not isSorting:
                    validation_result = RatingNappingController.validateWords(
                        products)
                    if validation_result is not None:
                        return validation_result

                # Create new ratings for products that don't have them
                new_ratings = []
                ids_products = products_map.keys()
                for item in products:
                    product_id = int(item["idProduct"])
                    if product_id not in existing_ratings_map and product_id in ids_products:
                        new_ratings.append(
                            Calificacion(
                                num_repeticion=0,
                                id_producto=products_map[product_id],
                                id_tecnica=participation.tecnica,
                                id_catador=participation.catador,
                            )
                        )

                if new_ratings:
                    Calificacion.objects.bulk_create(new_ratings)
                    existing_ratings_map = RatingNappingController.getExistingRatingsMap(
                        participation.tecnica, participation.catador)

                # Process DatoPunto instances from products array
                existing_points_map = RatingNappingController.getExistingPointsMap(
                    existing_ratings_map.values())

                points_to_create = []
                points_to_update = []

                for item in products:
                    product_id = int(item["idProduct"])
                    rating = existing_ratings_map.get(product_id)

                    if rating:
                        if rating.id in existing_points_map:
                            point = existing_points_map[rating.id]
                            point.x = item["x"]
                            point.y = item["y"]
                            points_to_update.append(point)
                        else:
                            points_to_create.append(
                                DatoPunto(
                                    x=item["x"],
                                    y=item["y"],
                                    calificacion=rating,
                                )
                            )

                if points_to_create:
                    DatoPunto.objects.bulk_create(points_to_create)

                if points_to_update:
                    DatoPunto.objects.bulk_update(points_to_update, ['x', 'y'])

                return (existing_ratings_map, products_map)

        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error al guardar los puntos"})

    @staticmethod
    def validateWords(data: list):
        for item in data:
            words = item.get("words", [])
            if words:
                dic_words = {}
                for index, word in enumerate(words, start=1):
                    dic_words[f"palabra_{index}"] = word

                form = ListWordsForm(dic_words, new_words=words)
                if not form.is_valid():
                    errors = []
                    for field, error_list in form.errors.items():
                        errors.extend(error_list)
                    return JsonResponse({"error": f"Error en validación de palabras: {', '.join(errors)}"})
        return None

    @staticmethod
    def processWordsForRatings(data: list, existing_ratings_map: dict):
        all_words = set()
        for item in data:
            words = item.get("words", [])
            if words:
                all_words.update(words)

        if not all_words:
            return

        existing_words = Palabra.objects.filter(
            nombre_palabra__in=all_words
        )
        existing_words_map = {w.nombre_palabra: w for w in existing_words}

        word_objects = {}
        for word_name in all_words:
            if word_name in existing_words_map:
                word_objects[word_name] = existing_words_map[word_name]
            else:
                word_obj, created = Palabra.objects.get_or_create(
                    nombre_palabra=word_name
                )
                word_objects[word_name] = word_obj

        for item in data:
            words = item.get("words", [])
            if words:
                product_id = int(item["idProduct"])
                rating = existing_ratings_map.get(product_id)

                if rating:
                    words_to_set = [word_objects[word_name]
                                    for word_name in words]
                    rating.palabras.set(words_to_set)

    @staticmethod
    def getProductsMap(id_tecnica):
        products_qs = Producto.objects.filter(id_tecnica=id_tecnica)
        return {p.id: p for p in products_qs}

    @staticmethod
    def getExistingRatingsMap(id_tecnica, id_catador):
        ratings = Calificacion.objects.filter(
            id_tecnica=id_tecnica,
            id_catador=id_catador,
        )
        return {r.id_producto.id: r for r in ratings}

    @staticmethod
    def getExistingPointsMap(ratings):
        points = DatoPunto.objects.filter(calificacion__in=ratings)
        return {p.calificacion.id: p for p in points}
