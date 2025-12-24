from django.shortcuts import render

def clist(request):
    return render(request,'customer/clist.html')
