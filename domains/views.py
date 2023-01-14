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
# Forms
from .forms import (
    AppInsert as FormAppInsert
)

class Menu(View):
    template_name   = "apps/domains/includes/menu.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        token   = request.session.get("token")
        user    = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            # Api domains
            try:
                app_exid    = kwargs.get("app_exid")
                endpoint    = f"data/application/{app_exid}/domains?auth={token}"
                api_domains = Credential(endpoint=endpoint).get()
            except Exception as error:
                context = {"Message" : error}
                return render(request, "errors/page-unload.html", context)
            else:
                domains = api_domains.data if api_domains.is_success() else []
            
            context = {"Domains" : domains}
            return render(request, self.template_name, context)
        else:
            context = {"Message" : user.message}
            return render(request, "errors/page-unload.html", context)

class AppInsert(View):
    template_name   = "apps/domains/includes/app_insert.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        token   = request.session.get("token")
        user    = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            initial = {"applications" : kwargs.get("app_exid")}
            context = {
                "ApplicationEXID"   : kwargs.get("app_exid"),
                "FormInsert"        : FormAppInsert(initial=initial),
            }
            return render(request, self.template_name, context)
        else:
            context = {"Message" : user.message}
            return render(request, "errors/401.html", context)
        
    def post(self, request, *args, **kwargs):
        token   = request.session.get("token")
        user    = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            initial     = {"applications" : kwargs.get("app_exid")}
            form_insert = FormAppInsert(request.POST or None, initial=initial)
            if form_insert.is_valid():
                try:
                    endpoint            = f"data/domains?auth={token}"
                    payload             = form_insert.cleaned_data
                    api_domain_insert   = Credential(endpoint=endpoint, payload=payload).post()
                except Exception as error:
                    response    = ajax_response(0, message=error)
                    return JsonResponse(response)
                else:
                    if api_domain_insert.is_success():
                        response    = ajax_response(1, message=api_domain_insert.message, data=api_domain_insert.data)
                    else:
                        response    = ajax_response(0, message=api_domain_insert.message)
            else:
                errors      = errors_to_html(form_insert.errors)
                response    = ajax_response(0, message=errors)
        else:
            response    = ajax_response(0, message=user.message)
        
        return JsonResponse(response)
    