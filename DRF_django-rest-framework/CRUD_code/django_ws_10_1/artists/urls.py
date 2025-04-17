from django.urls import path
from . import views

urlpatterns = [
    
    path('artists_create/', views.artists_create),
    path('total_list/', views.artists_list),
    path('detail/<int:page_pk>/', views.artists_detail),
    path('artists/search', views.artists_search),
]
