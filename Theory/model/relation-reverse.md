# Many to one relationship
1. N:1 or 1:N
2. 한 테이블의 0개 이상의 레코드가 다른 테이블의 레코드 한개와 관련된 관계
3. 예시
   1. comment(N) = Article(1) --> 0개 이상의 댓글은 1개의 게시글에 작성될 수 있음 
   2. 테이블 관계도
   ![alt text](image.png)

<br><br>
# 🔗 ForeignKey와 모델 간 관계

Django에서 모델 간의 관계를 설정할 때 가장 자주 쓰는 것이 `ForeignKey`다. 이는 **1:N 관계(다대일)** 를 표현할 때 사용된다.
데이터베이스에서는 외래키로 구현한다. 

### ✅ 기본 예시

```python
# models.py
class Article(models.Model):
    title = models.CharField(max_length=100)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()

# ForeingKey 클래스의 인스턴스 이름은 참조하는 모델 클래스 이름의 단수형으로 작성하는 것을 권장
# 외래키는 foreginKey 클래스를 작성하는 위치와 관계없이 테이블의 마지막 필드로 생성됨 

# ForeignKey(Article, on_delete=models.CASCADE)
# 위의 형태는 ForeignKey(to, on_delete)
  # to는 참조하는 모델 클래스 이름
  # on_delete는 외래키가 참조하는 객체(1)가 사라졌을때, 외래키를 가진 객체(n)을 어떻게 처리할지 정의하는 설정(데이터 무결성)
  # CASCADE는 참조된 객체(부모객체)기 삭제될때 이를 참조하는 모든 객체도 삭제되도록 지정하는 것 
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

