from django.contrib import admin
from django.urls import path
from .views import PostList, PostDetail, PostCreate, CategoryList


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_details'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('categories/<str:category>', CategoryList.as_view(), name='category_list'),
]
