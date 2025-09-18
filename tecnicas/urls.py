from django.urls import path
from django.conf import settings

from . import views

app_name = "cata_system"
urlpatterns = [
    path("", views.mainPanel, name="index"),

    # Atentificacion
    path("autenticacion",
         views.autentication,
         name="autenticacion"),

    path("catador-login",
         views.testerLogin,
         name="catador_login"),


    # Gestion de catadores
    path("panel-catadores",
         views.testerMenu,
         name="panel_catadores"),

    path("crear-catador",
         views.testerCreate,
         name="crear_catador"),

    path("buscar-catador",
         views.testerSearch,
         name="buscar_catador"),


    # Creacion de sessiones sensoriales
    path("seleccion-tecnica",
         views.selecionTecnica,
         name="seleccion_tecnica"),

    path("panel-configuracion-basic",
         views.configurationPanelBasic,
         name="panel_configuracion_basic"),

    path("panel-configuracion-tags",
         views.configurationPanelTags,
         name="panel_configuracion_tags"),

    path("panel-configuracion-codes",
         views.configurationPanelCodes,
         name="panel_configuracion_codes"),

    path("panel-configuracion-words",
         views.configurationPanelWords,
         name="panel_configuracion_words"),

    path("creando-sesion",
         views.createSession,
         name="creando_sesion"),


    # Gestion de sesiones sensoriales
    path("panel-sesiones/<int:page>",
         views.sesionsPanel,
         name="panel_sesiones"),

    path("detalles-sesion/<str:session_code>",
         views.sessionDetails,
         name="detalles_sesion"),


    # APIs
    path("nueva-etiqueta",
         views.newTag,
         name="nueva_etiqueta"),

    path("api/palabras",
         views.words,
         name="api_palabras"),
]
