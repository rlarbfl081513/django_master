# 🔗 ForeignKey 필드명과 Count() 관계 완전 정리

Django에서 모델 간 관계를 표현할 때 사용하는 **ForeignKey**와,  
`annotate(Count(...))`에서 **왜 특정 이름을 써야 하는지**에 대한 개념을 구체적으로 정리한 문서입니다.

---

## ✅ ForeignKey란?

> 다른 모델(테이블)을 참조하기 위한 Django의 관계 필드

예를 들어, `Review` 모델이 `Book` 모델을 참조한다면:

```python
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
```

- 이때 `book`이 바로 ForeignKey **필드명**입니다.
- 각 Review는 **하나의 Book에 속함** → 1:N 관계

---

## 🧩 역참조란?

Django에서는 ForeignKey를 기준으로 반대 방향으로도 접근 가능해요.  
즉, `Book` 인스턴스에서 자신에게 연결된 `Review`들을 참조할 수 있습니다.

```python
book = Book.objects.get(pk=1)
book.review_set.all()  # ✅ 기본 역참조 이름은 model명 + _set
```

- 여기서 `review_set`은 Django가 자동으로 만들어준 이름입니다.
- 만약 `related_name='reviews'`로 지정했다면 `book.reviews.all()`이 됩니다.

---

## 🧠 그럼 Count()에서 왜 ForeignKey 필드명을 써야 할까?

### 🔍 상황 예시
```python
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
```

이 구조에서 Book 입장에서 **리뷰 수를 세고 싶을 때**:

```python
from django.db.models import Count

Book.objects.annotate(num_of_review=Count('review'))
```

### 🔥 여기서 `'review'`가 뭐냐?
> `Review` 모델 안에서 Book을 가리키는 ForeignKey의 이름 = `book`

Django는 이걸 자동으로 **Book에서 역참조할 때 사용할 이름을 'review'로 매핑**합니다.

즉, `Count('review')`는:
> “Review 모델에서 **book이라는 ForeignKey**를 기준으로
> 나(Book)와 연결된 Review들을 세어줘.” 라는 의미예요.

---

## 🔄 정리: 상황별 이름 비교

| 사용하는 위치 | 써야 할 이름 | 예시 |
|----------------|----------------|-------|
| Python 코드에서 직접 참조 | 역참조 이름 (`review_set`) | `book.review_set.count()` |
| annotate 내부에서 Count | ForeignKey 필드 이름 (`review`) | `Count('review')` |

---

## ✅ 관련 추가 팁: related_name 지정 시

```python
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
```

- 이 경우 Python에서는 `book.reviews.all()`로 접근 가능
- 그러나 annotate에서는 여전히 ForeignKey 필드명을 써야 하므로 `Count('review')`는 그대로 사용합니다!

---

## ✅ 요약 정리

| 개념 | 의미 | 예시 |
|------|------|------|
| ForeignKey 필드명 | 참조하는 필드 이름 | `book = models.ForeignKey(Book)` |
| 역참조 이름 | 기본적으로 model명 + `_set` | `book.review_set.all()` |
| annotate에서 쓰는 이름 | 항상 ForeignKey 필드명 | `Count('review')` |

---

## ✅ 마무리 비유
> 외우기보다 **관계 방향을 이해**하면 좋아요!
- `Review.book` ← ForeignKey 필드명 → annotate에서 사용
- `Book.review_set` ← 역방향 참조 → Python 코드에서 사용

---

필요하면 실제 예제 코드, 쿼리셋 결과 예시도 추가해줄 수 있어요.  
ForeignKey + annotate 잘 이해하면 ORM 마스터에 가까워집니다 💪

