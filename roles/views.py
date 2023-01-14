from os import O_ASYNC
from time import strptime
from urllib import response
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
    AppInsert as FormAppInsert,
    AppUpdate as FormAppUpdate,
)

class AppInsert(View):
    template_name   = "apps/roles/includes/app_insert.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        token       = request.session.get("token")
        user        = Permission(token=token, role_can_access=self.role_can_access)
        app_exid    = kwargs.get("app_exid")
        if user.granted_permission():
            initial = {"application" : app_exid}
            context = {
                "FormInsert"        : FormAppInsert(initial=initial),
                "ApplicationEXID"   : kwargs.get("app_exid")
            }
            return render(request, self.template_name, context)
        else:
            context = {"Message" : user.message}
            return render(request, "errors/unload-page.html", context)
    
    def post(self, request, *args, **kwargs):
        token   = request.session.get("token")
        user    = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            form_insert = FormAppInsert(request.POST or None)
            if form_insert.is_valid():
                # Api role
                try:
                    endpoint    = f"data/roles?auth={token}"
                    payload     = form_insert.cleaned_data
                    api_role    = Credential(endpoint=endpoint, payload=payload).post()
                except Exception as error:
                    response    = ajax_response(0, error)
                    return JsonResponse(response)
                else:
                    if api_role.is_success():
                        response    = ajax_response(1, message=api_role.message, data=api_role.data)
                    else:
                        response    = ajax_response(0, message=api_role.message)
            else:
                errors      = errors_to_html(form_insert.errors)
                response    = ajax_response(0, message=errors)
        else:
            response    = ajax_response(0, message=user.message)
            
        return JsonResponse(response)

class AppUpdate(View):
    template_name   = "apps/roles/includes/update.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        token       = request.session.get("token")
        user        = Permission(token=token, role_can_access=self.role_can_access)
        app_exid    = kwargs.get("app_exid")
        role_exid   = kwargs.get("role_exid")
        if user.granted_permission():
            # Api role detail
            try:
                endpoint        = f"data/roles/{role_exid}?auth={token}"
                api_role_detail = Credential(endpoint=endpoint).get()
            except Exception as error:
                context = {"Message" : error}
                return render(request, "errors/page-unload.html", context)
            else:
                role    = api_role_detail.data if api_role_detail.is_success() else []
            
            initial                 = role
            initial["application"]  = app_exid
            context                 = {
                "RoleEXID"          : role.get("external_id"),
                "ApplicationEXID"   : kwargs.get("app_exid"),
                "FormUpdate"        : FormAppUpdate(initial=role)
            }
            return render(request, self.template_name, context)
        
    def post(self, request, *args, **kwargs):
        token       = request.session.get("token")
        user        = Permission(token=token, role_can_access=self.role_can_access)
        role_exid   = kwargs.get("role_exid")
        app_exid    = kwargs.get("app_exid")
        if user.granted_permission():
            initial     = {
                "external_id"   : role_exid,
                "application"   : app_exid
            }
            form_update = FormAppUpdate(request.POST or None, initial=initial)
            if form_update.is_valid():
                # Api role update
                try:
                    role_exid       = form_update.cleaned_data.get("external_id")
                    payload         = form_update.cleaned_data
                    endpoint        = f"data/roles/{role_exid}?auth={token}"
                    api_role_update = Credential(endpoint=endpoint, payload=payload).put()
                except Exception as error:
                    response    = ajax_response(0, message=error)
                    return JsonResponse(response)
                else:
                    if api_role_update.is_success():
                        response    = ajax_response(1, message=api_role_update.message, data=api_role_update.data)
                    else:
                        response    = ajax_response(0, message=api_role_update.message)
            else:
                errors      = errors_to_html(form_update.errors)
                response    = ajax_response(0, message=errors)
        else:
            response    = ajax_response(0, message=user.message)
            
        return JsonResponse(response)