from django.db import models


# Create your models here.

class Buttons(models.Model):
    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=64)


class Phrase(models.Model):
    button = models.ForeignKey(Buttons, on_delete=models.CASCADE)
    user_n = models.CharField(max_length=64)
    text = models.TextField()
    created_at = models.DateField()
    lang = models.CharField(max_length=2)
