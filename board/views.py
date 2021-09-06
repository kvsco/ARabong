from django.db import models
import requests
from bs4 import BeautifulSoup as bs
import datetime
from django.http import request
from django.utils import timezone
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import Point, B_list_write, Promise, Member, Usercount
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict


@csrf_exempt
def map(request):
    if request.method == "POST":
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        title = request.POST.get('title')
        p = Point(title=title, lat=lat, lng=lng)
        p.save()

    if request.method == "GET":
        if request.GET.get('userCount'):
            usercount = request.GET.get('userCount')
            roomname = request.GET.get('roomname')
            roomurl = request.GET.get('roomUrl')
            # print(usercount)
            # print(roomname)
            u = Usercount(roomName=roomname, roomUrl=roomurl, userCount=usercount)
            u.save()

        return render(request, 'board/map.html', {})

    return HttpResponse("not anything")


def map_data(request):
    p_object = Point.objects.all()
    p_list = []
    for i in p_object:
        i = model_to_dict(i)
        p_list.append(i)

    return JsonResponse(p_list, safe=False)

def room_data(request):
    u_object = Usercount.objects.all()
    u_list = []
    for i in u_object:
        i = model_to_dict(i)
        u_list.append(i)

    return JsonResponse(u_list, safe=False)


class Board_ListView(ListView):
    model = B_list_write
    paginate_by = 5
    context_object_name = 'listview'
    template_name = 'board/list.html'

    def get_queryset(self):  # 게시글의 리스트를 최근 작성순으로 표시
        listview = B_list_write.objects.order_by('-id')
        return listview

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) /
                          page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context

    def Board_list(request):
        article_list = B_list_write.objects.all()
        context = {
            'article_list': article_list
        }

        return render(request, 'board/list.html', context)


def Page(request):
    Board_list = B_list_write.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(Board_list, '1')
    page_obj = paginator.page(page)
    return render(request, 'board/list.html', {'page_obj': page_obj})


def Board_write(request):
    if request.method == 'GET':
        return render(request, 'board/write.html')

    else:
        t = request.POST['title']
        c = request.POST['contents']
        w = B_list_write(title=t, contents=c, date=timezone.now(),
                         member_id=request.session['user_id'])
        w.save()

        return redirect('../board_list/')


def comment(request, index_id):

    post = B_list_write.objects.get(id=index_id)
    co = request.POST.get('content')
    user_id = request.session['user_id']
    author = Member.objects.get(user_id=user_id)
    d = post.comment_set.create(author=author, content=co, date=timezone.now())
    d.save()
    return render(request, 'board/read.html', {'post': post})


def Board_rewrite(request, index_id):
    bw = B_list_write.objects.get(id=index_id)
    # bw.member_id == request.session['member_id']
    if request.method == 'POST':
        n_title = request.POST.get('title')
        n_contents = request.POST.get('contents')
        bw.title = n_title
        bw.contents = n_contents
        bw.save()
        return redirect('/board/board_read/%s/' % index_id)
    else:
        return render(request, 'board/rewrite.html', {'bw': bw})


def Board_delete(request, index_id):
    bw = B_list_write.objects.get(id=index_id)

    bw.delete()
    return redirect('../../../board/board_list/')


def Board_read(request, id):
    if request.method == "GET":
        # article = get_object_or_404(B_list_write, pk = pk)
        # try:
        article = B_list_write.objects.get(id=id)
        print(article)
        print(article.comment_set.all())
        context = {
            'index_id': id,
            'id': article.member_id,
            'title': article.title,
            'contents': article.contents,
            'date': article.date,
            'article': article
        }
        return render(request, 'board/read.html', context)


def promise(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        user_name = request.session['user_name']
        title = request.POST['p_title']
        type = request.POST.getlist('p_type[]')
        time = request.POST['p_time']
        contents = request.POST['p_contents']
        print(time)

        p = Promise(name=user_name, member_id=user_id, title=title,
                    contents=contents, time=time, type=type)
        p.save()
        messages.success(request, '약속 등록 완료!!')

        return redirect('promise')
    else:
        try:
            page = request.GET.get('page')
            if not page:
                page = 1

            p_list = Promise.objects.order_by('-id')
            p = Paginator(p_list, 5)
            info = p.page(page)
            start_page = (int(page) - 1) // 10 * 10 + 1
            end_page = start_page + 9

            if end_page > p.num_pages:
                end_page = p.num_pages

            context = {
                'info': info,
                'pagination': range(start_page, end_page+1),
            }

            return render(request, 'board/promise.html', context)
        except:
            return render(request, 'board/promise.html')


def promise_write(request):
    return render(request, 'board/promise_write.html', {})


def promise_read(request, id):
    if id:
        p = Promise.objects.get(id=id)
        title = p.title
        contents = p.contents
        time = p.time
        type = p.type
        name = p.name
        context = {
            'name': name,
            'type': type,
            'time': time,
            'title': title,
            'contents': contents
        }
        return render(request, 'board/promise_read.html', context)
    else:
        return HttpResponse("id load 실패")


def news(request):
    res = requests.get("http://news.tf.co.kr/list/all")
    soup = bs(res.text, 'html.parser')
    n_title = soup.select('.txtList > ul > li > a')
    n_date = timezone.now()
    news_list = []
    i_count = 0
    # print(n_date)
    for i in n_title:
        i_count += 1
        dic = {
            'index': i_count,
            'title': i.string,
            'link': i.attrs['href']
        }
        news_list.append(dic)
    context = {
        'date': n_date,
        'news_list': news_list
    }
    return render(request, 'board/news.html', context)


def promotion(request):
    return render(request, 'board/promotion.html', {})


def help(request):
    return render(request, 'board/help.html', {})
