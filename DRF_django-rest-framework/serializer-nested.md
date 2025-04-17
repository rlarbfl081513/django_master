# 🤩 DRF 중차 Serializer(Nested Serializer)

## ✅ 목적
ForeignKey로 연결된 목록의 **자세한 정보를 응답에 포함**시키고 싶을 때 사용.

예를 들어, `Comment` 목록이 `Article`을 참조하고 있을 때:
- 기본 Serializer는 `article` 필드를 ID 값으로만 응답함
- → 게시글 제목 같은 정보도 보여주고 싶으면 **중차 Serializer** 사용

---

## 🔁 기본 ForeignKey 응답 예시

```json
{
  "id": 1,
  "content": "댓글 내용",
  "article": 3
}
```

---

## 🤩 중차 Serializer 적용 예시

```python
class ArticleTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title')

class CommentSerializer(serializers.ModelSerializer):
    article = ArticleTitleSerializer(read_only=True)  # 읽기전용으로 해서 입력은 받지 않도록

    class Meta:
        model = Comment
        fields = '__all__'
```

### 응답 예시
```json
{
  "id": 1,
  "content": "댓글 내용",
  "article": {
    "id": 3,
    "title": "게시글 제목"
  }
}
```

---

## 📅 `read_only=True`가 필요한 이유

- `fields = '__all__'`로 했는데 `article`을 중차 Serializer로 결정해 보여주면
  DRF가 그 필드에 대해 “입력”도 받으려고 함.
- 그러면 입력시 오류가 발생할 수 있게 되기 때문에,
  `article` 필드는 **read_only=True** 로 해서 입력을 비하고 응답에만 포함되게 해야 해.

---

## 포인트 정리

| 기능 | 설명 |
|--------|--------|
| ForeignKey 필드 기본 응답 | ID(정수) 만 포함 |
| 중첩 Serializer 사용 시 | 연결된 모델의 상세 필드 포함 가능 (예: 제목) |
| 입력값 유효성 검사 회피 | `read_only=True` 설정 필수 |
| `Meta.read_only_fields` | 중첩 serializer에는 잘 작동안 함 → 직접 `read_only=True` 처리 필요 |

---

## 파일 복사 체인
❌ `read_only_fields = ('article',)`
- Meta 내에서 설정해도 → 중차 serializer에는 적용이 안 됨
- → 필드에서 `read_only=True` 바로 적용해야 함

---

🚀 이 설정은 `drf-crud` 폴더에 다른 CRUD 여러 예제가 들어가는 것과 같이 꼭 하나보다는 “함수적 패턴”을 설명해준 것이기 때문에 다운콤히 다룰 수 있어.

