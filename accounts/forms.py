from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
User = get_user_model()


# Sign Up Form
class RegisterForm(UserCreationForm):

    # BOT CATCHER
        botcatcher = forms.CharField(required=False, widget=forms.HiddenInput)
        def clean_botcatcher(self):
            botcather = self.cleaned_data['botcatcher']
            if len(botcather)>0:
                raise forms.ValidationError('Something went wrong, try again!')
            return botcather
    #///

        def clean_first_name(self):
            return self.cleaned_data['first_name'].capitalize()

        def clean_last_name(self):
            return self.cleaned_data['last_name'].capitalize()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['email'].widget.attrs.update({'autofocus': False})
            self.fields['first_name'].widget.attrs.update({'autofocus': True})

        class Meta:
            model = User
            fields = [
                'first_name', 
                'last_name', 
                'email', 
                'password1', 
                'password2',
                ]



# Edit Profile Form
class ProfileForm(forms.ModelForm):

    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()

    birth_date = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder':'dd/mm/yyyy'} ),
        # attrs={'label':'dd/mm/yyyy'},
        # attrs={'class':'datepicker'},
        input_formats=('%d/%m/%Y', ),
        label='dd/mm/yyyy',
        )
         

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].required = False

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'birth_date',
            'email',
            'profile_pic',
            ]

from django.contrib.auth.forms import SetPasswordForm

class SetPasswordUserForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']


#RECOVER PASSWORD
from django.contrib.auth.forms import PasswordResetForm

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': True})
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())