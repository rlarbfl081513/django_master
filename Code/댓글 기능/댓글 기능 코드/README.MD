# 댓글 기능 코드 보기위해 봐야할 파일들
1. articles
   1. models.py
      1. 댓글창을 위한 모델 생성 (댓글쓰는 필드, 작성자필드, Article모델 참조하는 코드)
   2. forms.py
      1. 모델폼을 위한 코드
   3. urls.py
      1. 댓글 작성, 삭제를 위한 코드
   4. views.py
      1. 댓글 생성, 댓글 삭제 + 디테일페이지에서 댓글 리스트를 출력하기위한 코드 
      2. comments_create, comments_delete, detail 뷰함수 확인하기 