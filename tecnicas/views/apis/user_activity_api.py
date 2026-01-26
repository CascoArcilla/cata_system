from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from tecnicas.models import SesionSensorial
from tecnicas.controllers import ParticipacionController

@method_decorator(csrf_exempt, name='dispatch')
class UserActivityApi(View):
    def post(self, request: HttpRequest):
        try:
            action = request.POST.get('action')
            session_code = request.POST.get('session_code')
            
            if not request.user.is_authenticated or not hasattr(request.user, 'user_catador'):
                return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)
                
            try:
                session = SesionSensorial.objects.get(codigo_sesion=session_code)
            except SesionSensorial.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Session not found'}, status=404)

            tester = request.user.user_catador

            if action == 'heartbeat':
                ParticipacionController.updateActivity(tester, session)
                return JsonResponse({'status': 'success', 'message': 'Heartbeat received'})

            elif action == 'exit':
                ParticipacionController.outSession(tester, session)
                return JsonResponse({'status': 'success', 'message': 'Exit received'})
            
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
