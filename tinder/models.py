from django.db import models

class User(models.Model):
    """
    A basic class for a user.
    """


    # basic information
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    bio = models.TextField(blank=True)
    schools = models.CharField(max_length=50, blank=True)
    jobs = models.CharField(max_length=50, blank=True)

    # social media
    instagram_username = models.CharField(max_length=30, blank=True)
    mentions_snapchat = models.BooleanField(default=False)
    mentions_kik = models.BooleanField(default=False)
    mentions_instagram = models.BooleanField(default=False)
