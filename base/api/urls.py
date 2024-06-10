from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('notes/', views.getNotes),	
    path('doctors/', views.getPostDoctorList),	
    path('doctors/<int:pk>/', views.getDoctor),	
    path('schedule/', views.postDoctorSchedule),	
    path('schedule/<int:doctor_id>/', views.getDoctorSchedule),	
]