from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('transaksi/', views.transaksi_view, name='transaksi'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/create/', views.dashboard_create, name='dashboard_create'),
    path('dashboard/edit/', views.dashboard_edit, name='dashboard_edit'),
]