from django.core.management.base import BaseCommand, CommandError
from django.core.files.images import ImageFile
from common.models import BaseUser, Member, Partner, Organization, PaymentTransaction, BankDetail

import sys


class Command(BaseCommand):
    help = 'Prepopulates the database with data for demo'

    def handle(self, *args, **options):
        # raise CommandError('Error')
        # self.stdout.write('Hello' + self.style.SUCCESS('Success'))

        # global refs
        admin = None

        # instantiate admins
        self.stdout.write('Creating admins...')
        try:
            u = BaseUser.objects.create_superuser(
                'admin@codeine.com',
                'password',
                first_name='David',
                last_name='Chen',
            )
            u.save()

            admin = u
            self.stdout.write(self.style.SUCCESS('Success') + ': Admin instantiated')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(self.style.ERROR('Error') + ': ' + repr(e))
        # end try-except

        # instantiate members
        self.stdout.write('Creating members...')
        try:
            u = BaseUser.objects.create_user(
                'm1@m1.com',
                'password',
                first_name='Jack',
                last_name='Johnson',
                is_active=True
            )
            u.profile_photo.save('m1.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/m1.jpeg', 'rb')))
            u.save()

            m = Member(user=u)
            m.save()

            u = BaseUser.objects.create_user(
                'm2@m2.com',
                'password',
                first_name='Suzuki',
                last_name='Haneda',
                is_active=True
            )
            u.profile_photo.save('m2.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/m2.jpeg', 'rb')))
            u.save()

            m = Member(user=u)
            m.save()
            self.stdout.write(self.style.SUCCESS('Success') + ': Members instantiated')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(self.style.ERROR('Error') + ': ' + repr(e))
        # end try-except

        # instantiate partners
        self.stdout.write('Creating partners...')
        try:
            u = BaseUser.objects.create_user(
                'p1@p1.com',
                'password',
                first_name='Vanessa',
                last_name='Fred',
                is_active=True
            )
            u.profile_photo.save('p1.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/p1.jpeg', 'rb')))
            u.save()

            p = Partner(user=u)
            p.save()

            u = BaseUser.objects.create_user(
                'p2@p2.com',
                'password',
                first_name='Suzuki',
                last_name='Haneda',
                is_active=True
            )
            u.profile_photo.save('p2.jpeg', ImageFile(open('./codeine_django/common/management/demo_assets/p2.jpeg', 'rb')))
            u.save()

            p = Partner(user=u)
            p.save()
            self.stdout.write(self.style.SUCCESS('Success') + ': Partners instantiated')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(self.style.ERROR('Error') + ': ' + repr(e))
        # end try-except

        # creating a React Course
        self.stdout.write('Creating partners...')
        try:
            partner = Partner.objects.first()
            print(partner)
            self.stdout.write(self.style.SUCCESS('Success') + ': Partners instantiated')
        except:
            e = sys.exc_info()[0]
            self.stdout.write(self.style.ERROR('Error') + ': ' + repr(e))
        # end try-except
    # end def
