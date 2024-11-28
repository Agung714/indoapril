from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Model pengguna kustom yang diperluas dari AbstractUser.
    Anda dapat menambahkan field tambahan di sini jika diperlukan.
    """
    pass


class UserRole(models.Model):
    """
    Model untuk menentukan peran pengguna.
    """
    ROLE_CHOICES = [
        ('kasir', 'Kasir'),
        ('manajer', 'Manajer'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_role')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Produk(models.Model):
    """
    Model produk yang mencatat detail produk.
    """
    kode_produk = models.CharField(max_length=10, unique=True)
    nama_produk = models.CharField(max_length=100)
    harga_jual = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nama_produk


class Transaksi(models.Model):
    """
    Model transaksi untuk mencatat penjualan.
    """
    total_harga = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pembayaran = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    kembalian = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaksi {self.id} pada {self.tanggal.strftime('%d-%m-%Y %H:%M:%S')}"


class ItemTransaksi(models.Model):
    """
    Model item transaksi yang mencatat detail setiap produk dalam transaksi.
    """
    transaksi = models.ForeignKey(Transaksi, related_name='items', on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.produk.nama_produk} x {self.jumlah}"
    
class Restok(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    tanggal = models.DateTimeField(auto_now_add=True)
    stock_lama = models.PositiveIntegerField()
    stock_tambah = models.PositiveIntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Restok {self.produk.nama_produk} - {self.tanggal.strftime('%d-%m-%Y %H:%M:%S')}"