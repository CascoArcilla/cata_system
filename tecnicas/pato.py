from django.db import models

class Presentador(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    nombre_usuario = models.CharField(max_length=255)
    contrasena = models.CharField(max_length=255)

class Palabra(models.Model):
    nombre_palabra = models.CharField(max_length=255, unique=True)

class Vocabualario(models.Model):
    nomre_vocabulario = models.CharField(max_length=255, unique=True)
    palabras = models.ManyToManyField(Palabra)

class EstiloPalabra(models.Model):
    nombre_estilo = models.CharField(max_length=255, unique=True)

class EsAtributo(models.Model):
    id_estilo = models.ForeignKey(EstiloPalabra, on_delete=models.CASCADE, related_name="estilo_esatributo")

class ListaPalabra(models.Model):
    id_palabra = models.ForeignKey(Palabra, on_delete=models.CASCADE, related_name="palabra_listapalabras")
    id_atributos = models.ForeignKey(EsAtributo, on_delete=models.CASCADE, related_name="atributo_listapalabras")

class EsVocabulario(models.Model):
    id_estilo = models.ForeignKey(EstiloPalabra, on_delete=models.CASCADE, related_name="estilo_esvacabulario")
    id_vocabulario = models.ForeignKey(Vocabualario, on_delete=models.CASCADE, related_name="vocabulario_esvocabulario")

class Tecnica(models.Model):
    nombre_tecnica = models.CharField(max_length=255)
    maximas_repeticiones = models.IntegerField(default=0)
    repecion = models.IntegerField(default=0)
    limite_catadores = models.IntegerField()
    instrucciones = models.CharField(max_length=255)
    id_estilo = models.ForeignKey(EstiloPalabra, on_delete=models.CASCADE, related_name="estilo_tecnica")

class SesionSensorial(models.Model):
    fechaCreacion = models.DateTimeField("date published")
    activo = models.BooleanField(default=False)
    creadoPor = models.ForeignKey(Presentador, on_delete=models.CASCADE, related_name="presentador_sesion")
    tecnica = models.ForeignKey(Tecnica, on_delete=models.CASCADE, related_name="sesion_tecnica")