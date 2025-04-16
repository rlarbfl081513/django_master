# ✅ URL에서 pk, user_pk, comment_pk 등 파라미터 정리와 사용 흐름

### ❓ 사용자 질문:
> 나는 아직도 urls에서 쓰는 pk, user_pk가 뭔지, 뷰에서도 그걸 가져와서 쓰고,
> 그리고 a태그에서도 url이랑 같이 부르고, 그런데 이제 n:m이 되니까 그게 훨씬 많아져서 막 헷갈려.
> 어떻게 해야 할까?

---

### ✅ 용어 정리: pk, user_pk, comment_pk의 의미

- **pk**: primary key, 즉 기본 키. 보통 모델 인스턴스 하나를 고유하게 식별할 수 있는 값
- **user_pk**: 특정 유저의 pk
- **comment_pk**: 특정 댓글의 pk
- **book_pk**: 특정 도서의 pk

`<int:pk>`, `<int:user_pk>` 같은 건 결국 URL 경로 안에 있는 **동적 매개변수**를 뜻함.

```python
# 예시
path('users/<int:user_pk>/follow/', views.follow)
```
- 위 URL은 특정 유저를 식별할 수 있는 숫자 pk를 전달함
- 이 값은 view 함수에서 `user_pk`라는 이름으로 전달됨

---

### ✅ URL → View → Template 흐름

#### 1. urls.py
```python
path('articles/<int:article_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete')
```

#### 2. views.py
```python
def comment_delete(request, article_pk, comment_pk):
    article = Article.objects.get(pk=article_pk)
    comment = article.comment_set.get(pk=comment_pk)
    comment.delete()
    return redirect('articles:detail', article_pk)
```

#### 3. template.html (a 태그)
```html
<a href="{% url 'articles:comment_delete' article.pk comment.pk %}">삭제</a>
```

→ 이렇게 URL의 구조가 그대로 view 함수 파라미터로 들어가고,  
→ 그 이름을 맞춰줘야 하고,  
→ 템플릿에서도 그 값들을 넘겨주는 구조야.

---

### ✅ N:M 관계에서의 혼란 정리

#### 예시: 유저가 여러 책을 좋아할 수 있고, 책도 여러 유저에게 좋아요 받을 수 있음
```python
# models.py
class User(models.Model):
    ...
    liked_books = models.ManyToManyField('Book', related_name='liked_by')
```

- 이럴 경우 "누가 어떤 책을 좋아했는가"를 명확히 하기 위해 URL에 **두 개의 pk**가 함께 등장함:

```python
path('users/<int:user_pk>/books/<int:book_pk>/like/', views.like_book, name='like_book')
```

→ `user_pk`, `book_pk`처럼 구체적으로 이름을 정해줘야 코드가 헷갈리지 않음

---

### ✅ URL의 pk는 그 자체로는 기능이 없음 (중요 개념)

#### ❓ 사용자 질문:
> 그러면 url파일에서 `path('articles/<int:article_pk>/comments/<int:comment_pk>/delete/', ...)` 이렇게 있을 때는
> 각각의 pk 관련 매개변수들이 그냥 하나의 이름을 가지고 있는 거고 뭔가를 불러올 수 있는 기능은 아예 없다가
> 뷰 함수에 가서 아래처럼 쓰여야지만 그제서야 뭔가를 가리키는 변수인 거지?
> 그리고 그냥 이름일 뿐이니까 사실은 article_pk가 new_pk여도 상관없는 거고?

#### 💡 답변:
완전히 맞는 이해야!

- `<int:article_pk>`는 그 자체로 아무런 기능이 없음
- 단순히 URL 안에 있는 숫자를 `article_pk`라는 이름으로 view 함수에 넘겨주는 것뿐
- 실질적으로 모델에서 데이터를 가져오거나 하는 건 **view 함수 내부**에서 처리됨

```python
# 이 시점에야 비로소 DB에서 실제 객체를 가져옴
article = Article.objects.get(pk=article_pk)
```

- 그리고 이름은 사실 아무거나 써도 동작함:
```python
path('articles/<int:new_pk>/comments/<int:another_pk>/delete/', views.comment_delete)

def comment_delete(request, new_pk, another_pk):
    article = Article.objects.get(pk=new_pk)
    comment = article.comment_set.get(pk=another_pk)
```
- 하지만 협업이나 유지보수할 때 의미가 드러나는 이름이 훨씬 좋기 때문에 `article_pk`, `user_pk` 등을 사용하는 것

