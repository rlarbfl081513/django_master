from django.urls import path
from . import views 

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/detail/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
