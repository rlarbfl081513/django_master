# 장고는 원래 User모델만 알고있음
  # 우리가 새로만든 CustomUser는 모름 때문에 아래와 같이 등록해줘야함 
  # --> 안그럼 어드민 사이트에 아무것도 안뜸, 슈퍼유저로 로그인해도 사용자 관리가 불가능  

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser
# from .forms import CustomUserCreationForm, CustomUserChangeForm

# class CustomUserAdmin(UserAdmin):  # 기존의 UserAdmin 상속해서 커스터마이징 
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['id', 'password', 'nickname', 'age', 'age_limit'] # 관리자 리스트 화면에 보일 필드들 

# # 진짜 등록 
# admin.site.register(CustomUser, CustomUserAdmin)
