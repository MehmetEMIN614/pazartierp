from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.core.models import Org, OrgSetting

User = get_user_model()


class Command(BaseCommand):
    help = 'Setup initial project configurations including main org and admin user'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Starting project setup...')

        # Create main organization
        main_org, created = Org.objects.get_or_create(
            name="Main Organization",
            defaults={
                'active': True,
                'address': "Main Address",
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created main organization: {main_org.name}'))

            # Create org settings
            OrgSetting.objects.create(
                org=main_org,
                language='en-us',
                timezone='UTC',
                decimal_precision=2
            )
        else:
            self.stdout.write('Main organization already exists')

        # Create admin user
        admin_email = 'admin@admin.com'
        admin_password = '1'  # Change this in production

        admin_user, created = User.objects.get_or_create(
            email=admin_email,
            defaults={
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
                'first_name': 'Admin',
                'last_name': 'User',
            }
        )

        if created:
            admin_user.set_password(admin_password)
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_email}'))
        else:
            self.stdout.write('Admin user already exists')

        # Add user to organization
        admin_user.orgs.add(main_org)
        admin_user.set_current_org(main_org)

        self.stdout.write('Creating additional test organizations...')

        # Create test organizations
        test_orgs = [
            {'name': 'Test Org 1', 'address': 'Test Address 1'},
            {'name': 'Test Org 2', 'address': 'Test Address 2'},
        ]

        for org_data in test_orgs:
            org, created = Org.objects.get_or_create(
                name=org_data['name'],
                defaults={
                    'active': True,
                    'address': org_data['address'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created organization: {org.name}'))

                OrgSetting.objects.create(
                    org=org,
                    language='en-us',
                    timezone='UTC',
                    decimal_precision=2
                )

                # Add admin to this org too
                admin_user.orgs.add(org)

        self.stdout.write(self.style.SUCCESS('''
Setup completed successfully!
--------------------------------
Admin User Email: admin@example.com
Admin Password: admin123
Main Organization: Main Organization
Additional orgs created: Test Org 1, Test Org 2
--------------------------------
Please change the admin password in production!
        '''))
