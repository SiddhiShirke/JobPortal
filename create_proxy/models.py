from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import date,datetime
from django.utils import timezone

import datetime
# Create your models here.

today = timezone.now
class User(AbstractUser):
    class Types(models.TextChoices):
        EMPLOYER = "EMPLOYER",'Employer'
        CANDIDATE = 'CANDIDATE','Candidate'

    type = models.CharField(max_length=50, choices=Types.choices,default=Types.CANDIDATE)
    name = models.CharField(_('Name of User'),blank=True,max_length=255)
    email = models.EmailField(_('Enter Your Email Id'), unique=True,
                              error_messages={
                                  "unique":"Email ID already exists"
                              }
                              )
    username = models.CharField(max_length=250)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','type']
    EMAIL_FIELD = 'email'






class EmployerManager(models.Manager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=User.Types.EMPLOYER)


class Employer(User):
    base_type = User.Types.EMPLOYER
    objects = EmployerManager()
    class Meta:
        proxy =True
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type= User.Types.EMPLOYER
        return super().save(*args,**kwargs)


def only_int(value):
    if value.isdigit() == False:
        raise ValidationError('Contact Number Contains Charaters')
    if len(value) != 10:
        raise ValidationError('Contact Number should be of 10 digits ')

def present_future_dates(value):
    if value < date.today():
        raise ValidationError('Cannot Enter Past Dates')

def no_future_present_dates(value):
    obj = date.today()
    obj1 = obj.year - 18
    if value.year > obj1:
        print("True")
        raise ValidationError('You seem to be young or you have entered wrong birth date')

class CandidateManager(models.Manager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=User.Types.CANDIDATE)


class Candidate(User):
    base_type = User.Types.CANDIDATE
    objects = CandidateManager()
    @property
    def more(self):
        return self.candidatemore

    class Meta:
        proxy = True



    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.CANDIDATE
        return super().save(*args,**kwargs)

class EmployerMore(models.Model):
    user = models.OneToOneField(Employer, on_delete=models.CASCADE)
    name_of_company = models.CharField(max_length=30, null=False,unique=True)
    website = models.CharField(max_length=500, null=False)
    contact_number = models.CharField(null=False, validators=[only_int], max_length=10)
    company_email_id = models.EmailField(unique=False, null=False)
    company_address=models.CharField(max_length=200,default='')
    upload_photo = models.ImageField(upload_to='profile1_image', blank=True)

    def __str__(self):
        return self.user.email
class JobPost(models.Model):
    pa_pm=[('p.m.','Monthly'),('p.a.','Annual')]
    jobtype=[('1-months-internship','1-Months Internship'),
             ('2-months-internship', '2-Months Internship'),('3-months-internship','3-Months Internship'),('4-months-internship','4-Months Internship'),('5-months-internship','5-Months Internship'),('6-months-internship','6-Months Internship'),('7-months-internship','7-Months Internship'),('8-months-internship','8-Months Internship'),('9-months-internship','9-Months Internship'),('10-months-internship','10-Months Internship'),('11-months-internship','11-Months Internship'),('12-months-internship','12-Months Internship'),
        ('full-time','Full-Time'),('part-time','Part-Time')]
    total_working_hours=models.CharField(max_length=200,default='12hrs')
    user = models.ForeignKey(Employer,on_delete=models.CASCADE)  #foreign key
    job_type=models.CharField(max_length=50,choices=jobtype,default='full-time')
    job_title= models.CharField(max_length=100)
    job_description=models.CharField(max_length=200,default=' ')
    location = models.CharField(max_length=100)
    skills_required = models.CharField(max_length=255)
    salary = models.PositiveIntegerField()
    monthly_annually= models.CharField(_('Monthly or Annual'),max_length=20,choices=pa_pm,default='p.a')
    last_date_of_applying = models.DateField(validators=[present_future_dates])

    def __str__(self):
        return self.job_title
    @property
    def comp_name(self):
        return self.user

