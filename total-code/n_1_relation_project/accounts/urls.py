from django.urls import path

# views.py에서 함수들 가져옴 
from . import views # 이 파일과 같은 디렉토리에 있는 views.py를 가져온다는거

# 이 앱의 이름 공간 지정 ( url 이름 충돌 방지용 )
  # 활용
    # <a href="{% url 'articles:index' %}">홈으로</a>
    # articles:index는 aritlces라는 앱의 name='index인 url을 찾아준다.
    # 앱네임을 설정안하면 그냥 index라고 쓸수 있지만, 다른 앱들과 이름이 같거나하면 충돌하는 문제 발생 
app_name = 'accounts'
urlpatterns = [

    # url 패턴등록 : 홈/에 접소하면 index함수 실행 
    # 빈 문자열은 홈주소 
    # view.index는 views.py에 정의된 index 함수를 실행한다는 거임
    # name='index'는 이 url 패턴의 이름(템플릿이나 리디렉션에서 사용)
    path('', views.index, name='index'),

    # 회원가입 url 
    path('signup/', views.signup, name='signup'),
    # 회원탈퇴 
    path('signout/', views.signout, name='signout'),
    # 회원정보 수정 
    path('userEdit/', views.userEdit, name='userEdit'),
    # 비밀번호 수정 
    path('password/', views.change_password, name='change_password'),

    # 로그인 
    path('login/', views.login, name='login'),
    # 로그아웃 
    path('logout/', views.logout, name='logout'),
]
