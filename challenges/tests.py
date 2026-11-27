from django.test import TestCase
from django.urls import reverse

from candidates.models import Candidate

from .models import Challenge, ChallengeAssignment, normalize_output


class NormalizeTests(TestCase):
    def test_ignores_trailing_whitespace_and_newline_style(self):
        self.assertEqual(normalize_output("1\r\n2  \n\n"), "1\n2")


class ChallengeFlowTests(TestCase):
    def setUp(self):
        self.candidate = Candidate.objects.create(
            first_name="Ada", last_name="Lovelace", email="ada@example.com", position="Engineer"
        )
        self.challenge = Challenge.objects.create(
            title="Test", code_snippet="print(1 + 1)", expected_output="2"
        )

    def test_seed_migration_created_challenges(self):
        self.assertTrue(Challenge.objects.filter(title="Sum the odd numbers").exists())

    def test_assign_creates_assignment(self):
        resp = self.client.post(
            reverse("challenges:assign", args=[self.candidate.pk]), {"challenge": self.challenge.pk}
        )
        self.assertRedirects(resp, self.candidate.get_absolute_url())
        self.assertEqual(self.candidate.challenge_assignments.count(), 1)

    def test_correct_answer(self):
        a = ChallengeAssignment.objects.create(candidate=self.candidate, challenge=self.challenge)
        self.client.post(a.get_absolute_url(), {"answer": " 2 \n"})
        a.refresh_from_db()
        self.assertTrue(a.is_submitted)
        self.assertTrue(a.is_correct)

    def test_incorrect_answer_and_single_attempt(self):
        a = ChallengeAssignment.objects.create(candidate=self.candidate, challenge=self.challenge)
        self.client.post(a.get_absolute_url(), {"answer": "3"})
        self.client.post(a.get_absolute_url(), {"answer": "2"})  # second try ignored
        a.refresh_from_db()
        self.assertFalse(a.is_correct)
        self.assertEqual(a.answer, "3")

    def test_portal_shows_snippet(self):
        a = ChallengeAssignment.objects.create(candidate=self.candidate, challenge=self.challenge)
        resp = self.client.get(a.get_absolute_url())
        self.assertContains(resp, "print(1 + 1)")
        self.assertNotContains(resp, "+ Add candidate")  # recruiter nav hidden

    def test_detail_page_lists_assignment(self):
        ChallengeAssignment.objects.create(candidate=self.candidate, challenge=self.challenge)
        resp = self.client.get(self.candidate.get_absolute_url())
        self.assertContains(resp, "Technical challenges")
        self.assertContains(resp, "Pending")
