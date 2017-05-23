from django.core.management.commands import test


class Command(test.Command):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('-f','--firefox',
            action='store_true', dest='firefox', default=None,
            help='Use Mozilla Firefox for functional tests (Default is Google Chrome)'),
