# 🔗 관계(Relation) 기능 예제: 작가 및 책 등록 시스템

## 📌 개요

- `Author(작가)`와 `Book(책)`은 **1:N 관계**
- 작가 상세 페이지에서 책을 등록하는 구조
- `ForeignKey`를 활용하여 관계를 설정함

---

## 🧱 모델 정의 (models.py)

```python
class Author(models.Model):
  name = models.TextField(max_length=50)
  age = models.IntegerField()
  birth = models.DateField()
  nationality = models.TextField()

class Book(models.Model):
  author = models.ForeignKey(Author, on_delete=models.CASCADE)
  title = models.TextField(max_length=100)
  description = models.TextField()
  adult = models.BooleanField()
  price = models.IntegerField()
```

- `Book`은 `Author`에 `ForeignKey`로 연결됨
- `on_delete=models.CASCADE`: 작가 삭제 시 연결된 책도 함께 삭제됨

---

## 🧾 폼 정의 (forms.py)

```python
class AuthorForm(forms.ModelForm):
  class Meta:
    model = Author
    fields = '__all__'

class BookForm(forms.ModelForm):
  class Meta:
    model = Book
    exclude = ['author']
```

- `BookForm`에서는 `author`를 직접 입력하지 않고, 뷰에서 자동 할당

---

## 🧠 뷰 함수 정의 (views.py)

```python
def index(request):
  authors = Author.objects.all()
  context = {
    'authors': authors,
  }
  return render(request, 'libraries/index.html', context)

def detail(request, pk):
  author = Author.objects.get(pk=pk)
  books = author.book_set.all()
  book_form = BookForm()
  context = {
    'author': author,
    'books': books,
    'book_form': book_form,
  }
  return render(request, 'libraries/detail.html', context)

def create(request, pk):
  author = Author.objects.get(pk=pk)
  book_form = BookForm(request.POST)
  if book_form.is_valid():
    book = book_form.save(commit=False)
    book.author = author
    book.save()
  return redirect('libraries:detail', author.pk)
```

---

## 🌐 URL 설정 (urls.py)

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/detail/', views.detail, name='detail'),
    path('<int:pk>/detail/create/', views.create, name='create'),
]
```

---

## 🧩 템플릿 예시

### 📄 index.html

```html
{% for item in authors %}
  <a href="{% url 'libraries:detail' item.pk %}">
    <li>{{ item.name }}</li>
    <li>{{ item.nationality }}</li>
  </a>

  {% for book in item.book_set.all %}
    <li>{{ book.title }}</li>
  {% endfor %}
<hr>
{% endfor %}
```

### 📄 detail.html

```html
<h3>작가에 대한 정보</h3>
<li>{{ author.name }}</li>
<li>{{ author.age }}</li>
<li>{{ author.birth }}</li>
<li>{{ author.nationality }}</li>

<h3>작가의 책에 대한 정보</h3>
{% for book in books %}
  <li>{{ book.title }}</li>
  <li>{{ book.description }}</li>
  <li>{{ book.price }}</li>
  <hr>
{% endfor %}

<h1>신규 등록</h1>
<form action="{% url 'libraries:create' author.pk %}" method='POST'>
  {% csrf_token %}
  {{ book_form.as_p }}
  <input type="submit">
</form>
```

---

## 💡 팁

- 관계 역참조는 `author.book_set.all`처럼 사용 가능
- `book.author = author`는 `ForeignKey` 필드를 뷰에서 명시적으로 지정하는 방식
- `exclude = ['author']` 설정을 통해 폼에 노출시키지 않고 뷰에서 처리함
