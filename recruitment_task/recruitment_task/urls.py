"""recruitment_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from images.views import ImageCreateApiView, ImageListApiView, ExpiringLinkCreateApiView, ExpiringLinkRetrieveApiView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('images/', ImageCreateApiView.as_view(), name='image-create'),
    path('images/list/', ImageListApiView.as_view(), name='image-list'),
    path('links/generate', ExpiringLinkCreateApiView.as_view(), name='generate-link'),
    path('links/get_by_code/<str:code>', ExpiringLinkRetrieveApiView.as_view(), name='get_image_by_code')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
