from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
class Command(BaseCommand):

	def add_arguments(self, parser):
		parser.add_argument('name')
		parser.add_argument('email')
		parser.add_argument('password')

	def handle(self, *args, **options):
		User = get_user_model()
		group_name = "clients_" + options['name']
		user = User.objects.create_user(options['name'], options['email'], options['password'])
		user.save()
		group = Group.objects.get(name='Dietitians')
		user.groups.add(group)
		Group.objects.get_or_create(name=group_name)


