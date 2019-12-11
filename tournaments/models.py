from django.contrib.auth.models import User
from django.db import models
import datetime


class TournamentJoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tournament = models.IntegerField()
    name = models.CharField(max_length=150,default='manoj')
    email = models.EmailField(max_length=150, default='asd@asd.com')
    tournament_name = models.CharField(max_length=150, default='t1')
    start_date = models.DateField(default=datetime.date.today())
    end_date = models.DateField(default=datetime.date.today())
    location = models.CharField(max_length=150, default='chennai')

    class Meta:
        unique_together = ('user', 'tournament')

    def __str__(self):
        return self.user.username
