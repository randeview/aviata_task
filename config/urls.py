from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.contrib import admin

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

admin.site.index_title = ' '

internal_schema_view = get_schema_view(
    openapi.Info(
        title="AVIATA API", default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

schema_view = get_schema_view(
    openapi.Info(
        title="AVIATA API", default_version="v1",
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui", ),
    path("api/docs/internal/", internal_schema_view.with_ui("swagger", cache_timeout=0),
         name="schema-internal-swagger-ui", ),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json", ),
    path("api/", include("apps.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
