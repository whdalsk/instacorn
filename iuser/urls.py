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
        path('inslogin.do', views.inslogin),
        path('insjoin.do', views.insjoin),
        path('inslogout.do', views.inslogout),
        path('insmember_modify.do', views.insmember_modify),
        path('inspwd_modify.do', views.inspwd_modify),
        
        #비밀번호 찾기
        path('inspwdreset.do', views.password_reset_request, ),
        

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
