"""
URL configuration for lms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from .routers import restricted_router
from django.conf import settings
from django.conf.urls.static import static
from app.views import ReportGenerateView
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        #  add your swagger doc title
        title="Showroom API",
        #  version of the swagger doc
        default_version='v1',
        # first line that appears on the top of the doc
        description="Test description",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(restricted_router.urls)),
    path('reports/',ReportGenerateView.as_view(), name='report_generate'),
    # path('doc/', schema_view),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

