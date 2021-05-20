from django.shortcuts import render, redirect

# Create your views here.

def login(request):
	return render(request, "login.html")

def register(request):
	return render(request, "register.html")

def logout(request):
	return render(request, "login.html")

def client(request):
	return render(request, "client.html")

def add_client(request):
	return render(request, "add_client.html")

def home(request):
	return render(request, "home.html")

def add_meal(request):
	return render(request, "add_meal.html")

def no_assigment(request):
	return render(request, "no_assigment.html")

def client_view(request):
	return render(request, "client_view.html")