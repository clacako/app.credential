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
    Insert as FormInsert,
    Update as FormUpdate,
    SecretKey as FormSecretKey,
)

class Applications(View):
    template_name   = "apps/applications/index.html"
    role_can_access = ["superuser"]    
    
    def get(self, request, *args, **kwargs):
        token   = request.session.get("token")
        user    = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            context = {
                "HeadTitle" : "Applications",
                "PageTitle" : "Applications"
            }
            return render(request, self.template_name, context)
        else:
            context = {"Message" : user.message}
            return render(request, "errors/401.html", context)
    
class Insert(View):
    template_name   = "apps/applications/includes/insert.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        token   = request.session.get("token")
        user    = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            context = {"FormInsert" : FormInsert}
            return render(request, self.template_name, context)
        else:
            context = {"Message" : user.message}
            return render(request, "errors/401.html", context)
            
    def post(self, request, *args, **kwargs):
        form_insert = FormInsert(request.POST or None)
        if form_insert.is_valid():
            # Api app register
            try:
                token               = request.session.get("token")
                endpoint            = f"data/applications?auth={token}"
                api_app_register    = Credential(endpoint=endpoint, payload=form_insert.cleaned_data).post()
            except Exception as error:
                response    = ajax_response(0, message=error)
                return JsonResponse(response)
            else:
                if api_app_register.is_success():
                    response    = ajax_response(1, message=api_app_register.message, data=api_app_register.data)
                else:
                    response    = ajax_response(0, message=api_app_register.message)
        else:
            errors      = errors_to_html(form_insert.errors)
            response    = ajax_response(0, message=errors)
            
        return JsonResponse(response)
 
class List(View):
    template_name   = "apps/applications/includes/list.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        token   = request.session.get("token")
        user    = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            # Api applications
            try:
                token               = request.session.get("token")
                endpoint            = f"data/applications?auth={token}"
                api_applications    = Credential(endpoint=endpoint).get()
            except Exception as error:
                context = {"Message" : error}
                return render(request, "errors/page-unload.html", context)
            else:
                applications    = api_applications.data if api_applications.is_success() else []
            
            context = {"Applications" : applications}
            return render(request, self.template_name, context)
        else:
            context = {"Message" : user.message}
            return render(request, "errors/page-unload.html", context)
        
class Update(View):
    template_name   = "apps/applications/includes/update.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        token   = request.session.get("token")
        user    = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            # Api application detail
            try:
                app_exid        = kwargs.get("app_exid")
                endpoint        = f"data/application/{app_exid}?auth={token}"
                api_app_detail  = Credential(endpoint=endpoint).get()
            except Exception as error:
                context = {"Message" : error}
                return render(request, "errors/page-unload.html", context)
            else:
                application = api_app_detail.data if api_app_detail.is_success() else []
            
            context = {
                "Application"   : application,
                "FormUpdate"    : FormUpdate(initial=application)
            }
            return render(request, self.template_name, context)
        else:
            context = {"Message" : user.message}
            return render(request, "erros/page-unload.html", context)
        
    def post(self, request, *args, **kwargs):
        token   = request.session.get("token")
        user    = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            initial     = {"external_id" : kwargs.get("app_exid")}
            form_update = FormUpdate(request.POST or None, initial=initial)
            if form_update.is_valid():
                # Api application update
                try:
                    app_exid        = form_update.cleaned_data.get("external_id")
                    payload         = form_update.cleaned_data
                    endpoint        = f"data/application/{app_exid}?auth={token}"
                    api_app_update  = Credential(endpoint=endpoint, payload=payload).put()
                except Exception as error:
                    response    = ajax_response(0, message=error)
                    return JsonResponse(response)
                else:
                    if api_app_update.is_success():
                        response    = ajax_response(1, message=api_app_update.message, data=api_app_update.data)
                    else:
                        response    = ajax_response(0, message=api_app_update.message)
            else:
                errors      = errors_to_html(form_update.errors)
                response    = ajax_response(0, message=errors)
        else:
            response    = ajax_response(0, message=user.message)
            
        return JsonResponse(response)
    
class Details(View):
    template_name   = "apps/applications/includes/details.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        token   = request.session.get("token")
        user    = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            # Api application detail
            try:
                app_exid        = kwargs.get("app_exid")
                endpoint        = f"data/application/{app_exid}?auth={token}"
                api_app_detail  = Credential(endpoint=endpoint).get()
            except Exception as error:
                context = {"Message" : error}
                return render(request, "errors/page-unload.html", context)
            else:
                application = api_app_detail.data if api_app_detail.is_success() else []
            
            context = {
                "HeadTitle"     : f"{application.get('shortname')} App",
                "PageTitle"     : f"{application.get('shortname')} App",
                "Application"   : application
            }
            return render(request, self.template_name, context)
        
class SecretKey(View):
    template_name   = "apps/applications/includes/secret_key.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        token   = request.session.get("token")
        user    = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            # Api application secret key
            try:
                app_exid        = kwargs.get("app_exid")
                endpoint        = f"data/application/{app_exid}/secretKey?auth={token}"
                api_app_detail  = Credential(endpoint=endpoint).get()
            except Exception as error:
                context = {"Message" : error}
                return render(request, "errors/page-unload.html", context)
            else:
                application = api_app_detail.data if api_app_detail.is_success() else []
        
            context = {
                "FormSecretKey" : FormSecretKey(initial=application),
                "Application"   : application
            }
            return render(request, self.template_name, context)
        else:
            context = {"Message" : user.message}
            return render(request, "errors/401.html", context)
    
    def post(self, request, *args, **kwargs):
        token   = request.session.get("token")
        user    = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            form_secret_key = FormSecretKey(request.POST or None)
            if form_secret_key.is_valid():
                # Api application secret key
                try:
                    app_exid        = form_secret_key.cleaned_data.get("external_id")
                    endpoint        = f"data/application/{app_exid}/secretKey?auth={token}"
                    payload         = form_secret_key.cleaned_data
                    api_app_detail  = Credential(endpoint=endpoint, payload=payload).put()
                except Exception as error:
                    response    = ajax_response(0, message=error)
                    return JsonResponse(response)
                else:
                    if api_app_detail.is_success():
                        response    = ajax_response(1, message=api_app_detail.message, data=api_app_detail.data)
                    else:
                        response    = ajax_response(0, message=api_app_detail.message)
            else:
                errors      = errors_to_html(form_secret_key.errors)
                response    = ajax_response(0, message=errors)
        else:
            response    = ajax_response(0, message=user.message)
            
        return JsonResponse(response)