class CandidateMore(models.Model):
    gender = [('male', 'Male'), ('female', 'Female'), ('not_say', 'Decline to answer')]
    status = [('married', 'Married'), ('unmarried', 'Unmarried')]
    degree = [('10th', 'Secondary (10th Pass)'),
              ('12th Science', 'Higher Secondary(Science 12th Pass )'),
              ('12th Commerce', 'Higher Secondary(Commerce 12th Pass)'),
              ('12th Arts', 'Higher Secondary(Arts 12th Pass)'),
              ('BCA', 'Bachelor of Computer Applications'),
              ('BBA', 'Bachelor of Business Administration'),
              ('BBM', 'Bachelor of Business Management'),
              ('MCA', 'Master of Computer Application'),
              ('MBA', 'Master of Business Administration'),
              ('BSE', 'Bachelor of Software Engineering'),
              ('B.A', 'Bachelor of Arts'),
              ('B.TECH', 'Bachelor of Technology')]
    # first_name = models.CharField(max_length=30)
    # middle_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)
    user = models.OneToOneField(Candidate,on_delete=models.CASCADE)
    upload_photo=models.ImageField(upload_to='profile_image',blank=True)
    full_name = models.CharField(max_length=100,default='')
    birth_date = models.DateField(validators=[no_future_present_dates])
    gender = models.CharField(max_length=30, choices=gender, null=False)
    marital_status = models.CharField(max_length=30, choices=status, null=False)
    qualification = MultiSelectField(choices=degree)
    contact_number = models.CharField(max_length=10, validators=[only_int])
    hobbies = models.CharField(max_length=100)
    skills =models.CharField(max_length=100)
    objective =models.CharField(max_length=500)
    upload_cv = models.FileField(upload_to='media', blank=True,null=True)

    def __str__(self):
        return self.user.email



class applied_jobs(models.Model):
    status=[('in-touch', 'In-Touch'), ('Selected', 'selected'),('Rejected','rejected')]
    candidate = models.ForeignKey(CandidateMore,on_delete=models.CASCADE,default='-1')
    post = models.ForeignKey(JobPost,on_delete=models.CASCADE,default='-1')
    employer = models.ForeignKey(User,on_delete=models.CASCADE,default='-1')
    status = models.CharField(max_length=50,choices=status,default='Applied')
    applied_date=models.DateField(default=today)


    class Meta:
        unique_together=('candidate','post',)
    def __str__(self):
        return '{}  {}  {} '.format(self.candidate,self.post,self.employer)
    @property
    def job_title(self):
        return self.post.job_title

class Questions(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    q1=models.TextField(_('What are your strengths and weakness?'),max_length=250,blank=False)
    q2 = models.TextField(_('Describe your past experience in detail or any project that you have done related to our job profile if not then type N.A.'),max_length=250,blank=False)
    q3 = models.TextField(_('When could you start?'),blank=False,max_length=200)
    q4 = models.TextField(_('How will you handle stressfull situation. Lets say deadline is near and teammates are not working properly?'),max_length=250, blank=True)
    q5 = models.TextField(_('What all things do you consider when you have to be quick while making a decision?'),max_length=250, blank=True)
    q6 = models.TextField(_('What are your short terms and long terms goals?'), max_length=250, blank=True)
    q7 = models.TextField(_('Describe honesty in your own words.And tell me a situation where you chose to be honest instead of a lie'),max_length=250, blank=True)
    #q8 = models.TextField(_('When could you start?'), blank=True, max_length=200)
    jobpost = models.ForeignKey(JobPost,on_delete=models.CASCADE)

    def __str__(self):
        return '{}  {}'.format(self.user.email, self.jobpost)
    class Meta:
        unique_together =('user','jobpost')

experience = [
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5')
]
class Feedback(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    q1 = models.TextField(_('How can we improve our system?'),max_length=500,blank=False)
    q2 = models.TextField(_('What difficulties have you faced while using the website?'),max_length=500,blank=False)
    q3 = models.CharField(_('how_would_rate_your_overall_experience_with_Job_Praise'),max_length=250,choices=experience,default=1)

    def __str__(self):
        return 'Feedback from {} {}'.format(self.user.email,self.user.type)

