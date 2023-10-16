from django.contrib import admin

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import signup,signin,show_user,jobpost,candidatemore,employermore,home,applied,show_applied,showdetail,displaydel,questions,choose,resume,candidate_status_mail,update_candidate,update_employer,delete_jobpost,logout,dashboard,jobsapplied,seeposted,resp,delete_job,cand_profile,feedback,send_message_users
urlpatterns = [
    path('signup',signup,name='signup'),
    path('signin',signin,name='signin'),
    path('show',show_user,name='show'),
    path('jobpost',jobpost,name='jobpost'),
    path('canddel',candidatemore,name='canddel'),
    path('empdel',employermore,name='empdel'),
    path('',home,name='home'),
    path('applied/<int:id>',applied,name='applied'),
    path('showapply',show_applied,name='showapply'),
    path('showdel',showdetail,name='showdel'),
    path('del/<str:user_id>/<int:jobid>',displaydel,name='del'),
    path('quest/<int:id>',questions,name='quest'),
    path('choice',choose,name='choice'),
    path('pdf/', resume,name='resume'),
    path('mail/<int:jobid>/<str:user_id>/<int:id>',candidate_status_mail,name='mail'),
    path('update',update_candidate,name='update'),
    #path('update_emp',update_employer,name='update_emp'),
    path('delete_jobpost',delete_jobpost,name='delete_jobpost'),
    path('logout',logout,name='logout'),
    path('dashboard',dashboard,name='dashboard'),
    path('jobsapplied',jobsapplied,name='jobsapplied'),
    path('posted',seeposted,name='posted'),
    path('res',resp,name='res'),
    path('deletejob/<int:id>',delete_job,name='deletejob'),
    path('profile_candidate',cand_profile),
    path('feedback',feedback),
    path('msg/<str:user_id>/<int:id>',send_message_users)

]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)