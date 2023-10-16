from django.test import SimpleTestCase
from django .urls import reverse,resolve
from create_proxy.views import signup,signin,show_user,jobpost,candidatemore,employermore,home,applied,show_applied,showdetail,displaydel,questions,choose,resume,candidate_status_mail,update_candidate,update_employer,delete_jobpost,logout,dashboard,jobsapplied,seeposted,resp,delete_job



class TestUrls(SimpleTestCase):

    def test_home_url(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func,home)

    def test_signup_url(self):
        url = reverse('signup')
        print(resolve(url))
        self.assertEquals(resolve(url).func,signup)

    def test_show_url(self):
        url = reverse('show')
        print(resolve(url))
        self.assertEquals(resolve(url).func,show_user)

    def test_signin_url(self):
        url = reverse('signin')
        print(resolve(url))
        self.assertEquals(resolve(url).func,signin)

    def test_jobpost_url(self):
        url = reverse('jobpost')
        print(resolve(url))
        self.assertEquals(resolve(url).func,jobpost)

    def test_canddel_url(self):
        url = reverse('canddel')
        print(resolve(url))
        self.assertEquals(resolve(url).func,candidatemore)

    def test_empdel_url(self):
        url = reverse('empdel')
        print(resolve(url))
        self.assertEquals(resolve(url).func,employermore)

    def test_applied_url(self):
        url = reverse('applied',args=[12])
        print(resolve(url))
        self.assertEquals(resolve(url).func,applied)

    def test_showapply_url(self):
        url = reverse('showapply')
        print(resolve(url))
        self.assertEquals(resolve(url).func,show_applied)

    def test_showdel_url(self):
        url = reverse('showdel')
        print(resolve(url))
        self.assertEquals(resolve(url).func,showdetail)

    def test_del_url(self):
        url = reverse('del',args=['user',12])
        print(resolve(url))
        self.assertEquals(resolve(url).func,displaydel)

    def test_quest_url(self):
        url = reverse('quest',args=[12])
        print(resolve(url))
        self.assertEquals(resolve(url).func,questions)

    def test_choice_url(self):
        url = reverse('choice')
        print(resolve(url))
        self.assertEquals(resolve(url).func,choose)

    def test_resume_url(self):
        url = reverse('resume')
        print(resolve(url))
        self.assertEquals(resolve(url).func,resume)

    def test_updatecand_url(self):
        url = reverse('update')
        print(resolve(url))
        self.assertEquals(resolve(url).func,update_candidate)

    # def test_updateemp_url(self):
    #     url = reverse('update_emp')
    #     print(resolve(url))
    #     self.assertEquals(resolve(url).func,update_employer)

    def test_delete_jobpost_url(self):
        url = reverse('delete_jobpost')
        print(resolve(url))
        self.assertEquals(resolve(url).func,delete_jobpost)

    def test_logout_url(self):
        url = reverse('logout')
        print(resolve(url))
        self.assertEquals(resolve(url).func,logout)

    def test_dashboard_url(self):
        url = reverse('dashboard')
        print(resolve(url))
        self.assertEquals(resolve(url).func,dashboard)

    def test_jobsapplied_url(self):
        url = reverse('jobsapplied')
        print(resolve(url))
        self.assertEquals(resolve(url).func,jobsapplied)

    def test_posted_url(self):
        url = reverse('posted')
        print(resolve(url))
        self.assertEquals(resolve(url).func,seeposted)

    def test_res_url(self):
        url = reverse('res')
        print(resolve(url))
        self.assertEquals(resolve(url).func,resp)

    def test_delete_url(self):
        url = reverse('deletejob',args=[12])
        print(resolve(url))
        self.assertEquals(resolve(url).func,delete_job)

    def test_mail_url(self):
        url = reverse('mail',args=[12,'user',12])
        print(resolve(url))
        self.assertEquals(resolve(url).func,candidate_status_mail)