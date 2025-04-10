# 🔁 Django의 요청과 응답 흐름: `request`와 `render`

이 문서는 Django의 기본 처리 흐름인 **요청(request)과 응답(response)** 구조에 대해 정리한 내용입니다.  
특히 `request`, `GET`, `render`, `context`에 대한 개념을 실제 코드 주석과 함께 살펴봅니다.

---

## 🧠 1. 요청 객체 `request`

Django의 view 함수는 항상 첫 번째 인자로 `request` 객체를 받습니다.

```python
def index(request):
    ...
```

### ✅ request란?

- 사용자가 브라우저에서 요청한 모든 정보가 담긴 객체
- 타입: `WSGIRequest`
- 안에 다양한 정보가 있음: `method`, `path`, `GET`, `POST`, `FILES` 등

### 🔍 실습 예시

```python
query = request.GET.get('query')
print(request)            # <WSGIRequest: GET '/articls/?query=ssafy'>
print(type(request))      # <class 'django.core.handlers.wsgi.WSGIRequest'>
print(request.GET)        # <QueryDict: {'query': ['ssafy']}>
print(request.GET.get('query'))  # ssafy
```

---

## 🖨️ 2. 응답 함수 `render()`

```python
return render(request, 'articles/index.html', context)
```

### ✅ render의 역할

| 인자 | 설명 |
|------|------|
| `request` | 사용자 요청 정보가 담긴 객체 |
| `template_name` | 렌더링할 HTML 템플릿 경로 |
| `context` | 템플릿에서 사용할 데이터 딕셔너리 |

📌 HTML과 데이터를 결합해서 최종적으로 사용자에게 보여주는 HTML 파일을 완성함.

---

## 🧾 3. context란?

```python
context = {
    'query': query,
    'foods': ['국밥', '카레'],
    'picked': '국밥',
}
```

- `context`는 템플릿에서 사용할 변수들을 key-value 형태로 전달하는 딕셔너리
- 템플릿에서는 `{{ query }}`, `{{ picked }}`처럼 사용 가능

---

## 💡 전체 흐름 요약

```
[브라우저 요청] → URL → View 함수 실행(request 처리) 
→ render(HTML 템플릿 + context 딕셔너리) 
→ 응답 HTML 반환 → 브라우저에 출력
```

---

## 🔍 실습 예제 모음

### 1. index(request)

```python
def index(request):
    query = request.GET.get('query')
    context = {'query': query}
    return render(request, 'articls/index.html', context)
```

---

### 2. dinner(request)

```python
def dinner(request):
    foods = ['국밥','국수','카레','탕수육']
    picked = random.choice(foods)
    
    goods = {
        '한식' : ['밥','국','김치'],
        '양식' : ['스테이크','스파게티','리조토'],
        '중식' : ['탕수육','자장면','마라탕'],
        '일식' : ['오사카','도쿄','초밥'],
    }
    goods_pick = random.choice(list(goods.keys()))
    pickes_good = goods[goods_pick]
    
    context = {
        'foods' : foods,
        'picked' : picked,
        'goods_pick' : goods_pick,
        'pickes_good' : pickes_good,
    }
    
    return render(request, 'articls/dinner.html', context)
```

---

### 3. search(request)

```python
def search(request):
    return render(request, 'articls/search.html')
```

---

### 4. detail(request, num)

```python
def detail(request, num):
    context = {
        'num' : num,
    }
    return render(request, 'articls/detail.html', context)
```

---

## ✅ 정리

| 개념 | 설명 |
|------|------|
| `request` | 요청 정보를 담은 객체 |
| `request.GET.get()` | 쿼리스트링에서 데이터 추출 |
| `context` | 템플릿에서 사용할 데이터를 담은 딕셔너리 |
| `render()` | HTML 템플릿과 데이터를 합쳐 응답 생성 |

전체 흐름: 사용자 → URL → view → render(template + context)
