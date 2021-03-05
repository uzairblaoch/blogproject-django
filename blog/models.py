from django.db import models
import datetime
from froala_editor.fields import FroalaField
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=150)
    description = FroalaField(theme='dark')
    date_time = models.DateTimeField(auto_now=True)


# FroalaField(theme='dark')
