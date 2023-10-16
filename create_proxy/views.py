from .utils import render_to_pdf
from django.views.generic import View
from django.db import IntegrityError

from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .form import UserForm, EmployerForm, CandidateForm, JobPostForm, questform, email_Form,feedbackform
from django.contrib.auth import login, authenticate, logout as logout_auth
from django.contrib.auth.decorators import login_required
from .models import JobPost, applied_jobs, User, CandidateMore, EmployerMore, Questions,Feedback
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View
from django import template
from django.template.defaultfilters import stringfilter
from .models import Employer, User
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from datetime import date
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import send_mail
from django.db.models import Count

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np





def resp(request):
    return render(request,'responsive.html')


# Create your views here.
def signup(request):

    form = UserForm
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            print('valid')

            user = form.save()
            user.refresh_from_db()
            raw_password = form.cleaned_data.get('password')
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if user.type == 'EMPLOYER':
                messages.success(request,'Registered Successfully')
                return redirect('/empdel')
            else:
                messages.success(request, 'Registered Successfully')
                return redirect('/canddel')
        else:
            print('INVALID')
    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        messages.success(request,'You are Already Login-In')
        return redirect('/profile_candidate')
    else:
        form = AuthenticationForm()
        if request.method == "POST":
            email = request.POST['username']
            password = request.POST['password']
            # email = request.POST['email']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)

                if user.type == 'EMPLOYER':
                    messages.info(request, 'You logged in.')
                    return redirect('/choice')
                else:
                    messages.info(request, 'You logged in.')
                    return redirect('/')

            else:
                messages.error(request,'Invalid Credentials. User does not exist')
                #return render(request, 'signin.html', {'form': form})
                return redirect('/signin')
        else:
            print("Something went wrong")
        return render(request, 'signin.html', {'form': form})


@login_required(login_url='/signin')
def show_user(request):
    name = request.user.type
    n1 = request.user.username
    print(n1)
    if name == 'EMPLOYER':
        return HttpResponse('<h1>Employer Page</h1>')
    elif name == 'CANDIDATE':
        return HttpResponse('<h1>Candidate Page</h1>')
    else:
        return redirect('/')
    #return render(request, 'show.html', {'name': name})


@login_required(login_url='/signin')
def candidatemore(request):

    form = 'You are not a User'
    if request.user.type == 'CANDIDATE':
        form = CandidateForm()

        if request.method == 'POST':
            form = CandidateForm(request.POST, request.FILES or None)
            if form.is_valid():
                details = form.save(commit=False)
                user = request.user
                details.user = user
                #upload = request.FILES['uplaod_cv']
                #details.upload_cv =upload
                details.save()

                emails=user
                subject = 'Welcome To Job Praise'
                message = f'Hello {details.full_name}, Thank you for creating an account at Job Praise. Explore exiting and interesting job offers!!! If you think someone else has used your email id to register this account please contact us at siddhishirke@gmail.com'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [emails, ]
                send_mail(subject, message, email_from, recipient_list)
                messages.success(request, 'Details Entered Successfully and you now Signed-In')
                return redirect('/')
            else:
                messages.error(request,'Invalid Details')
                return render(request, 'details.html', {'form': form})
    return render(request, 'details.html', {'form': form})


