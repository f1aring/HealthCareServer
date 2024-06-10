from django.urls import path
from .views import UserRegView

urlpatterns = [
    path('', UserRegView.as_view()),
    
]