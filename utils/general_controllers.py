from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode


def getId(value: object | int) -> int | None:
    if isinstance(value, int):
        return value
    elif hasattr(value, "id"):
        return value.id
    elif hasattr(value, "pk"):
        return value.pk

    return None


def noValidTechnique(params: dict, query_params: dict, name_view: str):
    if query_params:
        query_string = urlencode(query_params)
        url_redireccion = f"{reverse(name_view, kwargs=params)}?{query_string}"
    else:
        url_redireccion = f"{reverse(name_view, kwargs=params)}"
    return redirect(url_redireccion)
