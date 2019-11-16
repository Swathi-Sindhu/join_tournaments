from django.contrib.auth.models import User
from django.db import models


class TournamentJoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tournament = models.IntegerField()

    def __str__(self):
        return self.user.username
