from django.db import models
from functools import partial
import json
import attr

# freeze init to false on attrs
attr.s = partial(attr.s, init=False)

def fields(*args):
    """
    return a dictionary of arg: attr.ib() for arg in args
    :param args:
    :return: {arg: attr.ib()}
    """
    return {arg: attr.ib() for arg in args}


@attr.s(these=fields("name", "age"))
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
    # distance in miles
    distance = models.FloatField(default=0.0)

    # social media
    instagram_username = models.CharField(max_length=30, blank=True)
    mentions_snapchat = models.BooleanField(default=False)
    mentions_kik = models.BooleanField(default=False)
    mentions_instagram = models.BooleanField(default=False)

    ## Programmatically set fields
    liked = models.BooleanField(default=False)
    # Did this user come from somewhere other than bonfire?
    from_other = models.BooleanField(default=False)
    # a dictionary representation from another source
    data = models.TextField(blank=True)

    def __str__(self):
        return self.__repr__()

    @property
    def photos(self):
        if self.data:
            d = json.loads(self.data)
            return d.get('photos', [])
        return []



