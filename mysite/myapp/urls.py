from django.urls import path
from . import views

appname="myapp"
urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.registration_view, name="registration"),
    path('user/', views.user_home_view, name='user'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path("my_files/", views.my_files, name="my_files"),
    path("public_files/", views.public_files, name="public_files"),
    path("shared_files/", views.shared_files, name="shared_files"),
    path("public/", views.public, name="public")
]
