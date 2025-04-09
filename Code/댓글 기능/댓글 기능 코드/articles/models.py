from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 댓글 기능을 위한 모델 생성
class Comment(models.Model):
    # 상대방의 이름의 단수형으로 --> article 
    # 단수형변수명 + _ + id로 테이블 필드 이름이 지어짐 
    # 참조를 위한 코드 (게시글 정보를 가져와서 해당 게시글에 댓글이 쓰이도록함)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  # CASECADE 위에서아래로 떨어진다는 의미를 가짐
                            #  Article이 to인자
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 작성자 표시를 위한 필드, 기본값은 익명으로, 로그인상태에서 댓글달면 내 계정이름이 작성자에 들어감 
    author_name = models.CharField(max_length=100, default='익명')