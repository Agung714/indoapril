from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Produk

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['kode_produk', 'nama_produk', 'stock', 'harga_jual']