from django.urls import path
from . import views


app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
    # 댓글 생성하는 주소 (게시글의 pk를 받아옴)
    path('<int:pk>/comments/', views.comments_create, name='comments_create'),
    # 각각의 댓글을 삭제하기위한 주소 ( 게시글의 pk + 댓글 개별의 pk 받아옴 )
    path('<int:pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
]
