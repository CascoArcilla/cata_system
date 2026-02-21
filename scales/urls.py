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
#     path("conf_tags",
#          views.main,
#          name="scales_conf_tags"),
#     path("conf_codes",
#          views.main,
#          name="scales_conf_codes"),
]
