from django.test import SimpleTestCase,TestCase
from create_proxy.form import UserForm, EmployerForm, CandidateForm, JobPostForm, questform, email_Form


class TestForms(TestCase):

    def test_jobpost_form_valid(self):
        form =JobPostForm(data={
            'user':'shraddha@gmail.com',
            'job_title':'Testing Officer',
            'job_description':'Day-to-day work will be testing and debugging the softwares',
            'location':'Mumbai',
            'skills_required':'Good with unit testing,system testing,selenium',
            'salary':35000,
            'monthly_annually':'p.m.',
            'last_date_of_applying':'2022-03-06',
            'total_working_hours':'12hrs',
            'job_type':'full-time',
        })
        self.assertTrue(form.is_valid())

    def test_jobpost_form_no_data(self):
        form =JobPostForm(data={})
        self.assertFalse(form.is_valid(),8)

    #INVALID DATE
    def test_jobpost_form_invalid_date(self):
        form = JobPostForm(data={
            'user': 'shraddha@gmail.com',
            'job_title': 'Testing Officer',
            'job_description': 'Day-to-day work will be testing and debugging the softwares',
            'location': 'Mumbai',
            'skills_required': 'Good with unit testing,system testing,selenium',
            'salary': 35000,
            'monthly_annually': 'p.m.',
            'last_date_of_applying': '2021-03-06'
        })
        self.assertFalse(form.is_valid())

    #INVALID SALARY
    def test_jobpost_form_invalid_salary(self):
        form = JobPostForm(data={
            'user': 'shraddha@gmail.com',
            'job_title': 'Testing Officer',
            'job_description': 'Day-to-day work will be testing and debugging the softwares',
            'location': 'Mumbai',
            'skills_required': 'Good with unit testing,system testing,selenium',
            'salary': -35000,
            'monthly_annually': 'p.m.',
            'last_date_of_applying': '2022-03-06'
        })
        self.assertFalse(form.is_valid())


    def test_user_form_valid(self):
        form = UserForm(data={
            'type':'EMPLOYER',
            'email': 'shraddha@gmail.com',
            'username':'shraddha01',
            'password':'Shrad@1234',
            'confirm_password':'Shrad@1234'

        })
        self.assertTrue(form.is_valid())

    #Password Not containing a Captial Letter
    def test_user_form_password1test_invalid(self):
        form = UserForm(data={
            'type':'EMPLOYER',
            'email': 'shraddha@gmail.com',
            'username':'shraddha01',
            'password':'shrad@1234',
            'confirm_password':'shrad@1234'

        })
        self.assertFalse(form.is_valid())

    #Confirm Password and Password not same
    def test_user_form_password2test_invalid(self):
        form = UserForm(data={
            'type':'EMPLOYER',
            'email': 'shraddha@gmail.com',
            'username':'shraddha01',
            'password':'Shir@1234',
            'confirm_password':'Shrad@1234'

        })
        self.assertFalse(form.is_valid())

    #Missing Special Characters
    def test_user_form_password3test_invalid(self):
        form = UserForm(data={
            'type':'EMPLOYER',
            'email': 'shraddha@gmail.com',
            'username':'shraddha01',
            'password':'Shrad1234',
            'confirm_password':'Shrad1234'

        })
        self.assertFalse(form.is_valid())


    # Invalid Email missing @
    def test_user_form_password4test_invalid(self):
        form = UserForm(data={
            'type':'EMPLOYER',
            'email': 'shraddhagmail.com',
            'username':'shraddha01',
            'password':'Shrad@1234',
            'confirm_password':'Shrad@1234'

        })
        self.assertFalse(form.is_valid())




    def test_employermore_valid(self):
        form =EmployerForm(data={
            'user':'santosh@gmail.com',
            'name_of_company':'ABC',
            'website':'www.abc.com',
            'contact_number':9874521360,
            'company_email_id':'abc@gmail.com',
            'upload_photo':'',
            'company_address':'MALAD'
        })
        self.assertTrue(form.is_valid())

    #Invalid company Email
    def test_employermore_email_invalid(self):
        form =EmployerForm(data={
            'user':'santosh@gmail.com',
            'name_of_company':'ABC',
            'website':'www.abc.com',
            'contact_number':9874521360,
            'company_email_id':'abcgmail.com'
        })
        self.assertFalse(form.is_valid())




    #Invalid Contact Number
    def test_employermore_phone_num_invalid(self):
        form =EmployerForm(data={
            'user':'santosh@gmail.com',
            'name_of_company':'ABC',
            'website':'www.abc.com',
            'contact_number':987452136,
            'company_email_id':'abc@gmail.com'
        })
        self.assertFalse(form.is_valid())


    # Valid CandidateMore
    def test_candidatemore_valid(self):
        form=CandidateForm(data={
            'user':'shraddha@gmail.com',
            'full_name':'Shraddha',
            'birth_date':'1998-2-2',
            'gender':'female',
            'marital_status':'married',
            'qualification':['MCA'],
            'contact_number':8745213690,
            'hobbies':'Dancing',
            'skills':'Good in Communication',
            'objective':'To Learn and Explore',
            'upload_cv':''
        })
        self.assertTrue(form.is_valid())

    # Invalid Contact Number
    def test_candidatemore_contact_number_invalid(self):
        form=CandidateForm(data={
            'user':'shraddha@gmail.com',
            'full_name':'Shraddha',
            'birth_date':'1998-2-2',
            'gender':'female',
            'marital_status':'married',
            'qualification':['MCA'],
            'contact_number':874521369,
            'hobbies':'Dancing',
            'skills':'Good in Communication',
            'objective':'To Learn and Explore',
            'upload_cv':''
        })
        self.assertFalse(form.is_valid())


    def test_candidatemore_present_future_date_invalid(self):
        form=CandidateForm(data={
            'user':'shraddha@gmail.com',
            'full_name':'Shraddha',
            'birth_date':'2022-5-2',
            'gender':'female',
            'marital_status':'married',
            'qualification':['MCA'],
            'contact_number':8745213690,
            'hobbies':'Dancing',
            'skills':'Good in Communication',
            'objective':'To Learn and Explore',
            'upload_cv':''


        })
        self.assertFalse(form.is_valid())


