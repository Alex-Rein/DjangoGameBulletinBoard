"""
URL configuration for bulletin_board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from board.views import BoardPostsList, BoardPostReplies

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/', include('allauth.urls')),
    path('', RedirectView.as_view(pattern_name='post_list'), name='index'),
    path('posts/', include('board.urls')),
    path('board/<str:username>', BoardPostsList.as_view(), name='board'),
    path('board/<str:username>/<int:pk>', BoardPostReplies.as_view(), name='board_post_replies')
]
