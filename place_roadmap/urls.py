"""
URL configuration for place_roadmap project.

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
from django.urls import include, path
from homepage.views import explore_place_result, home,explore_place
# from accounts.views import register, login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('explore_place/', explore_place, name='explore_place'),
    path('explore_place_result',explore_place_result,name='explore_place_result'),
    path('accounts/', include('accounts.urls'))

]
