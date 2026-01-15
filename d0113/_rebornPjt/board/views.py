from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment, PostImage
from django.db.models import F, Q # 검색 조건을 위해 필요합니다

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
    # 1. bno(ID)에 해당하는 글을 가져옵니다.
    post = get_object_or_404(Post, id=bno)
    print(f"--- 현재 카테고리: [{post.category}] ---")
    
    # 2. 조회수 중복 방지 로직 (세션 활용)
    viewed_posts = request.session.get('viewed_posts', [])

    if bno not in viewed_posts:
        post.views += 1
        post.save()
        viewed_posts.append(bno)
        request.session['viewed_posts'] = viewed_posts
        request.session.modified = True
        
    # 3. 카테고리별 글 목록 미리보기 로직 추가
    # 현재 게시글과 같은 카테고리의 모든 글을 최신순으로 가져옵니다.
    all_category_posts = Post.objects.filter(category=post.category).order_by('-created_at')
    
    # Paginator 세팅: 한 페이지에 5개씩 보여줌
    paginator = Paginator(all_category_posts, 5)
    page_number = request.GET.get('page', 1) # URL에 page 파라미터가 없으면 1페이지
    posts_in_category = paginator.get_page(page_number)

    # 이전글 (더 최신글)
    prev_post = Post.objects.filter(
        category=post.category,
        created_at__gt=post.created_at
    ).order_by('created_at').first()

    # 다음글 (더 예전글)
    next_post = Post.objects.filter(
        category=post.category,
        created_at__lt=post.created_at
    ).order_by('-created_at').first()
    
    # 해당 게시글에 달린 댓글들 가져오기
    comments = post.comments.all().order_by('-created_at')
    
    # context에 posts_in_category 추가
    context = {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
        'comments': comments,
        'posts_in_category': posts_in_category, # 템플릿에서 리스트 출력용
    }

    # 4. 카테고리에 따른 템플릿 분기 처리
    if post.category == 'notice':
        return render(request, 'board/nview.html', context)
    elif post.category == 'map':
        return render(request, 'board/mview.html', context)
    else:
        return render(request, 'board/bview.html', context)
# -----------------------------------------------------------------------------------------------


def bupdate(request, bno):
    post = get_object_or_404(Post, id=bno)
    
    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        
        # 2. 사진 수정 로직 추가
        new_images = request.FILES.getlist('images')  # 수정 폼에서 보낸 이미지들
        if new_images:
            # 기존 사진들을 DB에서 삭제 (실제 파일까지 삭제하려면 별도 처리가 필요하지만 일단 DB 삭제)
            post.images.all().delete() 
            
            # 새로 받은 사진들 저장
            for img in new_images:
                PostImage.objects.create(post=post, image=img)
        
        
        # [수정 후 카테고리별 이동 로직]
        if post.category == 'notice':
            return redirect('board:noticelist')
        elif post.category == 'map':
            return redirect('board:map')
        else:
            return redirect('board:blist')
    
    return redirect('board:bview', bno=post.id)

def bdelete(request, bno):
    post = get_object_or_404(Post, id=bno)
    
    if request.method == "POST":
        category = post.category  # 삭제하기 전에 카테고리를 미리 변수에 담아둡니다.
        post.delete()
        
        # [삭제 후 카테고리별 이동 로직]
        if category == 'notice':
            return redirect('board:noticelist')
        elif category == 'map':
            return redirect('board:map')
        else:
            return redirect('board:blist')
            
    return redirect('board:bview', bno=bno)


# -----------------------------------------------------------------------------------------------


def comment_write(request, bno):
    if request.method == "POST":
        post = get_object_or_404(Post, id=bno)
        content = request.POST.get('content')
        author = request.session.get('user_nm', '익명')
        parent_id = request.POST.get('parent_id')
        
        # ⭐ 사진 파일 가져오기
        image = request.FILES.get('image')

        if content:
            comment = Comment(
                post=post, 
                content=content, 
                author=author,
                image=image  # ⭐ 이미지 저장
            )
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            
    return redirect('board:bview', bno=bno)

