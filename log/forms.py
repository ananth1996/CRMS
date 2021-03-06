from django import forms
from .models import Student,Faculty
from django.contrib.auth import login,authenticate


class LoginForm(forms.Form):
	username = forms.CharField(max_length=255, required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if not user :
			raise forms.ValidationError("Username and Password Dont Match")
		elif not user.is_active:
			raise forms.ValidationError("Your Account Has Been Made Inactive Please Contact Admin")
		return self.cleaned_data

	def login(self, request):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		return user


class addStudForm(forms.ModelForm):

	password=forms.CharField(min_length=8,max_length=30,widget=forms.PasswordInput(attrs={'class': 'form-control' }))

	def __init__(self,*args,**kwargs):
		super(addStudForm, self).__init__(*args, **kwargs)
		self.fields['name'].required = True
		self.fields['dno'].label = "Department"
		self.fields['dno'].required = True




	class Meta:
		model = Student
		fields = ['name','usn','dno']


class addFacForm(forms.ModelForm):

	password=forms.CharField(min_length=8,max_length=30,widget=forms.PasswordInput(attrs={'class': 'form-control' }))

	def __init__(self,*args,**kwargs):
		super(addFacForm, self).__init__(*args, **kwargs)
		self.fields['name'].required = True
		self.fields['dno'].label = "Department"
		self.fields['dno'].required = True




	class Meta:
		model = Faculty
		fields = ['name','facultyid','dno']



class addPerForm(forms.Form):

	password=forms.CharField(min_length=8,max_length=30,widget=forms.PasswordInput(attrs={'class': 'form-control' }))
	username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control'}))
	name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control'}))
