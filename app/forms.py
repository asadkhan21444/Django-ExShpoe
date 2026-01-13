# # forms.py
# from django import forms
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError

# class SignUpForm(forms.Form):
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)
#     email = forms.EmailField(required=True)
#     password = forms.CharField(widget=forms.PasswordInput, required=True)
#     phone = forms.CharField(max_length=15, required=True)
    
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise ValidationError("This email is already registered.")
#         return email