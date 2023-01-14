from django import forms

class Register(forms.Form):
    roles   = forms.IntegerField(
        required    = False,
        widget      = forms.TextInput(
            attrs   = {
                "type"          : "text",
                "class"         : "form-control",
                "placeholder"   : "------"
            }
        )
    )
    
    applications    = forms.IntegerField(
        required    = False,
        widget      = forms.TextInput(
            attrs   = {
                "type"          : "text",
                "class"         : "form-control",
                "placeholder"   : "------"
            }
        )
    )
    
    firstname   = forms.CharField(
        widget  = forms.EmailInput(
            attrs   = {
                "type"          : "text",
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------"
            }
        )
    )
    
    lastname    = forms.CharField(
        required    = False,
        widget      = forms.EmailInput(
            attrs   = {
                "type"          : "text",
                "class"         : "form-control",
                "placeholder"   : "------"
            }
        )
    )
    
    phone_number    = forms.CharField(
        required    = False,
        widget      = forms.TextInput(
            attrs   = {
                "type"          : "tel",
                "class"         : "form-control",
                "placeholder"   : "------"
            }
        )
    )
    
    address = forms.CharField(
        widget      = forms.TextInput(
            attrs   = {
                "type"          : "textarea",
                "class"         : "form-control",
                "placeholder"   : "------"
            }
        )
    )
    
    email   = forms.CharField(
        widget  = forms.EmailInput(
            attrs   = {
                "type"          : "text",
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------"
            }
        )
    )
    
    secret_key  = forms.CharField(
        widget  = forms.PasswordInput(
            attrs   = {
                "type"          : "password",
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------"
            }
        )
    )
    
    re_password = forms.CharField(
        widget  = forms.PasswordInput(
            attrs   = {
                "type"          : "password",
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------"
            }
        )
    )
    
    def clean_roles(self):
        return 789878
    
    def clean_applications(self):
        return 456789
    
    def clean_re_password(self):
        password    = self.cleaned_data.get("secret_key")
        re_password = self.cleaned_data.get("re_password")
        print(password)
        if password != re_password:
            raise forms.ValidationError("Not match with password")
        
        return re_password

class Login(forms.Form):
    email   = forms.CharField(
        widget  = forms.EmailInput(
            attrs   = {
                "type"          : "text",
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------"
            }
        )
    )
    
    password   = forms.CharField(
        widget  = forms.PasswordInput(
            attrs   = {
                "type"          : "password",
                "class"         : "form-control",
                "required"      : "required",
                "placeholder"   : "------"
            }
        )
    )
    
    def clean_email(self):
        if not self.cleaned_data.get("email"):
            raise forms.ValidationError("Email must not be empty")
        
        return self.cleaned_data.get("email")
    
    def clean_password(self):
        if not self.cleaned_data.get("password"):
            raise forms.ValidationError("Password must not be empty")
        
        return self.cleaned_data.get("password")