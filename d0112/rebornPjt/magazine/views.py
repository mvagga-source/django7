from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import F,Q,Sum,Count,Max
from django.db.models.functions import ExtractYear, TruncYear
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from magazine.models import Magazine, MagazineCode, MagazineAdmin
from member.models import MyUser
import json
import urllib.request

def mtest(request):
    return render(request,'magazine/1.html')


def mlogin(request):
    
    if request.method == 'POST':
        
        mid = request.POST.get('mid')
        mpw = request.POST.get('mpw')
        
        qs = MagazineAdmin.objects.filter(Q(mid=mid) & Q(mpw=mpw))
        
        if not qs:
           context = {'result':'fail'}
        else:
            # equest.session['session_id'] = 'admin'
            context = {'result':'success'}
    
        return JsonResponse(context)
    else:
        return render(request,'magazine/mlogin.html')

def myearChart(request):
    
    if request.method == 'POST':

        # qs = Magazine.objects.aggregate(count=Count('mno')).annotate(year=ExtractYear('mdate'),magazineDesc=F('magazinecode__mtype_desc')).values('year','magazineDesc','magazinecode').order_by('year','magazinecode')
        # qs = Magazine.objects.annotate(year=TruncYear('mdate')).values('year').annotate(count=Count('mno')).order_by('year')
        # qs = Magazine.objects.all()
        
        qs = (
            Magazine.objects
            .annotate(year=ExtractYear('mdate'))
            .values('year','magazinecode__mtype_desc')
            .annotate(count=Count('mno'))
            .order_by('year')
        )

        years = sorted(set(item['year'] for item in qs))
        # print("year : ",years)
        
        # 카테고리별 데이터 구조 생성
        categories = sorted(set(item['magazinecode__mtype_desc'] for item in qs))        
        # print("categories : ",categories)

        data_by_category = {
            cat: [0] * len(years) for cat in categories
        }
        
        year_index = {year: idx for idx, year in enumerate(years)}
        # print("year_index : ",year_index)
        
        for item in qs:
            idx = year_index[item['year']]
            data_by_category[item['magazinecode__mtype_desc']][idx] = item['count']

        # print("data_by_category : ",data_by_category)            
        
        context = {'result':'success','years':years,'data_by_category':data_by_category}
    
        return JsonResponse(context)    

def mcategoryChart(request):
    
    if request.method == 'POST':
        
        qs = (
            Magazine.objects.values('magazinecode','magazinecode__mtype_desc')
            .annotate(max_cnt=Count('magazinecode'), magazineDesc = F('magazinecode__mtype_desc'))
        )
        
        # 객체일때 전체
        # Json으로 변경시 객체에서 pk키만 변환
        qs_list = list(qs)
        
        context = {'result':'성공','list':qs_list}
    
        return JsonResponse(context)
    
    
def mupdate(request):
    
    if request.method == 'POST':

        mno = request.POST.get('mno')
        mthumbnail = request.POST.get('thumbnail')
        
        qs = Magazine.objects.get(mno=mno)
        qs.mthumbnail = mthumbnail
        qs.save()
    
    context = {'result':'성공'}
    
    return JsonResponse(context)

def mmnge(request):
    
    sortlist = [
        {'value':'','desc':'- 정렬 -'},
        {'value':'no','desc':'번호'},
        {'value':'title','desc':'제목'},
        {'value':'like','desc':'좋아요'},
        {'value':'view','desc':'조회수'},
    ]
    
    category = request.GET.get('category','')
    sort = request.GET.get('sort','')
    search = request.GET.get('search','')
    
    # 매거진 코드 정보
    qs_code = MagazineCode.objects.all()
    
    # 매거진 리스트
    if search == '':
    
        if category == 'all':
            qs_category = Magazine.objects.all()
        else:
            qs_category = Magazine.objects.filter(magazinecode__mtype=category)
        
        if sort == 'like':
            qs = qs_category.annotate(mlikeOrder=Max('mlike')).order_by('-mlikeOrder')
        elif sort == 'title':
            qs = qs_category.order_by('mtitle')
        elif sort == 'view':
            qs = qs_category.order_by('-mhit')
        else:
            qs = qs_category.order_by('-mno')
            sort = 'no'
    else:
        qs = Magazine.objects.filter(Q(mtitle__contains=search)|Q(mcontent__contains=search)).order_by('-mno')
        sort = 'no'
        category = 'all'
        
        

    # 패이징
    page = int(request.GET.get('page',1))
    paginator = Paginator(qs,50)
    qs_list = paginator.get_page(page)
    
    context = {'mzcode':qs_code,'mzlist':qs_list,'sortlist':sortlist,'page':page,'category':category,'sort':sort}
    
    return render(request,'magazine/mmnge.html',context)
    
    
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


