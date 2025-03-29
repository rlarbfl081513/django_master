from django.contrib import admin

# 현재 위치에서 모델스라는 모듈안에 article이라는 클래스가 있다고 알려주는 거임
# .은 명시적 상대경로 나타내는 거임 (현재 위치에 있는 모델스 모듈 위치에서 article class를 가져오는 거임)
from .models import Article

# Register your models here.
admin.site.register(Article)