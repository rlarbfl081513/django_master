from django.shortcuts import render, redirect
## 회원가입 
# 회원가입 시 사용자 입력 데이터를 받는 biltin ModelForm
# UserCreationForm
  # 장고가 기본적으로 제공하는 회원가입용 폼 클래스
  # 내부적으로 username, password, 같은 필드가 정의되어있음 
  # ModleForm이라 User모델과 연결되어있음 
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, UserChangeForm
## 비밀번호 변경 시 세션 무효화를 막아주는 함수 (이거 안하면 비밀번호 변경하고 리다이렉트 되는 순간 로그아웃되버림)
  # 왜 비번 변경 시 로그아웃이 발생할까?
  # 장고는 로그인 상태를 세션에 저장한다. -> 세션 정보엔 로그인한 사용자의 해시 정보도 포함되어있음 -> 그런데 사용자의 비번이 변경되면 해쉬가 변겨오딤 -> 장고는 ??해쉬가 바뀌었네하면서 - 보안상 위험할수 있으니 세션 무효화하해버림 --> 자동 로그아웃되는 거임 ---> 장고의 보안 정책
  # 그래서 비번은 변경되었지만, 지금 로그인한 세션은 계속 유지해도된다고 장고에게 알려주는 역할 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

# 회원가입 커스텀 폼 
from .forms import CustomUserCreationForm, CustomUserChangeForm

## 로그인
from django.contrib.auth.forms import AuthenticationForm # 로그인 폼 (장고 기본 제공)
from django.contrib.auth import login as auth_login # 로그인 처리를 위한 함수 
from django.contrib.auth import logout as auth_logout

# request는 장고의 뷰함수에서 항상 첫번째 인자로 쓰는 이유
  # 사용자가 보낸 정보(요청)을 담고 있는 데이터 꾸러미
  # 뷰함수에서 이걸 받아서 누가 뭘 요청했는지 확인하고 그에 맞게 응답을 만드는 거임 
  # request안에는 메서드, GET/POST 데이터, 로그인 사용자 정보 등 이것저거 다 들어있음 
  # 그니까 이거 없으면 누가 뭘 어떻게 요청했는지 모르는거라 웹 개발 불가임 
def index(request):
  return render(request, 'accounts/index.html')

## 아래는 장고의 회원가입 내장함수를 그대로 사용한 경우 (커스텀 모델 사용하지 않은 버전)
# def signup(request):
#   # 어떻게 회원가입 폼에 입력한게 저장되는걸까
#     # reuqest.POST
#       # 사용자가 <form>을 POST방식으로 제출하면 -> 입력값들은 request.POST에 담긴다 -> 예.{'username': 'gyuri', 'password1': '1234', 'password2': '1234'} 이런식으로 
#     # UserCreationForm(request.POST)
#       # 사용자가 보낸 데이터를 폼 객체에 넣는것 
#       # 이 시점에서 폼에 값이 들어감 
#       # 아직 저장 안됐고, 유효성 검증도 아직 안함 

#   if request.method == 'POST':
#     form = UserCreationForm(request.POST) # 사용자가 보낸 데이터를 회원가입 폼에 넣음
#     print("폼 유효성:", form.is_valid())  # ← 추가
#     print("에러 내용:", form.errors)     # ← 추가
#     if form.is_valid(): # 유효성 검사 진행 
#       form.save() # 진짜로 user 객체를 DB에 저장
#       return redirect('articles:index')
#   # 제출버튼도 안눌렀고, 데이터도 안보내졌을떄 = 그냥 페이지 처음 열었을때 
#   # 아무것도 안했네? 그냥 빈폼 보여줘야지 
#   else:
#     form = UserCreationForm() # 빈 폼 생성
  
#   # 딕셔너리 변수를 context라고 내가 지은거임 
#     # 이 딕셔너리는 템플릿에 전달한 데이터 묶음을 말한다 
#     # render의 3번째 인자로 들어감 
#   context = {
#     'form' : form,
#   }