# 댓글 수정 (사진 수정 기능 추가)
def comment_update(request, bno, cno):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=cno)
        
        if request.session.get('user_nm') == comment.author:
            # 1. 텍스트 내용 수정
            comment.content = request.POST.get('content')
            
            # 2. ⭐ 새로운 사진이 들어왔는지 확인
            new_image = request.FILES.get('image')
            if new_image:
                comment.image = new_image  # 새로운 사진으로 교체
            
            comment.save()
            
        delete_image = request.POST.get('delete_image') # HTML에서 체크박스로 보낸 값
        if delete_image == 'on':
            comment.image.delete() # 기존 파일 삭제 및 필드 비우기    
            
    return redirect('board:bview', bno=bno)

# 댓글 삭제
def comment_delete(request, bno, cno):
    comment = get_object_or_404(Comment, id=cno)
    if request.session.get('user_nm') == comment.author:
        comment.delete()
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
    all_posts = Post.objects.filter(category='notice').order_by('-is_notice','-created_at')
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
        category = request.POST.get('category', 'notice')
        writer_nm = request.session.get('user_nm')
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



# -----------------------------------------------------------------------------------------------
#                                     맛집지도 페이지
# -----------------------------------------------------------------------------------------------


def map(request):
    # 1. 맛집 기본 필터링 (정렬은 마지막에 한 번만 수행)
    all_posts = Post.objects.filter(category='map')

    # 2. 카테고리(topic) 리스트 가져오기
    topic_list = Post.objects.filter(category='map').values_list('topic', flat=True).distinct()

    # 3. 파라미터 가져오기
    topic_filter = request.GET.get('topic', '') 
    search_kw = request.GET.get('search', '')
    sort = request.GET.get('sort', 'recent') # 정렬 파라미터

    # 4. 주제 및 검색어 필터링
    if topic_filter:
        all_posts = all_posts.filter(topic=topic_filter)

    if search_kw:
        all_posts = all_posts.filter(
            Q(title__icontains=search_kw) | Q(content__icontains=search_kw)
        ).distinct()

    # 5. 정렬 처리 (페이징 직전에 수행해야 함)
    if sort == 'likes':
        # Post 모델에 'likes' 필드가 실제 있는지 확인하세요. 
        # 만약 필드명이 다르면 그 이름으로 바꿔야 합니다.
        all_posts = all_posts.annotate(
            total_score=F('views') + F('likes')
        ).order_by('-total_score', '-id') # ID는 동점자 처리용
    else:
        # 최신순
        all_posts = all_posts.order_by('-created_at')

    # 6. 페이징 처리
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'board/map.html', {
        'posts': page_obj,
        'search_kw': search_kw,
        'current_topic': topic_filter,
        'topic_list': topic_list,
        'sort': sort, # HTML에서 active 표시용
    })

def mwrite(request):
    # 문지기 대신 우리가 직접 세션 장부를 확인합니다.
    if not request.session.get('login_user'):
        # 장부에 이름이 없으면? 로그인 페이지로 보냅니다.
        return redirect('member:login')

    if request.method == "POST":
        # 폼에서 넘겨준 데이터 받기
        title = request.POST.get('title')    # 제목
        content = request.POST.get('content') # 내용
        image = request.FILES.get('image') # ⭐ 이미지 가져오기
        
        # HTML의 <select name="category">에서 값을 가져오므로 'category'로 받아야 합니다.
        topic = request.POST.get('category') 
        
        # 세션에서 작성자 정보 가져오기
        writer_nm = request.session.get('user_nm')

        # DB에 저장
        post = Post.objects.create(
            title=title,
            content=content,
            topic=topic,      # 'free', 'hidden_gem' 등이 저장됩니다.
            author=writer_nm,
            category='map',   # 맛집지도 게시판 구분값
            
        )
        
        # 2. 여러 장의 이미지를 가져와서 하나씩 저장합니다.
        images = request.FILES.getlist('images') # HTML의 name="images"와 일치해야 함
        for img in images:
            PostImage.objects.create(post=post, image=img)

        return redirect('board:map')
        

    return render(request, 'board/mwrite.html')
