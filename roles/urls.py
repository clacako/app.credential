from django.urls import path
from .views import *

urlpatterns = [
    path("insert/in/application/<app_exid>", AppInsert.as_view(), name="app-insert"),
    path("<int:role_exid>/update/in/application/<app_exid>", AppUpdate.as_view(), name="app-update"),
]