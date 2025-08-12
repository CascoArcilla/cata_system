from django.http import JsonResponse

def general_error(message="informacion incorrecta"):
    respuesta = { "error" : message }
    return JsonResponse(respuesta)