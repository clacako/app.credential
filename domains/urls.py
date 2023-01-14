from typing import List
from django.urls import path
from .views import *

urlpatterns = [
    path("insert/in/application/<int:app_exid>", AppInsert.as_view(), name="app-insert"),
]