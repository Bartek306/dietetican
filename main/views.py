import mimetypes
import os
from wsgiref.util import FileWrapper

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout as django_logout
from django.contrib.auth import get_user_model
from .models import Diet, Ingredient, Meal
from .decorators import unauthenticated_user, allowed_users
from fpdf import FPDF


# user: test passw:testtest12
# deitetyk eloelo

def meal_list_creator(meals):
    i = []
    i_units = []
    i_values = []

    for meal in meals:
        for ingr in meal.ingredients.all():
            i.append(ingr.name)
            i_units.append(ingr.unit)
            i_values.append(ingr.amount)

    dict_v = {}
    dict_u = {}

    for n in i:
        dict_v[n] = 0

    for n, v, u in zip(i, i_values, i_units):
        dict_u[n] = u
        dict_v[n] += v

    return dict_v, dict_u


class PDF(FPDF):
    def titles(self, txt):
        self.set_xy(0.0, 0.0)
        self.set_font('sysfont', '', 16)
        self.set_text_color(220, 50, 50)
        self.cell(w=210.0, h=40.0, align='C', txt=txt, border=0)

    def texts(self, txt, offset):
        self.set_xy(10.0, 30.0 + offset * 10)
        self.set_text_color(76.0, 32.0, 250.0)
        self.set_font('sysfont', '', 12)
        self.cell(w=30.0, txt=txt)

    def names(self, txt, offset):
        self.set_xy(5.0, 10.0 + offset * 10)
        self.set_font('sysfont', '', 16)
        self.set_text_color(220, 50, 50)
        self.cell(w=30.0, h=40.0, align='C', txt=txt, border=0)

    def create_shopping_list(self, meals, filename):
        self.add_font('sysfont', '', r"c:\WINDOWS\Fonts\arial.ttf", uni=True)
        self.add_page()
        self.titles("Lista zakupów")
        dict_v, dict_u = meal_list_creator(meals)
        arr = dict_v.keys()
        value = 2
        for name in arr:
            self.texts(" - " + name + " " + str(dict_v[name]) + " " + str(dict_u[name]), value)
            value += 1

        self.output(filename)

    def create_pdf(self, meals, filename):
        self.add_font('sysfont', '', r"c:\WINDOWS\Fonts\arial.ttf", uni=True)
        self.add_page()
        self.titles("Dieta")

        for meal in meals:
            self.add_page()
            self.titles(str(meal.name))
            self.names("Skladniki: ", 1)
            count = 0
            for ingr in meal.ingredients.all():
                self.texts(str(ingr), 2 + count)
                count += 1

            self.names("Przepis: ", 2 + len(meal.ingredients.all()))
            self.texts(str(meal.recipe), 3 + len(meal.ingredients.all()))

        self.output(filename, 'F')


User = get_user_model()


@allowed_users(allowed_roles=['Clients'])
def home(request):
    username = request.user.id
    # diet = Diet.objects.filter(owner=username )
    try:
        diet = Diet.objects.all().filter(owner=username)
        diet = diet.filter(active=True)[0]
        meals = diet.meals.all()
    except:
        diet = None
        meals = None
    ingradients = []
    lst = ""
    if meals:
        for meal in meals:
            for ingr in meal.ingredients.all():
                lst += str(ingr) + " "
            ingradients.append(lst)
            lst = ""
        my_list = zip(meals, ingradients)
        pdf1 = PDF()
        pdf1.create_pdf(meals, "diet.pdf")
        pdf2 = PDF()
        pdf2.create_shopping_list(meals, "shopping_list.pdf")
    else:
        my_list = None

    return render(request, "home.html", {"my_list": my_list})


def download_diet(request):
    fl_path = 'diet.pdf'

    fl = open(fl_path, 'rb')
    wrapper = FileWrapper(fl)
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(wrapper, content_type=mime_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % 'dieta.pdf'
    return response


def download_shopping_list(request):
    fl_path = 'shopping_list.pdf'

    fl = open(fl_path, 'rb')
    wrapper = FileWrapper(fl)
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(wrapper, content_type=mime_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % 'lista_zakupow.pdf'
    return response


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
    return render(request, "register.html", {'flag': flag, 'message': message})


def logout(request):
    django_logout(request)
    return redirect('/login')


@unauthenticated_user
def client(request, username):
    flag = False
    t = User.objects.all().filter(id=username)
    try:
        diet = Diet.objects.all().filter(owner=username)
        name = diet
        if diet:
            flag = True
        diet = diet.filter(active=True)[0]
        meals = diet.meals.all()
    except:
        diet = None
        meals = None
    ingradients = []
    lst = ""
    if meals:
        for meal in meals:
            for ingr in meal.ingredients.all():
                lst += str(ingr) + " "
            ingradients.append(lst)
            lst = ""
        my_list = zip(meals, ingradients)
    else:
        my_list = None

    if diet is None and flag is False:
        name = "Brak"

    return render(request, "client.html", {"my_list": my_list,
                                           "username": t[0],
                                           "names": name})


@csrf_exempt
@allowed_users(allowed_roles=['Dietitians'])
def add_client(request):
    flag = False
    if request.method == "POST":
        email = request.POST.get('email', False)
        t = User.objects.all().filter(email=email).exists()
        print(t)
        if not t:
            flag = True
        else:
            return redirect('panel')

    return render(request, "add_client.html", {"flag": flag})


@allowed_users(allowed_roles=['Dietitians'])
def dietetican_panel(request):
    username = request.user.username
    group_name = "clients_" + username
    t = User.objects.all().filter(groups__name=group_name)
    return render(request, "dietetican_panel.html", {"users": t})


@csrf_exempt
@allowed_users(allowed_roles=['Dietitians'])
def add_meal(request):
    if request.method == "POST":
        name1 = request.POST.get('skladnik1', False)
        unit1 = request.POST.get('wartosc1', False)
        amount1 = request.POST.get("ilosc1", False)
        print(name1, unit1, amount1)
        return redirect('panel')
    return render(request, "add_meal.html")


@unauthenticated_user
def no_assigment(request):
    return render(request, "no_assigment.html")
