from django.test import TestCase
from django.urls import reverse

from .models import Candidate


class CandidateCrudTests(TestCase):
    def setUp(self):
        self.candidate = Candidate.objects.create(
            first_name="Ada", last_name="Lovelace", email="ada@example.com", position="Engineer"
        )

    def test_list(self):
        resp = self.client.get(reverse("candidates:list"))
        self.assertContains(resp, "Ada Lovelace")

    def test_create(self):
        resp = self.client.post(
            reverse("candidates:create"),
            {"first_name": "Alan", "last_name": "Turing", "email": "alan@example.com",
             "position": "Researcher", "status": "applied"},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Candidate.objects.filter(email="alan@example.com").exists())

    def test_update(self):
        resp = self.client.post(
            reverse("candidates:update", args=[self.candidate.pk]),
            {"first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.com",
             "position": "Engineer", "status": "interview"},
        )
        self.assertEqual(resp.status_code, 302)
        self.candidate.refresh_from_db()
        self.assertEqual(self.candidate.status, "interview")

    def test_delete(self):
        resp = self.client.post(reverse("candidates:delete", args=[self.candidate.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Candidate.objects.exists())
