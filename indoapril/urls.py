from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('transaksi/', views.transaksi_view, name='transaksi'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/create/', views.dashboard_create, name='dashboard_create'),
    path('dashboard/edit/', views.dashboard_edit, name='dashboard_edit'),
    path('restok/', views.restok_view, name='restok'),
    path('restok/create', views.restok_create, name='restok_create'),
    path('dashboard/edit/<str:kode_produk>/', views.dashboard_edit, name='dashboard_edit'),
    path('dashboard/delete/<str:kode_produk>/', views.dashboard_delete, name='dashboard_delete'),
    path('produk-detail/<str:kode_produk>/', views.produk_detail, name='produk_detail'),
    path('riwayat/', views.riwayat_view, name='riwayat'),
    path('riwayat/detail', views.riwayat_detail, name='riwayat_detail'),
]
