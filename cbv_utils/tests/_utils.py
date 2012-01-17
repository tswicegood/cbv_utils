from django.test import TestCase as DjangoTestCase
from django.test.client import Client, RequestFactory


class TestCase(DjangoTestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
