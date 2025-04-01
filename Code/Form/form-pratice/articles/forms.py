from django import forms
from .models import Article

# # 모델폼이 아닌 일반 폼 구현 코드
# class ArticleForm(forms.Form):
#   title = forms.CharField(max_length=10)

#   # forms라는 모듈안에 들어있는 위젯 클래스
#   # 인풋의 표현방법을 바꿔버림 
#   content = forms.CharField(widget=forms.Textarea) 


class ArticleForm(forms.ModelForm):
  class Meta:
    model = Article
    fields = '__all__'  # 전체 필드 출력 