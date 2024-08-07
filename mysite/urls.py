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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from .  import views
from .  import settings 
from django.urls import include 
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('admin/logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='admin_logout'),
    path('', views.index, name='index') ,
    path('', include('instacorn.urls')) ,
    path('', include('iuser.urls')) , 
    path('', include('imanager.urls')) , 
    path('', include('insta.urls')),
    #비밀번호 재설정
    path('inspwdreset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='instacorn/inspwdreset_done.html'),
         name='inspwdreset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='instacorn/inspwdreset_confirm.html'),
         name='inspwdreset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='instacorn/inspwdreset_complete.html'),
         name='password_reset_complete'),

] 
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 