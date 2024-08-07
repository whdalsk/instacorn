"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('instest.do', views.instest) ,

    #메인페이지
    path('home.do/', views.home),

    #업로드
    path('uploadsave.do/', views.uploadsave),

    #게시판 신고
    path('board_singo.do/', views.board_singo),
    
    #좋아요
    path('like.do/', views.like),
    path('del_like.do/', views.del_like),
    
    #검색페이지
    path('instaselect.do', views.instaselect),
    path('home.do/instaselect.do', views.instaselect, name='instaselect'),
    path('myprofile.do/instaselect.do', views.instaselect, name='instaselect'),

    #상세페이지
    path('insdetail.do', views.insdetail) ,
    path('insdelete.do', views.insdelete) , 
    path('insupdate.do', views.insupdate) ,
    path('insupdatesave.do', views.insupdatesave) ,

    #마이페이지
    path('myprofile.do/', views.myprofile),
    
    #팔로워 삭제
    path('del_follower.do/', views.del_follower),
    
    #팔로잉 취소
    path('del_following.do/', views.del_following),
    
    #팔로우
    path('follow.do/', views.follow),
    #유저 신고
    path('user_singo.do/', views.user_singo),
    #프로필 이미지 변경
    path('editImage.do/', views.editImage),
    
    #댓글
    path('insreplyinsert.do', views.insreplyinsert) ,
    path('insreplydelete.do', views.insreplydelete) ,
    path('insreplyupdate.do', views.insreplyupdate) ,

    #로그아웃
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
