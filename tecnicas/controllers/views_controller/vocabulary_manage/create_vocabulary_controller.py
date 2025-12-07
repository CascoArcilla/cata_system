from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpRequest
from tecnicas.forms import WordForm
from tecnicas.models import Vocabulario, Palabra
import json


class CreateVocabularyController():
    context = {}
    current_url = "tecnicas/manage_vocabulary/create-vocabulary.html"

    def __init__(self, form_word: WordForm = WordForm(), list_words: list = []):
        self.context["form_word"] = form_word
        self.context["words"] = list_words

    def controllGet(self, request: HttpRequest):
        self.context = {
            "form_word": WordForm(),
            "words": []
        }

        if "name_voca" in request.GET:
            current = Vocabulario.objects.get(
                nombre_vocabulario=request.GET["name_voca"])
            self.context["name_vacabulary"] = current.nombre_vocabulario
            self.context["words"] = current.palabras.all()

        return render(request, self.current_url, self.context)

    def controllPost(self, request: HttpRequest):
        self.context = {
            "form_word": self.context["form_word"],
            "words": self.context["words"],
        }

        if "nombre_vocabulario" not in request.POST:
            self.context["error"] = "Nombre de vocabulario requerido"
            return render(request, self.current_url, self.context)

        new_vocabulary_name = request.POST.get("nombre_vocabulario").strip()
        is_update = request.POST.get("is_update")

        if is_update:
            if "original_name" not in request.POST:
                self.context["error"] = "Nombre original de vocabulario requerido"
                return render(request, self.current_url, self.context)

            original_name = request.POST["original_name"].strip()

            if original_name != new_vocabulary_name:
                if Vocabulario.objects.filter(nombre_vocabulario=new_vocabulary_name).exists():
                    self.context["error"] = "Ya existe un vocabulario con el nombre pasado"
                    return render(request, self.current_url, self.context)

            try:
                current_vocababulary = Vocabulario.objects.get(
                    nombre_vocabulario=original_name)
            except Vocabulario.DoesNotExist:
                self.context["error"] = "No existe un vocabulario con ese nombre"
                return render(request, self.current_url, self.context)

            words_json = request.POST.get("words", "")
            if words_json:
                try:
                    words_list = json.loads(words_json)

                    ids = [int(w.get("id", 0))
                           for w in words_list if str(w.get("id", "")).isdigit()]

                    words = Palabra.objects.filter(id__in=ids)

                    current_vocababulary.palabras.set(words)
                    current_vocababulary.nombre_vocabulario = new_vocabulary_name
                    current_vocababulary.save()
                except (json.JSONDecodeError, ValueError):
                    self.context["error"] = 'Ocurrió un error al revisar las palabras, revise “Ver vocabularios”, para reasignar las palabras'
                    return render(request, self.current_url, self.context)

            self.context["message"] = 'Vocabulario creado con éxito, puedes revisarlo en "Ver vocabularios"'
            return render(request, self.current_url, self.context)
        elif not is_update:
            try:
                new_vocababulary = Vocabulario.objects.create(
                    nombre_vocabulario=new_vocabulary_name)
            except IntegrityError:
                self.context["error"] = "Ya existe un vocabulario con ese nombre"
                return render(request, self.current_url, self.context)

            words_json = request.POST.get("words", "")
            if words_json:
                try:
                    words_list = json.loads(words_json)

                    ids = [int(w.get("id", 0))
                           for w in words_list if str(w.get("id", "")).isdigit()]

                    words = Palabra.objects.filter(id__in=ids)

                    new_vocababulary.palabras.add(*words)
                except (json.JSONDecodeError, ValueError):
                    self.context["error"] = 'Ocurrió un error al revisar las palabras, revise “Ver vocabularios”, para reasignar las palabras'
                    return render(request, self.current_url, self.context)

            self.context["message"] = 'Vocabulario actualziado con éxito, puedes revisarlo en "Ver vocabularios"'
            return render(request, self.current_url, self.context)
        else:
            pass
