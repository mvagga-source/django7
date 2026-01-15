from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from store.models import Book

# -------------------------------------------------------------
# [도서관리자페이지]: 도서를 추가,수정,삭제할 수 있는 관리자페이지
# -------------------------------------------------------------
# 1. 도서정보 글쓰기
def bwrite(request):
    # user_id = request.session.get('session_id')
    # if user_id == 'oeunji27':
        if request.method == 'GET':
            return render(request,'Book_Manage/bwrite.html')
        
        elif request.method == 'POST':
            btitle = request.POST.get('btitle') # 책제목
            bauthor = request.POST.get('bauthor')# 작가
            bpublisher = request.POST.get('bpublisher')# 출판사
            bpubdate = request.POST.get('bpubdate')# 출판일
            bprice = request.POST.get('bprice') # 가격
            bimage = request.POST.get('bimage') # 이미지
            bdescription = request.POST.get('bdescription') # 책 소개
            bisbn = request.POST.get('bisbn') # 책고유번호

            Book.objects.create(
                btitle=btitle,
                bauthor=bauthor,
                bpublisher=bpublisher,
                bpubdate=bpubdate,
                bprice=bprice,
                bimage=bimage,
                bdescription=bdescription,
                bisbn=bisbn
            )
            return redirect('store:slist')
        
# 2. 도서정보 리스트
def blist(request):
    # 게시글 모두 가져오기
    qs = Book.objects.all().order_by('-bpubdate','-created_at')
    # 하단 넘버링 (qs,10) -> 1페이지 10개씩
    paginator = Paginator(qs,10)  # 101 -> 11
    # 현재페이지 넘김.
    page = int(request.GET.get('page',1))
    list_qs = paginator.get_page(page) # 1page -> 게시글 10개를 전달
    
    context = {'list':list_qs,'page':page}
    return render(request,'Book_Manage/blist.html',context)


# 3.도서내용 상세보기
def bview(request,bisbn):
    if request.method == 'GET':
        qs = Book.objects.get(bisbn=bisbn)
        context = {'book':qs}
        return render(request,'Book_Manage/bview.html',context)

        
# 4.도서내용 수정하기
def bupdate(request,bisbn):
    if request.method == 'GET':
        qs = Book.objects.get(bisbn=bisbn)
        context = {'book':qs}
        return render(request,'Book_Manage/bupdate.html',context)
    
def bup_finish(request,bisbn):
    # 1단계: 수정할 책을 DB에서 먼저 꺼내옵니다. (불러오기)
    book = Book.objects.get(bisbn=bisbn) 

    if request.method == "POST":
        # 2단계: 꺼내온 책의 내용물을 폼에서 입력받은 새 내용으로 덮어씁니다.
        book.bisbn = request.POST['bisbn']
        book.btitle = request.POST['btitle']
        book.bauthor = request.POST['bauthor']
        book.bpublisher = request.POST['bpublisher']
        book.bpubdate = request.POST['bpubdate']
        book.bprice = request.POST['bprice']
        book.bimage = request.POST['bimage']
        book.bdescription = request.POST['bdescription']
        # 3단계: 변경된 내용을 DB에 반영합니다. (저장하기)
        book.save() 
        
        return redirect('store:slist') # 수정 후 목록으로 이동 


# 게시판 삭제
def bdelete(request,bisbn):
    # 게시글 가져오기
    qs = Book.objects.filter(bisbn=bisbn)
    qs.delete()
    return redirect('Book_Manage:blist')






