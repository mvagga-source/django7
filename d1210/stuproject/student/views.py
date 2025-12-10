from django.shortcuts import render, redirect
from django.urls import reverse
from student.models import Student

# Create your views here.


# 학생 등록
def write(request):
    if request.method == 'GET':
        return render(request,'student/write.html')
    elif request.method == 'POST':
        
        # form에서 넘어온 데이터 처리
        # print(request.POST.get("name"))
        # print(request.POST.get("age"))
        # print(request.POST.get("grade"))
        # print(request.POST.get("gender"))
        # print("hobby : ",hobbys)        
        
        name = request.POST.get("name")
        age = request.POST.get("age")
        grade = request.POST.get("grade")
        gender = request.POST.get("gender")
        hobby = request.POST.getlist("hobby")
        hobbys = ','.join(hobby) # 리스트 타입을 문자열타입으로 변환하는 방법
        
        qs = Student(name=name,age=age,grade=grade,gender=gender,hobby=hobbys)
        qs.save()

        # return render(request,'student/write.html')
        # return redirect('/student/list/')
        return redirect(reverse('student:list'))

# 학생 리스트
def list(request):
    
    qs = Student.objects.all().order_by('-sno','name')
    context = {"list":qs}
    return render(request,'student/list.html',context)

# 학생 상세보기
def view(request,sno,name):
    # sno = request.GET.get("sno") # 데이터 없으면 None
    # age = request.GET['age'] # 데이터 없으면 에러
    
    # print("넘어온 데이터 sno :",sno)
    # print("넘어온 데이터 name :",name)
    
    qs = Student.objects.get(sno=sno)
    context = {"student":qs}  # list = qs
    return render(request,'student/view.html',context)

# 학생 삭제
def delete(request):
    
    return render(request,'student/list.html')
    