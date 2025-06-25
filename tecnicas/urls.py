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
]