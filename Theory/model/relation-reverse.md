# 🔗 ForeignKey와 모델 간 관계

Django에서 모델 간의 관계를 설정할 때 가장 자주 쓰는 것이 `ForeignKey`다. 이는 **1:N 관계(다대일)** 를 표현할 때 사용된다.

### ✅ 기본 예시

```python
# models.py
class Article(models.Model):
    title = models.CharField(max_length=100)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
```

- `Comment` 모델에서 `Article` 모델을 참조한다. → 이를 **정참조(Forward Reference)** 라고 한다.
- 한 개의 `Article`에는 여러 개의 `Comment`가 연결될 수 있다.

## 🔁 역참조 (Reverse Relationship)

ForeignKey 관계가 설정되면, 참조된 모델(여기선 `Article`)에서 자동으로 역참조가 가능해진다. Django는 기본적으로 `모델명_set` 형식의 Related Manager를 생성한다.

### 🔄 정참조 vs 역참조
- **정참조 (Forward Reference)**: `Comment`에서 `Article`을 참조 → `comment.article`
- **역참조 (Reverse Reference)**: `Article`에서 연결된 `Comment`들을 가져옴 → `article.comment_set.all()`

즉, `comments = article.comment_set.all()` 이 코드가 바로 **역참조**이다.

### ✅ 기본 역참조 예시

```python
article = Article.objects.get(id=1)
comments = article.comment_set.all()
```

- `comment_set`은 `Comment` 모델 이름 + `_set`으로 자동 생성됨.
- 위 코드는 해당 `article`에 연결된 모든 댓글을 가져오는 예시.

## 🛠 related_name으로 이름 바꾸기

`ForeignKey` 필드에 `related_name` 옵션을 설정하면 역참조할 때 사용할 이름을 커스터마이징할 수 있다.

```python
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
```

이제는 아래와 같이 사용할 수 있다:

```python
article = Article.objects.get(id=1)
comments = article.comments.all()
```

→ 가독성이 훨씬 좋아지고, `comment_set` 대신 원하는 이름으로 사용할 수 있음.

## 🔍 요약

| 개념 | 설명 |
|------|------|
| `ForeignKey` | 다른 모델과 1:N 관계 설정 (정참조) |
| `comment_set.all()` | 기본 역참조 방식 (모델명 + `_set`) |
| `related_name='comments'` | 역참조 이름 커스터마이징 |
| 정참조 | 자식 모델에서 부모 모델로 접근 (`comment.article`) |
| 역참조 | 부모 모델에서 자식 모델 목록을 접근 (`article.comment_set.all()`) |

---

실무에서는 `related_name`을 적극 활용해 가독성 좋은 코드를 작성하는 것이 중요하다.

