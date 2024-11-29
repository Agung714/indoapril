from . import views
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProdukListViewSet
router = DefaultRouter() # Membuat router DRF
router.register(r'produk', ProdukListViewSet) # Menyambungkan StudentsViewSet ke URL /students/

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('transaksi/', views.transaksi_view, name='transaksi'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/create/', views.dashboard_create, name='dashboard_create'),
    path('dashboard/edit/<str:kode_produk>/', views.dashboard_edit, name='dashboard_edit'),
    path('dashboard/delete/<str:kode_produk>/', views.dashboard_delete, name='dashboard_delete'),
    path('restok/', views.restok_view, name='restok'),
    path('restok/tambah/', views.restok_create, name='restok_create'),
    path('produk-detail/<str:kode_produk>/', views.produk_detail, name='produk_detail'),
    path('riwayat/', views.laporan_transaksi, name='riwayat'),
    # path('riwayat/', views.riwayat_view, name='riwayat'),
    path('riwayat/<int:transaksi_id>/', views.riwayat_detail, name='riwayat_detail'),
    path('api/', include(router.urls)), # Ini akan menambahkan semua URL yang dibutuhkan untuk API
    path('logout/', views.logout_view, name='logout'),

]
  