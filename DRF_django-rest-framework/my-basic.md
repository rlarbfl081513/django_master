# ✅ Django REST Framework - Serializer 기초 정리

### Serializer란?
> Django 모델 데이터를 **JSON 형태로 변환해주는 도구**

- 마치 Django의 `forms.py`가 HTML 폼과 모델 사이의 다리 역할을 하듯,
- DRF의 `serializers.py`는 **모델 ↔ JSON** 사이의 변환을 도와줌

### 왜 필요할까?
- DRF는 API를 만들기 위한 도구이기 때문에, **JSON 데이터를 주고받는 게 기본**
- HTML을 렌더링하던 기존 Django와 달리, 여기선 **프론트엔드/앱에 JSON 응답**이 필요함
- 그래서 **모델 데이터를 JSON으로 바꾸는 시리얼라이저가 반드시 필요함**

---

### 기존 Django와의 비교
| 기능 | Django 방식 | DRF 방식 |
|------|--------------|----------|
| 데이터 응답 | render() + HTML 템플릿 | Response() + JSON |
| 폼과 모델 연결 | forms.py | serializers.py |
| HTML 반환 | 템플릿 사용 | ❌ 없음 |
| JSON 반환 | ❌ 직접 만들어야 함 | ✅ 자동 변환 지원 |

---

### 예제 코드 설명
```python
from .models import Article
from .serializers import ArticleListSerializer
from rest_framework.response import Response

def article_list(request):
    articles = Article.objects.all()  # ✅ 전체 게시글 조회 (QuerySet)

    #시리얼라이저로 QuerySet → JSON 데이터로 변환
    serializer = ArticleListSerializer(articles, many=True)
    
    # 변환된 JSON 데이터를 Response로 응답
    return Response(serializer.data)
```

#### 🔍 핵심 설명
- `Article.objects.all()` → 게시글 전체 데이터를 불러옴 (QuerySet)
- `ArticleListSerializer(articles, many=True)` → 여러 개 데이터를 시리얼라이저로 변환
- `Response(serializer.data)` → 변환된 JSON 데이터를 브라우저나 앱에 응답

---

### 시리얼라이저 역할 시각화
```python
# 모델 데이터
[<Article: 글1>, <Article: 글2>]

# 시리얼라이저 변환 결과
[
  {"id": 1, "title": "글1", "content": "내용1"},
  {"id": 2, "title": "글2", "content": "내용2"}
]
```

---

### 결론
- `serializers.py`는 모델 데이터를 API 응답용으로 가공하는 중요한 도구
- DRF에서는 View에서 모델 데이터를 불러오고 → 시리얼라이저로 변환한 후 → Response로 응답함
- 지금 배우는 이 흐름이 **모든 DRF의 기초가 되는 구조**이므로 꼭 익혀두자 💪

---
# ✅ DRF ModelSerializer 개념 및 사용 정리

### ModelForm과 ModelSerializer의 비교

| 구분 | Django ModelForm | DRF ModelSerializer |
|------|------------------|---------------------|
| 목적 | HTML 폼 ↔ 모델 변환 | JSON ↔ 모델 변환 |
| 기반 모듈 | `from django import forms` | `from rest_framework import serializers` |
| 사용하는 클래스 | `forms.ModelForm` | `serializers.ModelSerializer` |
| 검증 | `form.is_valid()` | `serializer.is_valid()` |
| 저장 | `form.save()` | `serializer.save()` |
| 응답 형식 | HTML 렌더링 | JSON 응답 |

---

### 예시 코드 설명

#### 1. 일부 필드만 변환 (목록용)
```python
from rest_framework import serializers
from .models import Article

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content')
```
- `Article.objects.all()` 등의 결과를 JSON으로 바꿔줄 때 사용
- 목록 화면 등에 필요한 일부 필드만 포함시킬 수 있음

#### 2. 전체 필드 변환 (상세/생성용)
```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
```
- 모델의 모든 필드를 JSON으로 변환하거나, JSON을 받아 모델 객체로 만들 때 사용
- 주로 상세 조회, 생성, 수정에 활용

---

### 왜 두 개를 따로 만들까?

#### ❓ 사용자 질문:
> 그런데 굳이 목록용, 상세용으로 두 개의 serializer 관련 클래스를 따로 만들지 않고,
> 그냥 HTML에서 보여줄 때 목록에서는 article.title만 보여주고,
> 상세에서는 article.title, article.content, article.author 이렇게 해도 되지 않아??
> ModelForm으로 HTML에 출력할 때는 이런 식으로 했던 것 같은데

#### 💡 상세 설명:
질문한 내용처럼, **기존 Django에서는 뷰에서 템플릿에 객체를 넘겨주고, HTML 안에서 보여줄 필드를 선택**해서 출력했었어. 예를 들어 아래처럼:

```html
<!-- 목록 페이지 -->
{{ article.title }}

<!-- 상세 페이지 -->
{{ article.title }}
{{ article.content }}
{{ article.author }}
```

하지만 **DRF에서는 JSON 데이터 자체가 응답 본문**이기 때문에,
어떤 필드가 들어갈지 템플릿이 아니라 **시리얼라이저에서 정확히 지정해줘야 해.**

즉, 템플릿이 "보여줄 데이터만 선택"하던 것과는 다르게,
DRF에서는 "**응답 자체를 구성하는 설계**"가 필요하기 때문에 시리얼라이저 구분이 중요한 거야.

---

### DRF에서 시리얼라이저를 구분해서 쓰는 이유

1. **DRF는 HTML을 렌더링하지 않고, JSON을 바로 반환함**
   - 템플릿이 없으므로 어떤 필드를 포함할지 직접 지정해줘야 함

2. **목록 페이지에서는 요약 정보만 필요함**
   - 예: 게시글 제목만 보여주고, 작성자나 본문 내용은 불필요

3. **상세 페이지에서는 모든 정보가 필요함**
   - 예: 게시글 내용, 작성일, 작성자 등 포함해야 함

4. **시리얼라이저에서 포함할 필드를 다르게 설정해야만, 목적에 맞는 JSON 응답을 줄 수 있음**
   - 하나의 시리얼라이저로 처리하면 필드가 너무 많거나, 불필요한 데이터가 전송될 수 있음

5. **실무에서는 보안과 효율성 측면에서도 필요함**
   - 예를 들어 목록 API에서 작성자 이메일이 포함되면 안 되는 경우 등

---

### 결론
- `ModelSerializer`는 DRF에서 폼 대신 사용하는 핵심 클래스
- 사용하는 방식도 Django의 `ModelForm`과 매우 유사함
- DRF는 템플릿 기반이 아닌 JSON 응답 기반이기 때문에, **시리얼라이저에서 포함할 필드를 명확히 지정해야 함**
- 그 결과, 목록/상세 등 **용도에 맞춰 시리얼라이저를 따로 구성하는 것이 DRF의 기본 설계 방식**임

