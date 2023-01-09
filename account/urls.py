from django.urls import path
from .views import RegistrationView, LoginView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
]