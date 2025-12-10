from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from student.models import Student


# Create your views here.

def write(request):
    
    if request.method == 'GET':
        return render(request,'student/write.html')
    elif request.method == 'POST':
        
        sno = request.POST.get("sno")
        name = request.POST.get("name")
        age = request.POST.get("age")
        grade = request.POST.get("grade")
        gender = request.POST.get("gender")
        hobbys = request.POST.getlist("hobby")
        hobby = ",".join(hobbys)
        
        Student.objects.create(name=name,age=age,grade=grade,gender=gender,hobby=hobby)
        
        # return render(request,'student/write.html')
        # return HttpResponse('hi..')
        return redirect('/student/list/')
        
def list(request):
    
    qs = Student.objects.all().order_by("-sno","name")
    context = {"list":qs}
    return render(request,'student/list.html', context)

def view(request,sno):
    
    qs = Student.objects.get(sno=sno)
    context = {"stu":qs}
    return render(request,'student/view.html',context)
