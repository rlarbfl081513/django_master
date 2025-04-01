from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm


# 메인 페이지를 응답하는 함수 (+ 전체 게시글 목록)
def index(request):
    # DB에 전체 게시글 요청 후 가져오기
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


# 특정 단일 게시글의 상세 페이지를 응답 (+ 단일 게시글 조회)
def detail(request, pk):
    # pk로 들어온 정수 값을 활용 해 DB에 id(pk)가 pk인 게시글을 조회 요청 
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


# 게시글을 작성하기 위한 페이지를 제공하는 함수
def new(request):
    form = ArticleForm()
    context = {
        'form' : form,
    }
    return render(request, 'articles/new.html',context)


# 사용자로부터 데이터를 받아 저장하고 저장이 완료되었다는 페이지를 제공하는 함수
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
    form = ArticleForm(request.POST)  # 사용자로부터 받은 데이터를 인자 통으로 넣어서 form instanse 생성성 

    # 데이터가 유효한지 검사하기 
    if form.is_valid():  # is로 시작하는 메서드는 반환값이 참거짓 
        # 유효성 검사를 통과하면
        article = form.save()  # 통과했으니 저장 (여기서 저장하는게 방금 생성된 글인거임), 반환값이 있기에 article로 이름지어서 줄 수 있음음
        return redirect('articles:detail', article.pk)  # 작성 후 제출시 해당 작성글로 링크가 이동되게 하는 코드 

    # 유효성 검사를 통과하지 못했다면, 뭐 떄문인지 is_vaild에 의해 메시지를 받을 수 있음 
    # 현재 사용자가  게시글을 작성하는 템플릿(현재 작성하던 페이지)를 다시 보여줌
    context = {
        # 왜 유효성 검사를 통과하지 못했는지에 대한 에러메시지를 담고 있음
        'form' : form,
    }
    # 여기서 is_valid(),save()를 쓸 수 있는 이유는 ModelForm 클래스를 사용하기 때문 

    return render(request, 'articles/new.html', context)



def delete(request, pk):
    # 어떤 게시글을 지우는지 먼저 조회
    article = Article.objects.get(pk=pk)
    # DB에 삭제 요청
    article.delete()
    return redirect('articles:index')


def edit(request, pk):
## 기존 코드
    # 몇번 게시글 정보를 보여줄지 조회
    # article = Article.objects.get(pk=pk)
    # context = {
    #     'article': article,
    # }
    # return render(request, 'articles/edit.html', context)

## modelForm 코드
    article = Article.objects.get(pk=pk)
    form = ArticleForm()
    conte


def update(request, pk):
    # 어떤 글을 수정하는지 먼저 조회
    article = Article.objects.get(pk=pk)
    # 사용자 입력 데이터를 기존 인스턴스 변수에 새로 갱신 후 저장
    article.title = request.POST.get('title')
    article.content = request.POST.get('content')
    article.save()
    return redirect('articles:detail', article.pk)
