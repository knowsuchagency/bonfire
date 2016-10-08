from django.db import models
from django.contrib.postgres.fields import JSONField
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


@attr.s(these=fields("name", "age", "instagram_username"))
class User(models.Model):
    """
    A basic class for a user.
    """


    # basic information
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    bio = models.TextField(default="")
    schools = models.CharField(max_length=100, blank=True)
    jobs = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    # distance in miles
    distance = models.FloatField(default=0.0)

    # social media
    instagram_username = models.CharField(max_length=30, default="None")
    mentions_snapchat = models.BooleanField(default=False)
    mentions_kik = models.BooleanField(default=False)
    mentions_instagram = models.BooleanField(default=False)

    ## Programmatically set fields
    liked = models.BooleanField(default=False)
    # Did this user come from somewhere other than bonfire?
    from_other = models.BooleanField(default=False)
    # a dictionary representation from another source
    data = JSONField()
    tinder_id = models.CharField(max_length=25)


    def __str__(self):
        return self.__repr__()

    @property
    def photos(self):
        return self.data['photos']


    @property
    def _data(self):
        return json.loads(self.data)

    @classmethod
    def from_pynder_user(cls, pynder_user):
        """
        factory method to initialize from pynder User class
        :param pynder_user: pynder.models.user.User
        :return: cls
        """
        fields = dict(
            data = pynder_user.data,
            name = pynder_user.name,
            age = pynder_user.age,
            bio = pynder_user.bio,
            birth_date = pynder_user.birth_date,
            jobs = pynder_user.jobs,
            schools = pynder_user.schools,
            instagram_username = pynder_user.instagram_username,
        )

        kwargs = {k: v for k, v in fields.items() if v}

        return cls(**kwargs)

    @classmethod
    def from_mongo(cls, mongodict):
        """
        factory method to import from old mongo db dictionaries
        :param mongodict: dictionary
        :return: cls

        """
        fields = dict(
            name = mongodict['name'],
            age = mongodict['age'],
            bio = mongodict['bio'],
            distance = mongodict['distance_mi'],
            instagram_username = mongodict['instagram_username'],
            mentions_snapchat = mongodict['mentions_snapchat'],
            mentions_kik = mongodict['mentions_kik'],
            tinder_id = mongodict['_id'],
            liked = True,
            from_other = True,
            data = mongodict,
        )

        kwargs = {k: v for k, v in fields.items() if v}

        user, created = cls.objects.get_or_create(**kwargs)
        return user

    # def get_photos(self, width=None):
    #     photos_list = []
    #     photos = self._data['photos']
    #     for photo in photos:
    #         if width is None:
    #             photos_list.append(photo.get("url"))
    #         else:
    #             sizes = ["84", "172", "320", "640"]
    #             if width not in sizes:
    #                 print("Only support these widths: %s" % sizes)
    #                 return None
    #             for p in photo.get("processedFiles", []):
    #                 if p.get("width", 0) == int(width):
    #                     photos_list.append(p.get("url", None))
    #     return photos_list










