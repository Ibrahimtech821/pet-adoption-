from django.test import TestCase
import time
from django.urls import reverse
from bs4 import BeautifulSoup

from petadoption.models import enterpets


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


