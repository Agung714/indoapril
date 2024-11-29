from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
import requests
from .models import UserRole, Produk, Transaksi, ItemTransaksi, Restok
from .forms import ProdukForm
from .decorators import role_required
from .serializers import ProdukSerializer, TransaksiSerializer, RestokSerializer


# URL base API
API_BASE_URL = "http://127.0.0.1:8000/api"
# ====================== Login & Logout Views ======================
def login_view(request):
    """
    Mengautentikasi pengguna berdasarkan username dan password.
    Jika berhasil, pengguna diarahkan ke halaman sesuai perannya.
    """
    error = None  # Variabel untuk menyimpan pesan kesalahan
    if request.method == "POST":  # Jika form dikirim melalui metode POST
        username = request.POST['username']  # Ambil username dari input form
        password = request.POST['password']  # Ambil password dari input form
        user = authenticate(request, username=username, password=password)  # Verifikasi kredensial
        if user:  # Jika autentikasi berhasil
            try:
                role = user.user_role.role  # Ambil peran pengguna dari model UserRole
                login(request, user)  # Login pengguna
                # Redirect berdasarkan peran pengguna
                if role == 'kasir':
                    return redirect('transaksi')  # Kasir diarahkan ke halaman transaksi
                elif role == 'manajer':
                    return redirect('dashboard')  # Manajer diarahkan ke halaman dashboard
            except UserRole.DoesNotExist:
                error = "Akun tidak memiliki peran yang valid."  # Error jika peran tidak ditemukan
        else:
            error = "Username atau password salah."  # Error jika autentikasi gagal
    return render(request, 'indoapril/login.html', {'error': error})  # Tampilkan halaman login dengan error

def logout_view(request):
    """
    Logout pengguna yang sedang login dan menghapus sesi mereka.
    """
    logout(request)  # Menghapus sesi pengguna
    return redirect('login')  # Arahkan kembali ke halaman login

# ====================== Dashboard View (Read) ======================
@login_required
@role_required('manajer')
def dashboard_view(request):
    """
    Menampilkan daftar produk dengan data yang diambil dari API atau database lokal.
    Mendukung pencarian dan paginasi.
    """
    search_query = request.GET.get('search', '')  # Ambil parameter pencarian dari URL
    produk_list = []  # Inisialisasi daftar produk kosong
    try:
        # Mengambil data dari API
        response = requests.get(f"{API_BASE_URL}/produk/", params={'search': search_query})
        response.raise_for_status()  # Periksa jika ada error HTTP
        produk_list = response.json()  # Konversi JSON ke list
    except requests.exceptions.RequestException as e:
        print(f"Error API: {e}")  # Debug
        # Jika API gagal, fallback ke database lokal
        if search_query:
            produk_list = Produk.objects.filter(kode_produk__icontains=search_query)
        else:
            produk_list = Produk.objects.all()

    # Pagination: Membatasi jumlah produk per halaman
    paginator = Paginator(produk_list, 10)  # 10 produk per halaman
    page_number = request.GET.get('page')  # Ambil nomor halaman dari parameter URL
    page_obj = paginator.get_page(page_number)  # Ambil data untuk halaman tertentu

    return render(request, 'indoapril/dashboard.html', {'page_obj': page_obj})


# ====================== Dashboard Create (Create) ======================
@login_required
@role_required('manajer')
def dashboard_create(request):
    if request.method == 'POST':  # Proses form jika menggunakan metode POST
        form = ProdukForm(request.POST)  # Ambil data dari form
        if form.is_valid():  # Validasi data form
            data = form.cleaned_data  # Data yang sudah dibersihkan
            try:
                response = requests.post(f"{API_BASE_URL}/produk/", data=data)  # Kirim data ke API
                response.raise_for_status()  # Periksa jika API memberikan error
                messages.success(request, "Produk berhasil ditambahkan ke API!")  # Notifikasi sukses
            except requests.exceptions.RequestException:
                form.save()  # Simpan ke database lokal jika API gagal
                messages.warning(request, "Produk ditambahkan ke lokal karena API gagal.")  # Notifikasi fallback
            return redirect('dashboard')  # Redirect ke halaman dashboard
        else:
            messages.error(request, "Terjadi kesalahan. Periksa data yang Anda masukkan.")  # Notifikasi error validasi
    else:
        form = ProdukForm()  # Buat form kosong untuk input
    return render(request, 'indoapril/form.html', {'form': form})  # Kirim form ke template



# ====================== Dashboard Edit ======================
@login_required
@role_required('manajer')
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

# ====================== Dashboard Delete ======================
@login_required
@role_required('manajer')
def dashboard_delete(request, kode_produk):
    produk = get_object_or_404(Produk, kode_produk=kode_produk)

    produk.delete()
    messages.success(request, f"Produk {produk.nama_produk} berhasil dihapus!")
    return redirect('dashboard')

# ====================== Restok ======================
@login_required
@role_required('manajer')
def restok_view(request):
    restok_list = Restok.objects.order_by('-tanggal')
    paginator = Paginator(restok_list, 10)  # 5 data per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'indoapril/restok.html', {'page_obj': page_obj})

