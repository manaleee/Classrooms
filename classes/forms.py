from django import forms
from .models import Classroom, Student
from django.contrib.auth.models import User 


#-------------------------------------------------------------------------------------------

class ClassroomForm(forms.ModelForm):
	class Meta:
		model = Classroom
		fields = [ "name", "subject", "year", "teacher" ]


#-------------------------------------------------------------------------------------------



class StudentForm(forms.ModelForm):
	class Meta:
		model = Student
		# classform --> from model
		fields = ["Classroom"]



#-------------------------------------------------------------------------------------------


# create SIGN UP 
class RegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'password']

		widgets = {
			# create password --> ******* 
			"password": forms.PasswordInput()
		}



#-------------------------------------------------------------------------------------------


class LoginForm(forms.Form):
	username = forms.CharField(required = True)
	password = forms.CharField(required = True , widget = forms.PasswordInput())


#-------------------------------------------------------------------------------------------


