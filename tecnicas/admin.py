from django.contrib import admin

from .models import CategoriaTecnica, TipoTecnica, TipoEscala, EstiloPalabra

from .models import Catador, Presentador

from .models import Tecnica, SesionSensorial

from .models import EsAtributo, Palabra

from .models import Etiqueta, Escala, EtiquetasEscala

from .models import Producto, Participacion

from .models import Orden, Posicion

from .models import Dato, ValorDecimal, ValorBooleano, Calificacion

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
