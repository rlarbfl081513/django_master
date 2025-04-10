# 회원 관련 기능 정리 문서 (Django 기반)

Django에서 회원가입, 로그인/로그아웃, 회원정보 수정, 비밀번호 변경, 회원탈퇴 등 **계정 관련 기능 전반**을 구현한 코드 구조와 흐름을 상세히 설명합니다. 이 문서는 추후 전체 기능을 다시 구현할 수 있도록 파일별, 기능별로 **구체적이고 실전 위주로 정리**됩니다.

---

## 📁 기능별 상세 설명

---

## 🟢 1. 회원가입 기능

### ✅ 개요
- 사용자가 `username`, `password` 등을 입력하여 새로운 계정을 생성
- Django가 제공하는 `UserCreationForm`을 상속하여 커스텀한 폼 사용
- 회원가입 시 이미 로그인된 사용자는 접근 제한
- 회원가입과 동시에 로그인 처리도 포함 가능

### ✅ 사용 파일 및 구성

#### 📄 views.py
```python
from django.contrib.auth import login as auth_login
from .forms import CustomUserCreationForm

def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
```

#### 📄 forms.py
```python
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
```

#### 📄 urls.py
```python
path('signup/', views.signup, name='signup')
```

#### 📄 signup.html
```django
<form action="{% url 'accounts:signup' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="회원가입">
</form>
```

#### 📝 핵심 개념
- `request.POST`를 폼에 넘겨서 데이터 바인딩
- 유효성 검사 후 `form.save()`로 DB에 사용자 저장
- `auth_login()` 호출로 가입 직후 로그인 상태 유지

---

## 🔵 2. 로그인 / 로그아웃 기능

### ✅ 로그인

#### 📄 views.py
```python
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
```

#### 📄 urls.py
```python
path('login/', views.login, name='login')
```

#### 📄 login.html
```django
<form action="{% url 'accounts:login' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="로그인">
</form>
```

#### 📝 핵심 개념
- `AuthenticationForm(request, POST)`로 로그인 처리
- `form.get_user()`로 인증된 사용자 객체 추출
- `auth_login()`으로 세션에 로그인 상태 저장

### ✅ 로그아웃

#### 📄 views.py
```python
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

@login_required
def logout(request):
    auth_logout(request)
    return redirect('articles:index')
```

#### 📄 urls.py
```python
path('logout/', views.logout, name='logout')
```

---

## 🟡 3. 회원정보 수정 기능

### ✅ 목적
- 로그인한 사용자가 본인의 `이름`, `이메일` 등 개인정보 수정

### ✅ 구성

#### 📄 views.py
```python
from .forms import CustomUserChangeForm

def userEdit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/userEdit.html', {'form': form})
```

#### 📄 forms.py
```python
from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')
```

#### 📄 urls.py
```python
path('userEdit/', views.userEdit, name='userEdit')
```

#### 📄 userEdit.html
```django
<form action="{% url 'accounts:userEdit' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="회원정보 수정">
</form>
<a href="{% url 'accounts:change_password' %}">비밀번호 변경</a>
```

---

## 🔴 4. 비밀번호 변경 기능

### ✅ 목적
- 로그인 상태에서 비밀번호 변경 가능
- 변경 후에도 로그인 상태 유지 (`update_session_auth_hash()` 사용)

#### 📄 views.py
```python
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:index')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
```

#### 📄 urls.py
```python
path('password/', views.change_password, name='change_password')
```

#### 📄 change_password.html
```django
<form action="{% url 'accounts:change_password' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="비밀번호 변경">
</form>
```

#### 📝 주의사항
- 비밀번호 변경 시 세션 해시가 바뀌므로 자동 로그아웃 방지 위해 반드시 `update_session_auth_hash()` 호출

---

## 🟤 5. 회원탈퇴 기능

### ✅ 구성

#### 📄 views.py
```python
@login_required
def signout(request):
    request.user.delete()
    return redirect('articles:index')
```

#### 📄 urls.py
```python
path('signout/', views.signout, name='signout')
```

#### 📄 index.html 일부
```django
<form action="{% url 'accounts:signout' %}" method="POST">
  {% csrf_token %}
  <input type="submit" value="회원탈퇴">
</form>
```

---

## 🧱 6. 인증된 사용자만 접근 허용

### ✅ is_authenticated
- `request.user.is_authenticated`: 현재 로그인 여부를 확인하는 속성 (괄호 없음)
- 사용 예:
```python
if request.user.is_authenticated:
    return redirect('articles:index')
```

### ✅ @login_required 데코레이터
- 로그인하지 않은 사용자는 자동으로 로그인 페이지로 리디렉트
```python
from django.contrib.auth.decorators import login_required

@login_required
def logout(request):
    ...
```

---

## 📌 추천 파일 구조
```
accounts/
├── models.py
├── forms.py
├── views.py
├── urls.py
├── templates/accounts/
│   ├── signup.html
│   ├── login.html
│   ├── userEdit.html
│   ├── change_password.html
│   └── index.html
```

---

이 문서를 기반으로 회원 관련 기능을 전체적으로 다시 구성할 수 있습니다. 필요한 경우 CustomUser 모델 및 admin 등록 예시도 확장 가능!

