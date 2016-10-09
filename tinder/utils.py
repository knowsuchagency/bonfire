import sys
import os
sys.path.extend(['/Users/stephanfitzpatrick/Dropbox/projects/bonfire'])

from pathlib import Path
from pynder import Session as PynderSession
from configparser import ConfigParser
import bonfire.settings
import django
import logging

# settings.configure(default_settings=bonfire.settings)
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

    def like_several(self, hopefuls):
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



if __name__ == "__main__":

    credentials_path = Path(bonfire.settings.BASE_DIR, 'credentials.ini')
    config = ConfigParser()
    config.read(str(credentials_path))
    token = config.get('facebook', 'token')

    session = Session(token)

    # let's start by just liking 10
    hopefuls = session.nearby_users()
    session.like_several(hopefuls)
    print('done')