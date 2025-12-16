from unittest.mock import patch
from django.test import Client, TestCase
import time
from django.urls import reverse
from bs4 import BeautifulSoup
from .models import enterpets,adoptionform
from django.contrib.auth.models import User


class PerformanceTests(TestCase):

    def test_pets_page_performance(self):
        url = reverse('pets')

        start = time.time()
        response = self.client.get(url)
        end = time.time()

        elapsed = end - start

        self.assertLess(elapsed, 0.5, f"Pets page is too slow ({elapsed} seconds)")
        self.assertEqual(response.status_code, 200)


class SecurityTests(TestCase):

    def test_csrf_token_present_in_post_forms(self):
        url = reverse('pets')
        response = self.client.get(url)

        soup = BeautifulSoup(response.content, "html.parser")
        post_forms = soup.find_all("form", method="post")

        
        if not post_forms:
            return
        
        for form in post_forms:
            csrf_token = form.find("input", {"name": "csrfmiddlewaretoken"})
            self.assertIsNotNone(csrf_token, "Missing CSRF token in a POST form")



class UsabilityTests(TestCase):

    def test_pets_page_contains_labels(self):
        url = reverse('pets')
        response = self.client.get(url)

        self.assertContains(response, "Search")
        self.assertContains(response, "Filter")
        self.assertContains(response, "Age")
        self.assertContains(response, "Breed")



class ScalabilityTests(TestCase):

    def setUp(self):
        for i in range(300):
            enterpets.objects.create(
                pet_name=f"Pet{i}",
                specie="dog",
                breed="breed",
                Age=2,
                color="white"
            )

    def test_large_pet_list(self):
        url = reverse('pets')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pet0")
        self.assertContains(response, "Pet299")

class CompatibilityTests(TestCase):

    def test_pets_page_renders_on_different_browsers(self):
        url = reverse('pets')
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1"
        ]

        for agent in user_agents:
            response = self.client.get(url, HTTP_USER_AGENT=agent)
            self.assertEqual(response.status_code, 200)

class registertest(TestCase):
    @patch('petadoption.views.generate_otp')
    def test_register_sends_otp(self, mock_send_otp):
        mock_send_otp.return_value = "123456"
        response=self.client.post(reverse('register'),{
            'username':'newuser', 
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'  })
        self.assertTrue(mock_send_otp.called)
        self.assertEqual(response.status_code,302)


class logintest(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='testuser',password='testpass')
    def test_login_sucess(self):
        respone =self.client.post(reverse('login'),{'username':'testuser','password':'testpass'})
        self.assertEqual(respone.status_code,302)
    def test_login_failure(self):
        respone =self.client.post(reverse('login'),{'username':'wronguser','password':'wrongpass'})
        self.assertEqual(respone.status_code,200)


class petsview(TestCase):
    def setUp(self):
        enterpets.objects.create(pet_name='Buddy', specie='Dog', breed='Labrador', Age=3, color='Yellow')
        enterpets.objects.create(pet_name='Mittens', specie='Cat', breed='Siamese', Age=2, color='Cream')

    def test_pets_view(self):
        response = self.client.get(reverse('pets'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')
        self.assertContains(response, 'Mittens')

    def test_pets_filter(self):
        response = self.client.get(reverse('pets') + '?specie=Dog')
        self.assertContains(response,'Buddy')
        self.assertNotContains(response,'Mittens')

    def test_pets_filter_by_breed(self):
        response = self.client.get(reverse('pets') + '?breed=Labrador')
        self.assertContains(response,'Buddy')
        self.assertNotContains(response,'Mittens')

    def test_pets_search(self):
        response=self.client.get(reverse('pets')+ '?search=Mittens')
        self.assertContains(response,'Mittens')

class petdetailview(TestCase):
    def setUp(self):
        self.pet = enterpets.objects.create(pet_name='Buddy', specie='Dog', breed='Labrador', Age=3, color='Yellow')

    def test_pet_detail_view(self):
        response = self.client.get(reverse('pet_detail', args=[self.pet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')
        self.assertContains(response, 'Dog')
        self.assertContains(response, 'Labrador')

class MyRequestsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        self.pet = enterpets.objects.create(pet_name='Cotton', specie='Cat')
        self.request = adoptionform.objects.create(user=self.user, pet=self.pet, age=2, why_you_wanna_adopt='Love pets', status='pending')

    def test_my_requests(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('my_requests'))
        self.assertContains(response, 'Cotton')
        self.assertContains(response, 'Pending')