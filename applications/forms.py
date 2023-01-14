from django import forms

class Insert(forms.Form):
    host    = forms.URLField(
        widget  = forms.URLInput(
            attrs   = {
                "type"          : "text",
                "class"         : "form-control",
                "required"      : "",
                "placeholder"   : "------"
            }
        )
    )
    
    shortname   = forms.CharField(
        widget  = forms.TextInput(
            attrs   = {
                "type"          : "text",
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------"
            }
        )
    )
    
    description = forms.CharField(
        widget  = forms.Textarea(
            attrs   = {
                "class"         : "form-control",
                "required"      : "requried",
                "style"         : "height: 150px",
                "placeholder"   : "------"
            }
        )
    )
    
    email   = forms.EmailField(
        widget  = forms.EmailInput(
            attrs   = {
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------"
            }
        )
    )
    
class Update(forms.Form):
    external_id = forms.CharField(
        required    = False,
        widget      = forms.HiddenInput()
    )
    
    host    = forms.URLField(
        widget  = forms.URLInput(
            attrs   = {
                "type"          : "text",
                "class"         : "form-control",
                "required"      : "",
                "placeholder"   : "------"
            }
        )
    )
    
    shortname   = forms.CharField(
        widget  = forms.TextInput(
            attrs   = {
                "type"          : "text",
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------"
            }
        )
    )
    
    description = forms.CharField(
        widget  = forms.Textarea(
            attrs   = {
                "class"         : "form-control",
                "required"      : "requried",
                "style"         : "height: 150px",
                "placeholder"   : "------"
            }
        )
    )
    
    email   = forms.EmailField(
        widget  = forms.EmailInput(
            attrs   = {
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------"
            }
        )
    )
    
    def clean_external_id(self):
        return self.initial.get("external_id")
    
class SecretKey(forms.Form):
    external_id = forms.CharField(
        required    = False,
        widget      = forms.HiddenInput()
    )
    
    secret_key = forms.CharField(
        required    = False,
        widget      = forms.HiddenInput()
    )
