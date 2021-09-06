"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    #지도둘러보기
    path('map/', views.map, name='map'),
    path('map_data/', views.map_data, name='map_data'),
    path('room_data/', views.room_data, name='room_data'),
    
    #익명게시판
    path('board_list/', views.Board_ListView.as_view(), name='board_list'),
    path('board_write/', views.Board_write, name='board_write'),
    path('board_read/<int:id>/', views.Board_read, name='Board_read'),
    path('board_rewrite/<int:index_id>/', views.Board_rewrite, name='board_rewrite'),
    path('board_delete/<int:index_id>/', views.Board_delete, name='board_delete'),
    path('board_read/<int:index_id>/comment/', views.comment, name='comment'),
    
    #약속게시판
    path('promise/', views.promise, name='promise'),
    path('promise_write/', views.promise_write, name='promise_write'),    
    path('promise_read/<int:id>/', views.promise_read, name='Board_read'),

    #뉴스게시판
    path('news/', views.news, name='news'),

    #홍보게시판
    path('promotion/', views.promotion, name='promotion'),

    #도움말
    path('help/', views.help, name='help'),

]
