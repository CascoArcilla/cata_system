from django.http import JsonResponse


def general_error(message="informacion incorrecta"):
    result = {"error": message}
    return JsonResponse(result)


def controller_error(message="ha ocurrido un error inesperado"):
    result = {"error": message}
    return result
