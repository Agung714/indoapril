from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass

class UserRole(models.Model):
    ROLE_CHOICES = [
        ('kasir', 'Kasir'),
        ('manajer', 'Manajer'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_role')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class Produk(models.Model):
    kode_produk = models.CharField(max_length=100)
    nama_produk = models.CharField(max_length=200)
    stock = models.IntegerField()
    harga_jual = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nama_produk