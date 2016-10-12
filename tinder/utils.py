import sys; sys.path.append('/Users/stephanfitzpatrick/Dropbox/projects/bonfire')

from pathlib import Path
from pynder import Session as PynderSession
from configparser import ConfigParser
from operator import methodcaller
import bonfire.settings
import django
import logging
import os
import argparse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bonfire.settings')
django.setup()

from tinder.models import User

logging.basicConfig(
                    # filename='tinder.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler("tinder.log"),
                              logging.StreamHandler()]
                    )

class Session(PynderSession):


    @staticmethod
    def persist(hopeful):
        return User.from_pynder(hopeful)

    @staticmethod
    def like_and_persist(hopeful):
        hopeful.like()
        return Session.persist(hopeful)

    def like_several(self, hopefuls=None):
        hopefuls = hopefuls or self.nearby_users()
        while hopefuls:
            # make sure we are not using likes too quickly
            if self.can_like_in > 0:
                continue
            hopeful = hopefuls.pop()
            persisted = Session.like_and_persist(hopeful)
            logging.info("liked and saved: {}".format(persisted))

    def like_until_you_drop(self):
        hopefuls = self.nearby_users()
        while hopefuls:
            self.like_several(hopefuls)
            hopefuls = self.nearby_users()


def get_default_token():
    """
    Return the token from the ini file or None
    :return: str
    """

    token = None
    try:
        credentials_path = Path(bonfire.settings.BASE_DIR, 'credentials.ini')
        config = ConfigParser()
        config.read(str(credentials_path))
        token = config.get('facebook', 'token')
    except Exception as e:
        logging.warning(e)
    return token


parser = argparse.ArgumentParser(description="Tinder utilities")

parser.add_argument('-t',
                    '--token', dest='token',
                    default=get_default_token(),
                    help='Facebook token')

parser.add_argument('--like-all',
                    dest='method',
                    action='store_const',
                    const='like_until_you_drop',
                    default='like_several',
                    help='Like all nearby users (default: only a few)')


if __name__ == "__main__":

    namespace = parser.parse_args()
    command = methodcaller(namespace.method)

    session = Session(namespace.token)
    command(session)

