from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from controllers import PanelTagsController
from utils import deleteDataSession, delete_images


def configurationPanelTags(req: HttpRequest):
    url_main = req.session["sensorial_url_main"]

    if not req.session.get("form_basic"):
        images_cata = req.session.get("form_images_cata", {})
        if images_cata:
            delete_images(list(images_cata.values()))
        deleteDataSession(req)
        return redirect(reverse(url_main) + "?error=datos requeridos no encontrados")

    basic_data = req.session.get("form_basic")
    name_technique = basic_data["name_tecnica"]

    if req.method == "GET":
        if name_technique in ["escalas", "rata", "perfil flash"]:
            response = PanelTagsController(
                technique_name=name_technique,
                url_main=url_main,
                url_home=url_main
            ).controllGet(
                request=req, data=basic_data
            )
        else:
            response = redirect(reverse(url_main))

        return response

    elif req.method == "POST":
        if name_technique in ["escalas", "rata", "perfil flash"]:
            response = PanelTagsController(
                technique_name=name_technique,
                url_main=url_main,
                url_home=url_main
            ).controllPost(
                request=req, data=basic_data
            )
        else:
            response = redirect(reverse(url_main))
        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
