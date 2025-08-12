from django.urls import path
from django.conf import settings

from . import views

app_name = "cata_system"
urlpatterns = [
    path("", views.mainPanel, name="index"),
    path("autenticacion", views.autentication, name="autenticacion"),
    path("catador-login", views.catadorLogin, name="catador_login"),
    path("panel-catadores", views.managementCatadores, name="panel_catadores"),
    path("panel-sesiones", views.sesionesPanel, name="panel_sesiones"),
    path("seleccion-tecnica", views.selecionTecnica, name="seleccion_tecnica"),
    path("panel-configuracion-basic", views.configuracionPanelBasic, name="panel_configuracion_basic"),
    path("panel-configuracion-tags", views.configuracionPanelTags, name="panel_configuracion_tags"),
    path("panel-configuracion-codes", views.configurationsPanelCodes, name="panel_configuracion_codes"),
    path("nueva-etiqueta", views.newTag, name="nueva_etiqueta"),
    path("crear-catador", views.crearCatador, name="crear_catador"),
    path("buscar-catador", views.searchCatador, name="buscar_catador"),
    path("api/palabras", views.words, name="api_palabras"),
]