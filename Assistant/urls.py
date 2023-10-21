from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='members'),
    path('update-data/', views.update_data, name='update-data'),
]
