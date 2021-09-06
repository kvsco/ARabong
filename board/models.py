from django.db import models
from member.models import Member

# Create your models here.

# 지도 모델
class Point(models.Model):
    title = models.CharField(max_length=100, null=True)
    lat = models.FloatField()
    lng = models.FloatField()

# 채팅방 인원 수 모델
class Usercount(models.Model):
    roomName = models.CharField(max_length=100, primary_key=True)
    roomUrl = models.CharField(max_length=100)
    userCount = models.IntegerField()

# 익명게시판 모델
class B_list_write(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.TextField(max_length=100)
    contents = models.TextField()
    date = models.DateTimeField(null=True, blank=True)
    # writer = models.ForeignKey('fcuser.Fcuser', verbose_name="작성자", on_delete=models.CASCADE)
    # registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")
    # user_id = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.title

# 약속게시판 모델
class Promise(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.TextField(max_length=100)
    contents = models.TextField(null=True)
    time = models.TextField(null=True)
    type = models.TextField(null=True)
    name = models.CharField(max_length=50)
    
class Comment(models.Model):
    post = models.ForeignKey(B_list_write, on_delete=models.CASCADE)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    date = models.DateTimeField()