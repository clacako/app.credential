from urllib.parse import ParseResultBytes
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.generic.base import View
from django.conf import settings
from django.contrib import messages
from django.utils.html import strip_tags, mark_safe
from datetime import datetime
from systems.engines.apis import Credential
from systems.utilities.messages import ajax_response, errors_to_html
# Forms
from .forms import (
    Register as FormRegister,
    Login as FormLogin
)

class Register(View):
    template_name   = "apps/auth/register.html"
    
    def get(self, request, *args, **kwargs):
        context = {
            "HeadTitle"     : "Register",
            "FormRegister"  : FormRegister
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form_register   = FormRegister(request.POST or None)
        if form_register.is_valid():
            # Api user
            try:
                endpoint    = "data/users"
                payload     = form_register.cleaned_data
                api_user    = Credential(endpoint=endpoint, payload=payload).post()
            except Exception as error:
                response    = ajax_response(0, message=error)
                return JsonResponse(response)
            else:
                if api_user.is_success():
                    response    = ajax_response(1, message=api_user.message, data=api_user.data)
                else:
                    response    = ajax_response(0, message=api_user.message)
        else:
            errors      = errors_to_html(errors=form_register.errors)
            response    = ajax_response(0, message=errors)

        return JsonResponse(response)

class Login(View):
    template_name   = "apps/auth/login.html"
    
    def get(self, request, *args, **kwargs):
        token   = request.session.get("token")
        if token:
            # Api token
            try:
                endpoint        = "authentication/token"
                payload         = {"token" : token}
                api_auth_token  = Credential(endpoint=endpoint, payload=payload).put()
            except Exception as error:
                pass
            else:
                if api_auth_token.is_success():
                    del request.session["token"]
        
        context     = {
            "HeadTitle"     : "Login",
            "FormLogin"     : FormLogin
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form_login  = FormLogin(request.POST or None)
        if form_login.is_valid():
            # API Authentication
            try:
                endpoint    = "authentication/login"
                payload     = {
                    "email"         : form_login.cleaned_data.get("email"),
                    "secret_key"    : form_login.cleaned_data.get("password")
                }
                api_auth    = Credential(endpoint=endpoint, payload=payload).post()
            except Exception as error:
                messages.add_message(request, messages.INFO, error)
                return redirect("authentication:login")
            else:
                if api_auth.is_success():
                    request.session["token"]    = api_auth.data[0].get("token")
                    return redirect("applications:index")
                else:
                    messages.add_message(request, messages.INFO, mark_safe(api_auth.message))
                    return redirect("authentication:login")
        else:
            errors  = errors_to_html(form_login.errors)
            messages.add_message(request, messages.INFO, mark_safe(errors.message))
            return redirect("authentication:login")            
