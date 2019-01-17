from django.contrib.auth.models import User
from django.db import models


class Reviewer(models.Model):
    name = models.CharField()
    email = models.EmailField()


class Review(models.Model):
    user = models.ForeignKey(User)
    rating = models.SmallIntegerField(default=3)
    title = models.CharField(max_length=64)
    summary = models.TextField()
    ip = models.IPAddressField()
    submission_date = models.DateTimeField()
    company = models.CharField(max_length=255)
    reviewer = models.ForeignKey(Reviewer)

