# 🗨️ Django 댓글 기능 구현 정리

## 📌 기능 설명

- 일기(Diary) 객체에 대해 댓글(Comment)을 작성, 삭제할 수 있는 기능
- 댓글은 각각 특정 일기 객체에 연결되어 있으며, 템플릿에서 일기별로 댓글 목록을 출력하고 폼을 통해 새 댓글을 작성 가능

---

## 🧱 모델 (models.py)

```python
class Diary(models.Model):
    content = models.CharField(max_length=125)
    picture = models.ImageField(blank=True, upload_to='diary/%y/%b/%a')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    content = models.TextField(max_length=125)
    created_at = models.DateTimeField(auto_now_add=True)
```

- `Comment` 모델은 `Diary`와 1:N 관계
- `on_delete=models.CASCADE`: 일기가 삭제되면 관련 댓글도 함께 삭제됨

---

## 🧾 폼 (forms.py)

```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
```

- 댓글 작성 시 필요한 필드만 선택 (`content`)
- 템플릿에서 `{{ comeform }}`으로 사용

---

## 🧠 뷰 함수 (views.py)

```python
def comments(request, pk):
    diary = Diary.objects.get(pk=pk)
    comeform = CommentForm(request.POST)
    if comeform.is_valid():
        form = comeform.save(commit=False)
        form.diary = diary
        form.save()
        return redirect('diaries:index')

    context = {
        'diary': diary,
        'comeform': comeform,
    }
    return render(request, 'diaries/index.html', context)
```

- 댓글 저장 전 `commit=False`로 중간 저장 후 일기 객체 할당
- 저장 후 index 페이지로 리다이렉트

```python
def delete(request, pk, del_pk):
    comm = Comment.objects.get(pk=del_pk)
    comm.delete()
    return redirect('diaries:index')
```

- 특정 댓글을 삭제하는 뷰
- URL에서 댓글 ID 받아서 삭제

---

## 🌐 URL 설정 (urls.py)

```python
urlpatterns = [
    ...
    path('<int:pk>/comments/', views.comments, name='comments'),
    path('<int:pk>/comments/<int:del_pk>/delete/', views.delete, name='delete'),
]
```

- 댓글 생성: `POST /<diary_id>/comments/`
- 댓글 삭제: `GET /<diary_id>/comments/<comment_id>/delete/`

---

## 🧩 템플릿 (index.html 중 일부)

```html
<ul>
  {% for item in diary.comment_set.all %}
    <li>{{ item.content }}</li>
    <form action="{% url 'diaries:delete' diary.pk item.pk %}">
      {% csrf_token %}
      <input type="submit" value='삭제'>
    </form>
  {% endfor %}
</ul>

<form action="{% url 'diaries:comments' diary.pk %}" method='POST'>
  {% csrf_token %}
  {{ comeform }}
  <input type="submit" value='댓글생성'>
</form>
```

- 각 일기에 연결된 댓글을 반복 출력
- 댓글 삭제는 버튼으로 연결된 URL 실행
- 댓글 생성 폼은 `CommentForm` 인스턴스를 이용

---

## 💡 기타 팁

- 댓글 기능은 기본적으로 ForeignKey로 연관된 객체를 어떻게 다루는지를 보여주는 좋은 예
- 추후 Ajax를 적용해 비동기로 댓글을 추가하거나 삭제하는 것도 가능
