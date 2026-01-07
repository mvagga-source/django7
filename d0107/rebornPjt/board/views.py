from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment

# 게시판 리스트는 누구나 볼 수 있음
def blist(request):
    # 1. 모든 게시글을 가져온다. (변수명을 posts로 통일)
    # 모든 게시글을 최신순(ID 역순)으로 가져옵니다.
    all_posts = Post.objects.all().order_by('-id') 
    
    # 2. Paginator 설정 (첫 번째 인자에 위에서 선언한 변수 posts를 넣어야 함)
    paginator = Paginator(all_posts, 10) # 10개씩 자르기
    
    # 3. 현재 페이지 번호를 가져오고 해당 페이지 객체를 생성
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 4. 템플릿으로 데이터를 보냄
    # (page_obj를 'posts'라는 이름으로 전달하면 HTML의 {% for post in posts %}가 작동)
    # DB에서 모든 글을 가져와서 최신순으로 정렬
    posts = paginator.get_page(page_number)
    # all_posts = Board.objects.all().order_by('-id')
    return render(request, 'board/blist.html', {'posts': page_obj})

def notice(request):
    # 만약 DB에 '공지사항' 카테고리가 따로 있다면 필터링해서 가져올 수도 있다.
    # 지금은 단순히 notice.html을 보여주는 코드로 작성
    return render(request, 'board/notice.html')



# @login_required(login_url='/member/login/')  # 로그인 안 된 경우 로그인 페이지로 리다이렉트
def bwrite(request):
    # 문지기 대신 우리가 직접 세션 장부를 확인합니다.
    if not request.session.get('login_user'):
        # 장부에 이름이 없으면? 로그인 페이지로 보냅니다.
        return redirect('member:login')

    if request.method == "POST":
        # 폼에서 넘겨준 데이터 받기
        title = request.POST.get('title')    # 제목
        content = request.POST.get('content') # 내용
        # category = request.POST.get('category') # 주제 선택
        # author = request.session.get('user_nm') # 세션에 저장된 닉네임 사용
        
        # 데이터가 잘 들어왔는지 확인용 (터미널에 찍힘)
        print(f"가져온 제목: {title}")
        
        # 세션에서 작성자 정보 가져오기
        # writer_id = request.session.get('login_user')
        writer_nm = request.session.get('user_nm')

        # DB에 저장
        Post.objects.create(
            title=title,
            content=content,
            author=writer_nm
            # category=category,
            # writer_id=writer_id,
            # writer_nm=writer_nm,
            # write_date=timezone.now() # 현재 시간 저장
        )
        return redirect('board:blist') # 저장 후 다시 리스트로 이동

    return render(request, 'board/bwrite.html')


# 게시글 상세보기
def bview(request, bno):
    # 1. bno(ID)에 해당하는 글을 하나 가져옵니다.
    # 만약 번호가 없으면 에러 대신 404 페이지를 띄우는 get_object_or_404를 써도 좋습니다.
    post = Post.objects.get(id=bno)
    
    # 2. 조회수 올리기 (선택사항)
    post.views += 1
    post.save()
    
    # 해당 게시글에 달린 댓글들만 가져오기
    comments = post.comments.all().order_by('-created_at')
    
    return render(request, 'board/bview.html', {
        'post': post,
        'comments': comments
    })


# 댓글 작성 로직
def comment_write(request, bno):
    if request.method == "POST":
        post = get_object_or_404(Post, id=bno)
        content = request.POST.get('content')
        author = request.session.get('user_nm', '익명')

        if content:
            Comment.objects.create(
                post=post,
                content=content,
                author=author
            )
    return redirect('board:bview', bno=bno)



def comment_delete(request, bno, cno):
    comment = get_object_or_404(Comment, id=cno)
    
    # 세션의 사용자 이름과 댓글 작성자가 같을 때만 삭제
    if request.session.get('user_nm') == comment.author:
        comment.delete()
        
    return redirect('board:bview', bno=bno)











# 좋아요 로직
def post_like(request, bno):
    post = get_object_or_404(Post, id=bno)
    post.likes += 1
    post.save()
    return redirect('board:bview', bno=bno)