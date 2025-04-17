# 🧩 DRF `SerializerMethodField` 완전 정리

## ✅ 개념 요약

`SerializerMethodField`는 Django REST Framework에서 **모델에 존재하지 않는 필드 값을 커스터마이징해서 응답에 추가할 때** 사용하는 필드다.

> 반드시 `annotate`와 함께 쓰는 건 아니며, 단독으로 사용 가능하다.

---

## 🔍 언제 사용하나?

### 1. 기존에 있는 데이터를 가공해서, 새로운 값을 만들어 응답에 추가할 때 쓰는 거야.
- DB에는 ‘원자료’(예: 각 과목 점수)만 있지만,
우리가 출력할 땐 '가공된 요약 정보'(예: 평균점수) 도 보여주고 싶은 거잖아?
그때 SerializerMethodField가 딱 그 역할을 해주는 거야.

### 2. 응답에 계산된 값을 넣고 싶을 때
- 예: 댓글 개수, 좋아요 여부, 작성자 본인 여부 등

### 3. 모델에 존재하지 않는 값이지만, 응답에는 필요할 때
- 예: `is_mine`, `days_since_created`, `liked_by_user`, `is_following`, `preview_content`

---

## ✅ annotate 없이 사용하는 경우

### 예시: 댓글 개수를 보여주는 커스텀 필드
```python
class ArticleSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'comment_count')

    def get_comment_count(self, obj):
        return obj.comments.count()  # related_name='comments' 기준
```

- `obj`는 현재 직렬화되고 있는 Article 인스턴스
- `.comments`는 Comment 모델에서 지정한 related_name
- `count()`는 단순히 역참조 관계에서 댓글 수를 ORM으로 계산

**즉, DB에서 따로 annotate 안 해도 됨!**

---

## ✅ annotate와 함께 사용하는 경우

### 예시: DB에서 미리 계산해온 값을 응답에 활용
```python
from django.db.models import Count

# 뷰에서 annotate 사용
articles = Article.objects.annotate(comment_count=Count('comments'))
serializer = ArticleSerializer(articles, many=True)
```

```python
class ArticleSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'comment_count')

    def get_comment_count(self, obj):
        return obj.comment_count  # annotate로 생성된 속성 그대로 활용
```

이 방식은 **쿼리 효율이 훨씬 좋다.**  
(특히 리스트에서 `.count()`를 루프 돌며 여러 번 부르면 성능 안 좋아짐)

---

## 🔄 두 방식 비교

| 항목 | ORM 직접 접근 | annotate 사용 |
|------|----------------|----------------|
| 코드 | `obj.comments.count()` | `obj.comment_count` |
| 쿼리 효율 | 중복 쿼리 가능성 있음 (N+1 문제) | 단일 쿼리로 계산 완료 |
| 장점 | 구현 간단, 추가 코드 없음 | 대량 처리에 적합, 성능 우수 |
| 단점 | 성능 비효율 가능 | 뷰에서 annotate 추가 필요 |

---

## ✅ 정리

| 방식 | annotate 필요? | 설명 |
|------|----------------|------|
| `SerializerMethodField()` 단독 | ❌ | 응답에 커스텀 값 추가할 수 있음 |
| annotate + `SerializerMethodField()` | ✅ 선택 | 미리 계산된 값으로 효율 높임 |

> **핵심 포인트**: `SerializerMethodField`는 annotate 없이도 충분히 유용하며, annotate는 성능 최적화용 도구일 뿐이다.

---

## ✅ 추가 팁: 사용 흐름

```plaintext
[단일 조회] → obj.comments.count() 로도 충분함
[리스트 조회 + 성능 고민] → annotate(comment_count=Count('comments')) 추천
```

---

필요하면 실제 프로젝트 구조나 성능 개선 전략과 함께 더 확장해줄 수 있음!

