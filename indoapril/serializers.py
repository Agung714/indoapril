from rest_framework import serializers
from .models import Produk, Transaksi, Restok

class ProdukSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produk
        fields = '__all__'

class TransaksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaksi
        fields = '__all__'

class RestokSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restok
        fields = '__all__'
