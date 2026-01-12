from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment
from django.db.models import Q # 검색 조건을 위해 필요합니다

# 게시판 리스트는 누구나 볼 수 있음
def blist(request):
    # 1. 모든 게시글을 가져온다. (변수명을 posts로 통일)
    # 모든 게시글을 최신순(ID 역순)으로 가져옵니다.
    # 일반 게시글('general')만 가져온다.
    all_posts = Post.objects.filter(category='general').order_by('-created_at')
    # 검색어 가져오기
    search_kw = request.GET.get('search', '') # name="search"로 보낸 값
    # 검색어가 있다면 제목에서 검색
    if search_kw:
        all_posts = all_posts.filter(
            Q(title__icontains=search_kw) | # 제목 검색
            Q(content__icontains=search_kw)   # 내용 검색도 추가하면 더 편리해요!
        ).distinct()
    
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
    return render(request, 'board/blist.html', {
        'posts': page_obj,      # HTML의 {% for post in posts %} 부분
        'search_kw': search_kw  # 검색창에 내가 쓴 글자를 유지시키기 위해 전달
    })




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
            author=writer_nm,
            category='general'  # 일반 게시판용 태그
            # category=category,
            # writer_id=writer_id,
            # writer_nm=writer_nm,
            # write_date=timezone.now() # 현재 시간 저장
        )
        return redirect('board:blist') # 저장 후 다시 리스트로 이동

    return render(request, 'board/bwrite.html')


# 게시글 상세보기
def bview(request, bno):
    # 1. bno(ID)에 해당하는 글을 가져옵니다. (없으면 404 에러)
    from django.shortcuts import get_object_or_404
    post = get_object_or_404(Post, id=bno)
    
    # 2. 조회수 중복 방지 로직 (세션 활용)
    # 세션에서 'viewed_posts'라는 이름의 리스트를 가져옵니다. 없으면 빈 리스트([]) 생성.
    viewed_posts = request.session.get('viewed_posts', [])

    if bno not in viewed_posts:
        # 이 게시글을 처음 보는 경우에만 조회수 +1
        post.views += 1
        post.save()
        
        # 주머니(리스트)에 현재 게시글 번호를 추가
        viewed_posts.append(bno)
        # 업데이트된 리스트를 다시 세션에 저장
        request.session['viewed_posts'] = viewed_posts
        # 세션 데이터가 변경되었음을 장고에 알림
        request.session.modified = True
        

    # 이전글 (더 최신글): 현재보다 작성 시간이 큰(미래) 글 중 가장 오래된 것
    prev_post = Post.objects.filter(
        category=post.category, # ⭐ 현재 글과 같은 카테고리만!
        created_at__gt=post.created_at
    ).order_by('created_at').first()

    # 다음글 (더 예전글): 현재보다 작성 시간이 작은(과거) 글 중 가장 최신 것
    next_post = Post.objects.filter(
        category=post.category, # ⭐ 현재 글과 같은 카테고리만!
        created_at__lt=post.created_at
    ).order_by('-created_at').first()
    
    # 해당 게시글에 달린 댓글들 가져오기
    comments = post.comments.all().order_by('-created_at')
    
    context = {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
        'comments': comments,
    }

    
    # 4. 카테고리에 따른 템플릿 분기 처리
    if post.category == 'notice':
        return render(request, 'board/nview.html', context) # 공지사항용
    else:
        return render(request, 'board/bview.html', context)  # 일반 게시판용

# -----------------------------------------------------------------------------------------------


def bupdate(request, bno):
    # 수정할 게시글 데이터를 가져옵니다.
    # post = get_object_or_404(Post, bno=bno) 
    post = get_object_or_404(Post, id=bno)
    
    if request.method == "POST":
        # 사용자가 수정한 내용을 저장하는 로직
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        # ... 필요한 필드들 업데이트 ...
        post.save()
        return redirect('board:bview', bno=post.id)
    
    # GET 방식일 때는 수정 페이지(HTML)를 보여줍니다.
    return redirect('board:bview', bno=post.id)

def bdelete(request, bno):
    # Post 모델에는 bno 필드가 없으므로 id 필드로 조회해야 함
    post = get_object_or_404(Post, id=bno)
    
    if request.method == "POST":
        post.delete()
        return redirect('board:blist')
        
    return redirect('board:bview', bno=bno)


