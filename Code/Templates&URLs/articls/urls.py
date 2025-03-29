from django.urls import path
from . import views

app_name='articls'
urlpatterns = [
    path('', views.index, name='index'),
    path('dinner/', views.dinner, name='dinner'),  # path함수가 view함수를 호출
    path('search/', views.search, name='search'),
    path('<int:num>/', views.detail, name='detail'),
]
