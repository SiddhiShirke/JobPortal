import re
import datetime
from django.utils import timezone
from django import forms
from .models import User,EmployerMore,Employer,CandidateMore,Candidate,JobPost,Questions,Feedback
from datetime import date
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus.widgets import DatePickerInput
class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=200,widget=forms.PasswordInput())
    class Meta:
        model = User
        fields =('username','email','type','password','confirm_password')
        widgets ={
            'password':forms.PasswordInput
        }
    def clean(self):
        super(UserForm,self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if len(username) < 3:
            self.errors['username']=self.error_class(['Username should be of minimum 3 characters'])
        if len(password) < 8:
            self.errors['password'] = self.error_class(['Password should be minimum of 8 characters'])
        if not re.findall('\d',password):
            self.errors['password'] = self.error_class(['Password should contain atleast 1 digit'])
        if not re.findall('[A-Z]',password):
            self.errors['password'] = self.error_class(['Password should contain atleast 1 uppercase letter'])
        if not re.findall('[@#$&]',password):
            self.errors['password'] = self.error_class(['Password should contain atleast 1 of these @,#,$,& special characters'])
        if confirm_password != password:
            self.errors['password']=self.error_class(['Password and Confirm Password are not equal'])



    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class EmployerForm(forms.ModelForm):
    class Meta:
        model = EmployerMore
        exclude =['user']
        fields ='__all__'

    def clean(self):
        cleaned_data =super(EmployerForm, self).clean()
        name_of_company = self.cleaned_data.get('name_of_company')
        if (re.findall('[@#$&]',name_of_company)) or (re.findall('[@#$&]',name_of_company)) or (re.findall('\d',name_of_company)):
            self.errors['name_of_company'] = self.error_class(['Name field must contain only letter from A-Z'])


class CandidateForm(forms.ModelForm):
    class Meta:
        model = CandidateMore
        exclude =['user']
        fields = '__all__'

    def clean(self):
        cleaned_data = super(CandidateForm,self).clean()
        full_name = self.cleaned_data.get('full_name')
        if (re.findall('[@#$&]',full_name)) or (re.findall('[@#$&]',full_name)) or (re.findall('\d',full_name)):
            self.errors['full_name'] = self.error_class(['Name field must contain only letter from A-Z'])



class JobPostForm(forms.ModelForm):

    total_working_hours=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Give a range or specific hrs eg.8-10hrs'}))
    class Meta:
        model = JobPost
        exclude =['user']
        fields = ('job_type','job_title','job_description','location','skills_required','salary','total_working_hours','monthly_annually','last_date_of_applying')



    def clean(self):
        cleaned_data = super(JobPostForm,self).clean()

        e = self.cleaned_data.get('last_date_of_applying')
        sal = self.cleaned_data.get('salary')

        #print(deadline,'From Forms')
        now = datetime.date.today()
        print(now)
        # if now > deadline:
        #     print('Condition True')
        #     raise forms.ValidationError('Cannot Enter Past Dates')
        # if sal <10000000:
        #     raise ValidationError('Salary is less')


# raise ValidationError('Dates cannot be past')

class questform(forms.ModelForm):
    class Meta:
        model = Questions
        exclude =['user','jobpost']
        fields ='__all__'

class email_Form(forms.Form):
    Email=forms.EmailField()
    def __str__(self):
        return self.Email

class feedbackform(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude=['user']
        fields='__all__'
        widgets = {
            'q3': forms.RadioSelect
        }


