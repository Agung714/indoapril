from django.shortcuts import render

def transaksi(request):
    return render(request, "indoapril/transaksi.html")
def login(request):
    return render(request, "indoapril/login.html")

def dashboard(request):
    return render(request, 'indoapril/dashboard.html')


def dashboard_create(request):
    return render(request, 'indoapril/form.html') # Pastikan Anda mengirimkan form ke template
    # return render(request, 'indoapril/create.html', {'form': StudentsForm()}) # Pastikan Anda mengirimkan form ke template