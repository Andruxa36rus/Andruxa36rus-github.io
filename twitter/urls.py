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

from firstapp import views as firstapp
from user_profile_app import views as user_profile_app


from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', firstapp.index, name = 'index'),
    path('login/', firstapp.sign_in, name = 'sign_in'),
    path('logout/', firstapp.logout_view, name = 'logout'),
    path('registration/', firstapp.sign_up, name = 'sign_up'),
    path('search/', firstapp.search, name = 'search'),
    path('search/result/', firstapp.search_result, name = 'search_result'),
    path('create/', firstapp.create_post, name = 'create_post'),
    url(r'^(?P<post_id>\d+)/$', firstapp.post_detail, name = 'post_detail'),
    url(r'^(?P<post_id>\d+)/add/$', firstapp.add_comment, name = 'add_comment'),
    path('<post_id>?like/', firstapp.like, name = 'like'),
    path('<post_id>?edit=<username>', firstapp.edit_post, name = 'edit_post'),
    path('?edit=<username>&save', firstapp.edit_post_save, name = 'edit_post_save'),
    
    # user_profile_app
    path('profile/<username>', user_profile_app.profile, name = 'profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
