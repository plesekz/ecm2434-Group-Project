from django.db import models

class Player(models.Model):
    userID = models.CharField(max_length=64)
    role = models.CharField(max_length=16)
    email = models.EmailField(max_length=200)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=64)

    def __str__(self):
        return self.username