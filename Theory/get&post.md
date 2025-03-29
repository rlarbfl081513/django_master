**GET 방식과 POST 방식의 차이**

## 목표
사용자가 이름을 입력하고 제출하면,  
- `GET 방식`: 이름이 URL에 보이고
- `POST 방식`: 이름이 URL에 안 보인다

---
## GET vs POST 비교표

| 항목                 | GET 방식                                      | POST 방식                                      |
|----------------------|-----------------------------------------------|------------------------------------------------|
| 전송 방식            | URL 뒤에 붙여서 보냄 (`?key=value`)           | HTTP 메시지 body에 담아서 보냄 (숨김)          |
| 주소창에 보임?       | 보임 (`/search?query=고양이`)                 | 안 보임                                        |
| 용도                 | 주로 조회용 (검색, 필터 등)                  | 주로 저장/전송용 (회원가입, 로그인 등)         |
| 재요청 시 영향       | 그대로 다시 요청됨                           | 서버 상태 바뀔 수 있음 (주의 필요)             |
| Django에서 받기      | `request.GET.get('key')`                      | `request.POST.get('key')`                      |
---
## 1. Django 뷰 코드 (`views.py`)

```python
from django.shortcuts import render

def input_get(request):
    name = request.GET.get('name')  # GET 방식으로 받기
    return render(request, 'input_get.html', {'name': name})

def input_post(request):
    name = None
    if request.method == 'POST':
        name = request.POST.get('name')  # POST 방식으로 받기
    return render(request, 'input_post.html', {'name': name})
```

---

## 2. GET 방식 템플릿 (`input_get.html`)

```html
<h2>GET 방식 예제</h2>

<form method="get" action="/input-get/">
  <input type="text" name="name" placeholder="이름 입력">
  <input type="submit" value="제출">
</form>

{% if name %}
  <p>안녕하세요, {{ name }}님!</p>
{% endif %}
```

### URL 결과 예시:
```
http://127.0.0.1:8000/input-get/?name=규리
```

---

## 3. POST 방식 템플릿 (`input_post.html`)

```html
<h2>POST 방식 예제</h2>

<form method="post" action="/input-post/">
  {% csrf_token %}
  <input type="text" name="name" placeholder="이름 입력">
  <input type="submit" value="제출">
</form>

{% if name %}
  <p>안녕하세요, {{ name }}님!</p>
{% endif %}
```

- **중요**: `POST` 방식에는 꼭 `{% csrf_token %}` 넣어줘야 함 (보안용)

---

## 4. `urls.py` 등록

```python
from django.urls import path
from . import views

urlpatterns = [
    path('input-get/', views.input_get),
    path('input-post/', views.input_post),
]
```

---

## 실행해보면:

| 입력 방식 | 주소창 URL | 보안성 | 사용자 입장에서 |
|-----------|------------|--------|------------------|
| GET       | `/input-get/?name=홍길동` | 낮음 | 주소창에 다 보임 |
| POST      | `/input-post/`            | 높음 | 값은 안 보임      |
