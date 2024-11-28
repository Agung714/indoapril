from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import UserRole, Produk
from django.contrib import messages
from .forms import ProdukForm  

def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            try:
                role = user.user_role.role
                login(request, user)

                if role == 'kasir':
                    return redirect('transaksi')
                elif role == 'manajer':
                    return redirect('dashboard')
            except UserRole.DoesNotExist:
                error = "Akun tidak memiliki peran yang valid."
        else:
            error = "Username atau password salah."

    return render(request, 'indoapril/login.html', {'error': error})

@login_required
def transaksi_view(request):
    return render(request, 'indoapril/transaksi.html')

@login_required
def dashboard_view(request):
    return render(request, 'indoapril/dashboard.html')

@login_required
def dashboard_create(request):
    return render(request, 'indoapril/form.html')

@login_required
def dashboard_edit(request):
    return render(request, 'indoapril/edit.html')

@login_required
def dashboard_create(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            print("Form is valid. Saving data...")
            form.save()
            return redirect('dashboard')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = ProdukForm()

    return render(request, 'indoapril/form.html', {'form': form})

@login_required
def restok_view(request):
    return render(request, 'indoapril/restok.html')

@login_required
def restok_create(request):
    return render(request, 'indoapril/formstok.html')

# def dashboard_create(request):
#     if request.method == 'POST':
#         form = ProdukForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#     else:
#         form = ProdukForm()

#     return render(request, 'indoapril/form.html', {'form': form})


# @login_required
# def dashboard_edit(request, id):
#     produk = get_object_or_404(Produk, id=id)
#     if request.method == 'POST':
#         form = ProdukForm(request.POST, instance=produk)
#         if form.is_valid():
#             form.save() 
#             return redirect('dashboard')
#     else:
#         form = ProdukForm(instance=produk)

#     return render(request, 'indoapril/form.html', {'form': form})