@login_required(login_url='/signin')
def update_candidate(request):
    if request.user.type == 'CANDIDATE':
        obj = get_object_or_404(CandidateMore, user_id=request.user.id)
        form = CandidateForm(request.POST or None, request.FILES or None, instance=obj, )
        if form.is_valid():
            form.save()
            messages.success(request, 'Details Updated Successfully')
            return redirect('/choice')
    if request.user.type == 'EMPLOYER':
        obj = get_object_or_404(EmployerMore, user_id=request.user.id)
        form = EmployerForm(request.POST or None, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Details Updated Successfully')
            return redirect('/choice')

    return render(request, 'update.html', {'form': form})


@login_required(login_url='/signin')
def delete_jobpost(request):
    list_del = []
    object = JobPost.objects.filter(user_id=request.user.id)
    print(object, 'Before')
    for i in object:
        if i.last_date_of_applying < date.today():
            i.delete()

    print(object, 'After')
    messages.success(request, 'Jobs Deleted Successfully')
    return redirect('/choice')

def delete_job(request,id):
    job=JobPost.objects.get(id=id)
    job.delete()
    messages.success(request,'Job Deleted Successfully')
    return redirect('/choice')


@login_required(login_url='/signin')
def employermore(request):
    form = 'You are not a user'
    if request.user.type == 'EMPLOYER':
        form = EmployerForm()
        if request.method == 'POST':
            form = EmployerForm(request.POST,request.FILES or None)
            if form.is_valid():
                details = form.save(commit=False)
                user = request.user
                details.user = user
                details.save()
                emails = request.user
                subject = 'Welcome To Job Praise'
                message = f'Hello {details.name_of_company}, Thank you for creating an account as an Employer at Job Praise. Get amazing candidates for your companies and post exiting job offers!!! If you think someone else has used your email id to register this account please contact us at siddhishirke@gmail.com'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [emails, ]
                send_mail(subject, message, email_from, recipient_list)
                messages.success(request, 'Details Entered Successfully and you now Signed-In')
                return redirect('/')
            else:
                return render(request, 'details.html', {'form': form})
    return render(request, 'details.html', {'form': form})


@login_required(login_url='/signin')
def update_employer(request):
    obj = get_object_or_404(EmployerMore, user_id=request.user.id)
    form = EmployerForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request,'Updated Successfully')
        return redirect('/')

    return render(request, 'update.html', {'form': form})


@login_required(login_url='/signin')
def jobpost(request):
    name = request.user.type
    email = request.user
    if name == 'EMPLOYER':
        cname1 = EmployerMore.objects.get(user_id=request.user) #initial={"name_of_comp":}
        cname = cname1.name_of_company
        print(cname1.name_of_company)
        form = JobPostForm()
        if request.method == 'POST':
            form = JobPostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                email = request.user
                print(email)
                post.user = email
                post.save()
                messages.success(request, 'Job Posted Successfully')
                return redirect('/choice')
            else:
                messages.error(request,'Invalid Details')

    else:
        return HttpResponse('<h1>You not an employer</h1> <a href="/signin">Go Back</a>')
    return render(request, 'employer/post.html', {'form': form})

@login_required(login_url='/signin')
def seeposted(request):
    posted = JobPost.objects.filter(user=request.user)
    print(posted)
    return render(request,'posted.html',{'posted':posted})


def home(request):
    listopt =[]
    if request.method == "POST":
        search = request.POST['searched']
        print(search)
        obj = (JobPost.objects.filter(skills_required__icontains = search) | JobPost.objects.filter(location__icontains = search) | JobPost.objects.filter(job_title__icontains = search ) | JobPost.objects.filter(job_type__icontains = search ) | JobPost.objects.filter(job_description__icontains = search ) | JobPost.objects.filter(salary__icontains = search ))
        print(obj)
        if obj:
            for i in obj:
                if i.last_date_of_applying > date.today():
                    listopt.append(i)

        return render(request,'search.html',{'search': search,'obj':listopt})
    else:
        return render(request,'home.html')

