from django import forms
from .models import Article

# form : 사용자 입력 데이터를 db에 저장하지 않을 때 (검색이나 로그인)
# modelForm : 사용자 입력 데이터를 db에 저장해야할 때 (게시글 작성, 회원가입)

class ArticleForm(forms.ModelForm): 
    # Meta class : model form의 정보를 작성하는 곳
    class Meta:
        model = Article
        # fields & exclude 속성
            # exclude 속성을 통해 모델에서 포함하지 않을 필드를 지정할 수 있음
            # 장고에서 모델폼에 대한 추가정보나 속성을 작성하는 클래스 구조를 Meta클래스로 작성했을 뿐, 파이선의 이너클래스같은 문법적인 관점으로 접근하지 말것
        fields = '__all__'