# -----------------------------------------------------------------------------------------------


# 댓글 작성 로직 (대댓글 포함)
def comment_write(request, bno):
    if request.method == "POST":
        post = get_object_or_404(Post, id=bno)
        content = request.POST.get('content')
        author = request.session.get('user_nm', '익명')
        parent_id = request.POST.get('parent_id') # 아기 댓글일 경우 엄마 번호를 받아옴

        if content:
            comment = Comment(post=post, content=content, author=author)
            if parent_id: # 만약 엄마 번호가 있다면?
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            
    return redirect('board:bview', bno=bno)

# 댓글 삭제
def comment_delete(request, bno, cno):
    comment = get_object_or_404(Comment, id=cno)
    if request.session.get('user_nm') == comment.author:
        comment.delete()
    return redirect('board:bview', bno=bno)

# 댓글 수정 (간단 버전)
def comment_update(request, bno, cno):
    if request.method == "POST":
        # 1. 수정할 댓글을 찾아요
        comment = get_object_or_404(Comment, id=cno)
        
        # 2. 내 글이 맞는지 확인해요 (세션 이름 확인)
        if request.session.get('user_nm') == comment.author:
            # 3. 새로 쓴 내용을 가져와서 저장해요
            comment.content = request.POST.get('content')
            comment.save()
            
    # 4. 일이 끝나면 다시 보던 게시글 페이지로 돌아가요
    return redirect('board:bview', bno=bno)



# -----------------------------------------------------------------------------------------------


# 좋아요 로직
def post_like(request, bno):
    # 1. 어떤 게시글인지 찾습니다.
    post = get_object_or_404(Post, id=bno)
    
    # 2. 세션에서 "좋아요 리스트"를 가져옵니다. 없으면 빈 리스트를 만듭니다.
    # login_user의 id나 이름을 키값으로 사용합니다.
    user_id = request.session.get('user_nm') # 로그인 시 저장한 세션 키값에 맞게 수정하세요.
    
    if not user_id:
        # 로그인을 안 했으면 좋아요를 못 누르게 하고 싶을 때 (선택사항)
        return redirect('board:bview', bno=bno)

    # 3. 좋아요 로직 (토글 방식)
    # 세션 내부에 'liked_posts'라는 이름으로 내가 좋아요 누른 번호들을 저장합니다.
    liked_posts = request.session.get('liked_posts', [])

    if bno in liked_posts:
        # 이미 좋아요를 누른 상태라면? -> 취소!
        post.likes -= 1
        liked_posts.remove(bno) # 리스트에서 게시글 번호 삭제
    else:
        # 처음 누르는 거라면? -> 좋아요!
        post.likes += 1
        liked_posts.append(bno) # 리스트에 게시글 번호 추가

    # 4. 바뀐 좋아요 숫자와 리스트를 저장합니다.
    post.save()
    request.session['liked_posts'] = liked_posts
    request.session.modified = True # 세션이 변경되었음을 명시적으로 알림

    return redirect('board:bview', bno=bno)




# -----------------------------------------------------------------------------------------------
#                                     공지사항 페이지
# -----------------------------------------------------------------------------------------------


def noticelist(request):
    # 1. 모든 게시글을 가져온다. (변수명을 posts로 통일)
    # 모든 게시글을 최신순(ID 역순)으로 가져옵니다.
    all_posts = Post.objects.filter(category='notice').order_by('-created_at')
    # 검색어 가져오기
    search_kw = request.GET.get('search', '') # name="search"로 보낸 값
    # 검색어가 있다면 제목에서 검색
    if search_kw:
        all_posts = all_posts.filter(
            Q(title__icontains=search_kw) | # 제목 검색
            Q(content__icontains=search_kw)   # 내용 검색도 추가하면 더 편리해요!
        ).distinct()
    
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
    return render(request, 'board/noticelist.html', {
        'posts': page_obj,      # HTML의 {% for post in posts %} 부분
        'search_kw': search_kw  # 검색창에 내가 쓴 글자를 유지시키기 위해 전달
    })

def nwrite(request):
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
            author=writer_nm,
            category='notice'
            # category=category,
            # writer_id=writer_id,
            # writer_nm=writer_nm,
            # write_date=timezone.now() # 현재 시간 저장
        )
        return redirect('board:noticelist') # 저장 후 다시 리스트로 이동

    return render(request, 'board/nwrite.html')