def dashboard(request):
    num_of_users = User.objects.all().count()
    num_of_candidates = User.objects.filter(type='CANDIDATE').count()
    num_of_employer = User.objects.filter(type='EMPLOYER').count()
    num_of_company= EmployerMore.objects.all().count()
    num_of_jobpost = JobPost.objects.all().count()
    num_of_applied_jobs = applied_jobs.objects.all().count()
    selected_num_candidates = applied_jobs.objects.filter(status ='selected').count()
    print(selected_num_candidates,'MEE')
    frequent_title = JobPost.objects.values_list('job_title').annotate(freq_val=Count('job_title')).order_by('-freq_val')[0]
    print("Title" , frequent_title)
    frequent_location = JobPost.objects.values_list('location').annotate(freq_loc=Count('location')).order_by('-freq_loc')[0]
    frequent_title1 = JobPost.objects.values_list('job_title').annotate(freq_val=Count('job_title')).order_by('-freq_val')
    a=[]
    b=[]
    for i in frequent_title:
        a.append(frequent_title1[0])
        b.append(frequent_title1[1])
    print(a ," a" , b,"b")



    # demand_skills1 = JobPost.objects.values_list('skills_required').annotate(freq_skills1=Count('skills_required')).order_by('-freq_skills1')[0]
    # demand_skills2 = JobPost.objects.values_list('skills_required').annotate(freq_skills2=Count('skills_required')).order_by('-freq_skills2')[1]
    # demand_skills3 = JobPost.objects.values_list('skills_required').annotate(freq_skills3=Count('skills_required')).order_by('-freq_skills3')[2]
    # d1 = demand_skills1[0]
    # d2 = demand_skills2[0]
    # d3 = demand_skills3[0]
    # print(demand_skills1,demand_skills2,demand_skills3)
    frequent_comp = JobPost.objects.values_list('user_id').annotate(freq_comp = Count('user_id')).order_by('-freq_comp')[0]

    obj = EmployerMore.objects.get(user_id=frequent_comp[0])
    print(obj.name_of_company,"Here")

    title = frequent_title[0]
    location = frequent_location[0]
    #Get Company Name
    comp_name = JobPost.objects.values_list('user_id').annotate(freq_comp = Count('id')).order_by('-freq_comp')
    print(comp_name)
    lst =[]
    for i in comp_name:
        lst.append(i[0])
    print(lst)
    obj12 = JobPost.objects.all()
    for i in obj12:
        print(i.comp_name)

    context = {'usercount':num_of_users,'jobcount':num_of_jobpost,'countapplied':num_of_applied_jobs,'title':title,'location':location,'company1':obj,'select':selected_num_candidates,'candidate':num_of_candidates,'employer':num_of_employer,'company':num_of_company,'cname':frequent_title1}
    return render(request,'dashboard.html',context)

@login_required(login_url='/signin')
def applied(request,id):
    name1 = request.user.username

    if request.user.type == 'CANDIDATE':
        print(name1)
        post = JobPost.objects.get(id=id)
        user = User.objects.get(id=post.user_id)
        user1 = CandidateMore.objects.get(user_id = request.user)
        print(post, 'POST')
        print(user1,'user1')
        name = request.user.type
        name1 = request.user.email
        print(name1, 'I')
        try:
            apply = applied_jobs.objects.create(candidate=user1, post=post, employer=user)

            apply.save()
            messages.success(request,'Applied Successfully')
            # return redirect('/quest')
            return render(request, 'fillQ.html', {'post': post})
        except IntegrityError:
            return HttpResponse('<h2>Exception: You have already applied to this job</h2><a href="/">Go Back</a> <br> <a href="/jobsapplied" > Check Applied</a>')
    else:
        return HttpResponse('<h1>You are not a candidate</h1> <a href="/signin">Go Back</a>')
    # return render(request, 'apply.html', {'name': name1})


@login_required(login_url='/signin')
def show_applied(request):
    if request.user.type == 'EMPLOYER':
        user = request.user.username
        return HttpResponse(user)
    else:
        return HttpResponse('<h1>You not an employer</h1> <a href="/signin">Go Back</a>')


@login_required(login_url='/signin')
def showdetail(request):

    if request.user.type == 'EMPLOYER':

        details = applied_jobs.objects.filter(employer_id=request.user.id)

        return render(request, 'appliedcanddel.html', {'data': details})
    else:
        return HttpResponse('<h1>You are not a Employer</h1>')

@login_required(login_url='/signin')
def send_message_users(request,user_id,id):
    if request.method=='POST':
        print(user_id)
        obj = applied_jobs.objects.get(id=id)
        jobname=obj.job_title
        subject ='Message from employer'
        message = request.POST['msg'] + ' Message by {} and the job post applied was {}. You can reply to the employer on their email id'.format(request.user,jobname)
        emails =user_id
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [emails,]
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request,'Message send through Mail successfully !!!')
    return render(request,'msg.html')




@login_required(login_url='/signin')
def displaydel(request, user_id, jobid):
    dis_del = User.objects.get(email=user_id)
    print(dis_del)
    disCan = CandidateMore.objects.get(user_id=dis_del.id)
    print(disCan,'CandidateMore')
    questdel = Questions.objects.filter(jobpost_id=jobid,user_id=dis_del.id)
    obj = (applied_jobs.objects.get(candidate=disCan, post_id=jobid))
    print(jobid, obj, 'HEY')
    if request.user.type == 'EMPLOYER':
        if request.method == 'POST':
            status = request.POST['status']
            print(status)
            print(type(status))
            obj.status = status
            obj.save()
        print(obj.status)
    return render(request, 'showdel.html', {'display': dis_del, 'cand': disCan, 'q': questdel, 'appliedjobs': obj})



