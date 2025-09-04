from django.contrib import admin

from .models import CategoriaTecnica
from .models import TipoTecnica
from .models import TipoEscala
from .models import EstiloPalabra

from .models import Catador
from .models import Presentador

from .models import Tecnica
from .models import SesionSensorial

from .models import EsAtributo
from .models import Palabra

from .models import Etiqueta

from .models import Escala
from .models import EtiquetasEscala

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