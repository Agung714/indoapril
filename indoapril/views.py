from django.shortcuts import render

def login(request):
    return render(request, "indoapril/login.html")

def dashboard(request):
    return render(request, 'indoapril/dashboard.html')
def transaksi(request):
    return render(request, "indoapril/transaksi.html")

# from django.shortcuts import render

# def transaksi(request):
#     return render(request, 'transaksi.html', {'page': 'kasir'})

# def dashboard(request):
#     return render(request, 'dashboard.html', {'page': 'manajer'})


def dashboard_create(request):
    return render(request, 'indoapril/form.html') # Pastikan Anda mengirimkan form ke template
def dashboard_edit(request):
    return render(request, 'indoapril/edit.html') # Pastikan Anda mengirimkan form ke template
    # return render(request, 'indoapril/create.html', {'form': StudentsForm()}) # Pastikan Anda mengirimkan form ke template