from django.urls import path
from django.conf import settings

from . import views

app_name = "cata_system"
urlpatterns = [
    # Atentificacion
    path("autenticacion", views.autentication, name="autenticacion"),
    path("catador-login", views.loginTester, name="catador_login"),


    # Pantalla principal Presetador
    path("presenter/", views.mainPanel, name="index"),
    path("presenter/escalas", views.mainEscalas, name="index_escalas"),
    path("presenter/rata", views.mainRata, name="index_rata"),


    # Creacion de sessiones sensoriales
    path("presenter/seleccion-tecnica", views.selecionTecnica,
         name="seleccion_tecnica"),

    path("presenter/panel-configuracion-basic", views.configurationPanelBasic,
         name="panel_configuracion_basic"),

    path("presenter/panel-configuracion-tags", views.configurationPanelTags,
         name="panel_configuracion_tags"),

    path("presenter/panel-configuracion-codes", views.configurationPanelCodes,
         name="panel_configuracion_codes"),

    path("presenter/panel-configuracion-words", views.configurationPanelWords,
         name="panel_configuracion_words"),

    path("presenter/creando-sesion", views.createSession,
         name="creando_sesion"),

    # Gestion de Vocabularios
    path("presenter/panel-vocabulario",
         views.vocabularyMenu,
         name="panel_vocabulario"),

    path("presenter/crear-vocabulario",
         views.createVocabulary,
         name="crear_vocabulario"),

    path("presenter/ver-vocabulario/<str:nombre_vocabulario>",
         views.viewVocabulary,
         name="ver_vocabulario"),

    path("presenter/lista-vocabulario/<int:num_page>",
         views.listVocabulary,
         name="lista_vocabulario"),

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
    path("presenter/panel-sesiones/<int:page>", views.sesionsList, name="panel_sesiones"),
    path("presenter/escalas/panel-sesiones/<int:page>", views.sesionsListScales, name="panel_sesiones_escalas"),
    path("presenter/rata/panel-sesiones/<int:page>", views.sesionsListRata, name="panel_sesiones_rata"),


    path("presenter/detalles-sesion/<str:session_code>", views.sessionDetails, name="detalles_sesion"),

    path("presenter/monitor/<str:session_code>", views.sessionMonitor, name="monitor_sesion"),


    # Vistas para catadores
    path("testers/catador-main",
         views.mainPanelTester,
         name="catador_main"),

    path("testers/catador-list-sessions/<int:num_page>",
         views.sessionsListTester,
         name="catador_list_sessions"),

    path("testers/subscribe-session",
         views.subscribeSessionTester,
         name="catador_subscribe_session"),

    path("testers/init-session/<str:code_sesion>",
         views.initTesterForm,
         name="catador_init_session"),

    path("testers/init-session/<str:code_sesion>/convencional",
         views.convencionalScales,
         name="session_convencional"),

    path("testers/init-session/<str:code_sesion>/cata",
         views.cataTest,
         name="session_cata"),

    path("testers/init-session/<str:code_sesion>/perfil-flash",
         views.pfTest,
         name="session_pf"),

    path("testers/init-session/<str:code_sesion>/sort",
         views.sortTest,
         name="session_sort"),

    path("testers/init-session/<str:code_sesion>/nappping",
         views.nappingTest,
         name="session_napping"),

    path("testers/init-session/<str:code_sesion>/perfil-ideal/fase1",
         views.perfilIdealPhase1,
         name="session_perfil_ideal_phase1"),

    path("testers/init-session/<str:code_sesion>/perfil-ideal/fase2",
         views.perfilIdealPhase2,
         name="session_perfil_ideal_phase2"),


    # APIs
    path("presenter/api/nueva-etiqueta",
         views.newTag,
         name="nueva_etiqueta"),

    path("presenter/api/palabras",
         views.words,
         name="api_palabras"),

    path("presenter/api/vocabulario/<int:vocab_id>/palabras",
         views.wordsVocabulary,
         name="api_palabras_vocabulary"),

    path("testers/api/ratingword/escalas",
         views.ratingWordScales,
         name="api_rating_word_scalas"),

    path("testers/api/ratingword/cata",
         views.ratingWordCata,
         name="api_rating_word_cata"),

    path("testers/api/ratingword/pf/list",
         views.apiListWordsPF,
         name="api_rating_word_pf_list"),

    path("testers/api/rating-sort",
         views.ratingSort,
         name="api_rating_sort"),

    path("testers/api/rating-napping",
         views.ratingNapping,
         name="api_rating_napping"),

    path("testers/api/ratingword/perfil-ideal/fase1",
         views.ratingPerfilIdealPhase1,
         name="api_rating_perfil_ideal_phase1"),

    path("testers/api/ratingword/perfil-ideal/fase2",
         views.ratingPerfilIdealPhase2,
         name="api_rating_perfil_ideal_phase2"),

    path("testers/api/activity",
         views.UserActivityApi.as_view(),
         name="api_user_activity"),
]
