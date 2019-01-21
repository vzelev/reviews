import datetime

from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=3)
    title = models.CharField(max_length=64)
    summary = models.TextField()
    ip = models.GenericIPAddressField()
    submission_date = models.DateTimeField(default=datetime.datetime.now)
    company = models.CharField(max_length=255)
    reviewer = models.CharField(max_length=255)

admin.site.register(Review)