from django.http.response import JsonResponse
from config.settings import STATICFILES_DIRS
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.shortcuts import redirect, render
from board.models import Promise, B_list_write, Usercount
# Create your views here.


def index(request):
    promise = Promise.objects.order_by('-id')[:3]
    anonymous = B_list_write.objects.order_by('-id')[:3]
    user_num =  Usercount.objects.order_by('-userCount')[:4]
    context = {
        'promise': promise,
        'anonymous': anonymous,
        'user_num': user_num,
    }
    return render(request, 'firstapp/메인.html', context)


def sign_out(request):
    del request.session['user_name']
    del request.session['user_id']

    return render(request, 'firstapp/메인.html')


@csrf_exempt
def app_profile(request):
    username = request.session.get('user_name')
    today = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    if request.method == 'POST':
        dataurl = request.FILES.get('image')
        path = 'static/images/profile/'+username + '.png'
        with open(path, 'wb') as file:
            for chunk in dataurl.chunks():
                file.write(chunk)

        result = {'result': 200, 'path': '/%s' % path}
        return JsonResponse(result)

    return render(request, 'firstapp/app-profile.html', {})
