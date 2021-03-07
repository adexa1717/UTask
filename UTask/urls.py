"""UTask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from rest_framework.reverse import reverse_lazy

from tasks.urls import router
from tasks.views import users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(route='api-token-auth/', view=users.AuthViewSet.as_view()),
    path(route='logout/', view=users.Logout.as_view()),
    # Для удобства в браузере сразу перемещает на страницу DRF
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

]
