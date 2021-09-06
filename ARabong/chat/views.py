from config.settings import STATICFILES_DIRS
from django.conf import settings as django_settings
from datetime import datetime
from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import datetime

def index(request):
    
    return render(request, 'chat/index.html', {})

@csrf_exempt
def room(request, room_name):
    username = request.session.get('user_name')
    
    today = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    if request.method == 'POST':
        blob = request.FILES.get('blob')
        path = 'static/audio/'+username +"_"+ today +'.wav'
        with open(path, 'wb') as file:
            for chunk in blob.chunks():
                file.write(chunk)

        result = {'result': 200, 'path': '/%s' % path}
        return JsonResponse(result)

    return render(request, 'chat/room.html', {
        'room_name': room_name
    })