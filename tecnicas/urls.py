from django.urls import path
from django.conf import settings

from . import views

app_name = "cata_system"
urlpatterns = [
    # Atentificacion
    path("autenticacion",
         views.autentication,
         name="autenticacion"),

    path("catador-login",
         views.testerLogin,
         name="catador_login"),


    # Pantalla principal Presetador
    path("presenter/", views.mainPanel, name="index"),


    # Creacion de sessiones sensoriales
    path("presenter/seleccion-tecnica",
         views.selecionTecnica,
         name="seleccion_tecnica"),

    path("presenter/panel-configuracion-basic",
         views.configurationPanelBasic,
         name="panel_configuracion_basic"),

    path("presenter/panel-configuracion-tags",
         views.configurationPanelTags,
         name="panel_configuracion_tags"),

    path("presenter/panel-configuracion-codes",
         views.configurationPanelCodes,
         name="panel_configuracion_codes"),

    path("presenter/panel-configuracion-words",
         views.configurationPanelWords,
         name="panel_configuracion_words"),

    path("presenter/creando-sesion",
         views.createSession,
         name="creando_sesion"),


    # Gestion de catadores
    path("presenter/panel-catadores",
         views.testerMenu,
         name="panel_catadores"),

    path("presenter/crear-catador",
         views.testerCreate,
         name="crear_catador"),

    path("presenter/buscar-catador",
         views.testerSearch,
         name="buscar_catador"),

    path("presenter/listar-catador/<int:num_page>",
         views.testerList,
         name="listar_catador"),


    # Gestion de sesiones sensoriales
    path("presenter/panel-sesiones/<int:page>",
         views.sesionsPanel,
         name="panel_sesiones"),

    path("presenter/detalles-sesion/<str:session_code>",
         views.sessionDetails,
         name="detalles_sesion"),

    path("presenter/monitor/<str:session_code>",
         views.sessionMonitor,
         name="monitor_sesion"),


    # Vistas para catadores
    path("testers/catador-main",
         views.mainTesterForm,
         name="catador_main"),

    path("testers/en-session/convencional",
         views.convencionalScales,
         name="session_convencional"),


    # APIs
    path("api/nueva-etiqueta",
         views.newTag,
         name="nueva_etiqueta"),

    path("api/palabras",
         views.words,
         name="api_palabras"),

    path("testers/api/ratingword",
         views.reatingWord,
         name="api_rating_word"),
]
