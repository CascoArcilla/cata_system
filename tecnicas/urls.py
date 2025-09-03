from django.urls import path
from django.conf import settings

from . import views

app_name = "cata_system"
urlpatterns = [
    path("", views.mainPanel, name="index"),
    path("autenticacion", views.autentication, name="autenticacion"),
    path("catador-login", views.catadorLogin, name="catador_login"),
    path("panel-catadores", views.managementCatadores, name="panel_catadores"),
    path("panel-sesiones", views.sesionsPanel, name="panel_sesiones"),
    path("seleccion-tecnica", views.selecionTecnica, name="seleccion_tecnica"),
    path("panel-configuracion-basic", views.configurationPanelBasic, name="panel_configuracion_basic"),
    path("panel-configuracion-tags", views.configurationPanelTags, name="panel_configuracion_tags"),
    path("panel-configuracion-codes", views.configurationPanelCodes, name="panel_configuracion_codes"),
    path("panel-configuracion-words", views.configurationPanelWords, name="panel_configuracion_words"),
    path("creando-sesion", views.createSession, name="creando_sesion"),
    path("nueva-etiqueta", views.newTag, name="nueva_etiqueta"),
    path("crear-catador", views.testerCreate, name="crear_catador"),
    path("buscar-catador", views.testerSearch, name="buscar_catador"),
    path("api/palabras", views.words, name="api_palabras"),
]