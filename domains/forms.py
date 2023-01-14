from django import forms

class AppInsert(forms.Form):
    applications    = forms.IntegerField(
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
    
    url_name    = forms.CharField(
        required    = False,
        widget      = forms.TextInput(
            attrs   = {
                "class"         : "form-control",
                "placeholder"   : "------"
            }
        )
    )