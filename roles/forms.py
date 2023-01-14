from django import forms

class AppInsert(forms.Form):
    application     = forms.IntegerField(
        widget      = forms.TextInput(
            attrs   = {
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------",
                "readonly"      : "readonly"
            }
        )
    )
    
    name    = forms.CharField(
        widget  = forms.TextInput(
            attrs   = {
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------"
            }
        )
    )
    
class AppUpdate(forms.Form):
    external_id     = forms.IntegerField(
        required    = True,
        widget      = forms.TextInput(
            attrs   = {
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------",
                "readonly"      : "readonly"
            }
        )
    )
    
    application     = forms.IntegerField(
        required    = True,
        widget      = forms.TextInput(
            attrs   = {
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------",
                "readonly"      : "readonly"
            }
        )
    )
    
    name    = forms.CharField(
        widget  = forms.TextInput(
            attrs   = {
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------"
            }
        )
    )