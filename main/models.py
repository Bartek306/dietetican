from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Ingredient(models.Model):
	name = models.CharField(max_length=50)
	unit = models.CharField(max_length=5) # skrót jednostki
	amount = models.IntegerField()

	def __str__(self):
		return self.name + " [" + str(self.amount) +" " + self.unit + "]"



class Meal(models.Model):
	name = models.CharField(max_length=25)
	recipe = models.CharField(max_length=250)
	ingredients = models.ManyToManyField(Ingredient, blank=True, related_name="Ingredients")


class Diet(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", null=True)
	meals = models.ManyToManyField(Meal, blank=True, related_name="Meals") 

# Create your models here.
'''
logowanie/rejestracja :
google

grupy:
klient/dietetyk
sprawdzenie czy dany użytkownik moze miec dostep do podstrony
dekoratorami

import diety i lista zakupów jako json

baza danych :
składnik = {nazwa, ilość, jednostka}
posilek = {nazwy, składnik[] przepis}
dieta = {posilki[], user}
przepis = {tekst}


dodowanie posiłkow do konkretnej diety. Wybor diety

'''