---

### ✅ 꼭 URL에서 모든 pk를 받을 필요는 없음

#### ❓ 사용자 질문:
> 그럼 url에서 꼭 pk를 여러 개 부르지 않고도 그냥 뷰 함수에서 여러 개 불러서 할 수도 있는 거야??
> 왜냐하면 url에서 쓰는 건 그냥 나중에 구현 시 url 링크에 어떻게 나오게 될지의 외관에 관한 거니까

#### 💡 답변:
맞아, URL에 pk를 꼭 다 적지 않아도 돼! 중요한 건 **view 함수에서 필요한 데이터를 어떻게 가져오느냐**야.

예를 들어:
```python
# urls.py
path('comments/delete/', views.comment_delete, name='comment_delete')

# views.py
def comment_delete(request):
    article_id = request.GET.get('article_id')
    comment_id = request.GET.get('comment_id')
    article = Article.objects.get(pk=article_id)
    comment = article.comment_set.get(pk=comment_id)
    ...
```
- 위처럼 URL에 `article_pk`나 `comment_pk`를 직접 포함하지 않아도,  
  쿼리스트링이나 `POST` 데이터에서 받아서 처리할 수도 있어

---

### ✅ request.GET.get()으로 값을 가져오는 원리

```python
article_id = request.GET.get('article_id')
```
이렇게 작성하면, 다음과 같은 URL에서:
```
/comments/delete/?article_id=3&comment_id=7
```
- `request.GET`은 `QueryDict`라는 딕셔너리 비슷한 객체
- `.get('article_id')`는 `'3'`이라는 값을 반환함 (문자열)
- 이 값을 사용해서 `Article.objects.get(pk=article_id)`처럼 모델을 조회할 수 있음

### 관련 방식 요약
| 상황 | 메서드 | 설명 |
|------|--------|------|
| 쿼리스트링(GET)에서 값 추출 | `request.GET.get('key')` | URL 뒤의 `?key=value` 형식에서 값 추출 |
| POST 요청에서 값 추출 | `request.POST.get('key')` | 폼에서 전송된 데이터 추출 |
| 파일 업로드 추출 | `request.FILES['key']` | 업로드된 파일 객체 추출 |

---

하지만 실무에서는 **직관적이고 RESTful한 URL 구조**를 위해 보통 pk를 URL에 명시적으로 포함시켜 줘.
- 예: `/articles/3/comments/5/delete/` → 이 URL만 봐도 무슨 동작인지 명확함
- 그리고 템플릿에서 `href`로 넘기기도 편하고 유지보수도 쉬움

따라서 꼭 필수는 아니지만, 명확한 표현과 구조화를 위해 URL에 pk를 여러 개 쓰는 게 일반적인 패턴이야.

---

### ✅ 헷갈리지 않으려면?

1. **pk는 항상 '무엇의 pk인지' 명확하게 이름 붙이기**
   - `pk`보다는 `user_pk`, `book_pk`, `comment_pk`처럼 명시적으로 쓰기

2. **URL, view, 템플릿의 변수 이름을 항상 일치시키기**
   - 예: `article_pk`라고 적었으면 세 군데 다 똑같이 `article_pk`로 사용

3. **관계가 2개 이상 얽히면 URL도 계층적으로 구성**
   - 예: `articles/<int:article_pk>/comments/<int:comment_pk>/delete/`

4. **처리 흐름을 종이에 그려보거나 시각화해서 정리**
   - 특히 N:M에서는 누가 누구와 연결되는지를 화살표로 그려보면 이해가 쉬움

---

### ✅ 결론
- URL에서 pk류 파라미터는 객체를 정확히 식별하기 위한 것
- 그 자체로는 아무 동작도 하지 않으며, view 함수에서 사용될 때 의미를 가짐
- 꼭 URL에 모든 pk를 명시하지 않아도 되지만, 명확한 설계와 유지보수를 위해 포함시키는 경우가 많음
- 템플릿, 뷰, URL 이름이 항상 일치하도록 관리하면 훨씬 덜 헷갈림

