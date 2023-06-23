
from django import forms

# Create your forms here.

class ContactForm(forms.Form):
	first_name = forms.CharField(max_length = 50)
	last_name = forms.CharField(max_length = 50)
	email = forms.EmailField(max_length = 150)
	message = forms.CharField(widget = forms.Textarea, max_length = 5000)
	botcatcher = forms.CharField(required=False, widget=forms.HiddenInput)

	def clean_botcatcher(self):
		botcather = self.cleaned_data['botcatcher']
		if len(botcather)>0:
			raise forms.ValidationError('Something went wrong, try again!')
		return botcather