from django.shortcuts import render

from django.views.generic import FormView
from rest_framework import serializers, generics, permissions
from rest_framework_jwt import JSONWebTokenAuthentication


from jira import JIRA

from view_example.mixins import JIRAConnectionMixin, PostgresConnectionMixin
from view_example.serializers import UserCreationSerializer
# Create your views here.

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

class GenericPageView(TemplateView):
	"""
	This is just for rendering an html page.
	If you're doing html form validation,
	i.e. the classical django style,
	you want to redirect after a POST is done,
	unless it is an AJAX post.
	"""
	template_name = 'user_creation_page.html'


def create_user_fbv(request):
	"""
	FBV example, using a Form.
	I used the longwinded name for 
	the form because there is a generic form
	for user creation that django provides.
	I believe is is called SignupForm.
	Additionally, I believe there is
	a generic View available in the auth
	model for user creation - worth researching,
	might make your life easier depending on
	how many inputs you're dealing with.
	"""
	form = CustomUserCreationForm(request.POST or None)

			
	if request.method == 'POST':
		if form.is_valid():
			data = form.cleaned_data
			u = User.objects.create_user(
				first_name=data['first_name'],
				last_name=data['last_name'],
				email=data['email'],
			)
			conn = JIRAConnectionMixin(
				).get_jira_connection()
			combined_name = "%s.%s" % (
				data['first_name'],
				data['last_name']
				)
			creation_args
			conn.add_user(combined_name,
				data['email'],
				fullname=combined_name.replace(".",""),
				active=True
				)
			## not sure if necessary
			conn.close()
			
		return HttpResponseRedirect(reverse('generic_page'))
	context = {'form': form}
	return render(request, 'my_template.html', context)

class CreateUserView(JIRAConnectionMixin, FormView):
	"""
	The big benefit of class based views
	is that they handle a lot of stuff
	at the outset, and you just modify
	a basic set of behaviors by overriding
	a method. success_url determines
	where things get redirected to.
	"""
	template_name = 'my_form_page.html'
	form_class = CustomUserCreationForm
	success_url = '/generic_page/'

	def form_valid(self, form):
			data = form.cleaned_data
			u = User.objects.create_user(
				first_name=data['first_name'],
				last_name=data['last_name'],
				email=data['email'],
			)
			conn = self.get_jira_connection()
			combined_name = "%s.%s" % (
				data['first_name'],
				data['last_name']
				)
			creation_args
			conn.add_user(combined_name,
				data['email'],
				fullname=combined_name.replace(".",""),
				active=True
				)
			## not sure if necessary
			conn.close()

		return super().form_valid(form)


class CreateUserAPIView(JIRAConnectionMixin, generics.GenericAPIView):
	authentication_classes = [JSONWebTokenAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	"""
	This is using django REST framework.
	a "serializer" is how inputs get validated.
	With this, you'd be sending a post via JSON
	to an endpoint, and you'd control the html
	template logic separately.

	The permission classes are swappable too,
	the default is SessionAuthentication in DRF.
	JSONWebTokenAuthentication is from a library
	called djangorestframework-jwt
	"""
	def post(self, request, *args, **kwargs):

		serializer = UserCreationSerializer(request.data)
		if serializer.is_valid():
			data = serializer.validated_data
			u = User.objects.create_user(
				first_name=data['first_name'],
				last_name=data['last_name'],
				email=data['email'],
			)
			conn = self.get_jira_connection()
			combined_name = "%s.%s" % (
				data['first_name'],
				data['last_name']
				)
			creation_args
			conn.add_user(combined_name,
				data['email'],
				fullname=combined_name.replace(".",""),
				active=True
				)
			## not sure if necessary
			conn.close()
			return Response({"success": True,
				"id": u.id,
				"email": u.email,
				"first_name": u.first_name,
				"last_name": u.last_name
				}, status=status.HTTP_200_OK)
		else:
			return Response({
				"errors":serializer.errors},
				status=status.HTTP_400_BAD_REQUEST)

