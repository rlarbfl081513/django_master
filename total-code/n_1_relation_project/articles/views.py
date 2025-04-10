from django.shortcuts import render, redirect
from .forms import ArticleForm
from .models import Article

# Create your views here.
def index(request):
  articles = Article.objects.all()
  context = {
    'articles' : articles,
  }
  return render(request, 'articles/index.html', context)

def detail(request, pk):
  article = Article.objects.get(pk=pk)
  context = {
    'article' : article,
  }
  return render(request, 'articles/detail.html', context)


def create(request):
  if request.method == 'POST':
    # 모델폼의 2번째 인자로 요청받은 파일 데이터를 작성
      # 모델 폼의 상위 클래스인 BaseModelForm의 생성자 함수의 2번째 위치 인자로 파일을 받도록 설정돼있음 
    form = ArticleForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('articles:index')
  else:
    form = ArticleForm()
  
  context = {
    'form' : form,
  }

  return render(request, 'articles/create.html', context)


# 아래의 if else를 통한 구현은 수정과 업데이트를 하나에 담은 함수
  # context에 담기는 form은 
  # 1. is_vaild를 통과하지 못해 에러메시지를 담은 form이거나
  # 2. else문을 통한 form 인스턴스

# 조건문은 http 요청을 기준으로 조건을 건거임
  # 단순히 보면 GET은 달라는거고 POST는 생성해달라는 거임 

def edit(request,pk):
  article = Article.objects.get(pk=pk)
  # 어떻게 폼안에 내가 썼던게 들어가 있을까??
    # article = Article.objects.get(pk=pk) : article는 Artcle 클래스의 인스턴스 (pk로 해당 인스턴스를 가져옴)
    # ArticleForm(instance=article) : 그 인스턴스를 폼에 미리 채웒음, 그래서 템플릿에서 값이 채워져있는거임
      # article = Article.objects.get(pk=1)  # ← DB에서 가져온 인스턴스
      # form = ArticleForm(instance=article)  # ← 그 인스턴스로 폼 채우기


  if request.method == 'POST':
    # data는 첫번째 위치한 키워드 인자이기에 생략 가능, instance는 9번째 위치한 키워드 인이기에 이름 붙여서 불러야함
      # request.POST : 사용자가 입력한 새 데이터
      # instance : 수정 대상이 되는 기존 객체
      # form.save() : article 객체에 새 데이터로 덮어쓰기 후 저장
      # 인스턴스없이 리케스트 포스트만 있으면 그냥 또 새로운 게시글 쓰는거임, 근데 인스턴스 덕에 덮어쓰기해서 수정이라는 게 되는 거임
    form = ArticleForm(request.POST, instance=article)
    if form.is_valid():
      form.save()
      return redirect('articles:detail', pk=pk)
  else:
    form = ArticleForm(instance=article)
  
  context = {
    'form' : form,
    'article' : article,
  }

  return render(request, 'articles/edit.html', context)


## 게시글 삭제하기
  # 그냥 해당 게시글 정보 받아와서 delete 함수 실핼하면 끝 
def delete(request,pk):
  article = Article.objects.get(pk=pk)
  article.delete()
  return redirect('articles:index')