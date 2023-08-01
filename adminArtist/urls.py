from django.urls import path

from .Views.auth import *

urlpatterns = [
    path('signUp', signUp.as_view(), name="signUp"),
    path('login', LoginView, name="login"),

]
