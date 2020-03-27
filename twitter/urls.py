"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from firstapp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('login/', views.sign_in, name = 'sign_in'),
    path('logout/', views.logout_view, name = 'logout'),
    path('registration/', views.sign_up, name = 'sign_up'),
    path('search/', views.search, name = 'search'),
    path('search/result/', views.search_result, name = 'search_result'),
    path('create/', views.create_post, name = 'create_post'),
    url(r'^(?P<post_id>\d+)/$', views.post_detail, name = 'post_detail'),
    url(r'^(?P<post_id>\d+)/add/$', views.add_comment, name = 'add_comment'),
    path('<post_id>?like/', views.like, name = 'like'),
    path('<post_id>?edit=<username>', views.edit_post, name = 'edit_post'),
    path('?edit=<username>&save', views.edit_post_save, name = 'edit_post_save'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
