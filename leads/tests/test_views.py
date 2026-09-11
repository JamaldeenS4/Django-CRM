from django.test import TestCase
from django.shortcuts import reverse

# Create your tests here.
class LandingPageTest(TestCase):
    """ 
    Test whether the landing page returns 200 OK
    """
    def test_status_code(self):
        self.client.get(reverse('landing-page'))
        self.assertTrue(response.status_code)
        self.assertTemplateUsed(response, 'landing.html')