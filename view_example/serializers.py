from rest_framework import serializers
from django.contrib.auth import get_user_model


"""
This is the generic way to get 
a user model - if you set up
user models properly,
this model is derived from
the SETTINGS file in
the "core" app.
"""
User = get_user_model()


class UserCreationSerializer(serializers.Serializer):
	"""
	This is a construct from the django rest framework
	library. it's for data validation
	"""
	first_name = serializers.CharField(max_length=255)
	last_name = serializers.CharField(max_length=255)
	email = serializers.EmailField(max_length=255)



	"""
	the method names have to match
	the provided field attributes.
	They are not required, just optional
	"""
	def validate_email(self, data):
		u = User.objects.filter(email=data)
		if u.exists():
			raise serializers.ValidationError(
				"User with this email already exists"
				)
		else:
			return data

	def validate(self, data):
		"""
		This is the last validate method called,
		after the process is triggered by the .is_valid()
		method. Use it to validate inputs against one another.
		"""

		first_name, last_name = data['first_name'], data['last_name']
		q = User.objects.filter(first_name=first_name,
			last_name=last_name)
		if q.exists():
			raise serializers.ValidationError(
				"""
			A User with this first name last name
			combination already exists.
				"""
			)
		return data
