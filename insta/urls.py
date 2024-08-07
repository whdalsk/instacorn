from django.urls import path, include
from . import views

urlpatterns = [
    path('dm.do', views.main, name='main_view'), # 정보 보내기 받기
]