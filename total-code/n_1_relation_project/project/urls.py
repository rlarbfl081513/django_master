"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

# path는 하나의 url패턴을 정의
    # path('주소/', 실행할_함수_or_include)
    # 예) path('about/', views.about) --> about이라는 url에 들어오면 about()함수 실행 

# include는 다른 url 설정 파일을 불러와서 연결 

# include는 url분리는 위해서 사용하는 함수 
# 이경로로 들어오면 해당 앱의 urls.py 파일을 참고하라고 말하는 거임 
from django.urls import path, include

urlpatterns = [
    # 이건 장고가 기본으로 제공하는 관리자페이지를 url패턴을 연결하는 코드
    # admin/에 들어오면 장고가 자동으로 만든 뷰들을 실행하는 거임 
    path('admin/', admin.site.urls),

    # 장도는 articles/로 시작하는 모든 url은 aricles/urls.py에서 찾아보라고 알아들음 
    # 이걸 안 사용하면 여기 파일에 다 떄려넣는건데, 그럼 url이 많아져서 복잡해지고 유지보수 힘들어짐 
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
]
