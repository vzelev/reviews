"""reviews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from rest_framework import routers
from rest_framework.authtoken import views as auth_views

from reviews import views
from rest_framework_swagger.views import get_swagger_view


router = routers.DefaultRouter()
router.register(r'reviews', views.ReviewsViewSet)
router.register(r'register', views.RegisterView)



documented_urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('obtain-api-token/', auth_views.obtain_auth_token),
]

docs = get_swagger_view(title='Reviews API', patterns=documented_urlpatterns)
urlpatterns = [path('docs/', docs, name='docs')] + documented_urlpatterns


