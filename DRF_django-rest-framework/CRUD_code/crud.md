## ✅ DRF에서 Serializer로 구현하는 CRUD 흐름 정리

---

## ✅ 1. Create - 생성

### serializer = ArtistsSerializer(data=request.data)의 의미

```python
serializer = ArtistsSerializer(data=request.data)
```

이 한 줄은 DRF에서 **Create 작업의 핵심**이야.

#### 🔍 이 코드의 역할:
- `ArtistsSerializer`는 DRF에서 만든 **ModelSerializer 클래스**
- `request.data`는 클라이언트가 보낸 **JSON 형식의 요청 본문 데이터**
- `data=...`를 인자로 넘겨서 **직렬화 인스턴스를 만든다**

#### ✅ 해석:
> 사용자가 JSON으로 보낸 데이터를 받아서, Artists 모델 기준으로 검증하고 저장할 준비를 해라.

### 전체 흐름 (POST 기반 Create 예시)
```python
@api_view(['POST'])
def artists_create(request):
    # POST 요청으로 들어오면
    serializer = ArtistsSerializer(data=request.data)  # 사용자 데이터로 시리얼라이저 인스턴스 생성

    if serializer.is_valid(raise_exception=True):  # 유효성 검사 + 자동 에러 응답
        serializer.save()  # DB에 저장 (create 로직 수행)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

#### 각 단계 설명
| 단계 | 설명 |
|------|------|
| 시리얼라이저 생성 | `serializer = ArtistsSerializer(data=request.data)`<br>→ 요청으로 받은 JSON을 기반으로 데이터 준비 |
| 유효성 검사 | `serializer.is_valid()`<br>→ 필수 필드, 값 형식 등을 자동으로 체크함 |
| 저장 | `serializer.save()`<br>→ 유효하다면 `.save()`가 모델 인스턴스를 생성해서 DB에 저장 |
| 응답 반환 | `Response(serializer.data)`<br>→ 저장된 모델 데이터를 JSON으로 직렬화해서 클라이언트에게 응답 |

### request.data는 무엇인가?
- `request.data`는 DRF가 제공하는 기능으로, 클라이언트가 보낸 **POST, PUT, PATCH 등의 요청 본문(body)**에서
  **자동으로 JSON 파싱해서 딕셔너리 형태로 변환한 값**을 의미해.
- 예를 들어, 사용자가 아래와 같은 JSON을 보냈다면:
  ```json
  {
    "name": "BTS",
    "debut_year": 2013
  }
  ```
  → `request.data`는 아래처럼 딕셔너리로 변환돼서 접근 가능해:
  ```python
  {'name': 'BTS', 'debut_year': 2013}
  ```

---

## ✅ 2. Read - 조회 (목록 및 상세)

### 전체 목록 조회 기능: artists_list
```python
@api_view(['GET'])    
def artists_list(request):
    # 요청이 GET일 때
    if request.method == 'GET':
        # Artists 모델의 모든 데이터를 가져옴 (QuerySet)
        artist = Artists.objects.all()

        # 가져온 데이터를 JSON으로 변환할 준비
        # many=True 옵션은 여러 개의 객체를 직렬화할 때 꼭 필요함
        all_info = ArtistsListSerializer(artist, many=True)

        # 직렬화된 JSON 데이터를 클라이언트에게 응답으로 전송
        return Response(all_info.data)
```

#### 💡 추가 설명:
- `Artists.objects.all()`은 데이터베이스에서 모든 artist 레코드를 가져오는 Django ORM 쿼리셋
- `ArtistsListSerializer`는 아마 일부 필드만 보여주는 용도의 시리얼라이저로 추정됨 (예: 리스트 전용)
- `many=True`가 없으면 오류 발생함 (QuerySet은 리스트이기 때문)
- 이 함수는 전체 아티스트 목록을 JSON으로 응답하는 API 엔드포인트 역할을 함

---

### 상세 조회 기능: artists_detail
```python
@api_view(['GET'])    
def artists_detail(request, page_pk):
    artist = Artists.objects.get(pk=page_pk)
    if request.method == 'GET':
        serializer = ArtistsSerializer(artist)
        return Response(serializer.data)
```

#### 💡 추가 설명:
- `page_pk`는 URL에서 전달된 artist의 pk 값
- `Artists.objects.get(pk=page_pk)`는 해당 pk를 가진 artist 하나를 DB에서 조회
- `ArtistsSerializer(artist)`로 해당 인스턴스를 직렬화함 (many=False 기본값)
- `.data`를 통해 JSON 형식으로 변환된 결과를 클라이언트에 응답
- GET 방식에서는 `request.data`를 절대 사용하지 않음 → 입력 데이터가 없기 때문

---

## ✅ 3. Update - 수정

### 아티스트 정보 수정 기능 (PUT 방식 전체 수정)
```python
@api_view(['GET', 'PUT'])
def artists_detail(request, page_pk):
    artist = Artists.objects.get(pk=page_pk)

    if request.method == 'GET':
        serializer = ArtistsSerializer(artist)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # 기존 객체(artist)에 사용자가 보낸 데이터(request.data)를 덮어씌움
        serializer = ArtistsSerializer(artist, data=request.data)

        if serializer.is_valid():
            serializer.save()  # DB에 수정 내용 저장
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Postman에서 수정하는 방법
1. 메서드를 `PUT`으로 변경
2. URL: `http://127.0.0.1:8000/api/v1/detail/2/`
3. Body 탭 선택 → `raw` → JSON 형식으로 설정
4. 전체 필드를 JSON으로 입력:
```json
{
  "name": "New Name",
  "agency": "New Agency",
  "debut_date": "2026-01-01",
  "is_group": true
}
```
5. Send 클릭 → 수정된 데이터가 응답으로 돌아오면 성공!

### 💡 보충 설명
- `PUT`은 기존 객체 전체를 덮어쓰기 때문에, 모든 필드를 보내야 함
- `PATCH`는 일부 필드만 보내도 되며, `partial=True` 옵션이 필요함
- `request.data`는 수정 요청 본문에서 받은 JSON 데이터를 담고 있음
- 수정 시에는 form-data 말고 반드시 `raw → JSON`을 사용해야 함

---

## ✅ 4. Delete - 삭제
(추후 내용 추가 예정)

