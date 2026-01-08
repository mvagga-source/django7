from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import F,Q,Sum,Count
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from magazine.models import Magazine, MagazineCode
from member.models import MyUser
import json
import urllib.request

def mtest(request):
    return render(request,'magazine/1.html')

def myearChart(request):
    
    if request.method == 'POST':
        
        print('1')
        
        qs = Magazine.objects.annotate(year=ExtractYear('mdate')).values('year').annotate(count=Count('mno')).order_by('year')
        print(qs)
        print('2')
        qs_list = list(qs.values())
        print('3')
        context = {'result':'성공','list':qs_list}
        print('4')
    
        return JsonResponse(context)    

def mcategoryChart(request):
    
    if request.method == 'POST':
        
        qs = Magazine.objects.values('magazinecode','magazinecode__mtype_desc').annotate(max_cnt=Count('magazinecode'))
        
        # 객체일때 전체
        # Json으로 변경시 객체에서 pk키만 변환
        qs_list = list(qs)
        
        context = {'result':'성공','list':qs_list}
    
        return JsonResponse(context)

def mmnge(request):
    
    return render(request,'magazine/mmnge.html')
    
    
def mnaver(request):
    
    page = int(request.GET.get('page',1))
    sort = request.GET.get('sort','sim')
    
    client_id = "j7KaOMGirpd_EoxbjKDB"
    client_secret = "98WTnc2agN"
    
    encText = urllib.parse.quote("음식매거진")
    display = 10
    start = (page - 1) * display + 1
    
    url = f'https://openapi.naver.com/v1/search/blog.json?query={encText}&display={display}&start={start}&sort={sort}'
    # url = "https://openapi.naver.com/v1/search/blog.json?query=" + encText  # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
    requestUr = urllib.request.Request(url)
    requestUr.add_header("X-Naver-Client-Id",client_id)
    requestUr.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(requestUr)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()

        dData = json.loads(response_body)
        nlist = dData['items']
        
        result = '1'        
        context = {'result':result,'page':page,'sort':sort,'nlist':nlist}

    else:
        print("Error Code:" + rescode)
        result = '0'
        context = {'result':result,'page':page,'sort':sort}

    return render(request,'magazine/mnaver.html', context)


def mlike(request):
    
    if request.method == 'POST':
        
        # mno = request.POST.get('mno')
        # qs_magazine = Magazine.objects.get(mno=mno)
        
        # print('0')
        
        # id = request.session['user_id']
        # qs_myuser = MyUser.objects.get(mem_id=id)

        # print('1')

        # if qs_magazine.mlike.filter(pk=qs_myuser.mem_id):
        #     print('2')
        #     qs_magazine.mlike.remove(qs_myuser)
        #     like_chk = 0
        # else:
        #     print('3')
        #     qs_magazine.mlike.add(qs_myuser)
        #     like_chk = 1
        
        mno = request.POST.get('mno')
        qs_magazine = Magazine.objects.get(mno=mno)        
        
        id = request.session['user_id']
        qs_myuser = MyUser.objects.get(mem_id=id)

        if Magazine.objects.filter(Q(mno=mno) & Q(mlike=qs_myuser)).exists():
            qs_magazine.mlike.remove(qs_myuser)
            like_chk = 0
        else:
            qs_magazine.mlike.add(qs_myuser)
            like_chk = 1        
        
        like_count = qs_magazine.mlike.count()
    
    context = {'result':'성공','like_chk':like_chk,'like_count':like_count}
    return JsonResponse(context)


def mview(request,mno):
    
    qs = Magazine.objects.get(mno=mno)
    
    qs_pre = Magazine.objects.filter(mdate__lt=qs.mdate).order_by('-mdate').first()
    qs_next = Magazine.objects.filter(mdate__gt=qs.mdate).order_by('mdate').first()
    
    context = {'mz':qs,'pre':qs_pre,'next':qs_next}
    return render(request,'magazine/mview.html',context)

def mhit(request,mno):
    
    qs = Magazine.objects.get(mno=mno)
    qs.mhit = F('mhit') + 1
    qs.save()
    
    return redirect(f'/magazine/mview/{mno}')

def mlist(request):

    category = request.GET.get('category','')
    search = request.GET.get('search','')
    # print('category : ',category,'search : ',search)
    
    # 매거진 코드 정보
    qs_code = MagazineCode.objects.all()

    # 매거진 리스트
    if not category: # 공란 처리
        
        if not search: # 공란 처리
            qs = Magazine.objects.all().order_by('-mdate')
        else:
            qs = Magazine.objects.filter(Q(mtitle__contains=search)|Q(mcontent__contains=search)).order_by('-mdate')

    else:
        qs_category = MagazineCode.objects.get(mtype=category)
        qs = Magazine.objects.filter(magazinecode=qs_category).order_by('-mdate')

    # 패이징
    page = int(request.GET.get('page',1))
    paginator = Paginator(qs,12)
    qs_list = paginator.get_page(page)
    
    # 남은 화면 출력
    if paginator.count < 5:
        etc = 4 - paginator.count
    else:
        etc = 4 - (paginator.count % 4)
        
    
    qs_maxGood = Magazine.objects.all().order_by('-mlike').first();
    qs_maxView = Magazine.objects.all().order_by('-mhit').first();
        
        
    # print('paginator.count :',paginator.count, 'etc : ',etc)
        
    context = {'qs_code':qs_code,'list':qs_list,'page':page,'etc_count':etc,'category':category,'search':search,'maxGood':qs_maxGood,'maxView':qs_maxView}
    return render(request,'magazine/mlist.html',context)


