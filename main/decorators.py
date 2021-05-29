from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper(request, *args, **kwargs):
		if request.user.is_authenticated:
			return view_func(request, *args, **kwargs)
		else:
			return redirect('/login')

	return wrapper

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
			   group = request.user.groups.all()[0].name
			if group is None:
				return redirect('/login')
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				if group == 'Dietitians':
					return redirect('/panel')
				else:
					return redirect('home')
		return wrapper
	return decorator	
