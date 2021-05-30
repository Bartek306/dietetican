from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout as django_logout
from django.contrib.auth import get_user_model
from .models import Diet, Ingredient, Meal
from .decorators import unauthenticated_user, allowed_users
# user: test passw:testtest12
User = get_user_model()


@allowed_users(allowed_roles=['Clients'])
def home(request):
	username = request.user.id
	#diet = Diet.objects.filter(owner=username )
	try:
		diet = Diet.objects.get(owner=username)
		meals = diet.meals.all()
	except:
		diet = None
		meals = None
	ingradients = []
	lst = ""
	if meals:
		for meal in meals:
			for ingr in meal.ingredients.all():
				lst += str(ingr) +  " "
			ingradients.append(lst)
			lst = ""
		my_list = zip(meals, ingradients)
	else:
		my_list = None
	return render(request, "home.html", {"my_list": my_list})


@csrf_exempt
def login(request):
	flag = False
	message = ""
	if request.user.is_authenticated:
		return redirect('home')
	if request.method == "POST":
		username = request.POST.get('username', False)
		password = request.POST.get('password', False)
		user = authenticate(username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return redirect('home')
		message = "Podane dane są nieprawidłowe"
		flag = True
	return render(request, "login.html", {'flag': flag, 'message': message})

@csrf_exempt
def register(request):
	flag = False
	message = ""
	if request.method == "POST":
		username = request.POST.get('username', False)
		password = request.POST.get('password', False)
		email = request.POST.get('e-mail', False)
		if len(password) < 8:
			flag = True
			message = "Hasło powinno mieć conajmniej 8 znaków"
		elif User.objects.filter(username=username).exists():
		 	flag = True
		 	message = "Użytkownik o takiej nazwie istnieje"
		elif User.objects.filter(email=email).exists():
		 	flag = True
		 	message = "Użytkownik o takim adresie e-mail istnieje"
		else:
			user = User.objects.create_user(username, email, password)
			user.save()
			return redirect('login')
	print(flag)
	return render(request, "register.html", {'flag': flag, 'message':message})

def logout(request):
	django_logout(request)
	return redirect('/login')

@unauthenticated_user
def client(request):
	return render(request, "client.html")

@unauthenticated_user
def add_client(request):
	return render(request, "add_client.html")

@allowed_users(allowed_roles=['Dietitians'])
def dietetican_panel(request):
	t = User.objects.all().filter(groups__name="Clients")
	return render(request, "dietetican_panel.html", {"users": t})

@csrf_exempt
@allowed_users(allowed_roles=['Dietitians'])
def add_meal(request):
	if request.method == "POST":
		name1 = request.POST.get('skladnik1', False)
		unit1 = request.POST.get('wartosc1', False)
		amount1 = request.POST.get("ilosc1", False)
		print(name1, unit1, amount1)
		return redirect('dietetican_panel')
	else:
		print("kutas")
	return render(request, "add_meal.html")

@unauthenticated_user
def no_assigment(request):
	return render(request, "no_assigment.html")
