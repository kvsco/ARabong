from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Member
from django.utils import timezone
from django.contrib import messages


def sign_up(request):
    if request.method == 'GET':
        return render(request, 'member/회원가입.html', {})
    else:
        user_id = request.POST['user_id'] 
        user_pw = request.POST['user_pw']
        user_name = request.POST['user_name']
        user_gender = request.POST['user_gender']
        user_phone = request.POST['user_phone']

        user_id = user_id+"@arabong.com"
        member = Member(user_id=user_id, user_pw=user_pw, user_name=user_name,
                        user_gender=user_gender, user_phone=user_phone)
        member.c_date = timezone.now()
        member.save()
        messages.success(request, '회원가입이 완료되었습니다. 로그인을 해주세요.')
        # return redirect('sign_up/')
        return redirect('page_login')


def page_login(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']

        user_pw = request.POST['user_pw']
        user_name = ""
        user_id = user_id+"@arabong.com"
        try:
            member = Member.objects.get(user_id=user_id, user_pw=user_pw)
            user_name = member.user_name
            request.session['user_name'] = user_name
            request.session['user_id'] = user_id

            return redirect('/firstapp/')
            #return render(request, '/firstapp/')

        except Member.DoesNotExist:
            messages.success(request, '로그인 실패 로그인 정보를 확인하세요.')
            return redirect('page_login')
    else:

        return render(request, 'member/로그인.html')


def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'member/forgot-password.html')

    else:  # post
        email = request.POST['email']
        print(email)

        return render(request, 'member/로그인.html')
