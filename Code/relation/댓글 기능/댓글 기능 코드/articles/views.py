from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ArticleForm, CommentForm
from .models import Article,Comment


def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    # 댓글 폼 불러오기
    comment_form = CommentForm()
    # 작성된 댓글 리스트를 가져오기 
    # comment_set은 장고에서 알아서 만들어주는 거임, 이렇게해서 all하면 댓글 목록 가져와짐 
    comment = article.comment_set.all()
    
    context = {
        'article': article,
        'comment_form' : comment_form,
        'comment' : comment,
    }
    return render(request, 'articles/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


@login_required
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')


@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)

# 댓글 생성 뷰 함수
@login_required
def comments_create(request, pk):
    # ✅ 1. URL에서 받은 pk를 이용해 해당 게시글(article) 객체 가져오기
    article = Article.objects.get(pk=pk)

    # ✅ 2. POST 요청으로 전달된 데이터를 기반으로 댓글 폼 생성
    comment_form = CommentForm(request.POST)

    # ✅ 3. 폼 유효성 검사
    if comment_form.is_valid():
        # ⚠️ form.save(commit=False)는 아직 DB에 저장하지 않고, 객체만 생성함
        # 이걸 통해 추가적인 값을 직접 넣을 수 있음 (ex. article, author_name)
        comment = comment_form.save(commit=False)

        # ✅ 4. 생성된 comment 객체에 게시글 정보 연결
        comment.article = article

        # ✅ 5. 현재 로그인한 사용자의 username을 댓글 작성자로 저장
        comment.author_name = request.user.username

        # ✅ 6. 모든 정보가 다 채워졌으니 이제 DB에 저장
        comment.save()

        # ✅ 7. 댓글 작성 후 해당 게시글 상세 페이지로 리다이렉트
        return redirect('articles:detail', article.pk)

    # ✅ 8. 폼이 유효하지 않은 경우 다시 해당 페이지로 렌더링 (에러 메시지 포함 가능)
    context = {
        'article': article,
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)


# 댓글 삭제 뷰 함수
# 여기서 PK는 게시물의 PK이고, comment_pk는 개별 댓글의 PK야 
def comments_delete(request, pk, comment_pk):
    # 개별의 댓글을 불러오는 코드 
    comment = Comment.objects.get(pk=comment_pk)
    # 그리고 지워 
    comment.delete()
    return redirect('articles:detail', pk)