@login_required
@role_required('manajer')
def restok_create(request):
    if request.method == 'POST':
        kode_produk = request.POST.get('kode_produk', '').strip()
        stock_tambah = request.POST.get('restock', '').strip()
        note = request.POST.get('note', '').strip()

        if not kode_produk or not stock_tambah:
            messages.error(request, "Kode produk dan jumlah stok tidak boleh kosong.")
            return redirect('restok')

        try:
            produk = Produk.objects.get(kode_produk=kode_produk)

            try:
                stock_tambah = int(stock_tambah)
                if stock_tambah <= 0:
                    raise ValueError("Jumlah stok harus lebih dari nol.")

                # Tambah stok baru ke tabel Restok
                Restok.objects.create(
                    produk=produk,
                    stock_lama=produk.stock,
                    stock_tambah=stock_tambah,
                    note=note
                )

                # Update stok produk
                produk.stock += stock_tambah
                produk.save()

                messages.success(request, f"Stok produk '{produk.nama_produk}' berhasil ditambah sebanyak {stock_tambah}.")
                return redirect('restok')

            except ValueError as e:
                messages.error(request, f"Kesalahan input jumlah stok: {e}.")
                return redirect('restok')

        except Produk.DoesNotExist:
            messages.error(request, "Kode produk tidak ditemukan. Silakan periksa kembali.")
            return redirect('restok')

        except Exception as e:
            messages.error(request, f"Terjadi kesalahan pada server: {str(e)}.")
            return redirect('restok')

    return render(request, 'indoapril/formstok.html')


# ====================== Riwayat ====================== 
@login_required
def laporan_transaksi(request):
    """
    Menampilkan laporan transaksi berdasarkan filter bulan dan tahun.
    Menyediakan informasi ringkasan seperti total transaksi, pendapatan, dan produk yang terjual.
    Data juga mendukung fitur paginasi untuk menampilkan transaksi per halaman.
    """
    # Ambil parameter bulan dan tahun dari query string (default adalah bulan dan tahun saat ini)
    try:
        bulan = int(request.GET.get('bulan', datetime.now().month))  # Ambil bulan, atau gunakan bulan saat ini
        tahun = int(request.GET.get('tahun', datetime.now().year))  # Ambil tahun, atau gunakan tahun saat ini
    except ValueError:
        # Jika parameter bulan atau tahun tidak valid, gunakan nilai default
        bulan = datetime.now().month
        tahun = datetime.now().year

    # Filter transaksi berdasarkan bulan dan tahun yang dipilih
    transaksi_queryset = Transaksi.objects.filter(
        tanggal__year=tahun,  # Filter tahun transaksi
        tanggal__month=bulan  # Filter bulan transaksi
    ).order_by('-tanggal')  # Urutkan transaksi dari yang terbaru

    # Ringkasan data untuk laporan
    total_transaksi = transaksi_queryset.count()  # Total jumlah transaksi
    total_pendapatan = transaksi_queryset.aggregate(
        total=Sum('total_harga')  # Jumlahkan semua total harga transaksi
    )['total'] or 0  # Jika hasil None, gunakan 0
    total_produk_terjual = ItemTransaksi.objects.filter(
        transaksi__in=transaksi_queryset  # Filter item berdasarkan transaksi
    ).aggregate(
        total=Sum('jumlah')  # Jumlahkan semua produk yang terjual
    )['total'] or 0  # Jika hasil None, gunakan 0

    # Paginate hasil transaksi menjadi 10 transaksi per halaman
    paginator = Paginator(transaksi_queryset, 10)  # Tentukan ukuran halaman (10 transaksi per halaman)
    page_number = request.GET.get('page')  # Ambil nomor halaman dari query string
    page_obj = paginator.get_page(page_number)  # Ambil data untuk halaman tertentu

    # Daftar bulan dan tahun untuk dropdown filter
    daftar_bulan = list(range(1, 13))  # Buat daftar bulan (1 - 12)
    daftar_tahun = list(range(2020, 2030))  # Rentang tahun (ubah sesuai kebutuhan)

    # Kirim data ke template untuk ditampilkan
    context = {
        'total_transaksi': total_transaksi,  # Total transaksi dalam bulan dan tahun tersebut
        'total_pendapatan': total_pendapatan,  # Total pendapatan dari semua transaksi
        'total_produk_terjual': total_produk_terjual,  # Total produk yang terjual
        'page_obj': page_obj,  # Objek paginasi untuk transaksi
        'bulan': bulan,  # Bulan yang dipilih
        'tahun': tahun,  # Tahun yang dipilih
        'daftar_bulan': daftar_bulan,  # Daftar bulan untuk dropdown
        'daftar_tahun': daftar_tahun,  # Daftar tahun untuk dropdown
    }
    return render(request, 'indoapril/laporan_transaksi.html', context)  # Render ke template laporan transaksi


# ====================== Riwayat Detail ====================== 
@login_required
def riwayat_detail(request,transaksi_id):
    # Mengambil transaksi berdasarkan transaksi_id
    transaksi = Transaksi.objects.get(pk=transaksi_id)
    # Mengambil item terkait dengan transaksi tersebut
    items = transaksi.items.all()  # Ambil item terkait transaksi
    # Mengirimkan konteks ke template
    context = {
        'transaksi': transaksi,
        'items': items
    }
    return render(request, 'indoapril/transaksi_detail.html', context)

# ====================== Transaksi ====================== 
@login_required
@role_required('kasir')
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
    
class ProdukListViewSet(ModelViewSet):
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializer
    filter_backends = [SearchFilter]
    search_fields = ['kode_produk', 'nama_produk']

class TransaksiListViewSet(ModelViewSet):
    queryset = Transaksi.objects.all()
    serializer_class = TransaksiSerializer

class RestokListViewSet(ModelViewSet):
    queryset = Restok.objects.all()
    serializer_class = RestokSerializer

# def riwayat_view(request):
#     transaksi_list = Transaksi.objects.all().order_by('-tanggal')
#     paginator = Paginator(transaksi_list, 10)

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'indoapril/riwayat_transaksi.html', {'page_obj': page_obj})