from django.contrib import admin
from .models import User,Employer,Candidate, JobPost,CandidateMore,EmployerMore,applied_jobs,Questions,Feedback
# Register your models here.

admin.site.register(User)
admin.site.register(Employer)
admin.site.register(Candidate)
admin.site.register(JobPost)
admin.site.register(CandidateMore)
admin.site.register(EmployerMore)
admin.site.register(applied_jobs)
admin.site.register(Questions)
admin.site.register(Feedback)
