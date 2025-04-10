
  # 장고는 from django.contrib.auth.models import User를 기본적으로 쓰지만 
  # 기본 유저모델이든 커스텀 모델이든 현재 프로젝트에서 사용하는 진짜 유저모델을 가져오는 함수
from django.contrib.auth import get_user_model  
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    model = get_user_model()


class CustomUserChangeForm(UserChangeForm):
  class Meta(UserChangeForm.Meta):
    model = get_user_model()
    # 유저가 수정할 사항에 해당되는 폼만 보이도록 
    fields = ('first_name', 'last_name', 'email',)