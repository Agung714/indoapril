from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserRole, Produk, Transaksi, ItemTransaksi
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
def dashboard_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        produk_list = Produk.objects.filter(kode_produk__icontains=search_query)
    else:
        produk_list = Produk.objects.all()

    return render(request, 'indoapril/dashboard.html', {'produk_list': produk_list})


@login_required
def dashboard_create(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Produk berhasil ditambahkan!")
            return redirect('dashboard')
        else:
            messages.error(request, "Terjadi kesalahan. Periksa data yang Anda masukkan.")
    else:
        form = ProdukForm()

    return render(request, 'indoapril/form.html', {'form': form})

@login_required
def dashboard_edit(request, kode_produk):
    produk = get_object_or_404(Produk, kode_produk=kode_produk)

    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            messages.success(request, f"Produk {produk.nama_produk} berhasil diperbarui!")
            return redirect('dashboard')
        else:
            messages.error(request, "Terjadi kesalahan. Periksa data yang Anda masukkan.")
    else:
        form = ProdukForm(instance=produk)

    return render(request, 'indoapril/edit.html', {'form': form, 'produk': produk})

def dashboard_delete(request, kode_produk):
    produk = get_object_or_404(Produk, kode_produk=kode_produk)

    produk.delete()
    messages.success(request, f"Produk {produk.nama_produk} berhasil dihapus!")
    return redirect('dashboard')

@login_required
def restok_view(request):
    return render(request, 'indoapril/restok.html')

@login_required
def restok_create(request):
    return render(request, 'indoapril/formstok.html')

@login_required
def transaksi_view(request):
    if request.method == "POST":
        from json import loads

        try:
            data = loads(request.body)
            items = data.get("items", [])
            pembayaran = data.get("pembayaran", 0)

            if not items:
                return JsonResponse({'error': 'Tidak ada item dalam transaksi.'}, status=400)

            if pembayaran <= 0:
                return JsonResponse({'error': 'Pembayaran harus lebih besar dari 0.'}, status=400)

            transaksi = Transaksi.objects.create(total_harga=0, pembayaran=pembayaran, kembalian=0)
            total = 0

            for item in items:
                produk_id = item.get('produk_id')
                jumlah = int(item.get('jumlah', 0))

                produk = get_object_or_404(Produk, kode_produk=produk_id)

                if produk.stock < jumlah:
                    return JsonResponse({'error': f"Stok produk {produk.nama_produk} tidak mencukupi."}, status=400)

                subtotal = produk.harga_jual * jumlah
                ItemTransaksi.objects.create(
                    transaksi=transaksi,
                    produk=produk,
                    jumlah=jumlah,
                    subtotal=subtotal
                )
                produk.stock -= jumlah
                produk.save()
                total += subtotal

            transaksi.total_harga = total
            transaksi.kembalian = pembayaran - total
            transaksi.save()

            return JsonResponse({'success': True, 'transaksi_id': transaksi.id, 'kembalian': transaksi.kembalian})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    produk = Produk.objects.all()
    return render(request, 'indoapril/transaksi.html', {'produk': produk})

def produk_detail(request, kode_produk):
    try:
        produk = Produk.objects.get(kode_produk=kode_produk)
        return JsonResponse({
            'kode_produk': produk.kode_produk,
            'nama_produk': produk.nama_produk,
            'harga': float(produk.harga_jual),
            'stock': produk.stock
        })
    except Produk.DoesNotExist:
        return JsonResponse({'error': 'Produk tidak ditemukan.'}, status=404)
    
@login_required
def riwayat_view(request):
    return render(request, 'indoapril/riwayat_transaksi.html')

@login_required
def riwayat_detail(request):
    return render(request, 'indoapril/transaksi_detail.html')
