# 📝 Django 댓글 기능 (디테일 페이지 전용)

## 📌 기능 설명

- 각 게시글(Article)의 상세 페이지(detail.html)에서 댓글을 작성 및 삭제하는 기능
- 로그인한 사용자의 이름을 댓글 작성자로 자동 저장
- 댓글은 게시글과 1:N 관계로 연결

---

## 🧱 모델 정의 (models.py)

```python
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author_name = models.CharField(max_length=100, default='익명')
```

---

## 🧾 폼 정의 (forms.py)

```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
```

---

## 🧠 뷰 함수 (views.py)

### ✅ 댓글 생성

```python
@login_required
def comments_create(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.author_name = request.user.username
        comment.save()
        return redirect('articles:detail', article.pk)
    context = {
        'article': article,
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)
```

### ✅ 댓글 삭제

```python
def comments_delete(request, pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('articles:detail', pk)
```

---

## 🌐 URL 설정 (urls.py)

```python
urlpatterns = [
    ...
    path('<int:pk>/comments/', views.comments_create, name='comments_create'),
    path('<int:pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
]
```

---

## 🧩 템플릿 구현 (detail.html 중 일부)

```html
<h1>comment list</h1>
댓글 개수 : {{ article.comment_set.all|length }}개

{% for item in comment %}
  <p>작성자 ({{ item.author_name }})</p>
  <p>{{ item.content }}</p>
  <form action="{% url 'articles:comments_delete' article.pk item.pk %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="delete">
  </form>
{% endfor %}

<hr>
<form action="{% url 'articles:comments_create' article.pk %}" method="POST">
  {% csrf_token %}
  {{ comment_form }}
  <input type="submit">
</form>
```

---

## 💡 팁

- 댓글 작성자는 로그인한 사용자의 `username`으로 자동 설정됨
- 댓글 작성 및 삭제 후에는 해당 상세 페이지로 리다이렉트 처리
- 댓글 목록은 `article.comment_set.all`을 통해 불러옴


---

# 📝 Django 댓글 기능 (디테일 페이지 전용 - 뷰 함수 중심)

## 📌 기능 설명

- 각 게시글의 상세 페이지에서 댓글을 작성하고 삭제할 수 있음
- 댓글은 게시글(Article)에 연결되며, 로그인한 사용자의 이름으로 저장됨

---

## 🧠 전체 뷰 함수 코드 (views.py)

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import ArticleForm, CommentForm
from .models import Article, Comment

# 게시글 목록
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)

# ✅ 상세 페이지 (댓글 표시 + 댓글 작성 폼 포함)
def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    comment = article.comment_set.all()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comment': comment,
    }
    return render(request, 'articles/detail.html', context)

# ✅ 댓글 생성
@login_required
def comments_create(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.author_name = request.user.username
        comment.save()
        return redirect('articles:detail', article.pk)
    context = {
        'article': article,
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)

# ✅ 댓글 삭제
def comments_delete(request, pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('articles:detail', pk)
```

---

## 💬 요약

- `detail` 함수에서는 댓글 목록과 작성 폼을 함께 전달
- `comments_create`는 댓글 저장 시 `article`과 `author_name`을 수동으로 지정
- 댓글 삭제는 `pk`와 `comment_pk`를 기반으로 삭제 후 디테일 페이지로 리다이렉트
