from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.generic.base import View
from django.conf import settings
from django.contrib import messages
from django.utils.html import strip_tags, mark_safe
from datetime import datetime
from systems.cores.middleware import Permission
from systems.engines.apis import Credential
from systems.utilities.messages import ajax_response, errors_to_html

class Insert(View):
    template_name   = "app/users/includes/insert_by_app.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)