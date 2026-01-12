from django.db import models  # 장고에서 데이터베이스 도구(models)를 불러옴

# Post라는 이름의 테이블(표)을 정의
# models.Model을 상속받아야 장고가 "이건 데이터베이스용 클래스구나!"라고 인식
class Post(models.Model):
    # 제목
    title = models.CharField(max_length=200)

    # 내용: 글자 수 제한이 없음
    content = models.TextField()

    # 작성자:이름을 안 적으면 기본값으로 '익명'
    author = models.CharField(max_length=50, default='익명')

    # 작성일
    # auto_now_add=True는 "글이 처음 저장되는 순간의 시간"을 자동으로 기록하라는 뜻
    created_at = models.DateTimeField(auto_now_add=True)

    # 조회수: 0 이상의 양수만 저장하는 숫자 칸 
    # default=0은 처음 글이 올라오면 조회수가 0부터 시작한다는 뜻
    views = models.PositiveIntegerField(default=0)
    
    # [좋아요 기능 추가] 
    # 실제로는 User 모델과 연결해야 하지만, 현재 세션 방식을 쓰시므로 
    # 간편하게 숫자만 카운트하는 방식으로 먼저 구현하거나, 아이디 리스트를 저장할 수 있습니다.
    likes = models.PositiveIntegerField(default=0)
    
    # ⭐ 카테고리 필드 추가: general(일반), notice(공지/문의) 구분용
    category = models.CharField(max_length=20, default='general')

    # 이 함수는 관리자 페이지(Admin)나 터미널에서 데이터를 조회할 때,
    # 글 번호(Post object) 대신 실제 '글 제목'이 보이게 해주는 역할
    def __str__(self):
        return self.title
    
    
    # [댓글 모델 추가]
class Comment(models.Model):
    # 어떤 게시글의 댓글인지 연결 (Post가 삭제되면 댓글도 삭제됨)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # ⭐ 대댓글 핵심: 'self'는 나(Comment)를 다시 가리킨다는 뜻이에요. 
    # null=True는 일반 댓글(엄마 없는 첫 댓글)도 가능하게 해줍니다.
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"{self.author}님의 댓글"