# model
1. 모델 클래스는 테이블 설계도를 그리는 거임 
  - 개발자는 데이블구조를 어떻게 설계할지에 대한 코드만 제공하면됨 -> 상속을 활용한 프레임워크의 기능 제공 덕분 (코딩계의 밀키트 사용중인거임)
    
  - 테이블의 각 필드(열)이름을 정한거임 --> 이제부터는 필드라고 부를거임
  데이터의 유형과 제약조건을 정의함 -> 즉, 필드 타입과 필드 옵션을 작성하는 거임 
  
  - CharField라는 유형과 max_length라는 제약조건을 검
  - 클래스는 대문자로 시작하기에 대문자로 시작하면 클래스인걸 알 수 있음

## 필드 타입
1. 데이터의 종류를 정의 (models 모듈의 클래스로 정의되어있음)

### 필드 종류
1. charField
  - 캐릭터 필드 : 제한된 길이의 문자열 저장, max_length는 필수 옵션 
2. TextField
  - 길이 제한이 없는 대용량 텍스트 저장 ( 무한대는 아니지만 사용하는 시스템따라 달라짐 )
3. DateTimeField
    ```
      <필드 옵션>
      auto_now        
      # 데이터가 저장될떄마다 자동으로 현재 날짜시간을 저장 (수정 시 이용하는 것)
      auto_now_add    
      # 데이터가 처음 생성될때만 자동으로 현재 날짜시간 저장 ( 생성일에 사용)
    ```
    <details><summary> DateTimeField vs DateField 요약 보기</summary>

      ## Django `DateTimeField` vs `DateField` 비교 정리

      | 항목 | `DateTimeField` | `DateField` |
      |------|------------------|-------------|
      | 저장 형식 | 날짜 + 시간 (`YYYY-MM-DD HH:MM[:ss[.uuuuuu]]`) | 날짜만 (`YYYY-MM-DD`) |
      | 사용 용도 | 날짜와 시간이 모두 필요한 경우 | 날짜만 필요한 경우 (예: 생일, 기념일 등) |

      ---

      ## 공통 옵션들
      | 옵션 | 설명 |
      |------|------|
      | `auto_now_add=True` | **객체 생성 시** 현재 날짜/시간 자동 저장 |
      | `auto_now=True` | **객체 저장 시** 현재 날짜/시간 자동 갱신 |
      | `null=True` | DB에서 NULL 허용 |
      | `blank=True` | 폼에서 빈 값 허용 |
      | `default=...` | 기본값 지정 (`timezone.now`, 특정 날짜 등) |
      | `verbose_name='...'` | 필드 이름 설정 |
      | `help_text='...'` | 도움말 텍스트 설정 |

      ---

      ## 예시

      ```python
      from django.db import models
      from django.utils import timezone

      class MyModel(models.Model):
          created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간 저장
          updated_at = models.DateTimeField(auto_now=True)      # 수정 시간 저장
          birth_date = models.DateField(null=True, blank=True)  # 생일
      ```
    </details>

### 필드 옵션
1. 필드의 동작과 제약조건을 정의 
2. 제약조건
   - 특정규칙을 강제하기위해 테이블의 열이나 행에 ㅈ거용되는 규칙이나 제한사항 
3. 주요필드 옵션
    - null : 데이터베이스에서 null값을 허용할지 여부 결정 (기본값은 false)
    - blank : 폼에서 빈 값을 허용할지 여부 결정 (기본값은 false)
    - default : 필드의 기본값을 결정


# Migrations
```
<핵심 코드>
pyhton manage.py makemigrations   # model class 기반으로 최종설계도 만듦
python manage.py migrate    # 최종 설계도를 db에 전달하여 반영
```
1. 모델을 통한 DB 관리
2. model클래스의 변경사항(필드생성, 수정 삭제 등)을 DB에 최종 반영하는 방법
3. models.py에서 작성한 설계도를 db에 적용하도록 요청하는 것을  migrations라고함
4. 마이그레이션 과정
    ```
    modle class로 설계도 초안 작성 --> migrations 파일이라는 최종 설계도 그리는데에 makemigrations하여 전달 --> migrate를 통해 DB에 내가 작성한거 적용하는 거임 (설계도 기반으로 테이블 만들어짐)

    - model class에서 바로 DB로 점프해서 만들어지는 아님
    ```
    - 마이그레이션 파일이 계속해서 쌓이게 하는 이유 : 마치 커밋을 쌓는거임, 문제에대한 디버깅을 할 수 있도록, 
5. migrate
  - 작동시 아래처럼 길게 나오는 이유는 프로젝트의 setting파일에서 볼 수 있듯이, 기본내장앱이 이미 많은데 그거의 자체의 설계도임 -> 그설계도의 테이블도 같이 만들어지는거임
    ```
      python manage.py migrate

    Operations to perform:
      Apply all migrations: admin, articles, auth, contenttypes, sessions
    Running migrations:
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying admin.0002_logentry_remove_auto_add... OK
      Applying admin.0003_logentry_add_action_flag_choices... OK
      Applying articles.0001_initial... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
    ```
6. DB
  - [ 앱이름_클래스이름 ] : 이게 db에서의 테이블 이름
  - 데이터베이스는 기본적으로 빈값을 허용하지 않음
    - null blank같은 거라도 있어야함, 
  - 필드에 is가 붙는건 true/false를 묻는거임
  - 세가지의 사람이 있음
    - 관리자(superuser) / 스태프(is_staff) / 일반인
    - is_active는 휴면계정 onoff에서 사용되는 필드 
  - 데이터베이스에 들어가는 시간은 UTC임 -> 출력해서 보열줄떄는 해당 나라 시간으로 보여줌 

# admin site
1. 데이터 확인 및 테스트 등을 진행하는데 매우 유용, 장고가 추가 설치 및 설정없이 자동으로 제공하는 관리자 인터페이스
2. admin 계정이 생성되는 이유
    - db가 있다는 거임
    - django의 기본 내장 앱들이 사용하는 데이터베이스 테이블들도 함께 생성(migrate 시 긴 줄로 나오는) -> 이 과정에서 회원을 관리하는 db도 생성됨 -> 즉, 이 db덕에 admin 계정이 생성될 수 있는거임
3. 과정
    ```
      <admin 계정 생성>
      1. python manage.py createsuperuser
      2. db에 생성된 admin 계정 확인 (장고가 알아서 내장앱 통해 회원관련 db만들어놓음)
      3. admin에 모델 클래스 등록 : admin.py에 작성한 모델 클래스를 등록해야함 admin site에서 확인 가능 
        from .models import Article
        admin.site.register(Article)
    ```

# 참고
1. 마이그레이션 기타 명령어
    ```
      python manage.py showmigrations
      # 마이그레이션 파일들이 마이그레이트됐는지 여부 확인
      # [x] 표시 있으면, 마이그레이트 완료됨을 의미

      python manage.py sqlmigrate 클래스이름 마이크레이션파일번호(예, 0001)
    ```
2. SQLite
  - 데이터베이스 관리 시스템 중 하나이며, 장고의 기본 데이터베이스로 사용됨 (파일로 존재하며 가볍고 호환성이 좋음)