#   # 이 순서는 장고가 정한 함수 정의 방식 
#     # 파이선은 위치기반인자를 받을떄는 순서대로 해석하니까 정해진대로 써야함 
#       # 그런데 이름을 붙이면 순서 바껴도 상관없음
#       # 예) 키워드 인자는 순서가 상관없기 때문임 
#       # render(template_name='articles/signup.html', request=request, context=context) 

#     # 첫번째 인자 : request
#     # 두번째 인자 : templates_name (템플릿 파일 경로)
#     # 세번째 인자 : context (템플릿에 넘길 데이터 딕셔너리) 
#   return render(request, 'articles/signup.html', context)

## 회원가입 : 커스텀모델을 사용하여 뷰함수 생성하기 
def signup(request):
  # 이미 들어온 사용자면 로그인/회원가입 로직을 수행할 수 없게하기기
  # is_authenticated
    # 메서드가 아닌 속성값이다. 그래서 마지막에 ()도 안붙이는 거임 
    # 로그인된 사용자라면 True, 아니면 False
  # 이미 로그인 했으면 홈으로 보내고 아니면 로그인 진행시켜줘 
  if request.user.is_authenticated:
    return redirect('articles:index')

  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST) # 그냥 여기서 폼이름만 커스텀한 폼이름올 바꾸면됨 
    print("폼 유효성:", form.is_valid()) 
    print("에러 내용:", form.errors)     
    if form.is_valid(): 
      user = form.save() 
      auth_login(request, user) ## 여기에 이거 추가하면 회원가입 동시에 로그인됨 
      return redirect('articles:index')

  else:
    form = CustomUserCreationForm() # 그냥 여기서 폼이름만 커스텀한 폼이름올 바꾸면됨 

  context = {
    'form' : form,
  }

  return render(request, 'accounts/signup.html', context)


## 회원 탈퇴 
@login_required
def signout(request):
  request.user.delete()
  return redirect('articles:index')

## 회원정보 수정 
def userEdit(request):
  if request.method == 'POST':
    # instance=request.user
    # 현재 로그인한 사용자의 정보로 폼을 채우고 수정도 그 사용자 객체를 반영하라는 것 
    # instance는 이 폼은 누구를 수정하려고 만든거야라고 알려주는 대상 객체 
    # 회원가입 시에는 새 객체 생성이라 수정 대상이 없기에 안쓰는 거임 
    form = CustomUserChangeForm(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      return redirect('accounts:index')
  else:
    form = CustomUserChangeForm(instance=request.user)
  
  context = {
    'form' : form,
  }
  return render(request, 'accounts/userEdit.html', context)


## 비밀번호 수정
@login_required
def change_password(request):
  if request.method == 'POST':
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
      user = form.save()

      # 비밀번호 변경 시 세션이 무효화되어 자동 로그아웃되는걸 막아주는 거거
      # 꼭 저장 후에 아래 코드를 써야함 
      update_session_auth_hash(request, user) 
      return redirect('accounts:index')
  else:
    form = PasswordChangeForm(request.user)
  
  context = {
    'form' : form,
  }
  return render(request, 'accounts/change_password.html', context)


#  로그인 로그아웃  #################-------------------------------로그인 로그아웃

def login(request):
  # 이미 들어온 사용자면 로그인/회원가입 로직을 수행할 수 없게하기기
  if request.user.is_authenticated:
    return redirect('articles:index')
  
  if request.method == 'POST': # 사용자가 로그인 폼을 제출한경우
    form = AuthenticationForm(request, request.POST) # 사용자 입력 데이터로 폼 생성 (그니까 그냥 폼에 내용 채운다는 거임)
    if form.is_valid(): # 아이디 비번이 올바른 경우
      # request는 현재 요청 객체 / form.get_user()는 로그인폼에서 검증된 사용자 객체를 반환 
      auth_login(request, form.get_user()) # 로그인 처리 (세션에 사용자 저장)
      return redirect('articles:index')
  else:
    form = AuthenticationForm() # 로그인 페이지 처음 들어왔을때 (빈 폼 보여줌 )

  context = {
    'form' : form, # 템플릿에 전달할 폼 객체 
  }

  return render(request, 'accounts/login.html', context)

## 로그아웃 
@login_required
def logout(request):
  auth_logout(request)
  return redirect('articles:index')