from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from functools import partial
from pynder.api import TinderAPI
from django.utils import timezone
from datetime import date
from dateutil.parser import parse as parse_date
import logging
import pynder.errors
import attr
import tinder
import re

# config logging
# logging.basicConfig(filename='tinder_models.log', level=logging.INFO)

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
    class Meta:
        app_label = 'tinder'


    # basic information
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    bio = models.TextField(default="")
    schools = models.CharField(max_length=200, default="")
    jobs = models.CharField(max_length=200, default="")
    birth_date = models.DateField(blank=True, null=True)
    # distance in miles
    distance = models.FloatField(default=0.0)
    liked_date = models.DateField(default=timezone.now)

    # social media
    instagram_username = models.CharField(max_length=30, default="None")
    mentions_snapchat = models.BooleanField(default=False)
    mentions_kik = models.BooleanField(default=False)
    mentions_instagram = models.BooleanField(default=False)

    ## Programmatically set fields
    liked = models.BooleanField(default=True)

    # Did this user come from somewhere other than bonfire?
    from_other = models.BooleanField(default=False)

    # a dictionary representation from another source
    data = JSONField()
    tinder_id = models.CharField(max_length=25)


    def __str__(self):
        return self.__repr__()


    @classmethod
    def from_pynder(cls, pynder_user):
        """
        factory method to initialize from pynder User class
        :param pynder_user: pynder.models.user.User
        :return: cls
        """
        fields = dict(
            data = pynder_user._data,
            name = pynder_user.name,
            age = pynder_user.age,
            bio = pynder_user.bio,
            birth_date = pynder_user.birth_date,
            jobs = str(pynder_user.jobs),
            schools = str(pynder_user.schools),
            instagram_username = pynder_user.instagram_username,
            distance = pynder_user._data.get('distance_mi'),
            tinder_id = pynder_user._data['_id'],
        )

        kwargs = {k: v for k, v in fields.items() if v}

        try:
            user, created = cls.objects.get_or_create(**kwargs)
        except (UnicodeEncodeError) as e:
            pass
        return user


    def get_tinder_data(self, api=None, token=None):
        """
        Return tinder json response from tinder for user.
        api should already be authenticated with api.auth()
        :param api: pynder.api.TinderAPI()
        :param XAuthToken:
        :return:
        """
        if api is None and token is not None:
            api = TinderAPI()
            api.auth(token)
        try:
            return api.user_info(self.tinder_id)['results']
        except pynder.errors.RequestError as e:
            # logging.warning(e)
            pass
        return None

    def update_self_from_tinder(self, api=None, token=None):
        """
        update self with data from tinder
        :param api:
        :param token:
        :return: True if successful else None
        """

        tinder_data = self.get_tinder_data(api, token)
        if tinder_data:
            self.data = tinder_data
            self.save()
            return True
        return None

    def natural_key(self):
        return (self.tinder_id)

    @classmethod
    def from_tinder_dict(cls, d):

        def age_from_bday(birth_date):
            today = date.now()
            return (today.year - birth_date.year -
                    ((today.month, today.day) <
                     (birth_date.month, birth_date.day)))

        kwargs = dict(
            data = d,
            name = d['name'],
            age = age_from_bday(d['age']),
            bio = d['bio'],
            birth_date = d['birth_date'],
            jobs = d['jobs'],
            schools = d['schools'],
            instagram_username = d.get('instagram_username', {}).get('username'),
            distance = d['distance_mi'],
            tinder_id = d['_id'],
        )

        return cls(**kwargs)



    @property
    def photos(self):
        return self.get_photos()

    @property
    def thumbnails(self):
        return self.get_photos(width="84")

    @property
    def instagram_photos(self):
        if self.data.get("instagram", False):
            return [p for p in self._data['instagram']['photos']]

    def get_photos(self, width=None):
        photos_list = []
        for photo in self.data['photos']:
            if width is None:
                photos_list.append(photo.get("url"))
            else:
                width = str(width)
                sizes = ["84", "172", "320", "640"]
                if width not in sizes:
                    print("Only support these widths: %s" % sizes)
                    return None
                for p in photo.get("processedFiles", []):
                    if p.get("width", 0) == int(width):
                        photos_list.append(p.get("url", None))
        return photos_list

    @property
    def mentions_snapchat(self):

        patterns = [
            re.compile(r'SC'),
            re.compile('snapchat', re.I),
            re.compile(r'\Wsnap\W', re.I)
        ]
        return any(p.search(self.bio) for p in patterns)

    @property
    def mentions_kik(self):
        patterns = [
            re.compile(r'kik', re.I),
        ]

        return any(p.search(self.bio) for p in patterns)

    @property
    def mentions_instagram(self):
        patterns = [
            re.compile(r'IG'),
            re.compile(r'\Winsta\W', re.I),
        ]

        return any(p.search(self.bio) for p in patterns)

    @staticmethod
    def mentions_social(app, bio):
        """
        Return true if a bio mentions a certain app.
        :param app: snapchat || instagram || kik
        :param bio: bio string
        :return: bool or None
        """
        snapchat_patterns = [
            re.compile(r'SC'),
            re.compile('snapchat', re.I),
            re.compile(r'\Wsnap\W', re.I)
        ]

        instagram_patterns = [
            re.compile(r'IG'),
            re.compile(r'\Winsta\W', re.I),
        ]

        kik_patterns = [
            re.compile(r'kik', re.I),
        ]

        search = lambda patterns: any(p.search(bio) for p in patterns)
        if app == "snapchat":
            return search(snapchat_patterns)
        elif app == "instagram":
            return search(instagram_patterns)
        elif app == "kik":
            return search(kik_patterns)
        else:
            print("app parameter must be a string: {instagram} || {snapchat}} || {kik}")
            return None