class MenuRoles(View):
    template_name   = "apps/applications/includes/menu_roles.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        token   = request.session.get("token")
        user    = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            # Get roles
            try:
                app_exid        = kwargs.get("app_exid")
                endpoint        = f"data/application/{app_exid}/roles?auth={token}"
                api_app_roles   = Credential(endpoint=endpoint).get()
            except Exception as error:
                context = {"Message" : error}
                return render(request, "errors/page-unload.html", context)
            else:
                roles   = api_app_roles.data if api_app_roles.is_success() else []

            context = {"Roles" : roles}
            return render(request, self.template_name, context)
        else:
            context = {"Message" : user.message}
            return render(request, "errors/401.html", context)


class Roles(View):
    template_name   = "apps/applications/includes/roles.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        token       = request.session.get("token")
        user        = Permission(token=token, role_can_access=self.role_can_access)
        app_exid    = kwargs.get("app_exid")
        if user.granted_permission():
            # Get roles
            try:
                endpoint        = f"data/application/{app_exid}/roles?auth={token}"
                api_app_roles   = Credential(endpoint=endpoint).get()
            except Exception as error:
                context = {"Message" : error}
                return render(request, "errors/page-unload.html", context)
            else:
                roles   = api_app_roles.data if api_app_roles.is_success() else []
                
            context = {
                "ApplicationEXID"   : app_exid,
                "Roles"             : roles
            }
            return render(request, self.template_name, context)
        else:
            context = {"Message" : user.message}
            return render(request, "errors/401.html", context)                


class Domains(View):
    template_name   = "apps/applications/includes/domains.html"
    role_can_access = ["superuser"]

    def get(self, request, *args, **kwargs):
        token       = request.session.get("token")
        user        = Permission(token=token, role_can_access=self.role_can_access)
        app_exid    = kwargs.get("app_exid")
        if user.granted_permission():
            # Api application domains
            try:
                endpoint        = f"data/application/{app_exid}/domains?auth={token}"
                api_app_domains = Credential(endpoint=endpoint).get()
            except Exception as error:
                context = {"Message" : error}
                return render(request, "errors/page-unload.html", context)
            else:
                domains = api_app_domains.data if api_app_domains.is_success() else []
            
            context = {
                "Domains"           : domains,
                "ApplicationEXID"   : app_exid
            }
            return render(request, self.template_name, context)
        else:
            context = {"Message" : user.message}
            return render(request, "errors/page-unload.html", context)
        
class DomainDetails(View):
    template_name   = "apps/applications/includes/domain_details.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        token       = request.session.get("token")
        user        = Permission(token=token, role_can_access=self.role_can_access)
        if user.granted_permission():
            app_exid    = kwargs.get("app_exid")
            domain_exid = kwargs.get("domain_exid")
            # Api application detail
            try:
                endpoint        = f"data/application/{app_exid}?auth={token}"
                api_app_detail  = Credential(endpoint=endpoint).get()
            except Exception as error:
                context = {"Message" : error}
                return render(request, "errors/page-unload.html", context)
            else:
                application = api_app_detail.data if api_app_detail.is_success() else []
            
            # Get application domain
            try:
                endpoint        = f"data/application/{app_exid}/domain/{domain_exid}?auth={token}"
                api_app_domain  = Credential(endpoint=endpoint).get()
            except Exception as error:
                context = {"Message" : error}
                return render(request, "errors/page-unload.html", context)
            else:
                domain  = api_app_domain.data if api_app_domain.is_success() else []
                
            context = {
                "HeadTitle"         : f"{application.get('shortname')} App Domain Detail",
                "PageTitle"         : f"{application.get('shortname')}/{domain.get('name')}",
                "Domain"            : domain,
                "Application"       : application
            }
            return render(request, self.template_name, context)
        else:
            context = {"Message" : user.message}
            return render(request, "errors/401.html", context)

class DomainUsers(View):
    template_name   = "apps/applications/includes/domain_users.html"
    role_can_access = ["superuser"]
    
    def get(self, request, *args, **kwargs):
        token       = request.session.get("token")
        user        = Permission(token=token, role_can_access=self.role_can_access)
        app_exid    = kwargs.get("app_exid")
        domain_exid = kwargs.get("domain_exid")
        if user.granted_permission():
            # Api application domain users
            try:
                endpoint                = f"data/application/{app_exid}/domain/{domain_exid}/users?auth={token}"
                api_app_domain_users    = Credential(endpoint=endpoint).get()
            except Exception as error:
                context = {"Message" : error}
                return render(request, "errors/page-unload.html", context)
            else:
                users   = api_app_domain_users.data if api_app_domain_users.is_success() else []
            
            context = {
                "ApplicationEXID"   : app_exid,
                "DomainEXID"        : domain_exid,
                "Users"             : users
            }
            return render(request, self.template_name, context)
        else:
            context = {"Message" : user.message}
            return render(request, "errors/401.html", context)
        