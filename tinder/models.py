from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from functools import partial
from pynder.api import TinderAPI
import logging
import pynder.errors
import attr

# config logging
logging.basicConfig(filename='tinder_models.log', level=logging.DEBUG)

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
    schools = ArrayField(
        models.CharField(max_length=60, blank=True)
    )
    jobs = ArrayField(
        models.CharField(max_length=60, blank=True)
    )
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

        user, created = cls.objects.get_or_create(**kwargs)
        return user

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
            logging.warning(e)
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










