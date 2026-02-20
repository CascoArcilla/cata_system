from django.urls import path
from django.conf import settings
from . import views

app_name = "scales"
urlpatterns = [
    path("",
         views.main,
         name="main_escalas"),
#     path("conf-basic",
#          views.main,
#          name="scales_confi_basic"),
#     path("conf_tags",
#          views.main,
#          name="scales_conf_tags"),
#     path("conf_codes",
#          views.main,
#          name="scales_conf_codes"),
]
