from django.contrib import admin

from .models import CategoriaTecnica, TipoTecnica, TipoEscala, EstiloPalabra, Catador, Presentador, Tecnica, SesionSensorial, EsAtributo, Palabra, Vocabulario, Etiqueta, Escala, EtiquetasEscala, Producto, Participacion, Orden, Posicion, Dato, ValorDecimal, ValorBooleano, Calificacion, CalificacionEscala, ListaPalabras, GrupoProducto, Modalidad, TecnicaModalidad, DatoPunto, DatoHedonico

# Register your models here.
admin.site.register(CategoriaTecnica)
admin.site.register(TipoEscala)
admin.site.register(Etiqueta)
admin.site.register(TipoTecnica)
admin.site.register(EstiloPalabra)

admin.site.register(Catador)
admin.site.register(Presentador)

admin.site.register(Tecnica)
admin.site.register(SesionSensorial)

admin.site.register(EsAtributo)
admin.site.register(Palabra)
admin.site.register(Vocabulario)

admin.site.register(Escala)
admin.site.register(EtiquetasEscala)

admin.site.register(Producto)
admin.site.register(Participacion)

admin.site.register(Orden)
admin.site.register(Posicion)

admin.site.register(Dato)
admin.site.register(ValorDecimal)
admin.site.register(ValorBooleano)
admin.site.register(Calificacion)
admin.site.register(CalificacionEscala)
admin.site.register(DatoHedonico)

admin.site.register(ListaPalabras)
admin.site.register(GrupoProducto)

admin.site.register(Modalidad)
admin.site.register(TecnicaModalidad)

admin.site.register(DatoPunto)
