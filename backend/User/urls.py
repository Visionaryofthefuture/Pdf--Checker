from django.urls import path
from User import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.home, name = "home"),
    path('register/', views.registration, name = "register"),
    path('login/', views.login, name = "login"),
    path('logout/', views.logout, name = "logout")
]  