from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomUserCreationForm(forms.Form):
	first_name = forms.CharField(max_length=255)
	last_name = forms.CharField(max_length=255)
	email = forms.EmailField(max_length=255)

	def clean_email(self):
		data = self.cleaned_data=['email']
		u = User.objects.filter(email=data)
		if u.exists():
			raise ValidationError(
				"User with this email already exists"
				)
		else:
			return data
	def clean(self):
		"""
		This is the last validate method called,
		after the process is triggered by the .is_valid()
		method. Use it to validate inputs against one another.
		"""

		data = self.cleaned_data
		first_name, last_name = data['first_name'], data['last_name']
		q = User.objects.filter(first_name=first_name,
			last_name=last_name)
		if q.exists():
			raise ValidationError(
				"""
			A User with this first name last name
			combination already exists.
				"""
			)
		return data
