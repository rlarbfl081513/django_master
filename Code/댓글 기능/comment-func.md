# 💬 Django 댓글 작성자 저장 기능 정리

## ✅ 목표
- 댓글 작성 시 로그인된 사용자의 **username**을 댓글과 함께 저장하고,
- 로그아웃 후에도 **누가 쓴 댓글인지** 볼 수 있도록 구현한다.

---

## 1. 모델 수정
`Comment` 모델에 작성자 정보를 저장할 수 있는 필드를 추가한다.

```python
# models.py
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    author_name = models.CharField(max_length=100, default='익명')  # 작성자 이름 저장용
```

> 🔍 `default='익명'`을 지정하면 기존 데이터 마이그레이션 시 오류를 방지할 수 있다.

---

## 2. 뷰(View) 수정
댓글 작성 시 로그인된 사용자 이름을 함께 저장한다.

```python
# views.py
@login_required
def comments_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author_name = request.user.username  # 로그인한 사용자 이름 저장
            comment.save()
            return redirect('articles:detail', article_pk)
    else:
        form = CommentForm()
    return render(request, 'articles/detail.html', {'form': form})
```

---

## 3. 템플릿 출력
댓글 작성자 이름을 화면에 보여준다.

```html
{% for comment in article.comment_set.all %}
  <p><strong>{{ comment.author_name }}</strong>: {{ comment.content }}</p>
{% endfor %}
```

---

## 🔁 마이그레이션 시 주의사항
새 필드(`author_name`)를 추가하면 아래와 같은 메시지가 나올 수 있다:

```
It is impossible to add a non-nullable field 'author_name' to comment without specifying a default.
```

이 경우 **두 가지 방법 중 하나를 선택**:

1. **1번**: 즉석에서 기본값 입력 → 기존 댓글에 일괄 적용됨.
2. ✅ **2번**: `models.py`에 `default='익명'` 지정 후 다시 `makemigrations` 진행.

---

## 📝 정리
| 항목 | 설명 |
|------|------|
| 저장 필드 | `author_name` (`CharField`) |
| 저장 방식 | `request.user.username`을 뷰에서 저장 |
| 출력 위치 | 템플릿에서 `{{ comment.author_name }}` |
| 마이그레이션 | 기본값 설정 필요 (`default=` 사용) |

→ 이렇게 하면 로그아웃 후에도 댓글 작성자가 누구인지 알 수 있게 된다!

---
<br><br>
# 🧾 댓글 생성 뷰 함수 상세 설명

```python
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
```

---

## 🔍 `commit=False`가 중요한 이유
- `form.save(commit=False)`를 사용하면 **폼에서 생성된 객체를 DB에 저장하지 않고 먼저 가져올 수 있음**
- 그 상태에서 추가적으로 필드를 채워 넣은 뒤, `.save()`로 저장함

### 예시
```python
comment = comment_form.save(commit=False)  # DB에 저장은 아직 X
comment.article = article  # ForeignKey 설정
comment.author_name = request.user.username  # 사용자 정보 설정
comment.save()  # 이제야 진짜 DB에 저장됨
```

> 📌 `commit=False`를 안 쓰면, 아직 채워지지 않은 필드들 때문에 저장 오류가 날 수 있음 (예: article이 아직 안 채워짐)

---

## ✅ 정리표
| 단계 | 내용 |
|------|------|
| 1 | URL의 pk로 게시글(article) 가져오기 |
| 2 | POST 데이터로 댓글 폼 생성 |
| 3 | 폼 유효성 검사 |
| 4 | `form.save(commit=False)`로 DB 저장 지연 |
| 5 | article, author_name 직접 지정 |
| 6 | `comment.save()`로 최종 저장 |
| 7 | 댓글 작성 후 해당 게시글 상세 페이지로 이동 |


