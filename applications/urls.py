from django.urls import path
from .views import *

urlpatterns = [
    path("", Applications.as_view(), name="index"),
    path("insert", Insert.as_view(), name="insert"),
    path("list", List.as_view(), name="list"),
    path("<int:app_exid>/update", Update.as_view(), name="update"),
    path("<int:app_exid>/details", Details.as_view(), name="details"),
    path("<int:app_exid>/secretKey", SecretKey.as_view(), name="secret-key"),
    path("<int:app_exid>/roles", Roles.as_view(), name="roles"),
    path("<int:app_exid>/domains", Domains.as_view(), name="domains"),
    path("<int:app_exid>/domain/<int:domain_exid>/details", DomainDetails.as_view(), name="domain-details"),
    path("<int:app_exid>/domain/<int:domain_exid>/users", DomainUsers.as_view(), name="domain-users"),
    path("<int:app_exid>/menu/roles", MenuRoles.as_view(), name="menu-roles"),
]
