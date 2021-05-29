from django.urls import path, include
from . import views
urlpatterns = [
	path('', views.home, name="home"),
	path('register', views.register, name="register"),
	path('login', views.login, name="login"),
	path('logout', views.logout, name="logout"),
	path('client', views.client, name="client"),
	path('add_client', views.add_client, name="add_client"),
	path('add_meal', views.add_meal, name="add_meal"),
	path('no_assigment', views.no_assigment, name="no_assigment"),
	path('panel', views.dietetican_panel, name="dietetican_panel"),
]
