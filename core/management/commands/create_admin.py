from django.core.management.base import BaseCommand
from core.models import Admin


class Command(BaseCommand):
    help = 'Create initial admin user'

    def handle(self, *args, **options):
        if not Admin.objects.filter(username='admin').exists():
            admin = Admin(
                username='admin',
                name='Admin',
                surname='User',
                email='admin@school.com'
            )
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Admin user created successfully!'))
            self.stdout.write('Username: admin')
            self.stdout.write('Password: admin123')
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))
