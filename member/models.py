from django.db import models

class Member(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    user_pw = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    user_gender = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=50)
    c_date = models.DateTimeField()
    #img_url = models.(null = True)
# <img src = " url  " >