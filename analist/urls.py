from django.urls import path, include
from django.conf import settings
from . import views

app_name = "analist"
urlpatterns = [
    path("login", views.login_analist, name="login_analista"),
    path("escalas/", include("scales.urls")),
]