@login_required(login_url='/signin')
def questions(request, id):
    post = JobPost.objects.get(id=id)
    if request.user.type == 'CANDIDATE':
        form = questform()
        if request.method == 'POST':
            form = questform(request.POST)
            if form.is_valid():
                quest = form.save(commit=False)
                email = request.user
                print(email)
                quest.user = email
                quest.jobpost = post
                quest.save()
                messages.success(request,'Your response is recorded')
            return redirect('/')
    else:
        form = 'You are not a candidate'
    return render(request, 'quest.html', {'form': form})


@login_required(login_url='/signin')
def choose(request):
    if request.user.type == 'EMPLOYER':
        return render(request, 'choose.html')
    if request.user.type == 'CANDIDATE':
        return render(request, 'choice.html')
    return HttpResponse('<h1>Hello</h1>')



@login_required(login_url='/signin')
def resume(request):
    candidate = User.objects.get(id=request.user.id)
    moredetail = CandidateMore.objects.get(user_id=request.user.id)
    pdf = render_to_pdf('resume.html', {'candidate': candidate, 'more': moredetail})
    return HttpResponse(pdf, content_type='application/pdf')

@login_required(login_url='/signin')
def jobsapplied(request):
    user1 = CandidateMore.objects.get(user_id=request.user)
    applied = applied_jobs.objects.filter(candidate=user1)
    print(applied)
    return render(request,'jobsapplied.html',{'applied':applied})

@login_required(login_url='/signin')
def candidate_status_mail(request, user_id, jobid, id):
    user_id = user_id
    jobid = jobid
    # apply = ((applied_jobs.objects.filter(candidate=user_id)) & (applied_jobs.objects.filter(post_id=jobid)))
    # print(apply)
    # status = applied_jobs.objects.get()
    obj = applied_jobs.objects.get(id=id)

    status = obj.status
    jobname = obj.job_title
    ename = obj.employer
    print(obj.status)
    print(jobid)
    # messages.success(request, f'Your  You are now able to log in')
    if obj.status =='in-touch':
        subject = 'This mail is to inform you about your job application status'
        message = 'Your status of the applied job which is {} is {}. Contact your employer for further details {}'.format(jobname, status,ename)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_id, ]
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request,'Mail Sent Successfully')
    elif obj.status =='rejected':
        subject = 'This mail is to inform you about your job application status'
        message = 'Your status of the applied job which is {} is {}.'.format(jobname, status)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_id,]
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request, 'Mail Sent Successfully')
    elif obj.status =='Applied':
        subject = 'This mail is to inform you about your job application status'
        message = 'Your status of the applied job which is {} is {}.'.format(jobname, status)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_id, ]
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request, 'Mail Sent Successfully')

    else:
        subject = 'This mail is to inform you about your job application status'
        message = 'Your status of the applied job which is {} is {}. Contact your employer for further details {}'.format(
            jobname, status, ename)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_id, ]
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request, 'Mail Sent Successfully')
    return redirect('/')



def logout(request):
    if request.user.is_authenticated:
        logout_auth(request)
        messages.success(request,'You logged out')
        return redirect('/signin')
    else:
        messages.error(request,'You are not logged in. Please Login In')
        return redirect('/signin')


#@login_required(login_url='/signin')
def cand_profile(request):
    link=''
    if request.user.is_authenticated:
        if request.user.type=='CANDIDATE':
            try:
                user = CandidateMore.objects.get(user_id=request.user.id)
            except:
                user =None
                link ='/canddel'

            return render(request,'profile.html',{'user':user,'link':link})
        elif request.user.type=='EMPLOYER':
            try:
                user = EmployerMore.objects.get(user_id=request.user.id)
            except:
                user =None
                link='/empdel'
            return render(request,'profile1.html',{'user':user,'link':link})
    else:
        messages.error(request, 'You are not logged in. Please Login In')
        return redirect('/signin')

@login_required(login_url='/signin')
def feedback(request):
    form = feedbackform()
    if request.method == 'POST':
        form = feedbackform(request.POST)
        if form.is_valid():
            feedback1 = form.save(commit=False)
            email = request.user
            feedback1.user = email
            feedback1.save()
            messages.success(request, 'Your response is recorded')
        return redirect('/')
    return render(request,'feedback.html',{'form':form})