from django.test import TestCase, Client
from django.urls import reverse,resolve

from create_proxy.models import JobPost, applied_jobs, User, CandidateMore, EmployerMore, Questions
import json

class TestView(TestCase):

    def setUp(self):
        self.client =Client()
        self.home_url=reverse('home')
        self.applied_url=reverse('applied',args=[12])





    def test_home_GET(self):

        response =self.client.get(self.home_url)

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'home.html')





