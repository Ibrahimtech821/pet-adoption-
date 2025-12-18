from unittest.mock import patch
from django.test import Client, TestCase, RequestFactory, override_settings
import time
from django.urls import reverse
from bs4 import BeautifulSoup
from .models import enterpets,adoptionform, PetFood
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


class SubmitAdoptionRequestTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='adopter', password='pass')
        self.pet = enterpets.objects.create(pet_name='Rocky', specie='Dog', Age=2, breed='Mixed', color='Brown')

    def test_adopt_requires_login(self):
        url = reverse('submit_adoption_request', args=[self.pet.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_adopt_get_authenticated(self):
        self.client.login(username='adopter', password='pass')
        url = reverse('submit_adoption_request', args=[self.pet.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Adoption')

    def test_adopt_post_creates_request(self):
        self.client.login(username='adopter', password='pass')
        url = reverse('submit_adoption_request', args=[self.pet.id])
        payload = {
            'age': 25,
            'why_you_wanna_adopt': 'I love dogs',
            'do_you_have_any_experince_before_with_animals': 'yes',
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('adoption_success'))
        req = adoptionform.objects.get(user=self.user, pet=self.pet)
        self.assertEqual(req.status, 'pending')


class SearchPetsTests(TestCase):
    def setUp(self):
        enterpets.objects.create(pet_name='Bella', specie='Cat', Age=3, breed='Siamese', color='Cream')

    def test_search_pets_found(self):
        url = reverse('search_pets') + '?name=Bella'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bella')

    def test_search_pets_not_found(self):
        url = reverse('search_pets') + '?name=NoSuchPet'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No pets found matching your criteria.")


class PetQuizTests(TestCase):
    def test_quiz_requires_all_fields(self):
        response = self.client.post(reverse('pet_quiz'), data={})
        self.assertEqual(response.status_code, 200)
        # Ensure we didn't set quiz scores in session when fields missing
        self.assertNotIn('Scores', response.wsgi_request.session)

    def test_quiz_redirects_with_scores(self):
        payload = {
            'activity': 'high',
            'space': 'large',
            'allergy': 'no',
            'time': 'high',
            'interactive': 'yes',
            'noise': "I don't mind",
            'long_life': 'no',
            'kids': 'yes'
        }
        response = self.client.post(reverse('pet_quiz'), data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('pet_quiz_result'))

    def test_quiz_result_without_session_redirects(self):
        response = self.client.get(reverse('pet_quiz_result'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('pet_quiz'))


class PetFoodViewTests(TestCase):
    def setUp(self):
        PetFood.objects.create(brand_name='NutriPaws', food_type='dry', suitable_for='Adult Dogs', description='Tasty', image='', buy_link='https://example.com')

    def test_petfood_list(self):
        response = self.client.get(reverse('petfood_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NutriPaws')


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class AdminSaveModelTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'pass')
        self.request = self.factory.post('/')
        self.request.user = self.admin_user
        self.pet = enterpets.objects.create(pet_name='Buddy', specie='Dog', Age=3, breed='Labrador', color='Yellow')
        self.user = User.objects.create_user(username='requester', email='req@example.com', password='pass')

    def test_admin_accept_marks_pet_adopted(self):
        from django.contrib import admin
        from .admin import requestformadmin
        obj = adoptionform(user=self.user, pet=self.pet, age=30, why_you_wanna_adopt='Love pets', do_you_have_any_experince_before_with_animals='Yes', status='accepted')
        admin_view = requestformadmin(adoptionform, admin.site)
        admin_view.save_model(self.request, obj, form=None, change=False)
        self.pet.refresh_from_db()
        self.assertTrue(self.pet.is_adopted)

    def test_admin_reject_marks_pet_not_adopted(self):
        from django.contrib import admin
        from .admin import requestformadmin
        obj = adoptionform(user=self.user, pet=self.pet, age=30, why_you_wanna_adopt='Love pets', do_you_have_any_experince_before_with_animals='Yes', status='reject')
        admin_view = requestformadmin(adoptionform, admin.site)
        admin_view.save_model(self.request, obj, form=None, change=False)
        self.pet.refresh_from_db()
        self.assertFalse(self.pet.is_adopted)