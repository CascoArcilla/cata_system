from django.urls import path
from django.conf import settings
from . import views

app_name = "scales"
urlpatterns = [
    path("",
         views.main,
         name="main_escalas"),
    path("list-sessions/<int:page>",
         views.list_sessions_scales,
         name="list_sessions"),
    path("conf-basic",
         views.conf_basic_scales_view,
         name="conf_basic_scales"),
    path("conf-tags",
         views.conf_tags,
         name="conf_tags_scales"),
    path("conf-codes",
         views.conf_codes,
         name="conf_codes_scales"),
]
