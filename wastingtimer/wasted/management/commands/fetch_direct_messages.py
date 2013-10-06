from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from wastingtimer.wasted.services import DirectMessagesService


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--since_id',
            action='store_true',
            dest='since_id',
            default=None,
            help='The twitter since_id override. Taken from Database when not present'),
        )
    help = 'Fetch the lastest set of mentions from twitter.com'

    def handle(self, *args, **kwargs):
        self.kwargs = kwargs
        self.dms()

    def dms(self):
        dm_service = DirectMessagesService(hours_ago=self.kwargs.get('hours_ago', None), since_id=self.kwargs.get('since_id', None))
        dm_service.process()
        self.stdout.write('Successfully processed %d DirectMessages' % len(dm_service.tweets))
