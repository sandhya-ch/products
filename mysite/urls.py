from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notetake.urls')),
    path('', views.LoginView.as_view(), name='login'),
    path('', views.LogoutView.as_view(next_page='/'), name='logout'),
]
