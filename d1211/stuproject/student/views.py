from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from student.models import Student

# Create your views here.

# 학생 등록
def write(request):
    if request.method == 'GET':
        return render(request,'student/write.html')    
    elif request.method == 'POST':
        name = request.POST.get("name")
        age = request.POST.get("age")
        grade = request.POST.get("grade")
        gender = request.POST.get("gender")
        hobbys = request.POST.getlist("hobby")
        hobby = ','.join(hobbys)
        print("post확인: ",hobby)
        
        # Student db저장
        # Student.objects.create(name=name,age=age,grade=grade,gender=gender,hobby=hobby)
        qs = Student(name=name,age=age,grade=grade,gender=gender,hobby=hobby)
        qs.save()

        return redirect(reverse('student:list'))
        # return redirect(reverse('student:list'),arg=(1,'홍길동'))
    
    # return HttpResponse('Hi')

# 학생 리스트
def list(request):
    
    qs = Student.objects.all().order_by('-sno')
    context = {'list':qs}
    return render(request,'student/list.html',context)

# 학생 상세보기
def view(request, sno):
    
    qs = Student.objects.get(sno=sno)
    context = {'stu':qs}
    return render(request,'student/view.html',context)

# 학생 삭제
def delete(request, sno):
    
    qs = Student.objects.get(sno=sno)
    qs.delete()
    
    return redirect(reverse('student:list'))

def update(request,sno):
    
    if request.method == 'GET':
        
        qs = Student.objects.get(sno=sno)
        context = {"stu":qs}
        return render(request,'student/update.html',context)    
    
    elif request.method == 'POST':
        
        name = request.POST.get("name")
        age = request.POST.get("age")
        grade = request.POST.get("grade")
        gender = request.POST.get("gender")
        hobbys = request.POST.getlist("hobby")
        hobby = ','.join(hobbys)
        print("post확인: ",hobby)
        
        qs = Student.objects.get(sno=sno)
        qs.name = name
        qs.age = age
        qs.grade = grade
        qs.gender = gender
        qs.hobby = hobby

        qs.save()

        return redirect(reverse('student:list'))