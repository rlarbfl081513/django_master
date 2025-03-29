from django.db import models
# django.db라는 패키지안에 models(modles.py)라는 모듈을 쓰거라는 말
# Model은 model에 관련된 모든 코드가 이미 작성된 클래스를 말함
# https://github.com/django/django 이 링크에서 장고의 내부를 볼 수 있음


# Create your models here.

# 게시글이 저장될 테이블을 설계하는 클래스
#  클래스는 대문자로 시작하기에 대문자로 시작하면 클래스인걸 알 수 있음
class Article(models.Model): # model이라는 클래스를 다 들고 오겠다는 거임(이미 있는 걸 쓰겠다는 거임)
    # 하나하나의 컬럼을 만들 거임
    # 모델 클래스는 테이블 설계도를 그리는 거임 
    # 개발자는 데이블구조를 어떻게 설계할지에 대한 코드만 제공하면됨 -> 상속을 활용한 프레임워크의 기능 제공 덕분 (코딩계의 밀키트 사용중인거임)
    
    # 테이블의 각 필드(열)이름을 정한거임 --> 이제부터는 필드라고 부를거임
    # 데이터의 유형과 제약조건을 정의함 -> 즉, 필드 타입과 필드 옵션을 작성하는 거임 
    
        # CharField라는 유형과 max_length라는 제약조건을 검
    title = models.CharField(max_length=20)  # 모델이라는 모듈에 있는 클래스를 고르는 거임, max_length라는 인자 사용
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True)