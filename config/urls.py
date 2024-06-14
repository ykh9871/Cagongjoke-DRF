from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        schema.servers = [
            {"url": "http://localhost:8000/", "description": "Local Server"},
            {"url": "https://ohmolli.com:8000/", "description": "Dev Server"},
        ]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="SuddenAttack API",
        default_version="v1",
        description="SuddenAttack API Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ykh9871@gmail.com"),
        license=openapi.License(name="ykh License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=CustomOpenAPISchemaGenerator,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/cagong/", include("apps.cagong.urls")),
    path("api/user/", include("apps.users.urls")),
    path("api/user/", include("allauth.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
