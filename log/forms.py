from django import forms
from .models import Student,Faculty



class LoginForm(forms.Form):
	username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username' }))
	password=forms.CharField(min_length=8,max_length=30,widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password' }))



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