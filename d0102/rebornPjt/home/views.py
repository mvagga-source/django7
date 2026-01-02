from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def filPop(request):
    return render(request, 'filPop.html')