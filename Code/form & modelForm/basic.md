# 🧱 Article 모델, 폼, 뷰 함수 전체 흐름 정리 (주석 포함 + 보충 설명)

Django에서 게시글을 관리하는 Article 모델과 ModelForm, 뷰 함수 흐름을 **사용자 주석 중심으로** 정리했습니다.  
모델부터 폼, 데이터를 처리하는 뷰 로직까지 전체 흐름을 파악하기 쉽게 구성되어 있습니다.

---

## 📦 1. Article 모델 (models.py)

```python
from django.db import models
# django.db라는 패키지안에 models(modles.py)라는 모듈을 쓰거라는 말
# Model은 model에 관련된 모든 코드가 이미 작성된 클래스를 말함
# https://github.com/django/django 이 링크에서 장고의 내부를 볼 수 있음

# Create your models here.

# 게시글이 저장될 테이블을 설계하는 클래스
#  클래스는 대문자로 시작하기에 대문자로 시작하면 클래스인걸 알 수 있음
class Article(models.Model):  # model이라는 클래스를 다 들고 오겠다는 거임(이미 있는 걸 쓰겠다는 거임)
    # 하나하나의 컬럼을 만들 거임
    # 모델 클래스는 테이블 설계도를 그리는 거임 
    # 개발자는 테이블 구조를 어떻게 설계할지에 대한 코드만 제공하면됨 -> 상속을 활용한 프레임워크의 기능 제공 덕분 (코딩계의 밀키트 사용중인거임)

    # 테이블의 각 필드(열)이름을 정한거임 --> 이제부터는 필드라고 부를거임
    # 데이터의 유형과 제약조건을 정의함 -> 즉, 필드 타입과 필드 옵션을 작성하는 거임 
    
    # CharField라는 유형과 max_length라는 제약조건을 검
    title = models.CharField(max_length=20)  # 모델이라는 모듈에 있는 클래스를 고르는 거임, max_length라는 인자 사용
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True)
```

---

## 🧾 2. ArticleForm (forms.py)

```python
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
```

📌 보충 설명:
- 일반 폼을 쓰면 필드를 수동으로 정의해야 하고, ModelForm은 모델 기반으로 자동 생성
- `widget=forms.Textarea`는 단순 `<input>` 대신 `<textarea>`로 폼을 구성

---

## 🧠 3. 관련 뷰 함수 (views.py)

```python
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm
```

---

### ✅ 메인 페이지 (전체 게시글 목록)

```python
def index(request):
    # DB에 전체 게시글 요청 후 가져오기
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)
```

---

### ✅ 게시글 단건 조회

```python
def detail(request, pk):
    # pk로 들어온 정수 값을 활용 해 DB에 id(pk)가 pk인 게시글을 조회 요청 
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)
```

---

### ✅ 게시글 작성 폼 제공

```python
def new(request):
    form = ArticleForm()
    context = {
        'form' : form,
    }
    return render(request, 'articles/new.html', context)
```

---

### ✅ 게시글 생성 처리 (ModelForm 기반)

```python
def create(request):
    ## 기존 방식
      # # 사용자로 부터 받은 데이터를 추출
      # title = request.POST.get('title')
      # content = request.POST.get('content')

      # # DB에 저장 요청 (3가지 방법)
      # # 1.
      # # article = Article()
      # # article.title = title
      # # article.content = content
      # # article.save()

      # # 2.
      # article = Article(title=title, content=content)
      # article.save()
      
      # 3.
      # Article.objects.create(title=title, content=content)
      # return render(request, 'articles/create.html')
      # return redirect('articles:index')
      

    ## modelForm 방식
    form = ArticleForm(request.POST)  # 사용자로부터 받은 데이터를 인자 통으로 넣어서 form 인스턴스 생성

    # 데이터가 유효한지 검사하기 
    if form.is_valid():  # is로 시작하는 메서드는 반환값이 참거짓 
        # 유효성 검사를 통과하면
        article = form.save()  # 통과했으니 저장 (여기서 저장하는게 방금 생성된 글인거임), 반환값이 있기에 article로 이름지어서 줄 수 있음
        return redirect('articles:detail', article.pk)  # 작성 후 제출시 해당 작성글로 링크가 이동되게 하는 코드 

    # 유효성 검사를 통과하지 못했다면, 뭐 때문인지 is_valid에 의해 메시지를 받을 수 있음 
    # 현재 사용자가 게시글을 작성하는 템플릿(현재 작성하던 페이지)를 다시 보여줌
    context = {
        # 왜 유효성 검사를 통과하지 못했는지에 대한 에러메시지를 담고 있음
        'form' : form,
    }
    # 여기서 is_valid(), save()를 쓸 수 있는 이유는 ModelForm 클래스를 사용하기 때문 

    return render(request, 'articles/new.html', context)
```

📌 보충:
- `form.is_valid()`는 모든 필드가 올바른지 확인
- `form.save()`는 내부적으로 `Article.objects.create()` 호출

---

### ✅ 게시글 삭제

```python
def delete(request, pk):
    # 어떤 게시글을 지우는지 먼저 조회
    article = Article.objects.get(pk=pk)
    # DB에 삭제 요청
    article.delete()
    return redirect('articles:index')
```

---

### ✅ 게시글 수정 폼 (작성 중)

```python
def edit(request, pk):
    article = Article.objects.get(pk=pk)
    form = ArticleForm()
    conte  # ← 코드 미완성 상태로 보임
```

📌 보충:  
- 실제로는 `form = ArticleForm(instance=article)` 형태로 기존 데이터를 폼에 넣는 게 일반적
- return 구문과 context도 필요함

---

### ✅ 게시글 수정 처리

```python
def update(request, pk):
    # 어떤 글을 수정하는지 먼저 조회
    article = Article.objects.get(pk=pk)
    # 사용자 입력 데이터를 기존 인스턴스 변수에 새로 갱신 후 저장
    article.title = request.POST.get('title')
    article.content = request.POST.get('content')
    article.save()
    return redirect('articles:detail', article.pk)
```

📌 보충:
- 위 코드는 ModelForm을 쓰지 않고 수동 처리한 방식
- 보통 `form = ArticleForm(request.POST, instance=article)`을 통해 더 깔끔하게 처리 가능

---

## ✅ 전체 흐름 요약

| 구성 요소 | 설명 |
|-----------|------|
| models.py | DB 테이블 구조 정의 (Article) |
| forms.py  | ModelForm으로 폼 자동 생성 |
| views.py  | 요청 처리: 조회, 생성, 수정, 삭제 |
| 주석 스타일 | 코드 흐름 + Django 동작 방식까지 함께 이해 가능 |

이 문서는 Django의 핵심 구조(Model → Form → View)를 학습용으로 한눈에 파악할 수 있도록 구성되어 있습니다.
