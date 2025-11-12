'''
Para finalizar la sesion se debe realizar lo siguiente
# Obtener todas las participaciones

'''
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import SesionSensorial
from tecnicas.controllers import MonitorEscalasController, MonitorRATAController, MonitorPFController
from tecnicas.utils import noValidTechnique


def sessionMonitor(req: HttpRequest, session_code: str):
    if req.method == "GET":
        sensorial_session = SesionSensorial.objects.get(
            codigo_sesion=session_code)
        use_techinique = sensorial_session.tecnica.tipo_tecnica.nombre_tecnica

        if use_techinique == "escalas" or use_techinique == "rata" or use_techinique == "cata":
            controll_view = MonitorEscalasController(sensorial_session)
            response = controll_view.controllGetResponse(request=req)

        elif use_techinique == "perfil flash":
            controll_view = MonitorPFController(sensorial_session)
            response = controll_view.controllGetResponse(request=req)

        else:
            response = noValidTechnique(
                params={
                    "session_code": session_code,
                },
                query_params={
                    "message": "Aun no se puede monitorear sesiones con esta técnica"
                },
                name_view="cata_system:detalles_sesion"
            )
        return response
    elif req.method == "POST":
        sensorial_session = SesionSensorial.objects.get(
            codigo_sesion=session_code)
        use_techinique = sensorial_session.tecnica.tipo_tecnica.nombre_tecnica

        if use_techinique == "escalas":
            controll_view = MonitorEscalasController(sensorial_session)
            action = req.POST["action"]

            if action == "finish_session":
                response = controll_view.controllPostFinishSession(
                    request=req)
            else:
                response = controll_view.controlGetResponse(
                    request=req, error="No se ha definido la acción a realizar")

        elif use_techinique == "rata" or use_techinique == "cata":
            controll_view = MonitorRATAController(sensorial_session)
            action = req.POST["action"]

            if action == "finish_session":
                response = controll_view.controllPostFinishSession(
                    request=req)
            else:
                response = controll_view.controlGetResponse(
                    request=req, error="No se ha definido la acción a realizar")

        elif use_techinique == "perfil flash":
            controll_view = MonitorPFController(sensorial_session)
            action = req.POST["action"]

            if action == "finish_session":
                response = controll_view.controllPostFinishSession(
                    request=req)
            else:
                response = controll_view.controlGetResponse(
                    request=req, error="No se ha definido la acción a realizar")

        else:
            response = noValidTechnique(
                params={
                    "session_code": session_code,
                },
                query_params={
                    "message": "La técnica usada en la sesión aun no se implementa para esta función"
                },
                name_view="cata_system:detalles_sesion"
            )

        return response
    else:
        return JsonResponse({"error": "Método no permitido"})
